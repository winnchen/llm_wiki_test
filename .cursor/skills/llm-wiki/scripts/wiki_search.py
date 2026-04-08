#!/usr/bin/env python3
"""BM25 search over wiki markdown files.

Usage:
    python wiki_search.py <wiki_dir> "<query>" [--top N]

Example:
    python wiki_search.py wiki/ "transformer attention mechanism" --top 5
"""

import argparse
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9\u4e00-\u9fff]+", text.lower())


def load_documents(wiki_dir: str) -> list[tuple[str, str]]:
    docs = []
    for root, _, files in os.walk(wiki_dir):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as fh:
                    docs.append((path, fh.read()))
    return docs


class BM25:
    def __init__(self, documents: list[tuple[str, str]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.paths = [d[0] for d in documents]
        self.doc_tokens = [tokenize(d[1]) for d in documents]
        self.doc_lens = [len(t) for t in self.doc_tokens]
        self.avgdl = sum(self.doc_lens) / max(len(self.doc_lens), 1)
        self.n = len(documents)
        self.doc_freqs: dict[str, int] = Counter()
        for tokens in self.doc_tokens:
            for term in set(tokens):
                self.doc_freqs[term] += 1

    def _idf(self, term: str) -> float:
        df = self.doc_freqs.get(term, 0)
        return math.log((self.n - df + 0.5) / (df + 0.5) + 1)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        query_tokens = tokenize(query)
        scores: list[tuple[str, float]] = []
        for i, tokens in enumerate(self.doc_tokens):
            tf_map = Counter(tokens)
            score = 0.0
            dl = self.doc_lens[i]
            for qt in query_tokens:
                tf = tf_map.get(qt, 0)
                idf = self._idf(qt)
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                score += idf * numerator / denominator
            scores.append((self.paths[i], score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return [(p, s) for p, s in scores[:top_k] if s > 0]


def extract_title(content: str) -> str:
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# ") and not line.startswith("##"):
            return line[2:].strip()
        if line.startswith("title:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def main():
    parser = argparse.ArgumentParser(description="BM25 search over wiki markdown files")
    parser.add_argument("wiki_dir", help="Path to wiki directory")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top", type=int, default=10, help="Number of results")
    args = parser.parse_args()

    if not os.path.isdir(args.wiki_dir):
        print(f"Error: {args.wiki_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    docs = load_documents(args.wiki_dir)
    if not docs:
        print("No markdown files found.", file=sys.stderr)
        sys.exit(1)

    bm25 = BM25(docs)
    results = bm25.search(args.query, top_k=args.top)

    if not results:
        print("No results found.")
        return

    print(f"Top {len(results)} results for: {args.query}\n")
    doc_map = {d[0]: d[1] for d in docs}
    for rank, (path, score) in enumerate(results, 1):
        title = extract_title(doc_map[path])
        rel_path = os.path.relpath(path)
        display = f"{title} ({rel_path})" if title else rel_path
        print(f"  {rank}. [{score:.2f}] {display}")


if __name__ == "__main__":
    main()
