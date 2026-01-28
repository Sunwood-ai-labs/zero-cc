---
name: reg-commit-pr
description: |
  差分からIssueを作成 + プロジェクトに登録 + 複数コミット + プッシュ + PR作成で終了（analyze-diff + project-mgmt + repo-flow PR作成まで）。
  サブイシューを作成せず、1つのIssueのみを作成し、ファイル単位・機能単位で複数のコミットに分けるフラットなパターン。
  マージは実行せず、PR作成で終了します。
  トリガー例: 「/reg-commit-pr」
allowed-tools: Bash, Glob, Grep, Read, AskUserQuestion
arguments: auto-detect
user-invocable: true
---

# Reg Commit PR (Register & Commit - PR Only)

差分からIssueを作成してプロジェクトに登録し、ファイル単位・機能単位で複数のコミットに分けて、PR作成まで実行するスキルです。

**フロー**: `analyze-diff` → `project-mgmt` → `複数のコミット` → `プッシュ` → `PR作成`

**重要**: マージは実行しません。レビューを受けてから、手動でマージしてください。

## reg-commit-flat との違い

| スキル | フロー | 用途 |
|:------|:-----|:------|
| **reg-commit-flat** | Issue作成 → コミット → プッシュ → PR → **マージ → クリーンアップ** | レビュー不要な変更、自信がある変更 |
| **reg-commit-pr** | Issue作成 → コミット → プッシュ → **PR作成で終了** | レビューを受けたい変更、チーム開発 |

## 使い方

```
/reg-commit-pr
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
│     - マイルストーンの取得・設定（あれば）                       │
│     - プロジェクトへの追加                                     │
│     - ステータス設定（Todo または In Progress）                │
│     - 日付設定                                                 │
├─────────────────────────────────────────────────────────────┤
│  3. ブランチ作成                                               │
│     - develop からフィーチャーブランチを作成                    │
│     - ブランチ名: feature/<description>-<issue_number>         │
├─────────────────────────────────────────────────────────────┤
│  4. コミット                                                  │
│     - ファイル単位・機能単位で複数のコミットに分ける              │
│     - 巻き戻しやすいよう、細かくコミットする                      │
│     - すべてのコミットメッセージにIssue番号を含める              │
├─────────────────────────────────────────────────────────────┤
│  5. プッシュ                                                   │
│     - リモートにブランチをプッシュ                              │
├─────────────────────────────────────────────────────────────┤
│  6. PR 作成                                                   │
│     - プルリクエストを作成                                     │
│     - develop ブランチに対してPRを作成                          │
│     - ここで終了（マージは実行しない）                          │
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

### 3. マイルストーンの取得・設定（あれば）

```bash
# マイルストーン一覧を取得
gh api /repos/OWNER/REPO/milestones

# 出力例:
# [
#   {
#     "number": 1,
#     "title": "v0.1.0",
#     "state": "open",
#     "due_on": "2026-01-31T23:59:59Z"
#   },
#   {
#     "number": 2,
#     "title": "v0.2.0",
#     "state": "open"
#   }
# ]

# マイルストーンがある場合、Issueにアタッチ
gh api --method PATCH /repos/OWNER/REPO/issues/ISSUE_NUMBER \
  -f milestone=MILESTONE_NUMBER

# 例: v0.1.0（milestone: 1）をアタッチ
# gh api --method PATCH /repos/OWNER/REPO/issues/25 -f milestone=1
```

**注意**: マイルストーンがない場合は、この手順をスキップして進めてください。

### 4. プロジェクトに追加

```bash
gh project item-add PROJECT_NUMBER \
  --url "https://github.com/OWNER/REPO/issues/ISSUE_NUMBER" \
  --owner OWNER
```

### 5. ステータスと日付の設定

```bash
# ステータスを In Progress に設定（PR待ち状態）
gh project item-edit \
  --project-id PROJECT_GLOBAL_ID \
  --id ITEM_ID \
  --field-id STATUS_FIELD_ID \
  --single-select-option-id IN_PROGRESS_OPTION_ID

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

### 6. ブランチ作成

**重要**: コミットする前に、develop からフィーチャーブランチを作成します。

```bash
# develop に切り替え
git checkout develop 2>/dev/null || git checkout main
git pull

# フィーチャーブランチを作成
# ブランチ名: feature/<description>-<issue_number>
git checkout -b feature/docs-update-25

# 例:
# - feature/docs-update-25
# - feature/add-auth-system-42
# - feature/fix-login-bug-17
```

**ブランチ名の決め方**:
- Issueのタイトルや内容から簡潔な説明を抽出
- 英語の小文字とハイフンを使用
- 末尾にIssue番号を付ける

### 7. コミット（ファイル単位・機能単位で分割）

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

# 最後のコミットに Refs キーワードを含める（Issue参照用）
git add path/to/last-file.ext
git commit -m "🔧 chore: 設定ファイルの追加 (#ISSUE_NUMBER)

Refs #ISSUE_NUMBER

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**コミットの粒度**:
- 1ファイル = 1コミット（基本）
- 関連する変更はまとめてOK
- **すべてのコミットにIssue番号を付ける**（例: `#25`）
- **最後のコミットに `Refs #番号` を含める**（Issue参照用）

### 8. プッシュ

```bash
git push -u origin feature/<name>
```

