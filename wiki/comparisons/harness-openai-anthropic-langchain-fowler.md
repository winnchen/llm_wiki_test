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
| **[[OpenAI]]** | 真产品、大仓库、长期由代理改代码 | 短 `AGENTS.md` 当目录；`docs/` 当真源；**linter + 结构测试**；分层边界；本地可观测性（日志/指标/trace） | 用 **Chrome DevTools** 让代理复现 UI 问题、看真实运行，而不是只靠读代码猜 |
| **[[Anthropic]]** | 数小时自主搭应用；前端「好看不好」难验 | **多角色**：planner / generator / evaluator；评测用 **Playwright** 真点页面；需要时 sprint 合约 + 失败打回 | 生成器做 UI，评估器用浏览器操作、打分、写 critique，多轮改审美与可用性 |
| **[[LangChain]]** | 排行榜/基准上**固定模型**、只改外围提分 | **LangSmith trace** 批量找失败模式；把复盘做成技能；旋钮收敛为 **prompt / tools / middleware** | **交卷前 middleware**：拦截「要结束了」，强制再跑一轮对照 task spec 的验证（类似 Ralph 式钩子，但目标是 verify） |
| **[[Martin Fowler]]** | 教人**怎么谈论**编码代理周围的控制 | **Guides（前馈）** 与 **Sensors（反馈）**；算得快 vs 要 GPU 的推断式；按对象分 **可维护性 / 架构 / 行为** | 在**变更生命周期**里画清：哪些检查该在提交前、哪些在流水线、哪些是持续漂移类监控 |

**读表提示**：四行不是互斥「四种 harness」，而是**同一类工程**在不同战场上的**镜头不同**——有的写仓库治理，有的写 benchmark 迭代，有的写多代理编排，有的写词汇和分类。

## 简短分析（怎么想）

1. **场景决定显眼包**  
   OpenAI 必须回答「一百万行怎么不烂」→ 结构、文档真源、机械检查最显眼。Anthropic 要展示「几小时没人插手也能出完整产品」→ 分角色 + 真机评测显眼。LangChain 要证明「只动 harness 也能涨分」→ trace 外环和 middleware 显眼。Fowler 不负责替你部署 → 给你**分类和对话语言**，方便和团队对齐风险。

2. **重复出现的「老办法」**  
   多篇都出现：**不要把所有说明塞进一个巨型文件**、**用测试/规格当反馈**、**让代理能摸到运行环境**、**多代理时拆开写和评**。这与 [[X｜@GenAI_is_real：对 harness engineering 的批评与 how-to-sglang 经验]] 里说的「分离关注点、文档进仓、结构化路由」是**同一张饼**，只是有人叫 harness，有人叫常识。

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
