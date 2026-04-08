# Echo Wiki — Schema

这个文件定义 wiki 的结构、约定和工作流。LLM 和人类共同演进此文件。

## 项目

- **名称**: Echo Wiki
- **领域**: 全领域个人知识库——涵盖 AI/ML、技术、科学、商业、人文、生活等一切感兴趣的主题
- **语言**: 中英混合（中文主体，保留英文术语和专有名词原文）
- **维护者**: Echo

## 目录结构

```
raw/                  # 原始资料——不可变，人工策展
  assets/             # 全局附件（剪藏/手工下载的跨来源图片与媒体，非某一篇独占）
  web/                # 网页长文剪藏（扁平：每篇一个子目录 <slug>/）
    <slug>/article.md # 正文 + YAML 元数据（source_url、archived_at 等）
    <slug>/assets/    # 可选：本文独占图片（内文插图/示意图宜下载为本地相对路径，避免热链失效）
  xiaohongshu/        # 小红书笔记归档（xhs-fetch-to-raw）；每篇子目录内另有 assets/ 存该帖图片/视频
wiki/                 # LLM 维护的 wiki——结构化 markdown
  index.md            # 内容目录
  log.md              # 操作日志（时间线）
  sources/            # 每个摄入源一个摘要页
  entities/           # 实体页：人物、组织、产品、工具
  concepts/           # 概念页：理论、方法、技术、思想
  comparisons/        # 对比分析页
  synthesis/          # 综合分析与洞察
```

## 页面类型

| 类型 | 目录 | 用途 |
|------|------|------|
| source-summary | `wiki/sources/` | 一个原始资料的摘要 |
| entity | `wiki/entities/` | 跨资料出现的命名实体 |
| concept | `wiki/concepts/` | 跨资料出现的概念或方法 |
| comparison | `wiki/comparisons/` | 并列对比分析 |
| synthesis | `wiki/synthesis/` | 跨领域综合洞察 |

## 写作约定

- **文件名**: 小写 kebab-case，`.md` 后缀，不超过 60 字符
- **交叉引用**: 使用 `[[页面标题]]` wikilink 语法
- **源引用**: 使用 `> [!source] raw/filename.ext` callout
- **矛盾标记**: 用 `> [!contradiction]` 在两个页面同时标注
- **知识空白**: 用 `> [!gap]` 标注
- **过时信息**: 用 `> [!stale]` 标注
- **Frontmatter**: 每页必须包含 title, type, created, updated, sources, tags

## 语言规范

- 正文使用中文
- 技术术语保留英文原文，首次出现时可附中文注释，如: Transformer（变换器架构）
- 人名、组织名保留原文: Andrej Karpathy, OpenAI
- 代码、公式、数据保持英文

## 标签体系

使用小写英文标签，按领域分层：

- `ai`, `ml`, `llm`, `nlp`, `cv` — AI 与机器学习
- `tech`, `engineering`, `devops` — 技术与工程
- `science`, `physics`, `biology` — 自然科学
- `business`, `strategy`, `product` — 商业与战略
- `philosophy`, `psychology`, `culture` — 人文社科
- `health`, `productivity`, `life` — 生活与个人发展
- `meta` — 关于 wiki 自身的元内容

标签可以按需扩展，但保持简洁、一致。

## 工作流

### 元理念（LLM Wiki）

知识库的瓶颈往往在**维护与交叉引用**，而非「读过一遍」。LLM 负责 `wiki/` 的整理、链接与日志；人负责 `raw/` 的策展与取舍。对 Karpathy 式 **LLM Wiki** 的概括见 [gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)：三层（raw / wiki / schema）与 Ingest、Query、Lint 闭环。

### raw 层边界

- **常态**：`raw/` 视为**人工策展**的原文层；Ingest 时 LLM **只读** raw。
- **例外**：补全剪藏（例如内文配图落盘、元数据或排版修正）由**人发起**、Agent 协助执行即可；属策展延伸，与随意改写 wiki 不同。大批量或模糊来源的 raw 变更应先与人确认。

