---
title: Web｜OpenAI：Harness engineering（Codex）
type: source-summary
created: 2026-04-08
updated: 2026-04-08
density: high
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

Ryan Lopopolo（OpenAI，2026-02-11）记录一个内部产品从空仓库到**约 100 万行代码**、五个月内**零手写代码**的实验——所有代码（业务逻辑、测试、CI、文档、内部工具、可观测性）均由 Codex 生成。核心论点：工程师从「写代码」转向**设计环境、表达意图、构建反馈回路**。配图 4 幅（`assets/`）。

## 核心论点

瓶颈不在模型能力，而在**环境不充分**——早期进展慢是因为 agent 缺少可用的工具、抽象与结构，而非「不够聪明」。修复方法永远是「补缺什么能力并使其对 agent 可发现、可执行」。

## 关键数据

| 指标 | 值 |
|------|-----|
| 代码量 | ~100 万行 |
| PR 数 | ~1500（五个月） |
| 团队规模 | 3 → 7 工程师 |
| 人均日 PR | 3.5（且随团队增长未下降） |
| 单次运行时长 | 可达 6+ 小时（夜间无人值守） |

## 关键实践

### 仓库即系统

- 反对「一坨巨型 AGENTS.md」——context 稀缺、太多指导 = 无指导、单体文档必腐烂、难机械校验。
- `AGENTS.md`（~100 行）作 **table of contents**；深度内容在 `docs/`（design-docs / exec-plans / product-specs / references 等）。
- **Progressive disclosure**：agent 从稳定入口出发，被教会去哪里找深层信息。
- CI + linter **机械校验** docs 结构、交叉引用、新鲜度；**doc-gardening agent** 周期性扫描过时文档并开 fix-up PR。

### 可观测与可驱动

- **Per-worktree** 启动应用实例：每个 change 一个隔离环境（含日志/指标/trace），任务完成后销毁。
- **Chrome DevTools Protocol** → DOM 快照、截图、导航，使 Codex 能复现 bug、验证 fix、推理 UI 行为。
- 本地可观测性栈：**LogQL / PromQL** 让 agent 查 logs/metrics → 可执行「确保启动 < 800ms」类 prompt。

### 架构与「taste」

- **严格分层**：每个业务域 Types → Config → Repo → Service → Runtime → UI；横切关注点通过唯一接口 **Providers** 进入。
- 自定义 linter + 结构测试机械执行：命名规范、结构化日志、文件大小限制、平台可靠性要求等。
- Error message 里写 **remediation 指令**——正向 prompt injection。
- **「Boring technology」偏好**：composable、API 稳定、在训练集中充分表示的依赖；有时自实现比引入不透明外部库更划算（如自写带 OpenTelemetry 的 map-with-concurrency 替代 `p-limit`）。

### 吞吐与合并

- 高代理吞吐下缩短 PR 寿命、弱化阻塞门闩；flake 用 follow-up run 处理而非阻塞。
- Agent 使用 `gh`、local scripts 等标准工具直接操作——「**Ralph Wiggum Loop**」：Codex 自审 → 请求更多 agent review → 循环直到满意 → squash & merge。

### 熵与垃圾回收

- 早期人工每周五花 20% 清理「AI slop」→ 不可扩展 → 改为编码 **golden principles** + 周期性 Codex 扫描 → 开 PR 修复质量等级与漂移。

## 值得注意的论断

- 「Agent 看不见 = 不存在」——Slack 讨论、脑内共识对 agent 等价于不存在，与新人 onboarding 同理。
- 代码可读性**首先服务于下一任 agent**，不必完全匹配人类风格偏好。
- 最大困难已从写代码转向**设计环境、反馈回路与控制系统**。

## 实体

- [[OpenAI]] — 出品方；Codex / agent-first 工程实践
- [[Anthropic]] — 文中引用外部工程博文

## 概念

- [[Harness engineering（代理脚手架）]] — 工业界大规模 agent-first 落地案例
