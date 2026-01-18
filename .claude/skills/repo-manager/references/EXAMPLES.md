# Repo Manager 使用例

## 差分からタスク登録（完全実例）

ユーザー指示: 「https://github.com/orgs/Sunwood-AI-OSS-Hub/projects/2/views/1 のプロジェクトに差分からタスクを登録して」

### Step 1: 差分分析

```bash
# 現在の差分を確認
git status
git diff --stat

# 変更の詳細を確認
git diff .github/workflows/CLAUDE_GLM_DEV.yml
```

出力例:
```
 .github/workflows/CLAUDE_GLM_DEV.yml | 58 ++++++++++++++++++++++++++----------
 LICENSE                              |  0
 README.md                            |  0
 assets/header.svg                    |  0
 4 files changed, 42 insertions(+), 16 deletions(-)
```

### Step 2: タスク分割

差分から以下のタスクを抽出:

1. **GitHub Actionsワークフローの改善** - `CLAUDE_GLM_DEV.yml` の改善
2. **開発環境ファイルの追加** - `.env.example`, `.gitignore`
3. **ユーティリティスクリプトの追加** - `scripts/sync-*.sh`
4. **ワークフローの整理** - `disabled/` への移動

### Step 3: 親Issueの作成

```bash
gh issue create \
  --title "【開発環境整備】claude-glm-actions-lab の改善とユーティリティ追加" \
  --body "## 概要

GitHub Actionsワークフローの改善、開発環境ファイルの追加、ユーティリティスクリプトの追加を行う。

## 背景・目的

Claude Code + GLM の開発環境を改善し、チーム開発を効率化する。

## タスク

- [ ] GitHub Actionsワークフローの改善
- [ ] 開発環境ファイルの追加（.env.example, .gitignore）
- [ ] ユーティリティスクリプトの追加
- [ ] ワークフローの整理（無効化済みファイルの移動）

## サブイシュー

各カテゴリの詳細はサブイシューを参照。

## 関連リンク

- リポジトリ: https://github.com/Sunwood-AI-OSS-Hub/claude-glm-actions-lab" \
  --label "enhancement"
```

出力: `https://github.com/Sunwood-AI-OSS-Hub/claude-glm-actions-lab/issues/3`

### Step 4: サブイシューの作成

```bash
# Sub-1
gh issue create \
  --title "[Sub-1] GitHub Actionsワークフローの改善" \
  --body "## 概要

CLAUDE_GLM_DEV.yml ワークフローを改善し、並列実行制御とトリガー条件を最適化する。

## 親Issue

#3" \
  --label "enhancement"

# Sub-2, Sub-3, Sub-4 も同様に...
```

### Step 5: プロジェクト情報の取得

```bash
# プロジェクト情報を取得
gh project view 2 --owner Sunwood-AI-OSS-Hub --format json
```

出力例:
```json
{
  "id": "PVT_kwDODzy5ic4BM3lE",
  "number": 2,
  "title": "Sunwood AI OSS Hub Kanban"
}
```

### Step 6: プロジェクトへの追加

```bash
# 親Issueとサブイシューをプロジェクトに追加
for issue in 3 4 5 6 7; do
  gh project item-add 2 --owner Sunwood-AI-OSS-Hub \
    --url "https://github.com/Sunwood-AI-OSS-Hub/claude-glm-actions-lab/issues/$issue"
done
```

### Step 7: ステータスオプションの取得

```bash
gh api graphql -f query='
query($project: ID!) {
  node(id: $project) {
    ... on ProjectV2 {
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}
' -f project='PVT_kwDODzy5ic4BM3lE'
```

出力例:
```json
{
  "name": "Status",
  "options": [
    {"id": "f75ad846", "name": "Backlog"},
    {"id": "61e4505c", "name": "Ready"},
    {"id": "47fc9ee4", "name": "In progress"},
    {"id": "df73e18b", "name": "In review"},
    {"id": "98236657", "name": "Done"}
  ]
}
```

### Step 8: 親子関係の設定（CLI）

**重要: Issue番号ではなく `databaseId` を使用します。**

```bash
# 1. 各サブイシューの databaseId を取得
gh api graphql -f query='
query {
  repository(owner: "Sunwood-AI-OSS-Hub", name: "claude-glm-actions-lab") {
    issue(number: 4) {
      databaseId
    }
    issue2: issue(number: 5) {
      databaseId
    }
    issue3: issue(number: 6) {
      databaseId
    }
    issue4: issue(number: 7) {
      databaseId
    }
  }
}
'
```

出力例:
```json
{
  "issue": {"databaseId": 3826534320},
  "issue2": {"databaseId": 3826534952},
  "issue3": {"databaseId": 3826535083},
  "issue4": {"databaseId": 3826535150}
}
```

