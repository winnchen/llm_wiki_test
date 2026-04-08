---
title: Web｜LangChain：Improving Deep Agents with harness engineering
type: source-summary
created: 2026-04-08
updated: 2026-04-08
density: high
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

LangChain Blog（2026-02-17）记录 **deepagents-cli** 在 **Terminal Bench 2.0**（89 题，涵盖 ML / debug / biology 等）上仅通过改 harness（固定 **gpt-5.2-codex**）将分数从 **52.8%** 提到 **66.5%** 的路径。框架：把 harness 旋钮压缩为 **System Prompt / Tools / Middleware**；用 **LangSmith Traces** 做规模化失败分析；以 **Trace Analyzer** agent skill 技能化外环改进。正文含 5 幅图（`assets/`）。

## 核心论点

Harness engineer 的角色定义：**为代理准备并投递上下文**，使其能自主完成任务。模型是 black box，但 inputs/outputs 在文本空间可观测——trace 就是改进信号。

## 实验设置

- **Terminal Bench 2.0**：89 道跨域任务。
- **Harbor** 编排运行 → **Daytona** 沙箱。
- 所有 agent action 存入 **LangSmith**（含 latency、token count、cost）。

## 关键改进手段

### 1. Build–Verify 自证闭环

模型最常见失败：写完代码 → 自读代码 → 认为 OK → 停。缺少**对 task spec 而非自身代码**的验证。

四步引导：Planning & Discovery → Build（含写测试）→ **Verify（跑测试、对照 spec）** → Fix。

`PreCompletionChecklistMiddleware`：agent 提交前强制执行验证 pass（Ralph Wiggum Loop 式钩子）。

### 2. 环境注入

- `LocalContextMiddleware`：启动时映射 `cwd`、父/子目录、可用工具（Python 安装等）→ 减少搜索错误、**onboard agent 到环境**。
- **可测性提示**：告知 agent 代码将被程序化测试打分；提及文件路径需精确；强调 edge case。
- **Time budgeting**：注入时间预算警告 → 引导 agent 从实现切到验证（agent 默认不擅时间管理）。

### 3. 反死循环

`LoopDetectionMiddleware`：追踪 per-file 编辑次数 → 超过 N 次注入「考虑换思路」。针对当前模型弱点；模型变强后可能不再需要。

### 4. 推理预算三明治

gpt-5.2-codex 四档：`low` / `medium` / `high` / `xhigh`。

| 策略 | 分数 | 问题 |
|------|------|------|
| 全程 xhigh | 53.9% | 大量超时 |
| 全程 high | 63.6% | — |
| **xhigh–high–xhigh**（三明治） | **66.5%** | 规划+验证重推理，中间实现轻推理 |

### 5. Trace Analyzer Skill（外环）

1. 从 LangSmith 拉 experiment traces
2. 并行 spawn 错误分析 agents → 主 agent 汇总发现 + 建议
3. 人工可选参与 → 定向改 harness

类似 **boosting**：聚焦前一轮的错误。需防**过拟合单题**导致回归。

## 跨模型对照

- 同一 harness 换 **Claude Opus 4.6**（未经同等 improvement loop）：**59.6%**。
- 原则可迁移，但 **per-model 调参**仍必要（Codex prompting guide ≠ Claude prompting guide）。
- 未来方向：**multi-model harness**（大模型 plan → 小模型 implement）、**adaptive reasoning**（Claude / Gemini 已有）、**RLMs** 更高效挖掘 trace。

## 开放贡献

- 公开 **traces 数据集**：[LangSmith public](https://smith.langchain.com/public/29393299-8f31-48bb-a949-5a1f5968a744/d?tab=2)
- **Deep Agents** 开源：[Python](https://github.com/langchain-ai/deepagents) / [JavaScript](https://github.com/langchain-ai/deepagentsjs)

## 值得注意的论断

- Harness 改进的收益（+13.7pp）在固定模型上实现——证明 **环境设计 ≠ 换更大模型**。
- 「guardrails may dissolve as models improve, but they help now」——与 Anthropic「每个组件编码模型弱点假设」一致。

## 实体

- [[LangChain]] — 出品方；LangSmith / deepagents-cli / Terminal Bench 语境
- [[OpenAI]] — 固定使用 GPT-5.2-Codex；引用 Codex prompting guide

## 概念

- [[Harness engineering（代理脚手架）]] — 偏 benchmark + trace 驱动迭代与 middleware 旋钮
