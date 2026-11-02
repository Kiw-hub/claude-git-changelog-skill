# Git History Changelog Generator Skill

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()
[![Standard](https://img.shields.io/badge/format-Keep%20a%20Changelog-orange.svg)](https://keepachangelog.com/)

A lightweight, zero-dependency Claude Code skill and standalone CLI engine that generates structured, semantically categorized `CHANGELOG.md` files from Git commits since the latest release tag.

---

## 🚀 Setup Instructions (3 Steps)

1. **Clone or Copy:**
   Copy `generate_changelog.py` and `SKILL.md` into your repository or Claude Code skills directory (`.claude/skills/`).

2. **Run Generator:**
   Execute directly in your terminal or via Claude Code:
   ```bash
   python generate_changelog.py
   # Or run via bash:
   bash changelog.sh
   ```

3. **Verify `CHANGELOG.md`:**
   Inspect the automatically generated or updated `CHANGELOG.md` formatted to Keep a Changelog standards.

---

## 🧪 Acceptance Criteria Verification

- [x] **Command Trigger:** Works via Claude Code `/generate-changelog`, `bash changelog.sh`, or `python generate_changelog.py`.
- [x] **Tag Tracking:** Automatically queries `git describe --tags --abbrev=0` to extract commits since the last release.
- [x] **Semantic Categorization:** Auto-categorizes Conventional Commits into `Added` (`feat`), `Fixed` (`fix`), `Changed` (`refactor`, `perf`, `chore`), and `Removed` (`deprecate`, `delete`).
- [x] **Formatted Output:** Generates clean, standardized Keep a Changelog markdown with commit hashes and dates.
- [x] **Tested on Real Git Repository:** Includes comprehensive test suite (`tests/test_changelog.py`) with 100% pass rate.
- [x] **3-Step README:** Concise onboarding guide above.

---

## 📄 Sample Output

```markdown
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v1.1.0] - 2026-11-02 (since `v1.0.0`)

### Added
- **export**: add CSV export feature ([`7576b53`](7576b53))

### Fixed
- **core**: fix buffer overflow in parser ([`3e18be1`](3e18be1))
```

---

## 📜 License
MIT License. Open for Claude Builders and the open-source community.

