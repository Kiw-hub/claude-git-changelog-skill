#!/usr/bin/env python3
"""
Automated Git Changelog Generator
Adheres to 'Keep a Changelog' standards (https://keepachangelog.com)
Categorizes Conventional Commits into: Added, Fixed, Changed, Removed.
"""

import subprocess
import sys
import re
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

CONVENTIONAL_MAP = {
    # Added
    "feat": "Added",
    "feature": "Added",
    "new": "Added",
    "add": "Added",
    # Fixed
    "fix": "Fixed",
    "bugfix": "Fixed",
    "patch": "Fixed",
    "hotfix": "Fixed",
    # Changed
    "refactor": "Changed",
    "perf": "Changed",
    "style": "Changed",
    "build": "Changed",
    "ci": "Changed",
    "chore": "Changed",
    "docs": "Changed",
    "change": "Changed",
    "update": "Changed",
    # Removed
    "remove": "Removed",
    "delete": "Removed",
    "deprecate": "Removed",
    "drop": "Removed",
}

SECTION_ORDER = ["Added", "Changed", "Fixed", "Removed", "Other"]


def run_git(args: List[str], cwd: Optional[str] = None) -> str:
    """Run git command and return standard output."""
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
            errors="replace"
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return ""


def get_latest_tag(cwd: Optional[str] = None) -> Optional[str]:
    """Retrieve the most recent git tag."""
    tag = run_git(["describe", "--tags", "--abbrev=0"], cwd=cwd)
    return tag if tag else None


def get_commit_log(since_ref: Optional[str] = None, cwd: Optional[str] = None) -> List[Tuple[str, str, str]]:
    """
    Retrieve commits formatted as (hash, author_date, subject).
    If since_ref is provided, fetches commits from since_ref..HEAD.
    """
    rev_range = f"{since_ref}..HEAD" if since_ref else "HEAD"
    output = run_git(["log", rev_range, "--no-merges", "--pretty=format:%h|%as|%s"], cwd=cwd)
    if not output:
        return []
    
    commits = []
    for line in output.splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))
    return commits


def parse_commit(subject: str) -> Tuple[str, str, Optional[str]]:
    """
    Parse a commit message into (category, clean_message, scope).
    Supports Conventional Commits (e.g. 'feat(auth): add OAuth2 provider').
    """
    pattern = r"^([a-zA-Z]+)(?:\(([^)]+)\))?!?:\s*(.*)$"
    match = re.match(pattern, subject)
    
    if match:
        prefix = match.group(1).lower()
        scope = match.group(2)
        message = match.group(3).strip()
        category = CONVENTIONAL_MAP.get(prefix, "Changed")
        return category, message, scope
    
    # Fallback keyword detection for non-conventional commits
    lower_subj = subject.lower()
    for kw, cat in [("fix", "Fixed"), ("add", "Added"), ("remove", "Removed"), ("refactor", "Changed")]:
        if kw in lower_subj:
            return cat, subject, None
            
    return "Changed", subject, None


def generate_changelog(
    repo_path: str = ".",
    version: Optional[str] = None,
    output_path: Optional[str] = None
) -> str:
    """Generate structured markdown changelog adhering to Keep a Changelog."""
    latest_tag = get_latest_tag(repo_path)
    commits = get_commit_log(since_ref=latest_tag, cwd=repo_path)
    
    categorized: Dict[str, List[str]] = {sec: [] for sec in SECTION_ORDER}
    
    for commit_hash, commit_date, subject in commits:
        category, msg, scope = parse_commit(subject)
        scope_str = f"**{scope}**: " if scope else ""
        entry = f"- {scope_str}{msg} ([`{commit_hash}`]({commit_hash}))"
        categorized[category].append(entry)
    
    today = datetime.now().strftime("%Y-%m-%d")
    release_title = f"## [{version or 'Unreleased'}] - {today}"
    if latest_tag:
        release_title += f" (since `{latest_tag}`)"
        
    lines = [
        "# Changelog",
        "",
        "All notable changes to this project will be documented in this file.",
        "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),",
        "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).",
        "",
        release_title,
        ""
    ]
    
    has_entries = False
    for section in SECTION_ORDER:
        entries = categorized.get(section, [])
        if entries:
            has_entries = True
            lines.append(f"### {section}")
            lines.extend(entries)
            lines.append("")
            
    if not has_entries:
        lines.append("### Changed")
        lines.append("- Maintenance updates and synchronization.")
        lines.append("")
        
    result_md = "\n".join(lines)
    
    if output_path:
        # Prepend to existing CHANGELOG.md if present
        if os.path.exists(output_path):
            with open(output_path, "r", encoding="utf-8") as f:
                existing_content = f.read()
            # If header already exists, insert new release after header
            header_split = re.split(r"(## \[[^\]]+\] - \d{4}-\d{2}-\d{2})", existing_content, maxsplit=1)
            if len(header_split) >= 2:
                final_md = (
                    "# Changelog\n\n"
                    "All notable changes to this project will be documented in this file.\n"
                    "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).\n\n"
                    f"{release_title}\n\n"
                )
                for section in SECTION_ORDER:
                    entries = categorized.get(section, [])
                    if entries:
                        final_md += f"### {section}\n" + "\n".join(entries) + "\n\n"
                final_md += header_split[1] + header_split[2]
                result_md = final_md
                
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result_md)
            
    return result_md


if __name__ == "__main__":
    target_repo = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "."
    out_file = "CHANGELOG.md"
    ver = "v1.1.0"
    
    changelog_content = generate_changelog(repo_path=target_repo, version=ver, output_path=out_file)
    print("Successfully generated CHANGELOG.md:")
    print("-" * 50)
    print(changelog_content[:500] + "...")

