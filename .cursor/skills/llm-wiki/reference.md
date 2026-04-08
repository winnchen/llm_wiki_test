# LLM Wiki Reference

Detailed specifications for page types, formatting, and lint rules.

## Page Types

### 1. Source Summary (`wiki/sources/`)

**Purpose:** One page per ingested raw source. Captures key information so the original rarely needs re-reading.

**Filename:** kebab-case derived from source title, e.g. `attention-is-all-you-need.md`

**Required sections:**
- **Metadata** (frontmatter): title, type: source-summary, created, updated, sources, tags
- **Overview**: 2-3 sentence summary
- **Key Points**: bulleted list of main takeaways
- **Notable Claims**: claims that might conflict with or reinforce other sources
- **Entities Mentioned**: links to entity pages
- **Concepts Covered**: links to concept pages
- **Raw Source**: callout linking to the file in `raw/`

### 2. Entity Page (`wiki/entities/`)

**Purpose:** A page for a person, organization, place, product, dataset, or other named thing that appears across multiple sources.

**Filename:** kebab-case of entity name, e.g. `geoffrey-hinton.md`

**Required sections:**
- **Metadata** (frontmatter): title, type: entity, created, updated, sources, tags, aliases (optional)
- **Overview**: what/who this entity is
- **Key Facts**: structured data (dates, affiliations, metrics)
- **Appearances**: which sources mention this entity and in what context
- **Relationships**: links to related entity and concept pages
- **Open Questions**: things not yet known or contradicted across sources

### 3. Concept Page (`wiki/concepts/`)

**Purpose:** A page for an idea, theory, method, technique, or abstract topic that spans multiple sources.

**Filename:** kebab-case of concept name, e.g. `transformer-architecture.md`

**Required sections:**
- **Metadata** (frontmatter): title, type: concept, created, updated, sources, tags
- **Definition**: clear, concise definition
- **Context**: why this concept matters, where it fits
- **Key Sources**: which sources discuss this concept most deeply
- **Related Concepts**: links to related concept pages
- **Evolution**: how understanding of this concept has changed across sources (if applicable)

### 4. Comparison Page (`wiki/comparisons/`)

**Purpose:** Side-by-side analysis of two or more entities or concepts. Often created from query answers.

**Filename:** `X-vs-Y.md` or `comparing-X-Y-Z.md`

**Required sections:**
- **Metadata** (frontmatter): title, type: comparison, created, updated, sources, tags
- **Overview**: what is being compared and why
- **Comparison Table**: structured markdown table with dimensions as rows
- **Analysis**: narrative interpretation of the comparison
- **Sources**: which sources inform each dimension

### 5. Synthesis Page (`wiki/synthesis/`)

**Purpose:** Cross-cutting analysis, essays, or answers that draw from multiple wiki pages. The highest-value pages in the wiki.

**Filename:** descriptive kebab-case, e.g. `scaling-laws-implications.md`

**Required sections:**
- **Metadata** (frontmatter): title, type: synthesis, created, updated, sources, tags
- **Thesis**: one-paragraph thesis statement
- **Argument**: structured argument with wiki link citations
- **Evidence**: key data points from sources
- **Counterarguments**: known challenges to the thesis
- **Open Questions**: what remains unresolved

## Frontmatter YAML Schema

```yaml
---
title: string           # required — display title
type: string            # required — one of: source-summary, entity, concept, comparison, synthesis
created: date           # required — YYYY-MM-DD
updated: date           # required — YYYY-MM-DD, updated on every edit
sources:                # required — list of raw source filenames
  - filename.md
tags:                   # required — 1-5 lowercase tags
  - tag1
  - tag2
aliases:                # optional — alternative names for this page
  - alias1
status: string          # optional — draft | review | stable
confidence: string      # optional — low | medium | high
density: string         # optional (source-summary) — high | medium | low
---
```

### `density` field (source-summary only)

Assigned during ingest Delta analysis. Guides summary depth:

| Value | Meaning | Summary style |
|-------|---------|---------------|
| `high` | Information-dense; many new claims, data, or actionable items | Multi-section, detailed; may spawn new concept/entity pages |
| `medium` | Moderate new info; some overlap with existing wiki | Standard template (overview + key points + entities/concepts) |
| `low` | Mostly reinforcing or narrow scope | Short; consider folding into an existing concept page instead of standalone |

## Cross-Reference Conventions

| Pattern | Usage |
|---------|-------|
| `[[Page Title]]` | Link to another wiki page |
| `[[Page Title\|display text]]` | Link with custom display text |
| `> [!source] raw/filename.ext` | Cite a raw source file |
| `> [!source] raw/xiaohongshu/.../note.md` | Cite a nested raw file (e.g. archived 小红书) |
| `> [!contradiction]` | Flag a conflict between sources |
| `> [!gap]` | Mark a known knowledge gap |
| `> [!stale]` | Mark information that may be outdated |

