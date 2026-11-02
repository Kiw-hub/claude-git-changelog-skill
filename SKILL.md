---
name: generate-changelog
description: Automatically generates a structured, semantically categorized CHANGELOG.md from git history adhering to Keep a Changelog standards.
---

# 📝 Git History Changelog Generator Skill

Automatically inspects the local Git repository, resolves commits since the latest Git release tag, classifies Conventional Commit prefixes into canonical Keep a Changelog categories (`Added`, `Fixed`, `Changed`, `Removed`), and writes or prepends to `CHANGELOG.md`.

## Features
- **Zero Config:** Auto-detects the latest Git tag using `git describe --tags --abbrev=0`.
- **Semantic Classification:** Parses scopes and Conventional Commits (`feat`, `fix`, `refactor`, `perf`, `docs`, `chore`, `remove`).
- **Idempotent Prepend:** Cleanly prepends new releases above existing changelog records without overwriting past history.
- **Cross-Platform:** Works seamlessly on Windows, macOS, and Linux.

## Trigger Command
Execute:
```bash
/generate-changelog
```
Or run directly:
```bash
python generate_changelog.py
# or
bash changelog.sh
```

## Output Standard
Generates output conforming to [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/) and Semantic Versioning.

