---
title: Wiki Log
type: log
sources: []
tags:
  - meta
---

# Echo Wiki Log

所有 wiki 操作的时间线记录。最新在前。

<!-- 快速查看: grep "^## \[" wiki/log.md | head -10 -->

## [2026-04-08] ingest | Web：harness 工程与个人 AI 采用（4 raw）

- 源: `raw/web/harness-engineering-martinfowler/article.md`、`harness-engineering-openai/article.md`、`harness-design-long-running-apps/article.md`、`my-ai-adoption-journey/article.md`
- 新建 source-summary: `wiki/sources/web-martinfowler-harness-engineering-coding-agents.md`、`web-openai-harness-engineering-codex.md`、`web-anthropic-harness-design-long-running-apps.md`、`web-mitchellh-my-ai-adoption-journey.md`
- 新建 entity: [[Martin Fowler]]、[[OpenAI]]、[[Anthropic]]、[[Mitchell Hashimoto]]
- 新建 concept: [[Harness engineering（代理脚手架）]]、[[个人 AI 采用与工作流]]
- 更新: `wiki/index.md`、`wiki/log.md`
- 矛盾标注: 无（各文视角互补）

## [2026-04-08] raw | Web 剪藏（Martin Fowler — harness）

- 落盘 `raw/web/harness-engineering-martinfowler/article.md` — [Martin Fowler — Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)

## [2026-04-08] raw | Web 剪藏（agent harness 主题）

- 落盘 `raw/web/harness-design-long-running-apps/article.md` — [Anthropic — Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- 落盘 `raw/web/harness-engineering-openai/article.md` — [OpenAI — Harness engineering (Codex)](https://openai.com/index/harness-engineering/)
- 落盘 `raw/web/my-ai-adoption-journey/article.md` — [Mitchell Hashimoto — My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey)

## [2026-04-08] ingest | 小红书第二批（5 篇 Yosemite / 营地预约）

- 源: `raw/xiaohongshu/` 下 5 篇 `note.md`（Valley 停车、一日游、三天两夜、Recreation.gov 实操、最简 2–3 日）
- 新建 source-summary: `wiki/sources/xhs-68f5a72b-*` … `xhs-684f665f-*`（5）
- 更新 entity: [[Yosemite National Park]]
- 更新 concept: [[美国国家公园露营与营地]]、[[露营装备（新手）]]
- 更新: `wiki/index.md`、`wiki/log.md`
- 矛盾标注: 无

## [2026-04-08] ingest | 小红书美西露营与国家公园（5 篇 raw）

- 源目录: `raw/xiaohongshu/` 下 5 篇 `note.md`（露营装备 ×3、Sequoia 一日游、Yosemite 两日游）
- 新建 source-summary: `wiki/sources/xhs-*.md`（5）
- 新建 entity: [[Yosemite National Park]]、[[Sequoia National Park]]
- 新建 concept: [[露营装备（新手）]]、[[美国国家公园露营与营地]]
- 更新: `wiki/index.md`、`wiki/log.md`
- 矛盾标注: 无

## [2026-04-08] init | Wiki Created

- 领域: 全领域个人知识库
- 语言: 中英混合
- 创建初始目录结构: raw/, wiki/sources/, wiki/entities/, wiki/concepts/, wiki/comparisons/, wiki/synthesis/
- 创建 Schema: AGENTS.md
- 创建 Index: wiki/index.md
- 创建 Log: wiki/log.md
