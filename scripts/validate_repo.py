#!/usr/bin/env python3
"""Validate repository structure, internal links, lesson shape, and sample data."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)


def validate_links(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if not target or target.startswith("#") or SCHEME_RE.match(target):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                relative = path.relative_to(ROOT)
                errors.append(f"{relative}: broken internal link -> {raw_target}")
    return errors


def validate_markdown(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if not re.search(r"^ {0,3}# ", text, re.MULTILINE) and relative.name != "PULL_REQUEST_TEMPLATE.md":
            errors.append(f"{relative}: expected an H1")
        if text.count("```") % 2:
            errors.append(f"{relative}: unbalanced fenced code block")

    lesson_files = sorted((ROOT / "docs").rglob("*.md"))
    for path in lesson_files:
        text = path.read_text(encoding="utf-8")
        if "## Learning Objectives" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing Learning Objectives")
        if "## Official Resources" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing Official Resources")
    return errors


def count_csv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def validate_datasets() -> list[str]:
    errors: list[str] = []
    web_path = ROOT / "datasets" / "web_access.log"
    web_count = sum(1 for line in web_path.read_text(encoding="utf-8").splitlines() if line.strip())
    expected = {
        "datasets/web_access.log": (web_count, 36),
        "datasets/auth_events.csv": (count_csv_rows(ROOT / "datasets" / "auth_events.csv"), 30),
        "datasets/orders.csv": (count_csv_rows(ROOT / "datasets" / "orders.csv"), 20),
    }
    for name, (actual, wanted) in expected.items():
        if actual != wanted:
            errors.append(f"{name}: expected {wanted} events, found {actual}")
    return errors


def validate_required_files() -> list[str]:
    required = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "assets/banner.svg",
        "reference/spl-cheatsheet.md",
        "labs/README.md",
        ".github/workflows/validate.yml",
    ]
    return [f"missing required file: {name}" for name in required if not (ROOT / name).exists()]


def main() -> int:
    files = markdown_files()
    errors = (
        validate_required_files()
        + validate_links(files)
        + validate_markdown(files)
        + validate_datasets()
    )
    if errors:
        print("Repository validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    spl_blocks = sum(path.read_text(encoding="utf-8").count("```spl") for path in files)
    print(
        f"Validated {len(files)} Markdown files, {spl_blocks} SPL examples, "
        "all internal links, and 86 synthetic events."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
