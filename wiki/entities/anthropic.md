---
title: Anthropic
type: entity
created: 2026-04-08
updated: 2026-04-08
sources:
  - web/harness-design-long-running-apps/article.md
tags:
  - ai
  - business
aliases:
  - Anthropic Labs
---

# Anthropic

## 概述

AI 研究与产品公司；本库条目侧重 **Anthropic Engineering / Labs** 关于**长时程编码 harness** 与 **多代理（planner / generator / evaluator）** 设计的公开实验记录，以及与 **Claude**、**Agent SDK**、**Playwright MCP** 结合的实践。

## 要点

| 属性 | 说明 |
|------|------|
| 本库出现 | [[Web｜Anthropic：Harness design for long-running apps]] |
| 相关产品语境 | Claude、Claude Agent SDK、前端 design skill 插件生态（文中链接） |

## 出现记录

- [[Web｜Anthropic：Harness design for long-running apps]] — 长时程应用 harness 与 GAN 式生成-评估循环。
- [[Web｜Martin Fowler：Harness engineering for coding agent users]] — 被 Fowler 引用为 orchestration / 长时程 harness 背景。
- [[Web｜OpenAI：Harness engineering（Codex）]] — 文中引用其工程博文作为外部参考。

## 关联

- [[Harness engineering（代理脚手架）]] — 多代理与 evaluator 设计的代表来源。
- [[OpenAI]] — 工业界 agent-first 工程的并列参照。

## 开放问题

- 模型版本（如 Opus 4.5 / 4.6）与 harness 简化策略强相关，阅读时应对照发文日期。
