---
title: Web｜OpenAI：Harness engineering（Codex）
type: source-summary
created: 2026-04-08
updated: 2026-04-08
sources:
  - web/harness-engineering-openai/article.md
tags:
  - ai
  - engineering
  - llm
---

# Web｜OpenAI：Harness engineering（Codex）

> [!source] raw/web/harness-engineering-openai/article.md

## 概述

OpenAI 团队描述如何用 **Codex** 在约五个月内以「零手写代码」约束交付大规模内部产品：核心不是堆提示词，而是把 **仓库做成 agent 可读的系统**——结构化 `docs/`、短 **`AGENTS.md` 作目录**、**自定义 linter / 结构测试**、**分层架构规则**、**doc-gardening** 与「golden principles」式持续纠偏。配图（Chrome DevTools、可观测性、知识边界、分层架构）已落盘 `assets/`。

## 要点

- **角色转变**：工程师主要设计环境、意图表达与反馈回路，而非逐行写业务代码。
- **可观测与可驱动**：worktree 级启动应用、Chrome DevTools Protocol、本地日志/指标/追踪（LogQL/PromQL 等）让代理能验证 UI 与 SLO。
- **知识库**：反对单一巨型 `AGENTS.md`；以 `docs/` 为真源、渐进披露；CI/linter 校验结构与交叉引用。
- **架构**：强边界、分层依赖方向、Providers 承载横切关注点；以机械约束换速度而不放任腐化。
- **合并与吞吐**：高代理吞吐下缩短 PR 寿命、弱化阻塞门闩等规范需与风险匹配。
- **「垃圾回收」式治理**：周期性扫描文档/质量等级与漂移并开 PR 修复。

## 值得注意的论断

- 明确将困难归结为 **环境、反馈与控制** 设计，而非模型单点能力。
- 「全仓库由代理生成」意味着 **可读性优先服务于下一任代理**，与人类审美可分离。

## 实体

- [[OpenAI]] — 出品方与工程实践场域。
- [[Anthropic]] — 文中引用外部工程博文（架构品味等）。

## 概念

- [[Harness engineering（代理脚手架）]] — 工业界大规模 agent-first 落地案例。
