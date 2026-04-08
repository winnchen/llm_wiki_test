---
title: Harness engineering：定义、原则与实践清单
type: synthesis
created: 2026-04-08
updated: 2026-04-08
sources:
  - web/harness-engineering-martinfowler/article.md
  - web/harness-engineering-openai/article.md
  - web/harness-design-long-running-apps/article.md
  - web/my-ai-adoption-journey/article.md
tags:
  - ai
  - engineering
  - llm
---

# Harness engineering：定义、原则与实践清单

本文在概念页 [[Harness engineering（代理脚手架）]] 之上，把多篇公开叙述**压缩为可执行的定义、原则与 checklist**，便于团队对齐与自查。细颗粒引用见各 source-summary 与 `raw/web/` 原文。

## 工作定义

**Harness engineering** 指在 **coding agent** 场景下，围绕模型设计并持续演进的一整套**可控环境**：用可执行的规则、工具、测试与观测提高「一次做对」的概率，并在失败时产出**代理可消费的反馈**，使人类在注意力有限的前提下仍能对**质量与架构边界**保持信心。

它与「写一段超长 system prompt」不是同一类工作：核心是把意图与约束**落进仓库**——可发现、可版本化、尽量**可机械校验**，而不是仅停留在聊天或文档孤岛里。

语言上可叠用 Fowler 的 **guides（feedforward）** 与 **sensors（feedback）**，并区分 **computational**（快、确定）与 **inferential**（慢、语义、更不确定）两类控制。OpenAI 侧重 **仓库结构 + linter/结构测试 + 可观测性**；Anthropic 侧重 **多角色分工 + 真实环境评测**（如浏览器驱动）；Mitchell 侧重 **个人侧的 `AGENTS.md` 与真脚本工具**。尺度不同，问题是同构的。

## 原则

1. **默认可验证，少靠「说明书 blob」**  
   大段自然语言易腐烂；优先目录约定、边界解析、结构测试、自定义 lint；错误信息宜含**自纠提示**（remediation-in-the-message）。

2. **小入口、渐进披露**  
   `AGENTS.md`（或等价物）作**地图**与稳定指针；深度内容放在 `docs/` 等结构中，避免单文件挤爆上下文。

3. **反馈左移、全生命周期分布**  
   快检靠近编辑/提交；贵检进 CI；对**持续漂移**（依赖、死代码、测试质量等）用「常驻传感器」视角规划。

4. **需要时分离生成与评测**  
   主观质量或自评放水时，独立 **evaluator**（或人、或更冷/更强的审查代理）通常优于生成者自评；评测应贴近**真实运行路径**（UI/API/数据）。

5. **按调节对象选 harness，避免混谈**  
   维护性、架构 **fitness**、**行为正确性** 难度与工具集不同；行为类尤其忌**过度信任**「AI 写的测试全绿」即等于可靠（多篇原文的共识风险点）。

6. **Harness 是演进资产**  
   重复失败应回流为新的 guide/sensor 或文档规则（steering loop）；与「个人逐条补 `AGENTS.md`」同一逻辑。

7. **随模型能力重估脚手架**  
   每个组件往往编码了对**当前**模型弱点的假设；新模型发布后应做**减法实验**，拆除不再承重的复杂度。

8. **「看不见 = 不存在」**  
   仅存在于聊天、脑内或非版本化 wiki 的共识，对代理等价于不存在；与给新同事 onboarding 的要求一致。

## 实践清单（落地）

| 领域 | 可做项 |
|------|--------|
| 结构 | 分层/模块边界；**依赖方向**可测；横切关注点经**窄接口**进入（如 Providers 式聚合）。 |
| 知识 | `docs/`（或等价）为真源；交叉链接、所有权、新鲜度尽量可检查；周期性 doc-gardening。 |
| 运行时 | 隔离 dev/worktree 环境；日志、指标、trace 可查；必要时 UI 自动化或 API 探针。 |
| 流程 | PR 短命、反馈环短；高代理吞吐下，合并门闩与**风险**显式匹配。 |
| 个人 | 除文档外提供**可调用脚本**（截图、过滤测试、批处理），减少「口头教代理」。 |

## 与相邻条目

- **概念层定义与来源列表**：[[Harness engineering（代理脚手架）]]
- **个人采用路径（与团队 harness 衔接）**：[[个人 AI 采用与工作流]]
- **一手来源**：[[Web｜Martin Fowler：Harness engineering for coding agent users]]、[[Web｜OpenAI：Harness engineering（Codex）]]、[[Web｜Anthropic：Harness design for long-running apps]]、[[Web｜Mitchell Hashimoto：My AI adoption journey]]

## 局限

> [!gap] 公开文均为特定组织/时期的叙事；落地需按栈、合规与团队成熟度裁剪，并用自己的失败样本校准 evaluator 与 lint 规则。
