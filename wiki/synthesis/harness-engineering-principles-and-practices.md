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
  - web/x-genai-is-real-harness-engineering-critique/article.md
  - web/langchain-deep-agents-harness-engineering/article.md
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

语言上可叠用 Fowler 的 **guides（feedforward）** 与 **sensors（feedback）**，并区分 **computational**（快、确定）与 **inferential**（慢、语义、更不确定）两类控制。OpenAI 侧重 **仓库结构 + linter/结构测试 + 可观测性**；Anthropic 侧重 **多角色分工 + 真实环境评测**（如浏览器驱动）；Mitchell 侧重 **个人侧的 `AGENTS.md` 与真脚本工具**；LangChain 侧重 **固定模型下用 trace 做外环迭代**（Terminal Bench 上只改 harness 提分）。尺度不同，问题是同构的。

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

9. **Trace 驱动的 harness 外环（可选但强）**  
   批量跑任务 → 聚类失败模式 → **针对性**改 prompt / 工具 / 中间件；把分析流程技能化（如「Trace Analyzer」思路），避免只靠人肉看单次聊天。注意 **过拟合单题** 会伤泛化，改动需回归多任务。（见 `raw/web/langchain-deep-agents-harness-engineering/article.md`。）

10. **在「准备交卷」处强制自检**  
    代理默认容易「看一眼自己的代码就停」；用 **退出前钩子**（如 checklist middleware）显式要求：跑测试、对照 task spec 而非自我确认。（与 Ralph 式 loop 同类：用钩子补默认行为。）

11. **把运行环境说明喂给代理**  
    工作目录结构、可用解释器/工具链、**时限与评分方式**（若在 bench/CI 里）应用 **注入式上下文** 写好，减少瞎 `find`/猜路径；对「可测性」要在提示里写清评分依据。（LangChain 文中 *LocalContext*、可测性提示、时间预算等。）

12. **短期「反死循环」启发式**  
    对同一文件反复微调仍失败时，用中间件累计编辑次数并 **注入「考虑换思路」** 类提醒；这是针对**当前**模型弱点的临时护栏，模型变强后应复审是否拆除。

13. **推理/算力预算与任务阶段匹配**  
    在**强时限**场景，全程最高推理档可能导致超时；可尝试把重推理放在 **规划** 与 **验证** 两端（「三明治」启发式），中间实现用较轻设置——需用你自己的 SLA 与基准数据校准。

## 实践清单（落地）

| 领域 | 可做项 |
|------|--------|
| 结构 | 分层/模块边界；**依赖方向**可测；横切关注点经**窄接口**进入（如 Providers 式聚合）。 |
| 知识 | `docs/`（或等价）为真源；交叉链接、所有权、新鲜度尽量可检查；周期性 doc-gardening。 |
| 运行时 | 隔离 dev/worktree 环境；日志、指标、**trace** 可查；必要时 UI 自动化或 API 探针；批量跑分时有 **trace 归档** 便于外环改 harness。 |
| 流程 | PR 短命、反馈环短；高代理吞吐下，合并门闩与**风险**显式匹配。 |
| 个人 | 除文档外提供**可调用脚本**（截图、过滤测试、批处理），减少「口头教代理」。 |

## 与相邻条目

- **概念层定义与来源列表**：[[Harness engineering（代理脚手架）]]
- **各家长文怎么落在不同场景**：[[Harness 实践对照：OpenAI、Anthropic、LangChain 与 Fowler]]
- **个人采用路径（与团队 harness 衔接）**：[[个人 AI 采用与工作流]]
- **一手来源（已 ingest）**：[[Web｜Martin Fowler：Harness engineering for coding agent users]]、[[Web｜OpenAI：Harness engineering（Codex）]]、[[Web｜Anthropic：Harness design for long-running apps]]、[[Web｜Mitchell Hashimoto：My AI adoption journey]]、[[Web｜LangChain：Improving Deep Agents with harness engineering]]（原则 9–13 主要据此篇压缩）
- **对照声部**：[[X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验]] — 指出「环境设计」早于新词；实践上与本篇原则**大量同构**，分歧主要在**是否要用 harness engineering 作为学科标签**及社区传播方式。

## 元话语提醒

本篇 checklist **不依赖**「harness engineering」这一名称即可使用。[[Chayenne Zhao]] 的批评提醒我们：团队对齐时可以用**中性词**（环境、约束、路由、反馈环、仓库真源）沟通，避免把常识重包装后制造不必要的 FOMO；同时仍可单独引用各公司的**案例与数据**（benchmark、trace、中间件名等）。

## 局限

> [!gap] 公开文均为特定组织/时期的叙事；落地需按栈、合规与团队成熟度裁剪，并用自己的失败样本校准 evaluator 与 lint 规则。

> [!gap] **未来形态**：若模型持续变强，「环境由谁设计、多少今日原则会失效」仍是开放问题（参见 [[X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验]] 文末对 OpenClaw 式增长的疑问）。本篇原则偏**当前**人机分工，需随实践复审。
