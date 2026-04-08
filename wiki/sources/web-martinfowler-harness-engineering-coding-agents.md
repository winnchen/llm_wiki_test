---
title: Web｜Martin Fowler：Harness engineering for coding agent users
type: source-summary
created: 2026-04-08
updated: 2026-04-08
density: high
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

Martin Fowler（2026-04-02）为**使用编码代理的工程师**提出分类心智模型：用控制论式 **feedforward（guides）** 与 **feedback（sensors）** 构建外层 harness，区分 **computational**（确定、快、CPU）与 **inferential**（语义、慢、GPU/LLM）两类控制，并按调节目标分为三类 harness。正文含 6 幅示意图（已归档 `assets/`）；文末承认 **行为类 harness** 仍是最大缺口。

## 核心论点

Harness 在编码代理场景下的价值不在于让 agent 更聪明，而在于 **外部化人类经验**——把内隐的审美、惯例、组织对齐转为可机械校验的 guides / sensors，将有限人力导向**最需要判断力的环节**。

## 关键框架

### Guides vs Sensors

| 方向 | 作用 | 单独使用的缺陷 |
|------|------|----------------|
| **Guides（feedforward）** | 事前引导，提高首次正确率 | 编码了规则但不知是否生效 |
| **Sensors（feedback）** | 事后观测 + LLM 可消费的纠错信号 | 反复犯同一错误 |

### Computational vs Inferential

| 类型 | 特征 | 例子 |
|------|------|------|
| **Computational** | 确定、快、CPU | 测试、linter、类型检查、结构分析 |
| **Inferential** | 语义、慢、非确定 | AI 代码审查、LLM-as-judge |

### 三类 Harness

1. **可维护性（Maintainability）**：工具最成熟；computational sensors 可靠捕获重复代码、复杂度、覆盖率、风格等；**LLM 部分捕获**语义重复、过度工程；**均不可靠**的：误诊、过度工程、误解指令——即人类未明确 spec 时。
2. **架构契合（Architecture fitness）**：性能/可观测性/logging 标准等 → Fitness Functions（Thoughtworks 术语）。
3. **行为（Behaviour）**：功能正确性；当前主流仅 spec + AI 生成测试套件绿 + 手动探索；**过度信任 AI 测试仍不足**；approved fixtures 模式可选但非万能。

### 具体 examples 矩阵（原文表）

| 领域 | 方向 | 类型 | 实现举例 |
|------|------|------|----------|
| 编码惯例 | feedforward | Inferential | AGENTS.md、Skills |
| 新项目引导 | feedforward | Both | Skill + bootstrap 脚本 |
| Code mods | feedforward | Computational | OpenRewrite recipes 等 |
| 结构测试 | feedback | Computational | ArchUnit 检查模块边界 |
| 审查指令 | feedback | Inferential | Skills |

## 其他重要概念

- **Steering loop**：人持续迭代 harness；重复失败应回流为新 guide/sensor；**可用 AI 帮写结构测试、linter、规则草稿**。
- **Keep quality left**：与 CI/CD 一脉——快检在提交前、贵检进流水线；新增「持续漂移」传感器（死代码、覆盖率质量、依赖扫描、运行时 SLO 监控等）。
- **Harnessability**：强类型语言、清晰模块边界、框架惯例提供天然 sensor 位；**greenfield 可从 Day 1 内建**，legacy 最需要却最难建。
- **Harness templates**：企业常见服务拓扑可演化为「harness 模板包」；但与 service templates 同样面临**实例化后版本漂移**。
- **Ashby's Law**（控制论）：调控者的多样性需 ≥ 被调控系统——隐含 harness 的复杂度需与代码库匹配。

## 值得注意的论断

- 行为类 harness 上，**AI 测试「绿且高覆盖」≠ 可信**；社区还远未解决此问题。
- Harness 不应替代全部人类输入，而应**把人导向最高杠杆处**。
- 「Sensor 从不触发」可能是高质量，也可能是检测不足——需类似 mutation testing 的 harness 覆盖度度量。
- Stripe minions write-up（pre-push heuristic linter、blueprints）与文中框架互证。

## 实体

- [[Martin Fowler]] — 作者；Thoughtworks / 控制论 / Fitness Functions 语境
- [[OpenAI]] — 文中引用 harness 实践
- [[Anthropic]] — 文中引用长时程 harness

## 概念

- [[Harness engineering（代理脚手架）]] — 本文是术语与分类框架的主要来源之一
