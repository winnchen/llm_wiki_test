---
title: Harness engineering（代理脚手架）
type: concept
created: 2026-04-08
updated: 2026-04-08
sources:
  - web/harness-engineering-martinfowler/article.md
  - web/harness-engineering-openai/article.md
  - web/harness-design-long-running-apps/article.md
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

## 相关概念

- [[Harness engineering：定义、原则与实践清单]] — 在本页定义之上整理的合成原则与落地 checklist。
- [[个人 AI 采用与工作流]] — 个人侧 `AGENTS.md`、工具化与常驻代理，与团队/仓库级 harness 互补。
- **Context engineering** — 各文均隐含：如何把可验证、可发现的知识放进代理上下文。

## 演进理解

- **2026 前后公开叙事**从「单文件提示」转向 **可机械校验的结构**（目录、图、测试、lint）与 **多代理分工**（规划/实现/评测）。
- 不同机构侧重点不同：**OpenAI** 偏「百万行 mono-repo 治理」；**Anthropic** 偏「长时程自主与主观质量可评分」；**Fowler** 偏「分类语言与风险坦诚（尤其行为 harness）」——彼此可对照阅读，而非简单合并为一式方案。