## Naming Conventions

- All filenames: lowercase kebab-case, `.md` extension
- No spaces, no special characters beyond hyphens
- Source summaries: derive from source title
- Entities: use most common name
- Concepts: use standard terminology
- Keep filenames under 60 characters

## Domain-Aware Analysis Templates

During ingest step 2, select the template that best matches the source. Multiple may apply (e.g. a blog post with embedded data).

### Tech / AI article

| Dimension | What to extract |
|-----------|----------------|
| Core thesis | The author's main claim in 1–2 sentences |
| Methodology | How they reached the claim (experiment, case study, reasoning) |
| Data & evidence | Benchmarks, metrics, examples, code snippets |
| Limitations | Author-stated caveats, unstated assumptions you notice |
| Delta vs wiki | What this adds beyond existing concept/entity pages |

### Experience post (XHS / travel / life)

| Dimension | What to extract |
|-----------|----------------|
| Actionable info | Timelines, prices, coordinates, brand names, step-by-step |
| Subjective vs factual | Label opinions clearly; don't present taste as fact |
| Conditions & caveats | Season, weather, personal fitness level, date of visit |
| Delta vs wiki | New routes, contradicting tips, updated prices vs existing guides |

### Academic paper

| Dimension | What to extract |
|-----------|----------------|
| Hypothesis | What the paper sets out to prove |
| Method | Experimental setup, dataset, model architecture |
| Results | Key numbers, ablation studies, failure modes |
| Author limitations | Section "Limitations" or equivalent |
| Significance | Why it matters for wiki concepts |

### Opinion / social media

| Dimension | What to extract |
|-----------|----------------|
| Stance | Author's position in 1 sentence |
| Arguments | Supporting evidence or reasoning |
| Potential bias | Affiliation, incentive, selection bias |
| Counter-mapping | Which existing wiki pages argue the opposite |

### Data / tabular

| Dimension | What to extract |
|-----------|----------------|
| Key statistics | Mean, median, range, outliers |
| Distribution | Shape, skew, notable clusters |
| Comparability | Can this be compared with data already in the wiki? |
| Freshness | Date of collection; flag if likely stale |

## Operational cadence（与 Karpathy LLM Wiki 对齐）

- **Query → write-back**: 非平凡回答的**同一轮**末尾应主动提议写入 `wiki/`（并建议 synthesis / concept / comparison / 扩写），见仓库 **AGENTS.md**「Query」与 [SKILL.md Workflow 3](SKILL.md)。
- **Lint**: 用户触发时必跑；另建议约每 **10 次 ingest** 提醒或执行一次 `wiki_lint.py`，并在 `wiki/log.md` 留一条（即使无问题），便于追溯。
- **raw**: Ingest 时默认只读；补图等剪藏完善由人发起、Agent 执行，见 **AGENTS.md**「raw 层边界」。

## Lint Rules

| ID | Rule | Severity |
|----|------|----------|
| L001 | Every page must have complete frontmatter (title, type, created, updated, sources, tags) | error |
| L002 | Every page must have at least one outbound `[[wikilink]]` | error |
| L003 | Every page (except brand-new) should have at least one inbound link | warning |
| L004 | No broken `[[wikilinks]]` pointing to nonexistent pages | error |
| L005 | No thin pages (fewer than 3 sentences of body content) | warning |
| L006 | Source summary pages must link back to the raw source | error |
| L007 | Pages with `> [!contradiction]` callouts must be reviewed within 7 days | warning |
| L008 | `index.md` must list every wiki page | error |
| L009 | `log.md` must have an entry for every ingest operation | warning |
| L010 | No duplicate page titles across the wiki | error |

## Supported Source Formats

| Format | Extension / path | Ingest Strategy |
|--------|------------------|----------------|
| Web clip | `raw/web/<slug>/article.md` | Direct read; prefer `> [!source] raw/web/.../article.md`; cite `source_url` from YAML in prose if useful. If the source page has figures/diagrams referenced in the text, mirror them under `raw/web/<slug>/assets/` and use relative `![](assets/...)` links so the archive stays readable offline. |
| Markdown | `.md` | Direct read |
| Plain text | `.txt` | Direct read |
| PDF | `.pdf` | Text extraction via pdfplumber; images extracted separately |
| Images | `.png`, `.jpg`, `.webp` | Visual analysis by LLM, generate text description |
| CSV | `.csv` | Read structure, compute statistics, summarize |
| JSON | `.json` | Parse structure, extract key fields, summarize |
| Excel | `.xlsx` | Read sheets, compute statistics, summarize |
| Audio/Video | `.mp3`, `.mp4` | Requires external transcription first (Whisper), then ingest transcript |