```bash
# 2. サブイシューを親Issueに追加（REST API）
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/Sunwood-AI-OSS-Hub/claude-glm-actions-lab/issues/3/sub_issues" \
  -d '{"sub_issue_id":3826534320}'

# 他のサブイシューも同様に...
```

または、GUIで設定:
- 各サブイシューを開く
- 右側の「Parent issue」で親Issue #3 を選択

### Step 9: ステータスと日付の設定

```bash
# 親Issueを In Progress に
gh project item-edit \
  --project-id PVT_kwDODzy5ic4BM3lE \
  --id PVTI_lADODzy5ic4BM3lEzgj1X_M \
  --field-id PVTSSF_lADODzy5ic4BM3lEzg8BzGw \
  --single-select-option-id 47fc9ee4

# サブイシューを Done に（既に完了している場合）
for id in PVTI_lADODzy5ic4BM3lEzgj1X_U PVTI_lADODzy5ic4BM3lEzgj1X_c PVTI_lADODzy5ic4BM3lEzgj1X_o PVTI_lADODzy5ic4BM3lEzgj1X_4; do
  gh project item-edit \
    --project-id PVT_kwDODzy5ic4BM3lE \
    --id "$id" \
    --field-id PVTSSF_lADODzy5ic4BM3lEzg8BzGw \
    --single-select-option-id 98236657
done

# 日付を設定
gh project item-edit \
  --project-id PVT_kwDODzy5ic4BM3lE \
  --id PVTI_lADODzy5ic4BM3lEzgj1X_M \
  --field-id PVTF_lADODzy5ic4BM3lEzg8BzIw \
  --date "2026-01-18"

gh project item-edit \
  --project-id PVT_kwDODzy5ic4BM3lE \
  --id PVTI_lADODzy5ic4BM3lEzgj1X_M \
  --field-id PVTF_lADODzy5ic4BM3lEzg8BzI0 \
  --date "2026-01-25"
```

### Step 10: コミット＆プッシュ

```bash
# 変更をステージング
git add -A

# Issue番号を含めてコミット（自動クローズ）
git commit -m "feat: 開発環境整備 - GitHub Actions改善とユーティリティ追加

- GitHub Actionsワークフローの改善 (#4)
  - 並列実行制御の追加
  - @claudeトリガー条件の最適化
  - ブランチ名固定化による競合回避
  - GLM API設定の整理

- 開発環境ファイルの追加 (#5)
  - .env.example の追加
  - .gitignore の追加

- ユーティリティスクリプトの追加 (#6)
  - sync-repo.sh: リポジトリ同期スクリプト
  - sync-secrets.sh: シークレット同期スクリプト
  - sync-workflows.sh: ワークフロー同期スクリプト

- ワークフローの整理 (#7)
  - disabled/ ディレクトリの作成
  - MINIMAL.yml の移動

Closes #3, #4, #5, #6, #7

Co-Authored-By: Claude <noreply@anthropic.com>"

# プッシュ
git push origin main
```

### 結果確認

```bash
# Issueがクローズされたか確認
gh api graphql -f query='
query {
  repository(owner: "Sunwood-AI-OSS-Hub", name: "claude-glm-actions-lab") {
    issue(number: 3) {
      number
      state
      title
      subIssues(first: 10) {
        nodes {
          number
          state
          title
        }
      }
    }
  }
}
'
```

出力例:
```json
{
  "issue": {
    "number": 3,
    "state": "CLOSED",
    "title": "【開発環境整備】claude-glm-actions-lab の改善とユーティリティ追加",
    "subIssues": {
      "nodes": [
        {"number": 7, "state": "CLOSED", "title": "[Sub-4] ワークフローの整理"},
        {"number": 4, "state": "CLOSED", "title": "[Sub-1] GitHub Actionsワークフローの改善"},
        {"number": 5, "state": "CLOSED", "title": "[Sub-2] 開発環境ファイルの追加"},
        {"number": 6, "state": "CLOSED", "title": "[Sub-3] ユーティリティスクリプトの追加"}
      ]
    }
  }
}
```

## よくあるエラーと解決策

### エラー1: "The provided sub-issue does not exist"

**原因**: `sub_issue_id` に Issue番号を指定している

**解決策**: `databaseId` を使用する

```bash
# 間違い
-d '{"sub_issue_id":4}'

# 正しい
-d '{"sub_issue_id":3826534320}'
```

### エラー2: "Invalid request. is not of type integer"

**原因**: `sub_issue_id` が文字列として扱われている

**解決策**: curl で JSON を正しく送信する

```bash
# 正しい例
curl -L -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $(gh auth token)" \
  "https://api.github.com/repos/OWNER/REPO/issues/PARENT/sub_issues" \
  -d "{\"sub_issue_id\":$DATABASE_ID}"  # シェル変数展開で数値化
```

### エラー3: プロジェクトが見つからない

**原因**: プロジェクトIDまたは所有者が間違っている

**解決策**: プロジェクト一覧を確認

```bash
gh project list --owner OWNER
```
