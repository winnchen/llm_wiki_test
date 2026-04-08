# xhs-fetch-to-raw — Reference

## 支持的 URL 形态

| 形态 | 示例 |
|------|------|
| 短链 | `http://xhslink.com/o/...`（跟随重定向） |
| Web 详情 | `https://www.xiaohongshu.com/explore/{noteId}?xsec_token=...` |
| App 分享 | `https://www.xiaohongshu.com/discovery/item/{noteId}?xsec_token=...` |
| 404 落地页 | `https://www.xiaohongshu.com/404?noteId=...&xsec_token=...`（仍尝试拉取，常失败） |

`xsec_token` 必须在 query 中（或同义 `xsecToken`）。

## detail.json 顶层字段

| 字段 | 含义 |
|------|------|
| `fetched_at` | ISO 风格本地时间 |
| `source_urls` | `[用户输入, 解析后最终 URL]` |
| `note_id` | 笔记 ID |
| `cli_response` | `get-feed-detail` 完整 JSON（`note` + `comments`） |
| `local_assets.images` | 相对 `note.md` 的图片路径列表 |
| `local_assets.video` | 本地视频相对路径或 `null` |
| `video_candidate_urls` | 从 `note.video` 收集的 http 串（截断） |

## 与 llm-wiki Ingest

1. 确认 `note.md` / 图片已在 `raw/xiaohongshu/...`。
2. 按 `llm-wiki` skill 的 Ingest：讨论要点 → `wiki/sources/` 摘要页 → 实体/概念 → 更新 `wiki/index.md` 与 `wiki/log.md`。
3. 交叉引用使用 `[[标题]]`；源使用 `> [!source] raw/...`。
