---
name: llm-wiki
description: >-
  Build and maintain a persistent, interlinked markdown wiki using LLMs.
  Incrementally ingest sources, synthesize knowledge, and keep cross-references
  current. Use when the user mentions wiki, knowledge base, ingest source,
  wiki query, wiki lint, personal wiki, LLM wiki, or knowledge management.
---

# LLM Wiki

Build a persistent, compounding knowledge base as interlinked markdown files.
The LLM writes and maintains all wiki pages; the human curates sources, directs
analysis, and asks the right questions.

## Architecture

```
project-root/
├── raw/                  # Immutable source documents (human-curated)
│   ├── assets/           # Shared attachments (clips, cross-source media)
│   ├── xiaohongshu/      # Optional: XHS archives (xhs-fetch-to-raw); each note folder has its own assets/
│   └── ...               # Other topic folders, papers, data files
├── wiki/                 # LLM-maintained markdown wiki
│   ├── index.md          # Content catalog with links and summaries
│   ├── log.md            # Chronological operation log
│   ├── sources/          # One summary page per ingested source
│   ├── entities/         # Pages for people, orgs, places, products
│   ├── concepts/         # Pages for ideas, theories, methods
│   ├── comparisons/      # Side-by-side analyses
│   └── synthesis/        # Cross-cutting analyses and essays
└── AGENTS.md             # Schema: conventions, page types, workflows
```

**Three layers:**
- **Raw Sources** (`raw/`): immutable, read-only for the LLM
- **Wiki** (`wiki/`): LLM-owned, structured markdown with cross-references
- **Schema** (`AGENTS.md`): governs structure, conventions, and workflows

## Workflow 1: Init

When starting a new wiki project:

1. Read the schema template from [templates/schema-template.md](templates/schema-template.md)
2. Ask the user about domain, scope, and preferences
3. Create directory structure per `AGENTS.md`: at minimum `raw/`, `raw/assets/`, `wiki/sources/`, …; add domain folders (e.g. `raw/xiaohongshu/` for 小红书) when applicable
4. Generate `AGENTS.md` from the template, customized for the domain
5. Generate `wiki/index.md` from [templates/index-template.md](templates/index-template.md)
6. Generate `wiki/log.md` from [templates/log-template.md](templates/log-template.md)
7. Log the init operation

## Workflow 2: Ingest

When the user adds a source to `raw/` and asks to ingest it:

1. **Detect format** and read the source:
   - `.md`, `.txt`: read directly
   - `.pdf`: extract text with pdfplumber; note any images for separate viewing
   - `.png`, `.jpg`, `.webp`: analyze visually, generate description
   - `.csv`, `.json`, `.xlsx`: read structure, compute key statistics
   - `.mp3`, `.mp4`: remind user to transcribe first (e.g. Whisper), then ingest the transcript
2. **Discuss** key takeaways with the user — what matters, what to emphasize
3. **Create source summary** in `wiki/sources/` using [templates/source-summary.md](templates/source-summary.md)
4. **Update or create entity pages** in `wiki/entities/` using [templates/entity-page.md](templates/entity-page.md)
5. **Update or create concept pages** in `wiki/concepts/` using [templates/concept-page.md](templates/concept-page.md)
6. **Flag contradictions** — if new info contradicts existing wiki claims, note them explicitly on both pages
7. **Update `wiki/index.md`** — add new pages, update summaries of modified pages
8. **Append to `wiki/log.md`**:
   ```
   ## [YYYY-MM-DD] ingest | Source Title
   - Source: `raw/filename.ext`
   - Pages created: list
   - Pages updated: list
   - Contradictions flagged: list or "none"
   ```

**Important:** Use `[[wikilink]]` syntax for all cross-references between wiki pages. Every new page must link to at least one existing page, and at least one existing page must link back.

## Workflow 3: Query

When the user asks a question against the wiki:

1. **Read `wiki/index.md`** to identify relevant pages
2. If the wiki has >100 pages, use `scripts/wiki_search.py` for targeted search
3. **Read relevant pages** and synthesize an answer with `[[wikilink]]` citations
4. **Ask the user**: "Should I file this answer as a wiki page?"
   - If yes → create a page in `wiki/synthesis/` or `wiki/comparisons/`
   - Update index and log
5. **Suggest follow-ups**: related questions, sources to seek, gaps in the wiki

## Workflow 4: Lint

When the user asks to health-check the wiki, or periodically after every ~10 ingests:

1. Run `python scripts/wiki_lint.py wiki/` or perform manual checks:
   - **Orphan pages**: no inbound links from other wiki pages
   - **Broken links**: `[[wikilinks]]` pointing to nonexistent pages
   - **Missing pages**: frequently mentioned but never created
   - **Stale claims**: superseded by newer sources (check dates)
   - **Incomplete frontmatter**: missing required YAML fields
   - **Thin pages**: fewer than 3 sentences of content
2. Present findings as a checklist to the user
3. Fix issues with user approval
4. Log the lint pass in `wiki/log.md`

## Page Conventions

Every wiki page must have YAML frontmatter:

```yaml
---
title: Page Title
type: source-summary | entity | concept | comparison | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [filename1.md, filename2.pdf]
tags: [tag1, tag2]
---
```

Cross-reference rules:
- Use `[[Page Title]]` for internal wiki links
- Use `> [!source] raw/filename.ext` callouts when citing raw sources
- Every page must have at least one inbound and one outbound wiki link

For detailed page type specs, see [reference.md](reference.md).

## Index and Log Maintenance

**index.md** structure:
- Grouped by page type (sources, entities, concepts, comparisons, synthesis)
- Each entry: `- [[Page Title]] — one-line summary (N sources)`
- Updated on every ingest, query-to-page, and lint pass

**log.md** structure:
- Reverse-chronological (newest first)
- Each entry prefixed: `## [YYYY-MM-DD] operation | Title`
- Operations: `ingest`, `query`, `lint`, `init`, `update`
- Parseable with: `grep "^## \[" wiki/log.md | head -10`

## Tools

- **Search**: `python scripts/wiki_search.py wiki/ "query terms"` — BM25 search over wiki pages
- **Lint**: `python scripts/wiki_lint.py wiki/` — structural health check
- For large wikis (500+ pages), consider [qmd](https://github.com/tobi/qmd) for hybrid BM25/vector search
