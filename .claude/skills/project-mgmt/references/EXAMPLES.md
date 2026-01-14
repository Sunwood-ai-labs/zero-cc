# GitHub Project Manager - 使用例

このドキュメントでは、GitHub プロジェクト管理の実際の使用例を紹介します。

## 目次

1. [基本フロー: Issue 作成からプロジェクト登録まで](#基本フロー-issue-作成からプロジェクト登録まで)
2. [ラベル作成と追加](#ラベル作成と追加)
3. [マイルストーン設定](#マイルストーン設定)
4. [日付設定](#日付設定)
5. [ステータス変更](#ステータス変更)
6. [一括操作例](#一括操作例)

---

## 基本フロー: Issue 作成からプロジェクト登録まで

### シナリオ
新しい Issue を作成し、既存のプロジェクトに登録する。

### 手順

**1. リポジトリ情報の確認**
```bash
gh repo view --json name,owner
# 出力: {"name":"zero-cc","owner":{"login":"Sunwood-ai-labs"}}
```

**2. Issue 作成**
```bash
gh issue create \
  --title "テスト Issue 1: スキル機能の改善" \
  --body "## 概要

Agent ZERO のスキル機能を改善するためのテスト Issue。

## タスク

- [ ] スキルの自動生成機能を見直す
- [ ] ドキュメントを更新する
- [ ] テストを追加する" \
  --label "enhancement,good first issue"

# 出力: https://github.com/Sunwood-ai-labs/zero-cc/issues/7
```

**3. プロジェクト一覧の確認**
```bash
gh project list --owner Sunwood-ai-labs
# 出力:
# 11    Agent-ZERO    open    PVT_kwHOBnsxLs4BMiC9
# 10    @Sunwood-ai-labs's untitled project    open    ...
```

**4. プロジェクトに追加**
```bash
gh project item-add 11 \
  --url "https://github.com/Sunwood-ai-labs/zero-cc/issues/7" \
  --owner Sunwood-ai-labs
```

---

## ラベル作成と追加

### シナリオ
既存のラベルを確認し、新しいラベルを作成して Issue に追加する。

### 手順

**1. 既存ラベルの確認**
```bash
gh label list
# 出力:
# bug              Something isn't working           #d73a4a
# documentation     Improvements or additions...     #0075ca
# enhancement      New feature or request            #a2eeef
# ...
```

**2. 新しいラベルの作成**
```bash
gh label create test --color "#bfd4f2" --description "Test issue or pull request"
gh label create automation --color "#0052cc" --description "Automation related issues"
```

**3. Issue にラベルを追加**
```bash
gh issue edit 7 --add-label "test"
gh issue edit 8 --add-label "automation,test"
```

---

## マイルストーン設定

### シナリオ
複数のマイルストーンを作成し、Issue に紐付ける。

### 手順

**1. 既存マイルストーンの確認**
```bash
gh api /repos/Sunwood-ai-labs/zero-cc/milestones
# 出力: [] （まだマイルストーンなし）
```

**2. マイルストーンの作成**
```bash
# v0.1.0
gh api --method POST /repos/Sunwood-ai-labs/zero-cc/milestones \
  -f title="v0.1.0" \
  -f description="MVP リリース" \
  -f state="open"

# v0.2.0
gh api --method POST /repos/Sunwood-ai-labs/zero-cc/milestones \
  -f title="v0.2.0" \
  -f description="機能拡張" \
  -f state="open"

# v1.0.0
gh api --method POST /repos/Sunwood-ai-labs/zero-cc/milestones \
  -f title="v1.0.0" \
  -f description="本リリース" \
  -f state="open"
```

**3. Issue にマイルストーンを紐付け**
```bash
# Issue #7 に v0.1.0 を紐付け
gh api --method PATCH /repos/Sunwood-ai-labs/zero-cc/issues/7 -f milestone=1

# Issue #8 に v0.1.0 を紐付け
gh api --method PATCH /repos/Sunwood-ai-labs/zero-cc/issues/8 -f milestone=1
```

---

## 日付設定

### シナリオ
プロジェクトに日付フィールドを作成し、Issue に開始日と終了日を設定する。

### 手順

**1. 日付フィールドの作成**
```bash
gh project field-create 11 --owner Sunwood-ai-labs --name "開始日" --data-type DATE
gh project field-create 11 --owner Sunwood-ai-labs --name "終了日" --data-type DATE
```

**2. フィールド ID の確認**
```bash
gh project field-list 11 --owner Sunwood-ai-labs
# 出力:
# ...
# 開始日    ProjectV2Field    PVTF_lAHOBnsxLs4BMiC9zg71LEA
# 終了日    ProjectV2Field    PVTF_lAHOBnsxLs4BMiC9zg71LFU
```

**3. プロジェクトのグローバル ID を取得（jq 使用）**
```bash
PROJECT_ID=11
PROJECT_GLOBAL_ID=$(gh project view $PROJECT_ID --owner Sunwood-ai-labs --format json | jq -r ".id")
echo "$PROJECT_GLOBAL_ID"
# 出力: PVT_kwHOBnsxLs4BMiC9
```

**4. アイテム ID を取得（jq 使用）**
```bash
ITEM_ID=$(gh project item-list 11 --owner Sunwood-ai-labs --format json | jq -r ".[] | select(.content.number == 7) | .id")
echo "$ITEM_ID"
# 出力: PVTI_lAHOBnsxLs4BMiC9zgjpfng
```

**5. 日付を設定（変数を使用）**
```bash
# フィールドIDを取得
START_DATE_FIELD_ID=$(gh project field-list 11 --owner Sunwood-ai-labs | grep "開始日" | awk '{print $3}')
END_DATE_FIELD_ID=$(gh project field-list 11 --owner Sunwood-ai-labs | grep "終了日" | awk '{print $3}')

# Issue #7: 2026-01-15 〜 2026-01-20
ITEM_ID_7=$(gh project item-list 11 --owner Sunwood-ai-labs --format json | jq -r ".[] | select(.content.number == 7) | .id")

gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID_7 \
  --field-id $START_DATE_FIELD_ID \
  --date "2026-01-15"

gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID_7 \
  --field-id $END_DATE_FIELD_ID \
  --date "2026-01-20"

# Issue #8: 2026-01-18 〜 2026-01-25
ITEM_ID_8=$(gh project item-list 11 --owner Sunwood-ai-labs --format json | jq -r ".[] | select(.content.number == 8) | .id")

gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID_8 \
  --field-id $START_DATE_FIELD_ID \
  --date "2026-01-18"

gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID_8 \
  --field-id $END_DATE_FIELD_ID \
  --date "2026-01-25"
```

---

## ステータス変更

### シナリオ
Issue のステータスを「Todo」→「In Progress」→「Done」に変更する。

### 手順

**1. ステータスフィールドのオプションを取得（GraphQL + jq）**
```bash
# ステータス情報を取得
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

echo "Status Field ID: $STATUS_FIELD_ID"
echo "Todo: $TODO_OPTION_ID"
echo "In Progress: $IN_PROGRESS_OPTION_ID"
echo "Done: $DONE_OPTION_ID"
```

**出力:**
```
Status Field ID: PVTSSF_lAHOBnsxLs4BMiC9zg7yZ1U
Todo: f75ad846
In Progress: 47fc9ee4
Done: 98236657
```

**2. ステータスを In Progress に変更（変数を使用）**
```bash
# Issue #7
gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID_7 \
  --field-id $STATUS_FIELD_ID \
  --single-select-option-id $IN_PROGRESS_OPTION_ID

# Issue #8
gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID_8 \
  --field-id $STATUS_FIELD_ID \
  --single-select-option-id $IN_PROGRESS_OPTION_ID
```

**3. ステータスを Done に変更（変数を使用）**
```bash
# Issue #7
gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID_7 \
  --field-id $STATUS_FIELD_ID \
  --single-select-option-id $DONE_OPTION_ID

# Issue #8
gh project item-edit \
  --project-id $PROJECT_GLOBAL_ID \
  --id $ITEM_ID_8 \
  --field-id $STATUS_FIELD_ID \
  --single-select-option-id $DONE_OPTION_ID
```

---

## 一括操作例

### シナリオ
複数の Issue を一括で作成し、プロジェクトに登録する。

### シェルスクリプト例

```bash
#!/bin/bash

OWNER="Sunwood-ai-labs"
REPO="zero-cc"
PROJECT_ID=11

# Issue 作成とプロジェクト登録
issue_urls=()

# Issue 1
url1=$(gh issue create \
  --title "テスト Issue 1: スキル機能の改善" \
  --body "## 概要\n\nスキル機能を改善する。" \
  --label "enhancement,test")
issue_urls+=("$url1")

# Issue 2
url2=$(gh issue create \
  --title "テスト Issue 2: リポジトリ管理の自動化" \
  --body "## 概要\n\nリポジトリ管理を自動化する。" \
  --label "automation,test")
issue_urls+=("$url2")

# プロジェクトに追加
for url in "${issue_urls[@]}"; do
  gh project item-add $PROJECT_ID --url "$url" --owner $OWNER
done

echo "作成された Issues:"
for url in "${issue_urls[@]}"; do
  echo "  $url"
done
```

---

## 結果

以上の手順を実行すると、以下のような状態になります:

| 項目 | 値 |
|------|-----|
| Issue | #7, #8 |
| ラベル | enhancement, test, automation, documentation |
| プロジェクト | Agent-ZERO (#11) |
| マイルストーン | v0.1.0 |
| 開始日・終了日 | 設定済み |
| ステータス | Done |

GitHub で確認:
- Issue: https://github.com/Sunwood-ai-labs/zero-cc/issues
- プロジェクト: https://github.com/users/Sunwood-ai-labs/projects/11
- マイルストーン: https://github.com/Sunwood-ai-labs/zero-cc/milestone/1
