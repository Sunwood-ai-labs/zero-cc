<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/zero-cc/main/assets/release-header-v0.2.0.svg" alt="v0.2.0 Release"/>

# v0.2.0 - ワークフロー強化リリース / Workflow Enhancement Release

**リリース日 / Release Date:** 2026年1月12日 / January 12, 2026

---

## 日本語 / Japanese

### 概要

ZERO CC v0.2.0 は、Git Flow ワークフローと開発者体験を大幅に強化するリリースです。新しく `repo-flow` スキルが追加され、各スキルにリファレンステンプレートが提供されるようになりました。

### 新機能

#### スキル

**repo-flow** (新規追加)
- Git Flow ワークフローの完全サポート
- フィーチャーブランチの作成・管理
- プルリクエストの作成・レビュー・マージ
- Emoji コンベンション対応
- PR テンプレート付き

#### リファレンステンプレート

**repo-create**
- README テンプレート（日本語/英語バイリンガル）
- LICENSE オプションガイド
- バッジコレクション
- アニメーション付きヘッダー SVG テンプレート
- 使用例ドキュメント

**repo-maintain**
- リリースノートテンプレート
- リリースヘッダー SVG（アニメーション付き）
- ワークフロー改善

**extension-generator**
- プロジェクト設定パターンの追加

#### インストーラー

**script/install.sh** (全面刷新)
- uv スタイルの簡易インストール（`curl | bash`）
- Claude Code が未インストールの場合、自動で公式インストーラーを実行
- `~/.local/bin` の PATH 設定を自動追加
- 簡素化された引数（`--skip-claude-install` 追加）
- `cc-st`, `cc-glm`, `ccd-st`, `ccd-glm` コマンド提供

### バグ修正

- `script/install.sh`: `ccd-*` コマンドの `exec sudo` で引数が正しく渡らない問題を修正
- PR テンプレート: タイポの修正
- PR テンプレート: Co-Authored-By を削除（不要な重複回避）

### 変更

- `claude-code-extension-generator` → `extension-generator` にリネーム
- `git-flow-workflow` → `repo-flow` にリネーム（名称統一）
- `repo-maintain`: PR 機能を削除（`repo-flow` との重複回避）
- `.gitignore`: 外部ツールファイルを追加

### アップグレード方法

```bash
# Git タグから取得
git fetch --tags
git checkout v0.2.0

# または最新の main ブランチから
git pull origin main
```

### インストール

```bash
# インストーラーを使用（Claude Code も自動インストール）
curl -fsSL https://raw.githubusercontent.com/Sunwood-ai-labs/zero-cc/main/script/install.sh | bash

# または手動でクローン
git clone https://github.com/Sunwood-ai-labs/zero-cc.git
cd zero-cc
```

---

## English

### Overview

ZERO CC v0.2.0 is a workflow enhancement release that significantly improves the Git Flow workflow and developer experience. A new `repo-flow` skill has been added, and reference templates are now provided for all skills.

### What's New

#### Skills

**repo-flow** (New)
- Full Git Flow workflow support
- Feature branch creation and management
- Pull request creation, review, and merge
- Emoji conventions support
- Includes PR template

#### Reference Templates

**repo-create**
- README template (bilingual Japanese/English)
- LICENSE options guide
- Badge collection
- Animated header SVG template
- Usage examples documentation

**repo-maintain**
- Release notes template
- Release header SVG (with animations)
- Workflow improvements

**extension-generator**
- Added project configuration patterns

#### Installer

**script/install.sh** (Complete refresh)
- uv-style simple install (`curl | bash`)
- Auto-installs Claude Code if missing via official installer
- Auto-adds `~/.local/bin` to PATH
- Simplified arguments (added `--skip-claude-install`)
- Provides `cc-st`, `cc-glm`, `ccd-st`, `ccd-glm` commands

### Bug Fixes

- `script/install.sh`: Fixed `ccd-*` command `exec sudo` argument passing issue
- PR template: Fixed typos
- PR template: Removed Co-Authored-By (to avoid unnecessary duplication)

### Changes

- Renamed `claude-code-extension-generator` → `extension-generator`
- Renamed `git-flow-workflow` → `repo-flow` (naming consistency)
- `repo-maintain`: Removed PR functionality (to avoid duplication with `repo-flow`)
- `.gitignore`: Added external tool files

### Upgrade

```bash
# Fetch by git tag
git fetch --tags
git checkout v0.2.0

# Or from latest main branch
git pull origin main
```

### Installation

```bash
# Using installer (auto-installs Claude Code)
curl -fsSL https://raw.githubusercontent.com/Sunwood-ai-labs/zero-cc/main/script/install.sh | bash

# Or manually clone
git clone https://github.com/Sunwood-ai-labs/zero-cc.git
cd zero-cc
```

---

## ライセンス / License

MIT License - 詳細は [LICENSE](LICENSE) を参照 / see [LICENSE](LICENSE) for details.

---

## リンク / Links

- [リポジトリ / Repository](https://github.com/Sunwood-ai-labs/zero-cc)
- [イシュー / Issues](https://github.com/Sunwood-ai-labs/zero-cc/issues)
- [v0.1.0 リリース / v0.1.0 Release](https://github.com/Sunwood-ai-labs/zero-cc/releases/tag/v0.1.0)

---

## 変更統計 / Change Statistics

```
25 files changed, 2728 insertions(+), 679 deletions(-)
```

---

<div align="center">

[Claude Code](https://claude.ai/code) のために ❤️ を込めて / Made with ❤️ for [Claude Code](https://claude.ai/code)

 Developed with **GLM-4.7** by Zhipu AI

</div>
