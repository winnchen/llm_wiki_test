#!/usr/bin/env python3
"""Lint a wiki directory for structural issues.

Usage:
    python wiki_lint.py <wiki_dir>

Checks:
    L001  Missing frontmatter fields
    L002  No outbound wikilinks
    L003  No inbound wikilinks (orphan)
    L004  Broken wikilinks
    L005  Thin pages (<3 sentences)
    L006  Source summary missing raw source callout
    L008  Page missing from index.md
    L010  Duplicate titles
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED_FRONTMATTER = {"title", "type", "created", "updated", "sources", "tags"}
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
SENTENCE_RE = re.compile(r"[.!?。！？]\s")
SOURCE_CALLOUT_RE = re.compile(r">\s*\[!source\]")


def parse_frontmatter(content: str) -> dict[str, str]:
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in content[3:end].strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm


def extract_title(fm: dict[str, str], content: str) -> str:
    if "title" in fm:
        return fm["title"].strip('"').strip("'")
    for line in content.split("\n"):
        if line.startswith("# ") and not line.startswith("##"):
            return line[2:].strip()
    return ""


def body_after_frontmatter(content: str) -> str:
    if not content.startswith("---"):
        return content
    end = content.find("---", 3)
    if end == -1:
        return content
    return content[end + 3:]


def count_sentences(body: str) -> int:
    body = re.sub(r"^---.*?---", "", body, flags=re.DOTALL)
    body = re.sub(r"^#+\s.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^\s*[-*]\s", "", body, flags=re.MULTILINE)
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"`[^`]+`", "", body)
    parts = SENTENCE_RE.split(body.strip())
    return len([p for p in parts if len(p.strip()) > 10])


def load_index_entries(wiki_dir: str) -> set[str]:
    index_path = os.path.join(wiki_dir, "index.md")
    if not os.path.exists(index_path):
        return set()
    with open(index_path, encoding="utf-8") as f:
        content = f.read()
    return set(WIKILINK_RE.findall(content))


def main():
    if len(sys.argv) < 2:
        print("Usage: python wiki_lint.py <wiki_dir>", file=sys.stderr)
        sys.exit(1)

    wiki_dir = sys.argv[1]
    if not os.path.isdir(wiki_dir):
        print(f"Error: {wiki_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    pages: dict[str, tuple[str, dict, str]] = {}  # path -> (content, frontmatter, title)
    titles_to_paths: dict[str, list[str]] = defaultdict(list)

    for root, _, files in os.walk(wiki_dir):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            fm = parse_frontmatter(content)
            title = extract_title(fm, content)
            pages[path] = (content, fm, title)
            if title:
                titles_to_paths[title].append(path)

    known_titles = {t for _, (_, _, t) in pages.items() if t}
    outbound: dict[str, set[str]] = {}
    inbound: dict[str, int] = defaultdict(int)

    for path, (content, fm, title) in pages.items():
        links = set(WIKILINK_RE.findall(content))
        outbound[path] = links
        for link in links:
            inbound[link] += 1

    index_entries = load_index_entries(wiki_dir)
    errors = []
    warnings = []

    for path, (content, fm, title) in pages.items():
        rel = os.path.relpath(path)
        basename = os.path.basename(path)
        if basename in ("index.md", "log.md"):
            continue

        # L001: Missing frontmatter
        missing = REQUIRED_FRONTMATTER - set(fm.keys())
        if missing:
            errors.append(f"L001 [{rel}] Missing frontmatter: {', '.join(sorted(missing))}")

        # L002: No outbound wikilinks
        if not outbound[path]:
            errors.append(f"L002 [{rel}] No outbound [[wikilinks]]")

        # L003: No inbound wikilinks (orphan)
        if title and inbound.get(title, 0) == 0:
            warnings.append(f"L003 [{rel}] Orphan page — no inbound links to '{title}'")

        # L005: Thin page
        body = body_after_frontmatter(content)
        if count_sentences(body) < 3:
            warnings.append(f"L005 [{rel}] Thin page — fewer than 3 sentences")

        # L006: Source summary without raw source callout
        if fm.get("type") == "source-summary" and not SOURCE_CALLOUT_RE.search(content):
            errors.append(f"L006 [{rel}] Source summary missing > [!source] callout")

        # L008: Not listed in index.md
        if title and title not in index_entries:
            errors.append(f"L008 [{rel}] Page '{title}' not found in index.md")

    # L004: Broken wikilinks
    for path, links in outbound.items():
        rel = os.path.relpath(path)
        for link in links:
            if link not in known_titles:
                errors.append(f"L004 [{rel}] Broken link: [[{link}]]")

    # L010: Duplicate titles
    for title, paths in titles_to_paths.items():
        if len(paths) > 1:
            rels = [os.path.relpath(p) for p in paths]
            errors.append(f"L010 Duplicate title '{title}' in: {', '.join(rels)}")

    if errors:
        print(f"ERRORS ({len(errors)}):\n")
        for e in sorted(errors):
            print(f"  {e}")
        print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):\n")
        for w in sorted(warnings):
            print(f"  {w}")
        print()

    total = len(errors) + len(warnings)
    if total == 0:
        print("All checks passed. Wiki is healthy.")
    else:
        print(f"Summary: {len(errors)} errors, {len(warnings)} warnings across {len(pages)} pages.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
