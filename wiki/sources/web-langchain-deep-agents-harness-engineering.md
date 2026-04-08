---
title: Web｜LangChain：Improving Deep Agents with harness engineering
type: source-summary
created: 2026-04-08
updated: 2026-04-08
sources:
  - web/langchain-deep-agents-harness-engineering/article.md
tags:
  - ai
  - engineering
  - llm
---

# Web｜LangChain：Improving Deep Agents with harness engineering

> [!source] raw/web/langchain-deep-agents-harness-engineering/article.md

## 概述

LangChain 团队记录 **deepagents-cli** 在 **Terminal Bench 2.0** 上仅通过改 **harness**（固定 **gpt-5.2-codex**）将分数从 **52.8%** 提到 **66.5%** 的路径：以 **LangSmith Traces** 做规模化失败分析；压缩旋钮为 **System Prompt / Tools / Middleware**；用 **Trace Analyzer** 技能化「拉 trace → 并行错误分析 → 汇总改 harness」的外环；在内环强调 **build–verify**、`PreCompletionChecklistMiddleware`、`LocalContextMiddleware`、可测性提示与时间预算、`LoopDetectionMiddleware` 反 doom loop，以及 **reasoning sandwich**（xhigh–high–xhigh）应对超时与算力权衡。正文含多图（见 `assets/`）。

## 要点

- **Trace 外环**：把 trace 当改进信号；自动化分析省工时，但要防 **过拟合单题** 导致回归。
- **自证闭环**：规划时就想好如何验证；跑测试并对照 **task spec** 而非自我阅读代码即停。
- **环境注入**：启动时映射目录与工具链，减少搜索失误；明示评分/路径/边界用例与 **slop** 风险。
- **中间件**：退出前 checklist、循环检测、本地上下文等——属针对**当前**模型行为的工程护栏。
- **推理档位**：全程 xhigh 可能因超时更差；规划与验证两端加重推理的「三明治」启发式。
- **跨模型**：同一 harness 换 Claude Opus 需重新跑改进环；原则可迁移，**per-model 调参**仍必要。

## 值得注意的论断

- 明确 **harness engineer** 角色：为代理 **准备并投递上下文**，使其能自主完成任务。
- 公开 **traces 数据集** 与 Deep Agents **开源**（Python/JS）指向社区复现与对比。

## 实体

- [[LangChain]] — 出品方；LangSmith、deepagents-cli、Terminal Bench 实验语境。
- [[OpenAI]] — 文中固定使用 **GPT-5.2-Codex**；与 Codex 提示指南交叉引用。

## 概念

- [[Harness engineering（代理脚手架）]] — 偏 **benchmark + trace 驱动迭代** 与 **middleware 旋钮** 的一条工业叙事。
