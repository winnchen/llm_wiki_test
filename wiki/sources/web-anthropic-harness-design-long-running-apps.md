---
title: Web｜Anthropic：Harness design for long-running apps
type: source-summary
created: 2026-04-08
updated: 2026-04-08
density: high
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

Prithvi Rajasekaran（Anthropic Labs，2026-03-24）记录在**前端设计美感**与**长时程全栈自主构建**两条线上突破 baseline 的 harness 设计：借鉴 GAN 思路做 **generator + evaluator** 闭环，再扩展为 **planner + generator + evaluator** 三代理架构；对比 solo vs full harness 的成本/质量差；讨论随 Opus 4.6 演进**删减组件**的方法论。配图 8 幅（`assets/`）；DAW 段落依赖原文视频。

## 核心论点

Harness 中**每一层复杂度都编码了对当前模型弱点的假设**；新模型发布时应逐个组件 stress test，拆除不再承重的部件——「find the simplest solution possible, and only increase complexity when needed」。

## 两个关键问题

### 1. 上下文焦虑与 reset vs compaction

| 策略 | 做什么 | 优势 | 代价 |
|------|--------|------|------|
| **Compaction** | 原地摘要早期对话 | 保持连续性 | 不给 clean slate，焦虑可能持续 |
| **Context reset** | 彻底清窗 + 结构化 handoff | 消除焦虑 | 需高质量 handoff artifact；增加编排复杂度与延迟 |

Sonnet 4.5 上 compaction 不够 → reset 成为必须；Opus 4.6 移除焦虑行为 → 可去掉 reset、改用 SDK 自动 compaction。

### 2. 自评偏差

模型倾向自我表扬；独立 **evaluator** 更易调「怀疑度」：把评估从生成者剥离 → 可针对性 tune evaluator → generator 获得可迭代的外部反馈。

## 三代理架构

| 角色 | 职责 | 细节 |
|------|------|------|
| **Planner** | 1–4 句 prompt → 完整产品 spec | 偏重产品上下文与高层技术设计，不指定细粒度实现（避免错误级联）；可指示织入 AI features |
| **Generator** | 按 sprint/合约逐特性实现 | React + Vite + FastAPI + SQLite/PostgreSQL；sprint 结尾自评后交 QA |
| **Evaluator** | 通过 **Playwright MCP** 真机交互 → 打分 + 写 critique | 四维（设计 / 原创性 / 工艺 / 功能），权重偏前两项以对抗 AI slop；用 **few-shot** 校准评分 |

**Sprint 合约**：每个 sprint 前 generator 与 evaluator 协商「done 的定义」→ 双方认可后才开始编码。

**代理间通信**：**文件式**——一方写文件、另一方读取并回应（或写新文件），保持可追溯。

## 成本与效果数据

| 场景 | 时间 | 费用 | 备注 |
|------|------|------|------|
| Solo（Opus 4.5）| 20 min | $9 | 核心功能损坏 |
| Full harness v1（Opus 4.5）| 6 hr | $200 | 功能基本可用 |
| 简化 harness v2（Opus 4.6）| 3 hr 50 min | $124.70 | 去 sprint；evaluator 单轮末尾 |

v2 细分：Planner 4.7min/$0.46 → Build R1 2h7m/$71 → QA R1 8.8m/$3.2 → Build R2 1h2m/$37 → QA R2 6.8m/$3.1 → Build R3 10.9m/$5.9 → QA R3 9.6m/$4.1

## 前端设计实验亮点

- **「museum quality」措辞**直接影响生成方向——criteria prompting 本身就是引导。
- 5–15 轮迭代；分数通常上升但非线性（中间轮有时比末轮好）。
- 荷兰美术馆案例：第 10 轮从平面暗色着陆页跳跃到 CSS 3D 透视画廊空间——罕见的创意突变。

## 值得注意的论断

- Evaluator 开箱即用是**差劲 QA**——会发现问题后自说自话说「不算大事」并放行；需多轮人工校准 prompt 才可靠。
- 简化 harness 时应**逐个移除组件并测效果**，而非一刀切。
- Harness 研究的有趣组合空间**不随模型变强而缩小，而是移动**。

## 实体

- [[Anthropic]] — 出品方；Claude / Labs / Agent SDK 语境

## 概念

- [[Harness engineering（代理脚手架）]] — 多代理编排与长时程任务的代表性方案
