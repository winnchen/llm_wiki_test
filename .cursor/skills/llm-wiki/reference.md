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
---
```

## Cross-Reference Conventions

| Pattern | Usage |
|---------|-------|
| `[[Page Title]]` | Link to another wiki page |
| `[[Page Title\|display text]]` | Link with custom display text |
| `> [!source] raw/filename.ext` | Cite a raw source file |
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

| Format | Extension | Ingest Strategy |
|--------|-----------|----------------|
| Markdown | `.md` | Direct read |
| Plain text | `.txt` | Direct read |
| PDF | `.pdf` | Text extraction via pdfplumber; images extracted separately |
| Images | `.png`, `.jpg`, `.webp` | Visual analysis by LLM, generate text description |
| CSV | `.csv` | Read structure, compute statistics, summarize |
| JSON | `.json` | Parse structure, extract key fields, summarize |
| Excel | `.xlsx` | Read sheets, compute statistics, summarize |
| Audio/Video | `.mp3`, `.mp4` | Requires external transcription first (Whisper), then ingest transcript |
