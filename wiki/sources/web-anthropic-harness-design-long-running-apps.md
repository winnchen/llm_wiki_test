---
title: Web｜Anthropic：Harness design for long-running apps
type: source-summary
created: 2026-04-08
updated: 2026-04-08
sources:
  - web/harness-design-long-running-apps/article.md
tags:
  - ai
  - engineering
  - llm
---

# Web｜Anthropic：Harness design for long-running apps

> [!source] raw/web/harness-design-long-running-apps/article.md

## 概述

Anthropic Labs 作者记录如何在前端美感与**长时程自主构建**两条线上推进：借鉴 **GAN** 思路做 **generator + evaluator** 闭环；evaluator 用 **Playwright MCP** 在真实页面上交互、打分与写 critique；再扩展到 **planner + generator + evaluator** 三代理全栈 harness，对比 solo 与完整 harness 的成本与质量，并讨论随 **Opus 4.6** 等模型演进**删减 sprint 结构**、调整 evaluator 介入时机的经验。正文多图已归档 `assets/`；DAW 段落依赖**原文视频**，离线仅文字说明。

## 要点

- **自评偏差**：生成代理倾向自我表扬；独立 evaluator 更易调「怀疑度」并形成可迭代反馈。
- **前端四条评分维度**：设计整体性、原创性、工艺、功能性；强调前两项权重以对抗「AI slop」。
- **全栈三角色**：Planner 扩写短 prompt 为产品 spec；Generator 按 sprint/合约实现；Evaluator 按合约与 Playwright 实测打回问题。
- **上下文焦虑 vs reset vs compaction**：长任务中模型过早收尾；reset 换干净上下文但依赖 handoff 工件质量；与仅 compaction 不同。
- **成本与效果**：文中给出 solo / full harness 时间与费用量级对比；后续简化 harness（去 sprint、evaluator 单轮等）随模型变强而重估。

## 值得注意的论断

- Harness 中每一层复杂度都对应**对模型弱点的假设**；新模型发布时应**压力测试并拆除不再承重**的部件。
- 文件式通信（读写同一批工件）有助于在多代理间保持可追溯与合约感。

## 实体

- [[Anthropic]] — 出品方与 Claude / Labs 语境。

## 概念

- [[Harness engineering（代理脚手架）]] — 多代理编排与长时程任务的代表性方案。
