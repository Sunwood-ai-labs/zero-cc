<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/zero-cc/main/assets/release-header-v0.3.0_a.svg" alt="v0.3.0 Release"/>

# v0.3.0 - Agent ZERO 星来の覚醒 / Seira's Awakening

**リリース日 / Release Date:** 2025-01-17

---

## 日本語 / Japanese

### 概要

このリリースでは、**無重 星来（むじゅう せいら）** という新しいアシスタントキャラクターが登場し、Claude Code の設定が含まれます。また、リポジトリ管理スキルの大幅な拡張と、SNS への自動リリース通知機能が追加されました。

星来は重力から解放された存在として、あなたの開発作業をふわっと手伝います。

### 新機能

- **Agent ZERO CLAUDE.md 設定** - 無重 星来キャラクターの追加
  - ふわふわした浮世離れした口調
  - キャラクターとしての振る舞い定義
  - セキュリティ義務の明文化

- **repo-manager スキル** - タスク分割からプロジェクト管理を支援
  - Issue 登録の自動化
  - プロジェクト進捗の追跡
  - 日付設定ワークフロー

- **project-mgmt スキル** - GitHub プロジェクト管理の一括操作
  - Issue 一括作成
  - ラベル・プロジェクト設定
  - マイルストーン・日付・ステータス変更

- **repo-flow スキルの強化** - 自動ワークフロー実行
  - Git Flow ワークフローの自動化
  - develop → main のリリースフロー対応
  - 自動マージ機能

- **SNS 自動リリース通知** - Discord と X への自動投稿
  - リリース時に Discord へ通知
  - リリース時に X (Twitter) へ投稿

- **VSCode 設定** - エディタ設定の追加
  - プロジェクト固有の設定

- **Claude シンボリックリンクセットアップガイド** - ドキュメント追加
  - グローバル設定のシンボリックリンク手順

### バグ修正

- **project-mgmt**: jq を使用した動的 ID 解決に修正
  - GitHub API レスポンスからの確実な ID 取得

- **gemini-code-assist のレビューフィードバック**に対応

### 変更

- **repo-maintain スキル** - リリースワークフローの改善
  - v0.2.0 のフィードバックに基づく改善
  - バイリンガルリリースノート対応

- **repo-create スキル** - Git init 手順の明示化
  - リポジトリ作成プロセスの明確化

- **ファイル権限** - 実行可能スクリプトの権限更新

- **.gitignore** - ZERO_CC_PRJ サブディレクトリを追加
  - ローカル設定ファイルの除外

### ドキュメント

- リポジトリの examples セクションに claude-glm-actions-lab を追加
- repo-flow ドキュメント: main マージは人間の責任であることを明記

---

## English

### Overview

This release introduces **Seira Muju** as a new assistant character with Claude Code configuration, significant extensions to repository management skills, and automated release notification features to social media platforms.

Seira, a gravity-liberated existence, will gently assist your development workflow.

### What's New

- **Agent ZERO CLAUDE.md Configuration** - Added Seira Muju character
  - Soft, otherworldly speaking style
  - Character behavior definitions
  - Explicit security mandates

- **repo-manager Skill** - Task decomposition to project management support
  - Automated Issue registration
  - Project progress tracking
  - Date setting workflow

- **project-mgmt Skill** - Batch GitHub project management operations
  - Batch Issue creation
  - Label and project configuration
  - Milestone, date, and status changes

- **Enhanced repo-flow Skill** - Automatic workflow execution
  - Git Flow workflow automation
  - develop → main release flow support
  - Automatic merge functionality

- **SNS Auto Release Notifications** - Auto-post to Discord and X
  - Discord notifications on release
  - X (Twitter) posting on release

- **VSCode Settings** - Added editor configuration
  - Project-specific settings

- **Claude Symlink Setup Guide** - Documentation added
  - Global configuration symlink procedures

### Bug Fixes

- **project-mgmt**: Fixed to use dynamic ID resolution with jq
  - Reliable ID retrieval from GitHub API responses

- Addressed **gemini-code-assist review feedback**

### Changes

- **repo-maintain Skill** - Improved release workflow
  - Improvements based on v0.2.0 feedback
  - Bilingual release notes support

- **repo-create Skill** - Explicit git init steps
  - Clarified repository creation process

- **File Permissions** - Updated executable script permissions

- **.gitignore** - Added ZERO_CC_PRJ subdirectory
  - Excluded local configuration files

### Documentation

- Added claude-glm-actions-lab to repository examples section
- repo-flow documentation: clarified main merge is human responsibility

---

## Upgrade Method

```bash
# Method 1: From Git tags
git fetch --tags
git checkout v0.3.0

# Method 2: Pull latest merge
git pull origin main
```

---

## Contributors

@Sunwood-ai-labs

---

## Next Release Plans

- Further skill enhancements based on community feedback
- Additional automation workflows
- Expanded documentation and examples

---

## Links

- [GitHub Repository](https://github.com/Sunwood-ai-labs/zero-cc)
- [Issues](https://github.com/Sunwood-ai-labs/zero-cc/issues)
- [Previous Release (v0.2.0)](https://github.com/Sunwood-ai-labs/zero-cc/releases/tag/v0.2.0)

---

<div align="center">

[Claude Code](https://claude.ai/code) のために ❤️ を込めて / Made with ❤️ for [Claude Code](https://claude.ai/code)

Developed with **GLM-4.7** by Zhipu AI

</div>
