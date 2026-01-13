<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/zero-cc/main/assets/release-header-v0.3.0.svg" alt="v0.3.0 Release"/>

# v0.3.0 - Documentation & Examples Enhancement / ドキュメントと例の強化

**リリース日 / Release Date:** 2026-01-14

---

## 日本語 / Japanese

### 概要

v0.3.0 は、ドキュメントの改善と使用例の追加に焦点を当てたリリースです。`repo-maintain` スキルのワークフローを改善し、新しく `examples` セクションを追加して、ユーザーが各スキルの使用方法をより簡単に理解できるようにしました。

### 新機能

- **Examples セクション**: README に各スキルの使用例を追加しました
  - `claude-glm-actions-lab` の実践的な使用例を追加

### バグ修正

- なし

### 変更

- **repo-maintain ワークフロー改善**: リリース手順をより明確にしました
  - バイリンガルリリースノートのフォーマットを導入
  - リリースヘッダー画像のカスタマイズ手順を追加
- **.gitignore 更新**: `ZERO_CC_PRJ` サブディレクトリを除外

### ドキュメント

- README を更新し、examples セクションを追加
- リリースノートのフォーマットを改善

---

## English

### Overview

v0.3.0 focuses on documentation improvements and examples. We've enhanced the `repo-maintain` skill workflow and added a new `examples` section to make it easier for users to understand how to use each skill.

### What's New

- **Examples Section**: Added usage examples for each skill in the README
  - Added practical examples for `claude-glm-actions-lab`

### Bug Fixes

- None

### Changes

- **repo-maintain Workflow Enhancement**: Made the release process more clear
  - Introduced bilingual release note format
  - Added release header image customization steps
- **.gitignore Update**: Excluded `ZERO_CC_PRJ` subdirectory

### Documentation

- Updated README with examples section
- Improved release note format

---

## アップグレード方法 / Upgrade Guide

```bash
# 方法 1: Git タグから / From Git Tag
git fetch --tags
git checkout v0.3.0

# 方法 2: 最新のメインから / From Latest Main
git pull origin main
```

---

## ファイル変更 / File Changes

```
 .claude/skills/repo-maintain/SKILL.md | 118 ++++++++++++++++++++++++++--------
 .gitignore                            |   1 +
 README.md                             |  21 ++++++
 3 files changed, 113 insertions(+), 27 deletions(-)
```

---

## コントリビューター / Contributors

@Sunwood-ai-labs

---

## 次のリリース予定 / Upcoming Release

- 継続的なドキュメント改善
- ユーザーフィードバックによる機能強化

---

## リンク / Links

- [GitHub Repository](https://github.com/Sunwood-ai-labs/zero-cc)
- [Issues](https://github.com/Sunwood-ai-labs/zero-cc/issues)
- [Previous Release (v0.2.0)](https://github.com/Sunwood-ai-labs/zero-cc/releases/tag/v0.2.0)

---

<div align="center">

[Claude Code](https://claude.ai/code) のために ❤️ を込めて / Made with ❤️ for [Claude Code](https://claude.ai/code)

Developed with **GLM-4.7** by Zhipu AI

</div>