### Ingest（摄入）

#### 单篇模式（ingest-single）

1. **读源 + 格式检测**
   读取 `raw/` 中的原始资料（常见：`raw/web/<slug>/article.md` 网页剪藏；`raw/xiaohongshu/<folder>/note.md` 小红书归档；其他扩展名见 SKILL.md 支持格式表）

2. **领域感知分析**
   根据源的类型与领域，选择对应的分析维度（而非一刀切「列要点」）：
   - **技术 / AI 文章**：核心论点、方法论、数据与实验、局限声明、与已有 wiki 的增量
   - **经验帖（小红书/旅行/生活）**：可操作信息（时间线、价格、坐标、品牌）、主观判断需标注、与已有攻略的增量或矛盾
   - **论文**：假设、方法、结果、消融实验、作者自述局限
   - **观点 / 评论 / 社交媒体**：立场、论据、潜在偏见、与对立观点的映射
   - **数据 / 表格**：关键统计量、分布特征、与已有数据的可比性

3. **Delta 对照**（与已有 wiki 对比——**强制步骤**）
   1. 读 `wiki/index.md`，定位所有**可能相关**的已有 entity / concept / synthesis 页
   2. 读这些页面
   3. 显式分类本源信息为：
      - **新增**：wiki 中完全没有的信息
      - **强化**：佐证已有结论但补充了细节/数据
      - **矛盾**：与已有内容冲突（必须用 `> [!contradiction]` 双向标注）
      - **已覆盖**：wiki 已有且无增量（不重复写入）
   4. 在 source-summary 中标注密度：frontmatter 加 `density: high | medium | low`

4. **与用户对齐**
   只讨论**增量和矛盾**，已覆盖的跳过。材料极清晰且无矛盾时可缩短为一段确认。

5. **写 wiki**
   - 创建 source-summary（高密度源允许更长、分节更细；低密度源可以合并进已有 concept 页，不强制单建 summary）
   - 更新或新建 entity / concept 页（只写增量部分）
   - 矛盾处双向标注 `> [!contradiction]`

6. **Synthesis trigger check**（主动判断是否该综合）
   满足以下任一条件时，在本轮结尾**主动建议**新建 synthesis 或 comparison：
   - 某个 entity / concept 页的 `sources` 数量达到 **≥ 3**
   - 本次 ingest 产生了 **≥ 2 个矛盾标记**
   - 本次 ingest 涉及了 **≥ 2 个已有 concept 页**的交叉更新

7. **局部 lint**
   对本次新建/修改的页面跑一次 `wiki_lint.py`（或手动检查 frontmatter、outbound link、薄页），自动修复简单问题。

8. **更新 index.md 和 log.md**

#### 批量模式（ingest-batch）

同时摄入多篇相关源时（如同一主题的多篇文章）：
1. **先全读**：读完所有源，不急写 wiki
2. **跨源 Delta 分析**：源与源之间的重叠、矛盾、互补关系；与已有 wiki 的增量
3. **统一写 wiki**：避免先写的页面缺少后读到的信息
4. 其余步骤同单篇模式的 4–8

### Query（查询）
1. 读取 index.md 定位相关页面
2. 读取页面并综合回答（回答中善用 `[[wikilink]]`）
3. **写回闭环（强制）**：若回答超出一句确认/指链（即包含归纳、对比、清单、原则或可复用结论），**必须在同轮结尾主动询问**是否将内容归档为 wiki 页面，并**给出建议落点**（如扩写 [[某概念页]]、新建 `wiki/synthesis/`、`wiki/comparisons/`）。用户同意后再写入并更新 index.md、log.md。

### Lint（健康检查）
1. 检查孤儿页、断链、薄页、过时声明
2. 向用户展示发现
3. 经批准后修复
4. **节奏**：用户说「lint / 健康检查」时必跑；此外建议约每 **10 次 ingest** 主动提醒或执行一次，并在 `wiki/log.md` 记录 lint 批次
