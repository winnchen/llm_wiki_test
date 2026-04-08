---
name: xhs-fetch-to-raw
description: >-
  Archives Xiaohongshu (小红书) posts into a project raw folder: title, body,
  up to N comments, local images and optional video via xiaohongshu-skills cli.
  Use when the user shares xhslink.com links, asks to save 小红书 notes to raw,
  batch-fetch posts, or mirror XHS content into a wiki raw tree.
---

# 小红书归档到 raw（xhs-fetch-to-raw）

将笔记拉取到目标仓库的 `raw/xiaohongshu/<noteId>_<slug>/`，生成 `note.md`、`detail.json` 与 `assets/`，供后续 `llm-wiki` skill 的 Ingest 使用。

## 技能边界（强制）

- **唯一拉取方式**：通过 **xiaohongshu-skills** 仓库内的 `scripts/cli.py get-feed-detail`（优先 `uv run python scripts/cli.py`）。
- **禁止**使用其他 MCP、自建爬虫或非该项目的 Go/第三方工具拉取小红书。

## 前置条件

1. 已安装 [xiaohongshu-skills](https://github.com/autoclaw-cc/xiaohongshu-skills)，默认路径 `XHS_SKILLS_ROOT`（环境变量可覆盖），且已 `uv sync`。
2. Chrome + **XHS Bridge** 扩展 + **bridge_server**（默认 `ws://localhost:9333`），**已登录**小红书。
3. 本 skill 内置脚本路径（按实际项目替换 `<REPO>` 为仓库绝对路径）：
   - `<REPO>/.cursor/skills/xhs-fetch-to-raw/scripts/fetch_to_raw.py`

## 标准操作

在终端中执行（**使用绝对路径**）：

```bash
python3 <REPO>/.cursor/skills/xhs-fetch-to-raw/scripts/fetch_to_raw.py \
  --repo-root <REPO> \
  "http://xhslink.com/o/xxxx" \
  "https://www.xiaohongshu.com/explore/NOTE_ID?xsec_token=..."
```

常用参数：

| 参数 | 说明 |
|------|------|
| `--repo-root` | 目标仓库根（默认从 cwd 向上查找含 `raw/` 的目录） |
| `--raw-subdir` | 输出相对路径，默认 `raw/xiaohongshu` |
| `--max-comments` | 评论条数上限，默认 `20` |
| `--delay-min` / `--delay-max` | 篇与篇之间随机等待（秒），默认 `8`–`28` |

环境变量：

- `XHS_SKILLS_ROOT`：xiaohongshu-skills 根目录（默认 `~/.cursor/skills/xiaohongshu-skills`）。
- `RAW_BASE`：若设置，则**直接**作为输出根目录（覆盖 `--repo-root` + `--raw-subdir`）。

单条失败不中断整批；结束时 stderr 汇总成功/失败数。

## 落盘结构

```
raw/xiaohongshu/{noteId}_{slug}/
  note.md       # 正文、本地图片引用、评论摘要
  detail.json   # 完整 cli JSON + local_assets + video 候选 URL
  assets/       # img_01.webp …；失败时 *_FAILED.txt；m3u8 可能为 video.m3u8.url.txt
```

## 失败处理

| 现象 | 处理 |
|------|------|
| 未登录 / bridge 未连 | 提示用户检查扩展与 `bridge_server`，执行 xhs-auth 登录流程 |
| cli 非 0 退出 |  stderr 中有详情；常见为风控、笔记删除、token 失效 |
| 短链落到 404 且带 `noteId` | 脚本仍会尝试 cli；多数仍失败属正常 |
| 单张图下载失败 | `assets/img_XX_FAILED.txt` 记录 URL |

## 与 Echo Wiki 衔接

- 本 skill **只写 `raw/`**；写入 `wiki/sources/` 请走 **llm-wiki** 的 **Ingest** 流程。
- 源引用示例：`> [!source] raw/xiaohongshu/<folder>/note.md`（或 `detail.json`，按 AGENTS 约定）。

## 扩展阅读

URL 形态、`detail.json` 字段说明见 [reference.md](reference.md)。
