---
title: X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验
type: source-summary
created: 2026-04-08
updated: 2026-04-08
density: medium
sources:
  - web/x-genai-is-real-harness-engineering-critique/article.md
tags:
  - ai
  - engineering
  - llm
---

# X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验

> [!source] raw/web/x-genai-is-real-harness-engineering-critique/article.md

## 概述

[[Chayenne Zhao]]（@GenAI_is_real，2026-03-24）长帖（~156k 浏览 / 161 转 / 1252 赞 / 1621 书签）：批评 **harness engineering** 等术语把「自 ChatGPT 起就存在的环境设计」包装成新学科、制造 FOMO；同时肯定文中所引研究与案例的价值，并以 **how-to-sglang** 多代理问答系统为实例，说明核心做法与业界 harness 叙事**同构**却从未依赖新词汇。文末追问：模型指数增长后，环境是否仍由人构建。

## 核心论点

Prompt / context / harness engineering 是**同一问题的不同切面与营销周期**；工程模式本身有价值，但不断造新词再制造焦虑是有害的。

## how-to-sglang 架构（一手经验）

- **失败的第一版**：单一全能 Agent + 塞满所有 docs/code/cookbooks → 注意力分散、全面变差。
- **成功的第二版**：**多层子域专家架构**——按 SGLang 文档天然边界（advanced features / platforms / supported models / cookbooks）拆分独立 expert agent。
- **Expert Debating Manager**：接收问题 → 分解子问题 → 查 **Expert Routing Table** 激活对应 agent → 并行求解 → 综合答案。
  - 示例：GLM-5 INT4 问题同时激活 Cookbook Expert 与 Quantization Expert。

## 与业界 harness 叙事的对应

| 作者自称 | 业界术语 | 说明 |
|----------|----------|------|
| 不塞满、只加载本域知识 | Progressive disclosure | 失败过「全塞」后自然推出 |
| 知识全在 repo 的 markdown | Repo as source of truth | 早期也想写一个巨型 sglang-maintain.md，与 OpenAI 踩坑相同 |
| Expert Routing Table | Mechanized routing / structured constraints | Manager 查表激活，不靠 agent 猜测 |
| 传统术语同义 | 分离关注点、单一职责、docs-as-code、shift-left | 不需要新名字 |

## 对文献的细分态度

- **肯定**：SWE-agent ACI 概念、Anthropic initializer+coding 双代理、各公司 benchmark 与 trace 数据。
- **否定**：把常识重包装为「学科」、AI-written 万字长文制造热度。

## 开放问题

- **OpenClaw** 一个月从 40 万行到 100 万行，全由 AI 驱动——谁在构建环境？人还是 AI？
- 若模型持续指数增长，当前人主导的环境设计原则可能**两年内全部失效**。

## 值得注意的论断

- how-to-sglang 上**突破来自环境改进**而非换更强模型——与 LangChain Terminal Bench 结论一致。
- 巨型单文件 AGENTS.md「必腐烂」——与 OpenAI Codex 团队叙述**独立踩坑后收敛**。
- 阅读时需区分**话语层**（命名/焦虑）与**实践层**（工程模式有效）。

## 实体

- [[Chayenne Zhao]] — 作者；SGLang / how-to-sglang
- [[OpenAI]] — 引用其「AGENTS.md 失败」叙述
- [[Anthropic]] — 肯定 initializer + coding 双代理

## 概念

- [[Harness engineering（代理脚手架）]] — 从元话语侧补充：实践可重叠，命名与学科边界可争议
