---
name: reg-commit-flat
description: |
  差分からIssueを作成 + プロジェクトに登録 + 複数コミット + Gitフロー（analyze-diff + project-mgmt + repo-flow）。
  サブイシューを作成せず、1つのIssueのみを作成し、ファイル単位・機能単位で複数のコミットに分けるフラットなパターン。
  トリガー例: 「/reg-commit-flat」
allowed-tools: Bash, Glob, Grep, Read, AskUserQuestion
arguments: auto-detect
user-invocable: true
---

# Reg Commit Flat (Register & Commit - Flat)

差分からIssueを作成してプロジェクトに登録し、ファイル単位・機能単位で複数のコミットに分けてGitフローを実行する省略形スキルです。

**フロー**: `analyze-diff` → `project-mgmt` → `複数のコミット` → `Gitフロー`

**重要**: サブイシューは作成しません。1つのIssueに対して、複数のコミットを行います。巻き戻しやすいよう、変更はファイル単位・機能単位で細かくコミットします。

## reg-commit との違い

| スキル | 構造 | コミット | 用途 |
|:------|:-----|:---------|:------|
| **reg-commit** | 親Issue + サブイシュー | サブイシューごとに分割 | 大規模な変更、複数の独立した機能、各機能ごとにレビューを受けたい |
| **reg-commit-flat** | 単一Issueのみ | ファイル単位・機能単位で複数コミット | 小〜中規模の変更、単一の機能改善、巻き戻しを重視 |

## 使い方

```
/reg-commit-flat
```

## ワークフロー

```
┌─────────────────────────────────────────────────────────────┐
│  1. analyze-diff モジュール                                   │
│     - 現在の差分を解析（git status, git diff）                │
│     - タスク分割案の作成                                       │
├─────────────────────────────────────────────────────────────┤
│  2. project-mgmt モジュール                                    │
│     - 単一Issueを作成（サブイシューなし）                       │
│     - プロジェクトへの追加                                     │
│     - ステータス設定（Done）                                   │
│     - 日付設定                                                 │
├─────────────────────────────────────────────────────────────┤
│  3. コミット                                                  │
│     - ファイル単位・機能単位で複数のコミットに分ける              │
│     - 巻き戻しやすいよう、細かくコミットする                      │
│     - 最後のコミットメッセージにIssue番号を含める                 │
├─────────────────────────────────────────────────────────────┤
│  4. Gitフロー（repo-flow モジュール）                         │
│     - ブランチ作成                                             │
│     - プッシュ                                                 │
│     - PR 作成                                                 │
│     - develop へマージ                                        │
│     - クリーンアップ                                           │
└─────────────────────────────────────────────────────────────┘
```

## 実行手順

### 1. 差分解析

```bash
# 現在の差分を確認
git status
git diff --stat

# 変更の詳細を確認
git diff
```

### 2. Issue 作成（単一）

サブイシューを作成せず、1つのIssueのみを作成します。

```bash
gh issue create \
  --title "✨ feat: 機能改善のタイトル" \
  --body "## 概要

変更内容の概要を記述。

## 変更内容

- 変更1
- 変更2
- 変更3

## テスト

- [ ] テスト項目1
- [ ] テスト項目2" \
  --label "enhancement"
```

### 3. プロジェクトに追加

```bash
gh project item-add PROJECT_NUMBER \
  --url "https://github.com/OWNER/REPO/issues/ISSUE_NUMBER" \
  --owner OWNER
```

### 4. ステータスと日付の設定

```bash
# ステータスを Done に設定
gh project item-edit \
  --project-id PROJECT_GLOBAL_ID \
  --id ITEM_ID \
  --field-id STATUS_FIELD_ID \
  --single-select-option-id DONE_OPTION_ID

# 日付を設定
gh project item-edit \
  --project-id PROJECT_GLOBAL_ID \
  --id ITEM_ID \
  --field-id START_DATE_FIELD_ID \
  --date "YYYY-MM-DD"

gh project item-edit \
  --project-id PROJECT_GLOBAL_ID \
  --id ITEM_ID \
  --field-id END_DATE_FIELD_ID \
  --date "YYYY-MM-DD"
```

### 5. コミット（ファイル単位・機能単位で分割）

**重要**: 変更はファイル単位・機能単位で細かくコミットし、巻き戻しやすくします。

**Issue番号が判明している場合**: すべてのコミットメッセージにIssue番号を付けてください。

```bash
# ファイル1
git add path/to/file1.ext
git commit -m "✨ feat: 機能1の追加 (#ISSUE_NUMBER)

- 変更内容の詳細

Co-Authored-By: Claude <noreply@anthropic.com>"

# ファイル2
git add path/to/file2.ext
git commit -m "🐛 fix: バグの修正 (#ISSUE_NUMBER)

- 修正内容の詳細

Co-Authored-By: Claude <noreply@anthropic.com>"

# ファイル3
git add path/to/file3.ext
git commit -m "📚 docs: ドキュメント更新 (#ISSUE_NUMBER)

- 更新内容の詳細

Co-Authored-By: Claude <noreply@anthropic.com>"

# 最後のコミットに Closes キーワードを含める（自動クローズ用）
git add path/to/last-file.ext
git commit -m "🔧 chore: 設定ファイルの追加 (#ISSUE_NUMBER)

Closes #ISSUE_NUMBER

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**コミットの粒度**:
- 1ファイル = 1コミット（基本）
- 関連する変更はまとめてOK
- **すべてのコミットにIssue番号を付ける**（例: `#25`）
- **最後のコミットに `Closes #番号` を含める**（自動クローズ用）

