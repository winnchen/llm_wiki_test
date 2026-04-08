---
title: Harness engineering（代理脚手架）
type: concept
created: 2026-04-08
updated: 2026-04-08
sources:
  - web/harness-engineering-martinfowler/article.md
  - web/harness-engineering-openai/article.md
  - web/harness-design-long-running-apps/article.md
  - web/x-genai-is-real-harness-engineering-critique/article.md
  - web/langchain-deep-agents-harness-engineering/article.md
tags:
  - ai
  - engineering
  - llm
---

# Harness engineering（代理脚手架）

## 定义

在 **coding agent（编码代理）** 语境下，**harness** 指模型之外的**可控环境**：规则、工具、测试与反馈回路，用来提高首次成功率、支持自纠，并在人类监督成本与系统质量之间做权衡。不同作者使用的边界略有宽窄（见 [[Martin Fowler]] 对 bounded context 的说明）。

## 为何重要

LLM **非确定性**、上下文有限且对组织隐知识不可见；没有 harness，代理容易重复错误、漂移架构或产出「看起来能跑」但行为不可靠的系统。工业界公开实践表明，竞争重点正转向 **环境设计、反馈机制与可验证结构**。

## 关键来源

- [[Web｜Martin Fowler：Harness engineering for coding agent users]] — **guides / sensors**、computational vs inferential、**可维护性 / 架构 fitness / 行为** 三类调节对象；steering loop 与 harness templates。
- [[Web｜OpenAI：Harness engineering（Codex）]] — 仓库即系统：**`AGENTS.md` 作地图**、`docs/` 作真源、**linter/结构测试**、分层边界、可观测性与 doc-gardening。
- [[Web｜Anthropic：Harness design for long-running apps]] — **generator–evaluator**（及 planner）多代理；Playwright MCP；长上下文与 **reset / compaction** 的 harness 取舍；随模型变强**删减脚手架**。
- [[Web｜LangChain：Improving Deep Agents with harness engineering]] — **Terminal Bench** 上固定模型只改 harness；**LangSmith trace** 外环、**Trace Analyzer** 技能化复盘；**middleware**（退出前 checklist、环境注入、死循环检测、推理预算三明治等）。
- [[X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验]] — **元话语**视角：批评「新词造学科」与焦虑营销，但承认与 **how-to-sglang** 实践同构（渐进披露、仓库真源、结构化路由）；区分**话语包装**与**可验证工程模式**。

## 相关概念

- [[Harness engineering：定义、原则与实践清单]] — 在本页定义之上整理的合成原则与落地 checklist。
- [[Harness 实践对照：OpenAI、Anthropic、LangChain 与 Fowler]] — 各家长文场景、抓手与例子并排，避免概念叠床架屋。
- [[个人 AI 采用与工作流]] — 个人侧 `AGENTS.md`、工具化与常驻代理，与团队/仓库级 harness 互补。
- **Context engineering** — 各文均隐含：如何把可验证、可发现的知识放进代理上下文。

## 跨源共识模式

重新分析 5 篇原始资料后，以下模式在 ≥ 3 篇中**独立出现**：

| 模式 | 出现于 | 说明 |
|------|--------|------|
| **环境改进 > 换更大模型** | OpenAI、LangChain、X 帖 | 三方独立报告突破来自 harness 而非 model |
| **巨型单文件必腐烂** | OpenAI、X 帖、Fowler（隐含） | 收敛于 progressive disclosure + 结构化 `docs/` |
| **自评偏差 → 独立评测** | Anthropic、LangChain、Fowler（行为 harness） | 分离 generator 与 evaluator / QA |
| **每层复杂度编码模型弱点** | Anthropic（显式）、LangChain（guardrails dissolve）、Fowler（harnessability 随模型变） | 新模型应做减法实验 |
| **Ralph Wiggum Loop 式钩子** | OpenAI、LangChain、Anthropic（隐含） | 退出前强制自检 / 继续迭代 |

## 演进理解

- **2026 前后公开叙事**从「单文件提示」转向 **可机械校验的结构**（目录、图、测试、lint）与 **多代理分工**（规划/实现/评测）。
- 不同机构侧重点不同：**OpenAI** 偏「百万行 mono-repo 治理」（~100 万行 / 1500 PR / 3.5 PR/人/天）；**Anthropic** 偏「长时程自主与主观质量可评分」（solo $9 vs full harness $200）；**Fowler** 偏「分类语言与风险坦诚（尤其行为 harness）」；**LangChain** 偏「benchmark + trace 驱动的 harness 迭代与中间件旋钮」（52.8% → 66.5% 只改 harness）——彼此可对照阅读，而非简单合并为一式方案。
- **命名与学科边界**：社区存在「是否应称 harness engineering」的争议（见上 X 源）；本概念页仍用该词作**索引锚点**，涵盖上述实践，不等于主张其必须成为独立学科标签。