### 9. PR 作成

**重要**: ここで終了します。マージは実行しません。

```bash
gh pr create --base develop \
  --title "タイトル" \
  --body "PRボディ"
```

**PRボディテンプレート**:

```markdown
## 概要

変更内容の概要を記述。

## 変更内容

- 変更1
- 変更2
- 変更3

## テスト

- [ ] テスト項目1
- [ ] テスト項目2

Refs #ISSUE_NUMBER

Co-Authored-By: Claude <noreply@anthropic.com>
```

**完了メッセージ**:

```bash
echo "✅ PRを作成しました: https://github.com/OWNER/REPO/pull/PR_NUMBER"
echo ""
echo "📝 次のステップ:"
echo "1. レビューを受けてください"
echo "2. レビュー後、手動でマージしてください:"
echo "   gh pr merge PR_NUMBER --merge"
echo "3. マージ後、ローカルのブランチを削除:"
echo "   git checkout develop && git pull"
echo "   git branch -d feature/<name>"
```

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

# 3. マイルストーンの取得・設定（あれば）
gh api /repos/OWNER/REPO/milestones

# 出力例にマイルストーンがある場合、アタッチ
# 例: v0.1.0（milestone: 1）をアタッチ
gh api --method PATCH /repos/OWNER/REPO/issues/25 -f milestone=1

# 4. プロジェクトに追加・ステータス設定
gh project item-add 2 --owner OWNER \
  --url "https://github.com/owner/repo/issues/25"

# ステータスを In Progress に（PR待ち状態）
gh project item-edit \
  --project-id PVT_kwXXX \
  --id PVTI_XXX \
  --field-id PVTSSF_XXX \
  --single-select-option-id 47fc9ee4  # In Progress

# 5. ブランチ作成
git checkout develop
git pull
git checkout -b feature/docs-update-25

# 6. ファイル単位でコミット（複数）

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

# docs/api.md（最後のコミットに Refs を含める）
git add docs/api.md
git commit -m "📚 docs(api): API仕様をv2.0.0に更新 (#25)

エンドポイントの追加と廃止を反映しました。

Refs #25

Co-Authored-By: Claude <noreply@anthropic.com>"

# 7. プッシュ
git push -u origin feature/docs-update-25

# 8. PR 作成
gh pr create --base develop \
  --title "📚 docs: ドキュメントの更新と整備" \
  --body "## 概要

ドキュメントを一括更新しました。

## 変更内容

- README.md: インストール手順を最新化
- CONTRIBUTING.md: 開発環境設定手順を追加
- docs/api.md: API仕様をv2.0.0に更新

## テスト

- [x] リンク切れの確認
- [x] 誤字脱字のチェック

Refs #25

Co-Authored-By: Claude <noreply@anthropic.com>"

# 出力: https://github.com/owner/repo/pull/30

# 9. 完了メッセージ
echo "✅ PRを作成しました: https://github.com/owner/repo/pull/30"
echo ""
echo "📝 次のステップ:"
echo "1. レビューを受けてください"
echo "2. レビュー後、手動でマージしてください:"
echo "   gh pr merge 30 --merge"
echo "3. マージ後、ローカルのブランチを削除:"
echo "   git checkout develop && git pull"
echo "   git branch -d feature/docs-update-25"
```

## 使用するタイミング

**reg-commit-pr を使うべき時:**
- レビューを受けたい変更
- チーム開発で他のメンバーの確認が必要
- PRを作成してから、後でマージしたい
- 変更の規模が大きく、慎重に進めたい

**reg-commit-flat を使うべき時:**
- 小さな変更で自信がある
- レビューが不要な変更
- ドキュメントの修正など
- すぐにマージして終わらせたい

## 注意点

1. **サブイシューは作成しない**: 単一のIssueのみ作成します
2. **コミットは細かく分ける**: ファイル単位・機能単位でコミットし、巻き戻しやすくします
3. **すべてのコミットにIssue番号を付ける**: Issue番号が判明していれば、すべてのコミットメッセージに `#番号` を付けてください（例: `#25`）
4. **Refs キーワードを使用**: `Refs #番号` を含めるとIssueへの参照が表示されます（自動クローズはされません）
5. **マージは実行しない**: PR作成で終了し、レビュー後に手動でマージしてください

## 詳細

このスキルは以下のモジュールを組み合わせたものです：

- [.claude/skills/analyze-diff/SKILL.md](../analyze-diff/SKILL.md) - 差分解析 → タスク分割
- [.claude/skills/project-mgmt/SKILL.md](../project-mgmt/SKILL.md) - プロジェクト追加・ステータス設定・日付設定
- [.claude/skills/repo-flow/SKILL.md](../repo-flow/SKILL.md) - ブランチ作成・コミット・プッシュ・PR作成

## 関連スキル

| スキル | 用途 |
|:------|:------|
| **reg-commit-flat** | PR作成 + マージまで自動で行うパターン |
| **reg-commit** | サブイシューごとにコミットするパターン（大規模変更用） |
| **reg-issue** | 計画からIssueを作成 + プロジェクトに登録（plan + project-mgmt） |
| **repo-flow** | Gitフロー（ブランチ作成・PR・マージ） |
| **repo-manager** | 全モジュールを組み合わせたタスク管理 |
