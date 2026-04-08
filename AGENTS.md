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
  assets/             # 下载的图片和媒体文件
  xiaohongshu/        # 小红书笔记归档（由 xhs-fetch-to-raw skill 内置脚本写入）
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

### Ingest（摄入）
1. 读取 `raw/` 中的原始资料
2. 与用户讨论关键要点
3. 创建/更新 wiki 页面（源摘要、实体、概念）
4. 标记与已有内容的矛盾
5. 更新 index.md 和 log.md

### Query（查询）
1. 读取 index.md 定位相关页面
2. 读取页面并综合回答
3. 询问是否将回答归档为 wiki 页面

### Lint（健康检查）
1. 检查孤儿页、断链、薄页、过时声明
2. 向用户展示发现
3. 经批准后修复
