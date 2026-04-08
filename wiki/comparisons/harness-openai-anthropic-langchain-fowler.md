---
title: Harness 实践对照：OpenAI、Anthropic、LangChain 与 Fowler
type: comparison
created: 2026-04-08
updated: 2026-04-08
sources:
  - web/harness-engineering-openai/article.md
  - web/harness-design-long-running-apps/article.md
  - web/langchain-deep-agents-harness-engineering/article.md
  - web/harness-engineering-martinfowler/article.md
  - web/x-genai-is-real-harness-engineering-critique/article.md
tags:
  - ai
  - engineering
  - llm
---

# Harness 实践对照：OpenAI、Anthropic、LangChain 与 Fowler

## 概述

对比的是**公开长文**里各自强调的 harness：**OpenAI**（Codex 产品库）、**Anthropic**（长时程全栈与前端质量）、**LangChain**（基准分数 + trace 迭代）、**Martin Fowler**（给写代码的人用的分类框架）。不把「harness engineering」当成新哲学——只问：**他们各自在什么场景下、用什么具体手段、补模型的哪类短板**。另用 [[X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验]] 作**社区反思**：实践往往同构，差别常在**叙事与用词**。

## 对照表（场景 → 手段 → 一个例子）

| 声部 | 典型场景 | 最强调的抓手 | 一个可触摸的例子 |
|------|-----------|--------------|------------------|
| **[[OpenAI]]** | 真产品、大仓库、长期由代理改代码 | 短 `AGENTS.md` 当目录；`docs/` 当真源；**linter + 结构测试**；分层边界（Types→…→UI + Providers）；本地可观测性；偏好 **boring tech** | 用 **Chrome DevTools Protocol** 让代理复现 UI 问题、看真实运行，而不是只靠读代码猜 |
| **[[Anthropic]]** | 数小时自主搭应用；前端「好看不好」难验 | **多角色**：planner / generator / evaluator；评测用 **Playwright MCP** 真点页面；**sprint 合约**事前协商 done 标准；evaluator 需 **few-shot 校准** | 生成器做 UI，评估器用浏览器导航 + 截图 → 四维打分（设计 / 原创性 / 工艺 / 功能）→ 写 critique → 多轮改 |
| **[[LangChain]]** | 排行榜/基准上**固定模型**、只改外围提分 | **LangSmith trace** 批量找失败模式；**Trace Analyzer** 技能化复盘；旋钮收敛为 **prompt / tools / middleware**；**推理三明治**（xhigh–high–xhigh） | **交卷前 middleware**：拦截「要结束了」，强制再跑一轮对照 task spec 的验证（Ralph 式钩子用于 verify） |
| **[[Martin Fowler]]** | 教人**怎么谈论**编码代理周围的控制 | **Guides（前馈）** 与 **Sensors（反馈）**；computational vs inferential；按对象分 **可维护性 / 架构 fitness / 行为** 三类；**harnessability** 概念 | 在**变更生命周期**里画清：提交前 / 流水线 / 持续漂移类监控；追问 **harness 覆盖度**如何度量 |

### 数据对照

| 维度 | OpenAI | Anthropic | LangChain | Fowler |
|------|--------|-----------|-----------|--------|
| **规模/指标** | ~100 万行 / 1500 PR / 3.5 PR/人/天 | — | 89 题 Terminal Bench 2.0 | — |
| **效果量化** | 「1/10 时间」（自述估计） | solo $9/20min vs full harness $200/6hr | 52.8% → 66.5%（+13.7pp） | 定性框架，无 benchmark |
| **代理自治时长** | 单次可 6+ 小时（夜间无人） | 3–6 小时连续 | 受 Terminal Bench 超时限制 | N/A |
| **多代理 vs 单** | 单代理 + Ralph Wiggum Loop 自审链 | planner + generator + evaluator 三角色 | 单代理 + middleware 钩子 | 不限定 |
| **模型演进策略** | — | 逐个组件 stress test → 拆除不承重件 | per-model 需重新跑 improvement loop | harnessability 随语言/框架/模型变 |

**读表提示**：四行不是互斥「四种 harness」，而是**同一类工程**在不同战场上的**镜头不同**——有的写仓库治理，有的写 benchmark 迭代，有的写多代理编排，有的写词汇和分类。

## 简短分析（怎么想）

