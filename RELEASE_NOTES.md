<img src="https://github.com/Sunwood-ai-labs/zero-cc/releases/download/v0.1.0/release-header.svg" alt="v0.1.0 Release" width="1200"/>

# v0.1.0 - 初回リリース / Initial Release

**リリース日 / Release Date:** 2026年1月12日 / January 12, 2026

---

## 日本語 / Japanese

### 概要

ZERO CC v0.1.0 は、Claude Code 用カスタムスキルコレクションの初回リリースです。このリリースには、Claude Code のワークフローを強化する3つの強力なスキルが含まれています。

### 新機能

#### スキル

**claude-code-extension-generator**
- 自然言語から Claude Code 拡張機能を自動生成
- スキル、サブエージェント、プロジェクト設定に対応
- リファレンスドキュメントとテンプレート付き

**repo-create**
- GitHub リポジトリの作成・初期化
- README.md、.gitignore、LICENSE の自動生成
- initial commit の自動実行

**repo-maintain**
- リリース作成・リリースノート自動生成
- コミット履歴からの変更履歴生成
- プルリクエスト・イシュー作成
- リポジトリ状態サマリー表示

#### アセット

- アニメーション付き SVG ヘッダー（グラデーション＆アニメーション効果）
- バージョンアナウンス用リリースヘッダー画像

#### ドキュメント

- スキル説明付き包括的な README
- GLM-4.7 モデル情報
- セットアップ＆使用方法ガイド

### インストール

```bash
git clone https://github.com/Sunwood-ai-labs/zero-cc.git
cd zero-cc
```

Claude Code でプロジェクトを開くと、スキルが自動的に読み込まれます。

### 要件

- [GitHub CLI](https://cli.github.com/) (`gh`) がインストール済み
- `gh auth login` で認証済み

### 技術スタック

本プロジェクトの開発には **GLM-4.7** (Zhipu AI) が使用されました。

---

## English

### Overview

ZERO CC v0.1.0 is the initial release of the Claude Code custom skills collection. This release includes three powerful skills to enhance your Claude Code workflow.

### What's New

#### Skills

**claude-code-extension-generator**
- Automatically generate Claude Code extensions from natural language
- Support for skills, sub-agents, and project configurations
- Includes reference documentation and templates

**repo-create**
- Create and initialize GitHub repositories
- Automatic README.md, .gitignore, and LICENSE generation
- Initial commit automation

**repo-maintain**
- Release creation with automatic release notes
- Changelog generation from commit history
- Pull request and issue creation
- Repository status summary

#### Assets

- Animated SVG header with gradient effects and animations
- Release-specific header image for version announcements

#### Documentation

- Comprehensive README with skill descriptions
- GLM-4.7 model information
- Setup and usage instructions

### Installation

```bash
git clone https://github.com/Sunwood-ai-labs/zero-cc.git
cd zero-cc
```

Then open the project in Claude Code to automatically load the skills.

### Requirements

- [GitHub CLI](https://cli.github.com/) (`gh`) installed
- `gh auth login` completed

### Tech Stack

This project was developed using **GLM-4.7** by Zhipu AI.

---

## ライセンス / License

MIT License - 詳細は [LICENSE](LICENSE) を参照 / see [LICENSE](LICENSE) for details.

---

## リンク / Links

- [リポジトリ / Repository](https://github.com/Sunwood-ai-labs/zero-cc)
- [イシュー / Issues](https://github.com/Sunwood-ai-labs/zero-cc/issues)

---

<div align="center">

[Claude Code](https://claude.ai/code) のために ❤️ を込めて / Made with ❤️ for [Claude Code](https://claude.ai/code)

</div>
