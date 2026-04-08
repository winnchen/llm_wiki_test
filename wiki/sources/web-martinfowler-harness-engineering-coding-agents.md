---
title: Web｜Martin Fowler：Harness engineering for coding agent users
type: source-summary
created: 2026-04-08
updated: 2026-04-08
sources:
  - web/harness-engineering-martinfowler/article.md
tags:
  - ai
  - engineering
  - llm
---

# Web｜Martin Fowler：Harness engineering for coding agent users

> [!source] raw/web/harness-engineering-martinfowler/article.md

## 概述

面向**使用编码代理的工程师**，提出一套可讨论的心智模型：用 **feedforward（guides）** 与 **feedback（sensors）** 组合成外层 harness，区分 **computational** 与 **inferential** 控制，并按调节对象分为 **可维护性 / 架构契合（fitness）/ 行为** 三类 harness；强调人在回路中持续「掌舵」迭代 harness。正文含多幅示意图（已归档于同目录 `assets/`）。

## 要点

- **Harness 边界**：在「编码代理」语境下收窄 harness 含义；与「Agent = Model + Harness」等宽泛说法区分 **builder harness** 与 **user harness**。
- **Guides vs sensors**：事前引导与事后观测自纠；仅反馈或仅前馈都会失衡。
- **Computational vs inferential**：测试/静态分析/结构测试 vs 语义审查、LLM-as-judge；成本、速度与确定性不同。
- **三类 harness**：可维护性（当前工具最多）、架构 fitness（性能/可观测性等）、行为（功能正确性仍最难，依赖规格 + 测试套件 + 人工探索等）。
- **Harnessability**：语言类型、模块边界、框架惯例影响「可脚手架化」程度；绿场与遗留难度不同。
- **Harness templates**：企业常见拓扑可演化为「脚手架模板包」，但会有版本漂移问题。

## 值得注意的论断

- 行为类 harness 上，**过度信任 AI 生成的测试**仍不足；需配合如 approved fixtures 等模式，且无法一劳永逸。
- 将讨论从「单个 skill/MCP」上移到**控制系统整体设计**，与工业界 OpenAI、Stripe 等公开实践互证（文中引用）。

## 实体

- [[Martin Fowler]] — 作者、Thoughtworks 相关讨论背景。
- [[OpenAI]] — 文中引用其 harness 工程公开文。
- [[Anthropic]] — 文中引用长时程 harness 设计文。

## 概念

- [[Harness engineering（代理脚手架）]] — 本文是术语与分类框架的主要来源之一。
