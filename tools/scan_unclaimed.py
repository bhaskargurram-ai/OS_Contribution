#!/usr/bin/env python3
"""Scan repositories for genuinely unclaimed issues.

Unclaimed == open, no assignee, and no pull request linked to it. The
``-linked:pr`` search qualifier is GitHub's own notion of linkage, so this
reflects real state rather than heuristics.

Usage::

    export GITHUB_TOKEN=ghp_...
    python tools/scan_unclaimed.py                 # default repo set
    python tools/scan_unclaimed.py --repos a/b c/d
    python tools/scan_unclaimed.py --json out.json

Caveat: ``-linked:pr`` only excludes *formally linked* PRs. A contributor can
have an open PR that merely mentions the issue. Re-check the thread before
starting work.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import requests

API = "https://api.github.com"

DEFAULT_REPOS = [
    "huggingface/transformers",
    "huggingface/diffusers",
    "huggingface/peft",
    "huggingface/accelerate",
    "huggingface/datasets",
    "stanfordnlp/dspy",
    "vllm-project/vllm",
    "sgl-project/sglang",
    "pytorch/pytorch",
    "ray-project/ray",
    "run-llama/llama_index",
    "BerriAI/litellm",
    "openai/openai-agents-python",
    "modelcontextprotocol/python-sdk",
]

# Label vocabularies differ per project; a repo absent here is scanned unfiltered.
LABEL_SETS = {
    "huggingface/transformers": ["Good First Issue", "Good Second Issue", "Feature request"],
    "huggingface/diffusers": ["good first issue", "help wanted", "contributions-welcome"],
    "pytorch/pytorch": ["good first issue"],
    "vllm-project/vllm": ["good first issue", "help wanted"],
    "sgl-project/sglang": ["good first issue", "help wanted"],
    "ray-project/ray": ["good first issue", "help wanted"],
    "run-llama/llama_index": ["good first issue", "help wanted"],
    "BerriAI/litellm": ["good first issue", "help wanted"],
    "modelcontextprotocol/python-sdk": ["good first issue", "help wanted"],
    "openai/openai-agents-python": ["good first issue", "help wanted", "enhancement"],
}


def build_session(token: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    })
    return s


def search(session: requests.Session, query: str, per_page: int = 50) -> dict:
    """One search call, retrying on secondary rate limits."""
    for attempt in range(5):
        r = session.get(
            f"{API}/search/issues",
            params={"q": query, "sort": "updated", "order": "desc",
                    "per_page": per_page, "advanced_search": "true"},
            timeout=45,
        )
        if r.status_code == 200:
            # Search is capped at 30 req/min; stay comfortably under.
            time.sleep(2.2)
            return r.json()
        if r.status_code in (403, 429):
            reset = r.headers.get("x-ratelimit-reset")
            wait = max(5, min(90, int(reset) - int(time.time()) + 2)) if reset else 10
            print(f"  rate-limited, waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        r.raise_for_status()
    raise RuntimeError(f"search failed after retries: {query}")


def label_clause(repo: str) -> str:
    labels = LABEL_SETS.get(repo)
    if not labels:
        return ""
    # Comma-separated labels are an OR in GitHub search syntax.
    return " label:" + ",".join(f'"{l}"' for l in labels)


def scan(session: requests.Session, repos: list[str]) -> dict:
    results = {}
    for repo in repos:
        query = f"repo:{repo} is:issue is:open no:assignee -linked:pr{label_clause(repo)}"
        payload = search(session, query)
        items = [
            {
                "number": it["number"],
                "title": it["title"],
                "url": it["html_url"],
                "labels": [l["name"] for l in it.get("labels", [])],
                "comments": it.get("comments", 0),
                "reactions": (it.get("reactions") or {}).get("total_count", 0),
                "created_at": it["created_at"],
                "updated_at": it["updated_at"],
                "author": (it.get("user") or {}).get("login"),
            }
            for it in payload.get("items", [])
        ]
        results[repo] = {"total": payload.get("total_count", 0),
                         "query": query, "issues": items}
        print(f"{repo:40s} {payload.get('total_count', 0):5d} unclaimed", file=sys.stderr)
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repos", nargs="+", default=DEFAULT_REPOS)
    ap.add_argument("--json", metavar="PATH", help="write full results here")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("set GITHUB_TOKEN (public-repo read scope is enough)", file=sys.stderr)
        return 2

    results = scan(build_session(token), args.repos)

    if args.json:
        with open(args.json, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nwrote {args.json}", file=sys.stderr)

    print("\n| Repository | Unclaimed |")
    print("|---|---|")
    for repo, data in sorted(results.items(), key=lambda kv: -kv[1]["total"]):
        print(f"| {repo} | {data['total']} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