1. **场景决定显眼包**  
   OpenAI 必须回答「一百万行怎么不烂」→ 结构、文档真源、机械检查最显眼。Anthropic 要展示「几小时没人插手也能出完整产品」→ 分角色 + 真机评测显眼。LangChain 要证明「只动 harness 也能涨分」→ trace 外环和 middleware 显眼。Fowler 不负责替你部署 → 给你**分类和对话语言**，方便和团队对齐风险。

2. **重复出现的「老办法」（≥ 3 篇独立出现）**  
   - **环境改进 > 换更大模型**（OpenAI / LangChain / X 帖）  
   - **巨型单文件必腐烂** → progressive disclosure + 结构化 docs（OpenAI / X 帖 / Fowler 隐含）  
   - **自评偏差 → 独立评测**（Anthropic / LangChain / Fowler 行为 harness）  
   - **每层复杂度编码模型弱点 → 新模型做减法**（Anthropic / LangChain / Fowler）  
   - **退出前强制自检钩子**（OpenAI Ralph Loop / LangChain middleware / Anthropic 隐含）  
   详见 [[Harness engineering（代理脚手架）]] 的「跨源共识模式」表。这与 [[X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验]] 说的「分离关注点、文档进仓、结构化路由」是**同一张饼**，只是有人叫 harness，有人叫常识。

3. **不必强行统一术语**  
   对齐实践时，用**具体问题**比用标签快：我们现在是缺文档结构、缺评测、缺 trace 复盘，还是缺分工？对应上表某一列即可。

## 总结（三条）

- **共识**：都在给模型加**边界、反馈和可验证步骤**，减少「模型自己觉得对了」就结束的情况。  
- **差异**：主要来自**你要 ship 的东西**（长期产品 / 长任务 demo / 榜单分数 / 团队沟通框架），不是谁掌握了独家真理。  
- **用法**：做方案时**各取一段**——例如 OpenAI 式分层 + LangChain 式 trace 复盘 + Anthropic 式「写的人别评自己的人」——按你栈和成本拼装，不必先统一叫 harness engineering。

### 日常项目可直接抄的作业（概念用括号标注，按需搜原文）

1. **短入口 + 深内容分文件** — `AGENTS.md` / `CONTRIBUTING` 只写「地图」和铁律，细节进 `docs/` 或专题 md。（**渐进披露**）  
2. **能机读的检查优先上 CI** — 格式、import 边界、简单架构规则等，让代理和人类共用同一套红条。（**computational sensor**，偏 OpenAI / Fowler）  
3. **「交卷前」多一道硬步骤** — 合并或结束任务前固定跑：单测 / lint / 或对照 issue 勾选清单；可用脚本或 pre-commit，不必先上框架 middleware。（**build–verify**，偏 LangChain）  
4. **同一类错第二次就写进规则** — 把踩坑写成仓库里一条可引用说明，而不是只在聊天里纠正。（**steering loop** / 前馈 guide）  
5. **UI 或 API 用自动化戳一下** — 最小可行：一条 Playwright、e2e smoke、或 `curl` 健康检查；比纯「读代码认为 OK」稳。（**真实环境反馈**，偏 Anthropic）  
6. **留痕便于周回顾** — 保存几次失败会话的日志、diff 或 trace 截图，周末翻 20 分钟找重复模式；不必上 LangSmith 也能做**轻量 trace 外环**。  
7. **写和评尽量换人（或换角色）** — 同一人连续自评容易放水；至少隔一轮人类 CR，或第二个代理只读给 critique。（**生成 / 评测分离** 的迷你版）  
8. **画一张「什么时候跑什么检查」** — 提交前 / PR / 合并后 / 定时；避免所有检查堆在一条命令里又慢又难维护。（**生命周期分布**，偏 Fowler）

以上不要求一次全上；通常 **1 + 2 + 3** 就能挡住大半低级漂移。

## 依据来源

- [[Web｜OpenAI：Harness engineering（Codex）]]、[[Web｜Anthropic：Harness design for long-running apps]]、[[Web｜LangChain：Improving Deep Agents with harness engineering]]、[[Web｜Martin Fowler：Harness engineering for coding agent users]]  
- 元话语与 how-to-sglang 对照：[[X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验]]  
- 合并原则清单：[[Harness engineering：定义、原则与实践清单]]；概念索引：[[Harness engineering（代理脚手架）]]
