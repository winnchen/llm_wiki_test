# {{PROJECT_NAME}} Wiki — Schema

This file governs how the LLM maintains the wiki. Co-evolve it over time.

## Project

- **Domain**: {{DOMAIN_DESCRIPTION}}
- **Scope**: {{SCOPE_DESCRIPTION}}
- **Owner**: {{OWNER}}

## Directory Structure

```
raw/                  # Source documents — immutable, human-curated
  assets/             # Shared attachments (not tied to a single ingested file)
  xiaohongshu/        # Optional: e.g. 小红书 mirrors; each post dir may contain assets/
wiki/                 # LLM-maintained wiki — structured markdown
  index.md            # Content catalog
  log.md              # Chronological operation log
  sources/            # One summary per ingested source
  entities/           # Named things: people, orgs, products
  concepts/           # Ideas, theories, methods
  comparisons/        # Side-by-side analyses
  synthesis/          # Cross-cutting essays and analyses
```

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| source-summary | `wiki/sources/` | Summarize one raw source |
| entity | `wiki/entities/` | A named thing across sources |
| concept | `wiki/concepts/` | An idea or method across sources |
| comparison | `wiki/comparisons/` | Side-by-side analysis |
| synthesis | `wiki/synthesis/` | Cross-cutting analysis or essay |

## Conventions

- **Filenames**: lowercase kebab-case, `.md` extension, max 60 chars
- **Cross-references**: use `[[Page Title]]` wikilink syntax
- **Source citations**: use `> [!source] raw/filename.ext` callouts
- **Contradictions**: flag with `> [!contradiction]` callout on both pages
- **Knowledge gaps**: mark with `> [!gap]` callout
- **Frontmatter**: every page must have: title, type, created, updated, sources, tags

## Workflows

### Ingest
1. Read the raw source
2. Discuss key takeaways with the user
3. Create/update wiki pages (source summary, entities, concepts)
4. Flag contradictions with existing content
5. Update index.md and log.md

### Query
1. Read index.md to find relevant pages
2. Read those pages and synthesize an answer
3. Offer to file the answer as a wiki page

### Lint
1. Check for orphan pages, broken links, thin pages, stale claims
2. Present findings to the user
3. Fix with approval

## Domain-Specific Rules

{{DOMAIN_RULES}}

## Tags Taxonomy

{{TAGS_LIST}}
