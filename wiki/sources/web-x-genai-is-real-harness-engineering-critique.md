---
title: X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验
type: source-summary
created: 2026-04-08
updated: 2026-04-08
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

[[Chayenne Zhao]]（@GenAI_is_real）长帖：批评 **harness engineering** 等术语把「自 ChatGPT 起就存在的环境设计」包装成新学科、制造焦虑；同时肯定文中所引研究与案例的价值，并以 **how-to-sglang** 多代理问答系统为例，说明 **渐进披露、仓库真源、结构化路由** 等做法与业界 harness 叙事**同构**，但不必依赖新词汇即可从失败中推出。文末提出开放问题：模型能力指数增长后，环境是否仍主要由人构建（以 OpenClaw 为例）。正文与配图见 raw。

## 要点

- **术语疲劳**：prompt / context / harness engineering 被视为同一问题的不同切面与营销周期。
- **反「全能单 Agent + 塞满文档」**：上下文非 RAM；子域专家 + Manager 分解与路由，优于单一体。
- **与公开 harness 叙事的映射**：progressive disclosure、repo as source of truth、mechanized routing — 作者称为「正常工程」。
- **对文献的态度**：SWE-agent ACI、Anthropic initializer+coding 双代理等仍值得读；反感的是**新词造学科**而非具体技术。
- **经验法则（无新词版）**：信息少而准、模块化、知识在仓内、路由结构化、反馈环收紧；类比分离关注点、单一职责、docs-as-code、shift-left。
- **强模型未带来质变**：how-to-sglang 上突破来自环境而非换更大模型；并追问未来是否由模型自建环境。

## 值得注意的论断

- 巨型 `AGENTS.md` / 单文件维护说明与 OpenAI Codex 团队「一坨 AGENTS.md 必腐烂」的叙述**一致**（作者独立踩坑）。
- 对「harness engineering 是否构成独立学科」持**否定**，对其中**工程模式**持**肯定**——阅读时需区分**话语层**与**实践层**。

## 实体

- [[Chayenne Zhao]] — 作者；SGLang / how-to-sglang 语境。
- [[OpenAI]] — 文中作为「单文件 AGENTS.md 失败」的引用对照。
- [[Anthropic]] — 文中肯定 initializer + coding 双代理参考 value。

## 概念

- [[Harness engineering（代理脚手架）]] — 本文从**元话语**侧补充：实践可与本概念重叠，**命名与学科边界**可争议。
