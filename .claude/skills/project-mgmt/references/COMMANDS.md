# GitHub Project Manager - コマンドリファレンス

このドキュメントでは、GitHub プロジェクト管理で使用するコマンドの詳細を説明します。

## 目次

1. [Issue 関連](#issue-関連)
2. [ラベル関連](#ラベル関連)
3. [プロジェクト関連](#プロジェクト関連)
4. [マイルストーン関連](#マイルストーン関連)
5. [日付設定](#日付設定)
6. [ステータス変更](#ステータス変更)

---

## Issue 関連

### Issue 作成

```bash
gh issue create --title "タイトル" --body "本文" --label "label1,label2"
```

**オプション:**
- `--title`: Issue のタイトル
- `--body`: Issue の本文（Markdown 可）
- `--label`: カンマ区切りでラベルを指定

**例:**
```bash
gh issue create \
  --title "テスト Issue 1: スキル機能の改善" \
  --body "## 概要\n\nAgent ZERO のスキル機能を改善する。" \
  --label "enhancement,good first issue"
```

### Issue 編集

```bash
gh issue edit ISSUE番号 --add-label "label1,label2"
```

**例:**
```bash
# ラベル追加
gh issue edit 7 --add-label "test"

# マイルストーン設定（API 使用）
gh api --method PATCH /repos/OWNER/REPO/issues/7 -f milestone=1
```

---

## ラベル関連

### ラベル作成

```bash
gh label create ラベル名 --color "#カラー" --description "説明"
```

**オプション:**
- `--color`: カラーコード（16進数、先頭の `#` 必須）
- `--description`: ラベルの説明

**例:**
```bash
gh label create test --color "#bfd4f2" --description "Test issue or pull request"
gh label create automation --color "#0052cc" --description "Automation related issues"
```

### ラベル一覧

```bash
gh label list
```

---

## プロジェクト関連

### プロジェクト一覧

```bash
gh project list --owner OWNER
```

**例:**
```bash
gh project list --owner Sunwood-ai-labs
# 出力: 11    Agent-ZERO    open    PVT_kwHOBnsxLs4BMiC9
```

### プロジェクト ID の動的取得

```bash
# プロジェクト名から ID を取得（jq 使用）
PROJECT_ID=$(gh project list --owner $OWNER --format json | jq -r ".[] | select(.title == \"$PROJECT_NAME\") | .number")

# プロジェクトグローバルID の取得
PROJECT_GLOBAL_ID=$(gh project view $PROJECT_ID --owner $OWNER --format json | jq -r ".id")
```

**例:**
```bash
OWNER="Sunwood-ai-labs"
PROJECT_NAME="Agent-ZERO"

PROJECT_ID=$(gh project list --owner $OWNER --format json | jq -r ".[] | select(.title == \"$PROJECT_NAME\") | .number")
# 出力: 11

PROJECT_GLOBAL_ID=$(gh project view $PROJECT_ID --owner $OWNER --format json | jq -r ".id")
# 出力: PVT_kwHOBnsxLs4BMiC9
```

### プロジェクトに Item 追加

```bash
gh project item-add PROJECT番号 --url "IssueのURL" --owner OWNER
```

**例:**
```bash
gh project item-add 11 \
  --url "https://github.com/Sunwood-ai-labs/zero-cc/issues/7" \
  --owner Sunwood-ai-labs
```

### プロジェクト Item 一覧

```bash
gh project item-list PROJECT番号 --owner OWNER --format json
```

---

## マイルストーン関連

### マイルストーン作成

**注意:** `gh` に `milestone` サブコマンドがないため、API を使用します。

```bash
gh api --method POST /repos/OWNER/REPO/milestones \
  -f title="バージョン" \
  -f description="説明" \
  -f state="open"
```

**例:**
```bash
gh api --method POST /repos/Sunwood-ai-labs/zero-cc/milestones \
  -f title="v0.1.0" \
  -f description="MVP リリース" \
  -f state="open"
```

### マイルストーン一覧

```bash
gh api /repos/OWNER/REPO/milestones
```

### Issue にマイルストーン紐付け

```bash
gh api --method PATCH /repos/OWNER/REPO/issues/ISSUE番号 -f milestone=MILESTONE_ID
```

**例:**
```bash
gh api --method PATCH /repos/Sunwood-ai-labs/zero-cc/issues/7 -f milestone=1
```

---

## 日付設定

### 日付フィールド作成

```bash
gh project field-create PROJECT番号 --owner OWNER --name "フィールド名" --data-type DATE
```

**例:**
```bash
# 開始日フィールド
gh project field-create 11 --owner Sunwood-ai-labs --name "開始日" --data-type DATE

# 終了日フィールド
gh project field-create 11 --owner Sunwood-ai-labs --name "終了日" --data-type DATE
```

### フィールド一覧

```bash
gh project field-list PROJECT番号 --owner OWNER
```

**出力例:**
```
Title    ProjectV2Field    PVTF_lAHOBnsxLs4BMiC9zg7yZ1M
...
開始日    ProjectV2Field    PVTF_lAHOBnsxLs4BMiC9zg71LEA
終了日    ProjectV2Field    PVTF_lAHOBnsxLs4BMiC9zg71LFU
```

### 日付設定

```bash
# フィールドIDを取得
START_DATE_FIELD_ID=$(gh project field-list $PROJECT_ID --owner $OWNER | grep "開始日" | awk '{print $3}')
END_DATE_FIELD_ID=$(gh project field-list $PROJECT_ID --owner $OWNER | grep "終了日" | awk '{print $3}')

# 日付設定（変数を使用）
gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID \
  --field-id $START_DATE_FIELD_ID \
  --date "YYYY-MM-DD"
```

**重要:**
- `--project-id`: グローバルID（`PVT_...`）
- `--id`: アイテムID（`PVTI_...`）
- `--field-id`: フィールドID（`PVTF_...`）

**例:**
```bash
# Issue #7 に開始日を設定
ITEM_ID=$(gh project item-list $PROJECT_ID --owner $OWNER --format json | jq -r ".[] | select(.content.number == 7) | .id")

gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID \
  --field-id $START_DATE_FIELD_ID \
  --date "2026-01-15"
```

---

## ステータス変更

### ステータスフィールド情報取得（GraphQL + jq）

```bash
# ステータス情報を取得（GraphQL）
STATUS_INFO=$(gh api graphql -f query="
query {
  node(id: \"$PROJECT_GLOBAL_ID\") {
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
}")

# jq で各IDを抽出
STATUS_FIELD_ID=$(echo "$STATUS_INFO" | jq -r '.data.node.fields.nodes[] | select(.name == "Status") | .id')
TODO_OPTION_ID=$(echo "$STATUS_INFO" | jq -r '.data.node.fields.nodes[] | select(.name == "Status") | .options[] | select(.name == "Todo") | .id')
IN_PROGRESS_OPTION_ID=$(echo "$STATUS_INFO" | jq -r '.data.node.fields.nodes[] | select(.name == "Status") | .options[] | select(.name == "In Progress") | .id')
DONE_OPTION_ID=$(echo "$STATUS_INFO" | jq -r '.data.node.fields.nodes[] | select(.name == "Status") | .options[] | select(.name == "Done") | .id')
```

**出力例:**
```bash
echo "Status Field ID: $STATUS_FIELD_ID"
# 出力: Status Field ID: PVTSSF_lAHOBnsxLs4BMiC9zg7yZ1U

echo "Todo: $TODO_OPTION_ID"
# 出力: Todo: f75ad846

echo "In Progress: $IN_PROGRESS_OPTION_ID"
# 出力: In Progress: 47fc9ee4

echo "Done: $DONE_OPTION_ID"
# 出力: Done: 98236657
```

### ステータス変更

```bash
gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID \
  --field-id $STATUS_FIELD_ID \
  --single-select-option-id $IN_PROGRESS_OPTION_ID
```

**例:**
```bash
# Issue #7 を In Progress に変更
ITEM_ID=$(gh project item-list $PROJECT_ID --owner $OWNER --format json | jq -r ".[] | select(.content.number == 7) | .id")

gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID \
  --field-id $STATUS_FIELD_ID \
  --single-select-option-id $IN_PROGRESS_OPTION_ID
```

---

## ID の種類と取得方法（jq 使用）

| ID 種類 | 形式 | 取得コマンド（jq 使用） |
|---------|------|------------------------|
| プロジェクト ローカルID | 数字（例: `11`） | `gh project list --owner OWNER --format json \| jq -r ".[] \| select(.title == \"NAME\") \| .number"` |
| プロジェクト グローバルID | `PVT_...` | `gh project view 番号 --format json \| jq -r ".id"` |
| アイテムID | `PVTI_...` | `gh project item-list 番号 --format json \| jq -r ".[] \| select(.content.number == 7) \| .id"` |
| フィールドID | `PVTF_...` | `gh project field-list 番号 --owner OWNER \| grep "名前" \| awk '{print $3}'` |
| ステータスフィールドID | `PVTSSF_...` | GraphQL + `jq -r '.data.node.fields.nodes[] \| select(.name == "Status") \| .id'` |
| ステータスオプションID | 16進数（例: `47fc9ee4`） | GraphQL + `jq -r '.data.node.fields.nodes[] \| select(.name == "Status") \| .options[] \| select(.name == "In Progress") \| .id'` |

**重要:** JSON パースには `grep` や `awk` ではなく、必ず `jq` を使用してください。
