#!/usr/bin/env python3
"""
将小红书笔记归档到目标仓库的 raw/<subdir>/<noteId>_<slug>/（note.md、detail.json、assets/）。

依赖：xiaohongshu-skills（Chrome + XHS Bridge + 已登录），通过其 cli.py get-feed-detail 拉取。

用法:
  python fetch_to_raw.py [--repo-root PATH] [--raw-subdir raw/xiaohongshu] URL1 [URL2 ...]
  XHS_SKILLS_ROOT=... RAW_BASE=... python fetch_to_raw.py ...

环境变量:
  XHS_SKILLS_ROOT  默认 ~/.cursor/skills/xiaohongshu-skills
  RAW_BASE         若设置则直接作为输出根目录（覆盖 --repo-root + --raw-subdir）
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def find_repo_root(explicit: Path | None) -> Path:
    """定位 wiki 仓库根：优先 --repo-root，否则从 cwd 向上查找含 raw/ 的目录。"""
    if explicit is not None:
        p = explicit.expanduser().resolve()
        if not p.is_dir():
            raise NotADirectoryError(f"--repo-root 不是目录: {p}")
        return p
    cwd = Path.cwd().resolve()
    for p in [cwd, *cwd.parents]:
        if (p / "raw").is_dir():
            return p
    return cwd


def default_xhs_root() -> Path:
    env = os.environ.get("XHS_SKILLS_ROOT", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return (Path.home() / ".cursor/skills/xiaohongshu-skills").resolve()


def resolve_url(initial: str) -> str:
    req = urllib.request.Request(
        initial,
        headers={"User-Agent": UA},
        method="GET",
    )
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    with opener.open(req, timeout=45) as resp:
        return resp.geturl()


def parse_feed_from_url(final_url: str) -> tuple[str, str]:
    """解析 noteId 与 xsec_token：/explore/、/discovery/item/、404 落地页 query。"""
    parsed = urllib.parse.urlparse(final_url)
    qs = urllib.parse.parse_qs(parsed.query)
    token = (qs.get("xsec_token") or qs.get("xsecToken") or [""])[0]

    m = re.search(r"/explore/([0-9a-f]+)", parsed.path, re.I)
    if not m:
        m = re.search(r"/discovery/item/([0-9a-f]+)", parsed.path, re.I)
    if m:
        note_id = m.group(1)
    elif "/404" in parsed.path or parsed.path.rstrip("/").endswith("404"):
        note_id = (qs.get("noteId") or qs.get("note_id") or [""])[0]
        if not note_id:
            raise ValueError(f"404 页未带 noteId，笔记可能已删除: {final_url}")
    else:
        raise ValueError(f"无法从 URL 解析笔记 ID: {final_url}")

    if not token:
        raise ValueError(f"URL 中缺少 xsec_token: {final_url}")
    return note_id, token


def slug_title(title: str, max_len: int = 36) -> str:
    t = re.sub(r"[^\w\u4e00-\u9fff]+", "-", (title or "").strip())
    t = t.strip("-")[:max_len] or "note"
    return t


def shutil_which(name: str) -> str | None:
    from shutil import which

    return which(name)


def run_get_feed_detail(xhs_root: Path, feed_id: str, xsec_token: str, max_comments: int) -> dict:
    cli_py = xhs_root / "scripts" / "cli.py"
    if not cli_py.is_file():
        raise FileNotFoundError(f"找不到 cli.py: {cli_py}")

    args_tail = [
        "get-feed-detail",
        "--feed-id",
        feed_id,
        "--xsec-token",
        xsec_token,
        "--load-all-comments",
        "--max-comment-items",
        str(max_comments),
    ]

    if shutil_which("uv"):
        cmd = ["uv", "run", "python", "scripts/cli.py", *args_tail]
        cwd = str(xhs_root)
    else:
        cmd = [sys.executable, str(cli_py), *args_tail]
        cwd = str(xhs_root)

    env = {**os.environ, "PYTHONPATH": str(xhs_root / "scripts")}
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=600,
        env=env,
    )
    out = (proc.stdout or "").strip()
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        raise RuntimeError(f"cli 退出码 {proc.returncode}\n{err}\n{out[-2000:]}")
    return json.loads(out)


def ext_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    base = os.path.basename(path)
    if "." in base:
        ext = base.rsplit(".", 1)[1].lower()
        ext = re.sub(r"[^a-z0-9]", "", ext)[:8]
        if ext:
            return f".{ext}"
    return ".webp"


def download_binary(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Referer": "https://www.xiaohongshu.com/",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    dest.write_bytes(data)


def collect_http_strings(obj: object, out: list[str]) -> None:
    if isinstance(obj, dict):
        for v in obj.values():
            collect_http_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_http_strings(v, out)
    elif isinstance(obj, str) and obj.startswith("http"):
        out.append(obj)


def pick_video_url(video: dict | None) -> str | None:
    if not video:
        return None
    urls: list[str] = []
    collect_http_strings(video, urls)
    if not urls:
        return None
    for u in urls:
        if ".mp4" in u.lower():
            return u
    for u in urls:
        if ".m3u8" in u.lower():
            return u
    for u in urls:
        if any(k in u for k in ("sns-video", "xhscdn", "vod", "video")):
            return u
    return urls[0]


def build_note_markdown(
    note: dict,
    source_urls: list[str],
    image_rel_paths: list[str],
    video_rel: str | None,
    comments: list[dict],
    video_fallback_urls: list[str],
    max_comments: int,
) -> str:
    title = note.get("title") or "无标题"
    desc = note.get("desc") or ""
    author = (note.get("user") or {}).get("nickname") or ""
    nid = note.get("noteId") or ""
    lines = [
        f"# {title}",
        "",
        "> 抓取说明：正文与资源路径对应关系见同目录 `detail.json` 中的 `local_assets`。",
        "",
        "## 元数据",
        "",
        f"- **笔记 ID**: `{nid}`",
        f"- **作者**: {author}",
        f"- **类型**: {note.get('type', '')}",
        f"- **原文链接**: {' / '.join(source_urls)}",
        "",
        "## 正文",
        "",
        desc,
        "",
        "## 图片（本地）",
        "",
    ]
    for i, rel in enumerate(image_rel_paths, 1):
        lines.append(f"![图{i}]({rel})")
        lines.append("")
    if video_rel:
        lines.extend(["## 视频（本地）", "", f"[本地视频]({video_rel})", ""])
    elif video_fallback_urls:
        lines.extend(
            [
                "## 视频",
                "",
                "未能自动下载到本地（URL 可能为 m3u8 或需 ffmpeg）。候选地址已写入 `detail.json` 的 `video_candidate_urls`。",
                "",
            ]
        )
    lines.extend([f"## 评论（最多 {max_comments} 条）", ""])
    for i, c in enumerate(comments, 1):
        u = (c.get("user") or {}).get("nickname") or "匿名"
        content = (c.get("content") or "").replace("\n", " ")
        likes = c.get("likeCount", "")
        lines.append(f"{i}. **{u}**（赞 {likes}）: {content}")
        subs = c.get("subComments") or []
        for j, sc in enumerate(subs[:5], 1):
            su = (sc.get("user") or {}).get("nickname") or ""
            st = (sc.get("content") or "").replace("\n", " ")
            lines.append(f"   - {j}. {su}: {st}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def fetch_one(
    raw_base: Path,
    xhs_root: Path,
    link: str,
    max_comments: int,
) -> Path:
    link = link.strip()
    if "xiaohongshu.com/explore/" in link or "xiaohongshu.com/discovery/item/" in link:
        final = link
    else:
        final = resolve_url(link)
    note_id, xsec = parse_feed_from_url(final)

    data = run_get_feed_detail(xhs_root, note_id, xsec, max_comments)
    note = data.get("note") or {}
    comments = (data.get("comments") or [])[:max_comments]
    title = note.get("title") or "untitled"
    slug = slug_title(title)
    out_dir = raw_base / f"{note_id}_{slug}"
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    image_rel_paths: list[str] = []
    ilist = note.get("imageList") or []
    for idx, img in enumerate(ilist, 1):
        url = (img.get("urlDefault") or img.get("urlPre") or "").strip()
        if not url:
            continue
        ext = ext_from_url(url)
        fname = f"img_{idx:02d}{ext}"
        rel = f"assets/{fname}"
        try:
            download_binary(url, assets / fname)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as e:
            fname_fail = f"img_{idx:02d}_FAILED.txt"
            (assets / fname_fail).write_text(f"url={url}\nerror={e!r}\n", encoding="utf-8")
            rel = f"assets/{fname_fail}"
        image_rel_paths.append(rel)

    video_rel: str | None = None
    video_blob = note.get("video")
    video_candidates: list[str] = []
    if isinstance(video_blob, dict):
        collect_http_strings(video_blob, video_candidates)
    vurl = pick_video_url(video_blob if isinstance(video_blob, dict) else None)
    if vurl:
        vext = ".mp4" if ".m3u8" not in vurl.lower() else ".m3u8"
        if vext == ".mp4":
            try:
                download_binary(vurl, assets / f"video{vext}")
                video_rel = f"assets/video{vext}"
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
                video_rel = None
        else:
            (assets / "video.m3u8.url.txt").write_text(vurl + "\n", encoding="utf-8")

    manifest = {
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
        "source_urls": [link, final],
        "note_id": note_id,
        "cli_response": data,
        "local_assets": {
            "images": image_rel_paths,
            "video": video_rel,
        },
        "video_candidate_urls": video_candidates[:30],
    }
    (out_dir / "detail.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    note_md = build_note_markdown(
        note,
        [link, final],
        image_rel_paths,
        video_rel,
        comments,
        video_candidates,
        max_comments,
    )
    (out_dir / "note.md").write_text(note_md, encoding="utf-8")
    return out_dir


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="小红书笔记归档到 raw（通过 xiaohongshu-skills cli）",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="目标仓库根目录（默认：从当前目录向上查找含 raw/ 的目录）",
    )
    p.add_argument(
        "--raw-subdir",
        default="raw/xiaohongshu",
        help="相对 repo-root 的输出子路径（默认 raw/xiaohongshu）",
    )
    p.add_argument("--max-comments", type=int, default=20, help="最多拉取评论条数（默认 20）")
    p.add_argument("--delay-min", type=float, default=8.0, help="篇间随机延迟下限秒（默认 8）")
    p.add_argument("--delay-max", type=float, default=28.0, help="篇间随机延迟上限秒（默认 28）")
    p.add_argument("urls", nargs="+", help="笔记短链或 xiaohongshu 直链")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.delay_min > args.delay_max:
        print("错误: --delay-min 不能大于 --delay-max", file=sys.stderr)
        sys.exit(2)

    env_raw = os.environ.get("RAW_BASE", "").strip()
    if env_raw:
        raw_base = Path(env_raw).expanduser().resolve()
    else:
        repo = find_repo_root(args.repo_root)
        raw_base = (repo / args.raw_subdir).resolve()

    raw_base.mkdir(parents=True, exist_ok=True)
    xhs_root = default_xhs_root()
    links = [u.strip() for u in args.urls if u.strip()]

    print(f"XHS_SKILLS_ROOT={xhs_root}", file=sys.stderr)
    print(f"RAW_BASE={raw_base}", file=sys.stderr)

    ok: list[str] = []
    failed: list[tuple[str, str]] = []
    delay_range = (args.delay_min, args.delay_max)

    for i, link in enumerate(links):
        try:
            out = fetch_one(raw_base, xhs_root, link, args.max_comments)
            ok.append(str(out))
            print(f"OK {out}")
        except Exception as e:
            failed.append((link, str(e)))
            print(f"FAIL {link}\n  {e}", file=sys.stderr)
        if i < len(links) - 1:
            delay = random.uniform(*delay_range)
            print(f"(下一篇前等待 {delay:.1f}s …)", file=sys.stderr)
            time.sleep(delay)

    print(f"\n完成: 成功 {len(ok)} / {len(links)}", file=sys.stderr)
    if failed:
        for l, err in failed:
            print(f"  失败: {l}\n    {err[:500]}", file=sys.stderr)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