### 6. Gitフロー

`repo-flow` モジュールを実行して、ブランチ作成・プッシュ・PR・マージを行います。

## 実例

### シナリオ: ドキュメントを更新する場合

```bash
# 1. 差分を解析
git status
# 変更ファイル: README.md, CONTRIBUTING.md, docs/api.md

# 2. Issue 作成（単一）
gh issue create \
  --title "📚 docs: ドキュメントの更新と整備" \
  --body "## 概要

README、CONTRIBUTING、APIドキュメントを更新します。

## 変更内容

- README.md: インストール手順の更新
- CONTRIBUTING.md: 開発環境設定の追加
- docs/api.md: API仕様の最新化

## テスト

- [ ] リンク切れの確認
- [ ] 誤字脱字のチェック" \
  --label "documentation"

# 出力: https://github.com/owner/repo/issues/25

# 3. プロジェクトに追加・ステータス設定
gh project item-add 2 --owner OWNER \
  --url "https://github.com/owner/repo/issues/25"

# ステータスを Done に
gh project item-edit \
  --project-id PVT_kwXXX \
  --id PVTI_XXX \
  --field-id PVTSSF_XXX \
  --single-select-option-id 98236657  # Done

# 4. ファイル単位でコミット（複数）

# README.md
git add README.md
git commit -m "📚 docs(readme): インストール手順を最新化 (#25)

Node.js v20+ の要件を明記し、手順を更新しました。

Co-Authored-By: Claude <noreply@anthropic.com>"

# CONTRIBUTING.md
git add CONTRIBUTING.md
git commit -m "📚 docs(contributing): 開発環境設定手順を追加 (#25)

Docker Desktop を使用した開発環境のセットアップ手順を追加しました。

Co-Authored-By: Claude <noreply@anthropic.com>"

# docs/api.md（最後のコミットに Closes を含める）
git add docs/api.md
git commit -m "📚 docs(api): API仕様をv2.0.0に更新 (#25)

エンドポイントの追加と廃止を反映しました。

Closes #25

Co-Authored-By: Claude <noreply@anthropic.com>"

# 5. Gitフロー（repo-flow）
git checkout -b feature/docs-update-25
git push -u origin feature/docs-update-25
gh pr create --base develop \
  --title "📚 docs: ドキュメントの更新と整備" \
  --body "## 概要

ドキュメントを一括更新しました。

## 変更内容

- README.md: インストール手順を最新化
- CONTRIBUTING.md: 開発環境設定手順を追加
- docs/api.md: API仕様をv2.0.0に更新

Closes #25

Co-Authored-By: Claude <noreply@anthropic.com>"

# PRをマージ
git checkout develop
git pull
git merge feature/docs-update-25 --no-ff
git push origin develop

# クリーンアップ
git branch -d feature/docs-update-25
git push origin --delete feature/docs-update-25
```

## 使用するタイミング

**reg-commit-flat を使うべき時:**
- 小〜中規模の変更（1〜5ファイル）
- 単一の機能改善やバグ修正
- ドキュメント更新
- 設定ファイルの変更
- サブイシューに分けるほどの複雑さがない

**reg-commit を使うべき時:**
- 大規模な変更（6ファイル以上）
- 複数の独立した機能
- 各機能ごとにレビューを受けたい
- 複数人で並行して開発する

## 注意点

1. **サブイシューは作成しない**: 単一のIssueのみ作成します
2. **コミットは細かく分ける**: ファイル単位・機能単位でコミットし、巻き戻しやすくします
3. **すべてのコミットにIssue番号を付ける**: Issue番号が判明していれば、すべてのコミットメッセージに `#番号` を付けてください（例: `#25`）
4. **最後のコミットに Closes**: `Closes #番号` を含めると自動的にIssueがクローズされます

## 詳細

このスキルは以下のモジュールを組み合わせたものです：

- [.claude/skills/analyze-diff/SKILL.md](../analyze-diff/SKILL.md) - 差分解析 → タスク分割
- [.claude/skills/project-mgmt/SKILL.md](../project-mgmt/SKILL.md) - プロジェクト追加・ステータス設定・日付設定
- [.claude/skills/repo-flow/SKILL.md](../repo-flow/SKILL.md) - ブランチ作成・コミット・プッシュ・PR・マージ

## 関連スキル

| スキル | 用途 |
|:------|:------|
| **reg-commit** | サブイシューごとにコミットするパターン（大規模変更用） |
| **reg-issue** | 計画からIssueを作成 + プロジェクトに登録（plan + project-mgmt） |
| **repo-flow** | Gitフロー（ブランチ作成・PR・マージ） |
| **repo-manager** | 全モジュールを組み合わせたタスク管理 |
