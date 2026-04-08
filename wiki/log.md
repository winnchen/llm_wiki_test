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

## [2026-04-08] update | comparison：Harness 对照页补数据与跨源共识（re-ingest 联动）

- 更新 [[Harness 实践对照：OpenAI、Anthropic、LangChain 与 Fowler]]：对照表补 boring tech / sprint 合约 / Trace Analyzer / harnessability 等细节；新增「数据对照」子表（规模、效果量化、自治时长、多代理 vs 单、模型演进策略）；分析段「重复老办法」改为引用 concept 页跨源共识模式表 + 5 条显式列举

## [2026-04-08] update | synthesis：Harness 原则清单补增量（re-ingest 联动）

- 更新 [[Harness engineering：定义、原则与实践清单]]：工作定义段补数据；原则 4 补 evaluator 校准 + sprint 合约；原则 7 补 Opus 4.5→4.6 实例；原则 13 补推理档位数据；新增原则 14（boring tech / harnessability）、15（harness 覆盖度度量）；实践清单新增「评测」行 + 补充 per-worktree / doc-gardening / remediation 等

## [2026-04-08] re-ingest (batch) | Harness 5 篇源（新流程 v2）

- 模式: batch re-ingest（先全读 5 篇 → 跨源 Delta → 统一重写）
- 源: `raw/web/harness-engineering-martinfowler/`、`harness-engineering-openai/`、`harness-design-long-running-apps/`、`langchain-deep-agents-harness-engineering/`、`x-genai-is-real-harness-engineering-critique/`
- Delta: 大量 new（数据、架构细节、成本数据、跨源共识模式）/ reinforcing（已有框架）/ 0 contradicting / 部分 covered
- 重写: 5 个 source-summary（全部加 `density` 字段；按 Tech/AI 与 Opinion 分析模板深化；增加核心论点、关键数据/框架、值得注意的论断等分节）
- 更新: [[Harness engineering（代理脚手架）]]（新增「跨源共识模式」表 + 演进理解段补数据）
- Synthesis trigger: 已有 synthesis + comparison 页覆盖，无需新建
- 局部 lint: 0 error / 0 new warning

## [2026-04-08] update | schema：Ingest 流程升级（v2）

- 升级 `AGENTS.md`：Ingest 章节重写为单篇/批量双模式；新增领域感知分析、Delta 对照（强制）、synthesis trigger check、局部 lint 四个步骤
- 升级 `.cursor/skills/llm-wiki/SKILL.md`：Workflow 2 对齐 AGENTS.md 变更；增加 domain-aware analysis 维度矩阵、Delta 分类（new/reinforcing/contradicting/covered）、density 字段、batch ingest 流程、log 格式增加 delta 统计与 synthesis trigger 字段
- 升级 `.cursor/skills/llm-wiki/reference.md`：新增 Domain-Aware Analysis Templates（5 类源 × 4–5 维度）；Frontmatter Schema 增加 `density: high | medium | low` 字段说明

## [2026-04-08] update | concept：露营装备（新手）增加采购清单

- 更新 [[露营装备（新手）]]：原共识列表扩写为分类装备表（睡眠/安全照明/炊事/其他/Solo hiking）+ 新手策略 5 条；增加 [[优胜美地自驾路线与景点综合]] 反向链接

## [2026-04-08] synthesis | 优胜美地自驾路线与景点综合

- 新建: `wiki/synthesis/yosemite-routes-and-highlights.md`（[[优胜美地自驾路线与景点综合]]）
- 综合 6 篇小红书源：入园路线、Valley 单行线景点顺序、Valley 外区域、1–3 日动线、实操提示
- 更新: [[Yosemite National Park]]（反向链接）、`wiki/index.md`（+1 synthesis）、`wiki/log.md`

## [2026-04-08] update | comparison：Harness 对照页「日常可抄作业」

- 更新 [[Harness 实践对照：OpenAI、Anthropic、LangChain 与 Fowler]]：总结下增加 8 条日常项目手段 + 括号内概念锚点

## [2026-04-08] comparison | Harness：OpenAI / Anthropic / LangChain / Fowler

- 新建: `wiki/comparisons/harness-openai-anthropic-langchain-fowler.md`（[[Harness 实践对照：OpenAI、Anthropic、LangChain 与 Fowler]]）
- 更新: [[Harness engineering（代理脚手架）]]、[[Harness engineering：定义、原则与实践清单]]、`wiki/index.md`、`wiki/log.md`

## [2026-04-08] ingest | Web：LangChain deep agents harness（Terminal Bench）

- 源: `raw/web/langchain-deep-agents-harness-engineering/article.md`
- 新建 source-summary: `wiki/sources/web-langchain-deep-agents-harness-engineering.md`
- 新建 entity: [[LangChain]]
- 更新 concept: [[Harness engineering（代理脚手架）]]；synthesis: [[Harness engineering：定义、原则与实践清单]]（一手来源列表改为 wikilink）
- 更新 entity: [[OpenAI]]
- 更新: `wiki/index.md`、`wiki/log.md`
- 矛盾标注: 无

## [2026-04-08] update | synthesis：补 LangChain 原则与局限

- 更新 [[Harness engineering：定义、原则与实践清单]]：`sources` 增加 `raw/web/langchain-deep-agents-harness-engineering/`；新增原则 9–13（trace 外环、退出前自检、环境注入、反死循环、推理预算）；实践表与局限（未来形态 gap）微调

## [2026-04-08] ingest | X：@GenAI_is_real harness 批评 / how-to-sglang

- 源: `raw/web/x-genai-is-real-harness-engineering-critique/article.md`
- 新建 source-summary: `wiki/sources/web-x-genai-is-real-harness-engineering-critique.md`
- 新建 entity: [[Chayenne Zhao]]
- 更新 concept: [[Harness engineering（代理脚手架）]]；synthesis: [[Harness engineering：定义、原则与实践清单]]
- 更新 entity: [[OpenAI]]、[[Anthropic]]
- 更新: `wiki/index.md`、`wiki/log.md`
- 矛盾标注: 无（话语层争议，非事实互斥）

## [2026-04-08] raw | X 帖归档（@GenAI_is_real — harness engineering 命名批评 / how-to-sglang）

- 落盘 `raw/web/x-genai-is-real-harness-engineering-critique/article.md` + `assets/tweet-image-1.jpg` — [原帖](https://x.com/GenAI_is_real/status/2036266930290696599)（经已登录浏览器 DevTools 快照抓取正文）

## [2026-04-08] raw | Web 剪藏（LangChain — deep agents harness）

- 落盘 `raw/web/langchain-deep-agents-harness-engineering/article.md` — [Improving Deep Agents with harness engineering](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)（配图 5 张于 `assets/`）

## [2026-04-08] update | Schema：Query 写回、Lint 节奏、raw 边界

- 更新 **AGENTS.md**：元理念（链 Karpathy gist）、raw 层边界、Query 写回闭环（强制）、Lint 节奏
- 更新 **`.cursor/skills/llm-wiki/`**（`SKILL.md`、`reference.md`）与上述一致

## [2026-04-08] synthesis | Harness engineering：定义、原则与实践清单

- 新建: `wiki/synthesis/harness-engineering-principles-and-practices.md`（[[Harness engineering：定义、原则与实践清单]]）
- 依据: 四篇 `raw/web/` harness / 采用长文 + 概念页 [[Harness engineering（代理脚手架）]]
- 更新: `wiki/concepts/harness-engineering-agent-harness.md`（反向链接）、`wiki/index.md`、`wiki/log.md`

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
