---
name: plan
description: |
  タスク分割してIssue作成・親子関係設定。
  トリガー例: 「/plan ユーザー認証機能を追加して」
allowed-tools: Bash, Glob, Grep, Read, AskUserQuestion
arguments: auto-detect
user-invocable: true
---

# Plan

ユーザーからの要望やアイデアをタスク分割して、Issueを作成し、親子関係を設定します。

## 前提条件

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み
- サブイシュー機能が有効化されている（Organization設定）

## 除外条件

**プライベートリポジトリの場合は、このフローを実行しません。**

```bash
# リポジトリの可視性を確認
gh repo view --json visibility,owner,name
# visibility: "PRIVATE" の場合はスキップ
```

## ワークフロー

### 1. リクエスト解析

ユーザーからのリクエスト（`$ARGUMENTS`）を解析:

- 実現したい機能は何か？
- どのような問題を解決したいか？
- 優先順位は？

### 2. リポジトリの決定

```bash
# 現在のリポジトリを確認
git remote get-url origin
```

### 3. タスク分割

リクエストを具体的なタスクに分割:

1. **大まかなタスクを抽出**: リクエストの目的を達成するための主要なステップ
2. **各タスクを詳細化**: それぞれのタスクをさらに小さなサブタスクに
3. **優先順位付け**: 依存関係を考慮して順序を決定

### 4. Issue 作成（親子構造）

親Issueを作成し、各タスクをサブイシューとして作成:

```bash
# 1. 親Issueの作成
PARENT_URL=$(gh issue create \
  --title "【親タイトル】概要" \
  --body "## 概要\n\n全体の説明\n\n## サブイシュー\n\n各カテゴリの詳細はサブイシューを参照" \
  --label "enhancement" \
  --jq '.url')

# Issue番号を抽出
PARENT_NUMBER=$(echo "$PARENT_URL" | grep -oE '[0-9]+$')

# 2. サブイシューの作成
gh issue create \
  --title "[Sub-1] サブタスク1" \
  --body "## 概要\n\n詳細説明\n\n## 親Issue\n\n#$PARENT_NUMBER" \
  --label "enhancement"

# 同様に Sub-2, Sub-3... を作成
```

### 5. 親子関係の設定

**重要: `sub_issue_id` には Issue番号ではなく `databaseId` を使用します。**

```bash
# 1. 各サブイシューの databaseId を取得（GraphQL）
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: SUB_ISSUE_NUMBER) {
      databaseId
    }
  }
}'

# 2. サブイシューを親Issueに追加（REST API）
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/OWNER/REPO/issues/PARENT_NUMBER/sub_issues" \
  -d "{\"sub_issue_id\":DATABASE_ID}"

# または GUI で設定:
# - 各サブイシューを開く
# - 右側の「Parent issue」で親Issueを選択
```

### 6. 結果を出力

作成したIssueの情報を出力:

```bash
echo "親Issue: #$PARENT_NUMBER"
echo "サブイシュー: #$SUB1_NUMBER, #$SUB2_NUMBER, ..."
```

## Issue テンプレート

```markdown
## 概要

[タスクの概要説明]

## 背景・目的

[なぜこのタスクが必要なのか]

## タスク

- [ ] サブタスク1
- [ ] サブタスク2
- [ ] サブタスク3

## 受入条件

- [ ] 条件1
- [ ] 条件2

## 関連リンク

- 関連 Issue: #
- 関連 PR: #
- ドキュメント:
```

## 使用例

```
ユーザー: 「/plan ユーザー認証機能を追加して」

スキル:
1. 要望のヒアリング
2. タスク分割:
   - 親Issue: ユーザー認証機能の実装
   - Sub-1: JWTモジュールの実装
   - Sub-2: ログインエンドポイントの実装
   - Sub-3: ログアウトエンドポイントの実装
3. 親Issue & サブイシューを作成
4. 親子関係を設定
5. 結果を出力
```

## 注意点

1. **プライベートリポジトリ**: このフローを実行せず、通常の開発モードで作業
2. **サブイシュー**: `sub_issue_id` には Issue番号ではなく `databaseId` を使用する
3. **サブイシュー機能**: Organizationで有効化されている必要がある
4. **タスク粒度**: サブイシューは 1-2 日で完了できる粒度に分割

## 関連スキル

| スキル | 用途 |
|:------|:------|
| **project-mgmt** | プロジェクト追加・ステータス設定・日付設定 |
| **repo-flow** | ブランチ作成・コミット・プッシュ・PR・マージ |
| **issue** | plan + project-mgmt を組み合わせたスキル |
| **repo-manager** | 全モジュールを組み合わせたスキル |
