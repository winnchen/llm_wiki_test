# Echo Wiki

LLM 维护的个人知识库——人负责策展原始资料，LLM 负责整理、链接与日志。

灵感来自 Andrej Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 理念：三层架构（raw / wiki / schema）与 Ingest、Query、Lint 闭环。

## 目录结构

```
raw/                        # 原始资料（人工策展，不可变）
  assets/                   # 全局附件
  web/<slug>/article.md     # 网页剪藏（每篇一个子目录）
  xiaohongshu/<id>/note.md  # 小红书笔记归档
wiki/                       # LLM 维护的结构化 wiki
  index.md                  # 内容目录
  log.md                    # 操作日志（时间线）
  sources/                  # 每个摄入源的摘要页
  entities/                 # 人物、组织、产品、地点
  concepts/                 # 理论、方法、技术
  comparisons/              # 对比分析
  synthesis/                # 综合洞察
AGENTS.md                   # Wiki schema 与工作流定义
```

## 当前规模

- **32** 个 wiki 页面
- **16** 个已摄入源（网页剪藏 + 小红书笔记）
- 涵盖领域：露营 / 国家公园攻略、AI agent harness engineering

## 工作流

| 流程 | 说明 |
|------|------|
| **Ingest** | 读取 `raw/` → 讨论要点 → 创建/更新 wiki 页面 → 更新 index 与 log |
| **Query** | 读 index 定位 → 综合回答 → 有实质内容时主动建议归档到 wiki |
| **Lint** | 检查孤儿页、断链、薄页、过时声明 → 经批准后修复 |

## 写作约定

- 中英混合：中文主体，技术术语与专有名词保留英文原文
- 文件名：小写 kebab-case，`.md` 后缀
- 交叉引用：`[[页面标题]]` wikilink 语法
- 每页 frontmatter 必含：`title`, `type`, `created`, `updated`, `sources`, `tags`

## 工具

- `.cursor/skills/llm-wiki/` — LLM Wiki skill（Ingest / Query / Lint 指令与模板）
- `.cursor/skills/llm-wiki/scripts/wiki_lint.py` — 结构健康检查脚本

## License

私人知识库，仅供个人使用。
