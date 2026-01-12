<div align="center">

<img src="assets/header.svg" alt="ZERO CC Header" width="1200"/>

</div>

<div align="center">

### Claude Code 用カスタムスキル集

[![Claude Code](https://img.shields.io/badge/Claude-Code-purple?style=flat-square&logo=anthropic)](https://claude.ai/code)
[![GLM-4.7](https://img.shields.io/badge/Powered%20by-GLM--4.7-blue?style=flat-square)](https://open.bigmodel.cn/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

Claude Code を強化する、実用的なカスタムスキルコレクション。

</div>

---

## ✨ 概要

`zero-cc` は Claude Code の生産性を向上させるために作られたカスタムスキル集です。GitHub リポジトリの作成からメンテナンス、さらには新しいスキルの自動生成まで、開発ワークフローを自動化します。

## 📦 含まれるスキル

<div align="center">

| スキル | 説明 |
|:------:|------|
| **extension-generator** | 自然言語から Claude Code 拡張機能（スキル/エージェント）を自動生成 |
| **repo-create** | GitHub リポジトリを新規作成・初期化 |
| **repo-flow** | Git Flow ワークフロー（ブランチ/PR/マージ） |
| **repo-maintain** | 既存リポジトリのメンテナンス（リリース/変更履歴/状態確認） |

</div>

---

### 🔧 extension-generator

ユーザーの自然言語指示から Claude Code の拡張機能を自動生成するメタスキル。

**対応する拡張機能:**
- **スキル** - プロンプト再利用・専門知識・ワークフロー
- **サブエージェント** - 独立コンテキストの特化型AI
- **プロジェクト設定** - CLAUDE.md / .mcp.json

```bash
# スキルを作成
/extension-generator コードレビューするスキルを作って

# サブエージェントを作成
/extension-generator フロントエンドコードを最適化するエージェントを作って
```

---

### 📁 repo-create

GitHub リポジトリを新規作成・初期化します。

**機能:**
- `gh repo create` でリポジトリ作成
- README.md / .gitignore / LICENSE を自動生成
- initial commit を自動実行

```bash
/repo-create my-awesome-project
/repo-create my-app --private --description "My awesome app"
```

---

### 🌊 repo-flow

Git Flow ワークフローで開発からマージまでを実行します。

**機能:**
- **フィーチャーブランチ作成** - `develop` からブランチ作成
- **PR 作成** - 変更内容から PR を自動生成
- **コードレビュー** - PR のレビュー支援
- **マージ** - レビュー完了後にマージ実行

```bash
/repo-flow feature add-user-auth
/repo-flow pr
/repo-flow review
/repo-flow merge
```

---

### 🚀 repo-maintain

既存 GitHub リポジトリのメンテナンス作業を支援します。

**機能:**
- **リリース作成** - Gitタグ + GitHubリリース + リリースノート生成
- **変更履歴** - コミットログから自動分類
- **イシュー作成** - テンプレートベースのIssue作成
- **状態確認** - リポジトリのサマリー表示

```bash
/repo-maintain release 1.0.0
/repo-maintain changelog
/repo-maintain issue "Bug: Login fails"
/repo-maintain status
```

---

## 🚀 セットアップ

### 要件

- [GitHub CLI](https://cli.github.com/) (`gh`) がインストール済み
- `gh auth login` で認証済み

### インストール

#### 方法1: インストーラー使用（推奨）

Claude Code も一緒に自動インストールされます。

```bash
curl -fsSL https://raw.githubusercontent.com/Sunwood-ai-labs/zero-cc/main/script/install.sh | bash
```

インストール後、以下のコマンドが利用可能になります：
- `cc-st` - Claude Code（標準モード）
- `cc-glm` - Claude Code（GLM/Z.AI モード）
- `ccd-st` - Claude Code Dangerous（標準モード）
- `ccd-glm` - Claude Code Dangerous（GLM/Z.AI モード）

#### 方法2: 手動インストール

1. このリポジトリをクローン
2. Claude Code でプロジェクトを開く
3. スキルが自動的に読み込まれます

```bash
git clone https://github.com/Sunwood-ai-labs/zero-cc.git
cd zero-cc
```

---

## 📁 構造

```
zero-cc/
├── .claude/
│   └── skills/
│       ├── extension-generator/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── repo-create/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── repo-flow/
│       │   ├── SKILL.md
│       │   └── references/
│       └── repo-maintain/
│           ├── SKILL.md
│           └── references/
├── assets/
│   ├── header.svg
│   └── release-header-v0.2.0.svg
├── script/
│   └── install.sh
├── README.md
├── RELEASE_NOTES.md
└── LICENSE
```

---

## 🎮 事例 / Examples

ZERO CC を活用して作成されたプロジェクト例:

### [claude-glm-actions-lab](https://github.com/Sunwood-ai-labs/claude-glm-actions-lab)

GitHub Actions で Claude Code と GLM API を統合する実験的リポジトリ。

**使用した ZERO CC スキル:**
- `/repo-create` - リポジトリの初期化
- `/repo-maintain` - リリース管理
- `/extension-generator` - カスタムスキルの生成

**機能:**
- GitHub Actions で Claude Code を実行
- GLM API (Z.AI) との統合
- Issue コメント & PR レビュー対応
- Bot 自己トリガー防止機能

---

## 🤖 使用モデル

本プロジェクトの開発には **GLM-4.7** (Zhipu AI) が使用されています。

### GLM-4.7 について

- **開発者**: [Zhipu AI (智谱AI)](https://open.bigmodel.cn/)
- **リリース**: 2025年12月22日
- **特徴**: コーディングシーンに特化した最適化、マルチファイル処理、深い数学的推論
- **ツール互換性**: Claude Code を含む20以上のAIコーディングツールと互換性
- **ライセンス**: オープンウェイトモデル

---

## 📄 ライセンス

[MIT License](LICENSE)

---

<div align="center">

Made with ❤️ for [Claude Code](https://claude.ai/code)

</div>
