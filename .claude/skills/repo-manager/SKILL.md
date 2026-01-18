---
name: repo-manager
description: |
  ユーザーからのリクエストをタスク分割して Issue 登録・プロジェクト管理・進捗報告。
  トリガー例: 「差分からタスク登録して」「計画をIssueにして」「タスク管理」「実行して」「repo-manager」
allowed-tools: Bash, Glob, Grep, Read, AskUserQuestion
arguments: auto-detect
user-invocable: true
---

# Repo Manager

ユーザーからのリクエストをタスク分割して Issue 登録・プロジェクト管理・親子関係設定・進捗報告します。

**モジュール構成**: `plan` + `analyze-diff` + `project-mgmt` + `repo-flow`

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

## 省略オプション

何回も使う場合、プロジェクトURLを毎回指定するのは手間です。以下の省略方法が利用できます。

### デフォルトプロジェクト

プロジェクトURLを省略した場合、現在のリポジトリのデフォルトプロジェクトを使用します。

```bash
# 環境変数でデフォルトプロジェクトを設定
export REPO_MANAGER_DEFAULT_PROJECT="orgs/Sunwood-AI-OSS-Hub/projects/2"

# 省略形の呼び出し
/repo-manager ユーザー認証機能を追加して
```

### 短いエイリアス

よく使うパターンには短いエイリアスを用意しています。

```bash
/reg-issue    # 計画からIssueを作成 + プロジェクトに登録（plan + project-mgmt）
/plan         # 計画からIssueを作成（Issue作成のみ）
/reg-commit   # 差分からIssueを作成 + プロジェクトに登録 + コミット＆プッシュ（analyze-diff + plan + project-mgmt + repo-flow）
/task         # タスク管理（repo-managerのエイリアス）
```

### 使用例

```
# 完全指定
ユーザー: 「https://github.com/orgs/Sunwood-AI-OSS-Hub/projects/2/views/1 に、ユーザー認証機能を追加して」

# 省略形（デフォルトプロジェクトを使用）
ユーザー: 「/reg-issue ユーザー認証機能を追加して」

# さらに省略
ユーザー: 「ユーザー認証機能」
```

## ワークフロー

### パターン1: 計画からタスク登録

アイデア/要望があって、まだ実装していないタスクをIssueとして登録したい場合のフロー。

**フロー**: `plan` → `project-mgmt`

```
┌─────────────────────────────────────────────────────────────┐
│  1. plan モジュール                                           │
│     - 要望のヒアリング                                          │
│     - タスク分割                                               │
│     - Issue 作成（親子構造）                                   │
│     - 親子関係の設定                                           │
├─────────────────────────────────────────────────────────────┤
│  2. project-mgmt モジュール                                    │
│     - プロジェクトへの追加                                     │
│     - ステータス設定（Todo）                                   │
│     - 日付設定                                                 │
└─────────────────────────────────────────────────────────────┘
```

**実行手順**:

1. **plan スキルを呼び出す**
   - `/plan` スキルでタスク分割とIssue作成を実行
   - 親Issueとサブイシューが作成される

2. **project-mgmt スキルを呼び出す**
   - 作成したIssueをプロジェクトに追加
   - ステータスを「Todo」に設定
   - 開始日と終了日を設定

### パターン2: 差分からタスク登録

既にコードを書いていて、その変更をIssueとして登録し、コミット＆プッシュまで行う場合のフロー。

**フロー**: `analyze-diff` → `plan` → `project-mgmt` → `repo-flow`

```
┌─────────────────────────────────────────────────────────────┐
│  1. analyze-diff モジュール                                   │
│     - 現在の差分を解析（git status, git diff）                │
│     - タスク分割案の作成                                       │
├─────────────────────────────────────────────────────────────┤
│  2. plan モジュール                                           │
│     - タスク分割                                               │
│     - Issue 作成（親子構造）                                   │
│     - 親子関係の設定                                           │
├─────────────────────────────────────────────────────────────┤
│  3. project-mgmt モジュール                                    │
│     - プロジェクトへの追加                                     │
│     - ステータス設定（Done）                                   │
│     - 日付設定                                                 │
├─────────────────────────────────────────────────────────────┤
│  4. repo-flow モジュール                                      │
│     - ブランチ作成                                             │
│     - コミット（Issue番号を含める）                            │
│     - プッシュ                                                 │
│     - PR 作成                                                 │
│     - develop へマージ                                        │
│     - クリーンアップ                                           │
└─────────────────────────────────────────────────────────────┘
```

**実行手順**:

1. **analyze-diff スキルを呼び出す**
   - `/diff` スキルで現在の差分を解析
   - タスク分割案を作成

2. **plan スキルを呼び出す**
   - タスク分割案に基づいてIssueを作成
   - 親子関係を設定

3. **project-mgmt スキルを呼び出す**
   - 作成したIssueをプロジェクトに追加
   - ステータスを「Done」に設定
   - 開始日と終了日を設定

4. **repo-flow スキルを呼び出す**
   - `/repo-flow` スキルでコミット＆プッシュ
   - Issue番号を含めてコミット（自動クローズ）
   - PR作成、developへのマージ、クリーンアップ

## 使用例

### 計画からタスク登録（パターン1）

```
ユーザー: 「https://github.com/orgs/Sunwood-AI-OSS-Hub/projects/2/views/1 に、次の計画をIssueとして登録して：
- ユーザー認証機能の追加
- 管理者ダッシュボードの作成
- APIドキュメントの整備」

スキル:
1. /plan スキルを呼び出し:
   - タスク分割（親Issue + サブイシュー）
   - 親Issueを作成
   - 各サブイシューを作成
   - 親子関係を設定

2. /project-mgmt スキルを呼び出し:
   - プロジェクトに追加
   - ステータスを Todo に設定
   - 日付を設定
```

### 差分からタスク登録（パターン2）

```
ユーザー: 「https://github.com/orgs/Sunwood-AI-OSS-Hub/projects/2/views/1 のプロジェクトに差分からタスクを登録して」

スキル:
1. /diff スキルを呼び出し（analyze-diff）:
   - 現在の差分を解析（git status, git diff）

2. /plan スキルを呼び出し:
   - タスク分割（親Issue + サブイシュー）
   - 親Issueを作成
   - 各サブイシューを作成
   - 親子関係を設定

3. /project-mgmt スキルを呼び出し:
   - プロジェクトに追加
   - ステータスと日付を設定

4. /repo-flow スキルを呼び出し:
   - コミット（Issue番号を含めて）
   - プッシュ
   - PR作成
   - developへのマージ
   - クリーンアップ
```

### 基本的な使用例

```
ユーザー: 「GitHub Actions のワークフローを設定して」

スキル:
1. /plan スキルを呼び出し:
   - タスク分割:
     - 親Issue: CI/CD環境の構築
     - Sub-1: GitHub Actions の基本設定
     - Sub-2: CI/CD パイプラインの構築
     - Sub-3: テスト自動化の追加
   - 親Issue & サブイシューを作成
   - 親子関係を設定

2. /project-mgmt スキルを呼び出し:
   - プロジェクトに追加
   - ステータス設定（Todo）
   - 日付設定（開始日・終了日）
```

## モジュール詳細

各モジュールの詳細は以下を参照してください：

| モジュール | 説明 | ドキュメント |
|:---------|:-----|:------------|
| **plan** | タスク分割 → Issue作成 → 親子関係設定 | [.claude/skills/plan/SKILL.md](../plan/SKILL.md) |
| **analyze-diff** | 差分解析 → タスク分割 | [.claude/skills/analyze-diff/SKILL.md](../analyze-diff/SKILL.md) |
| **project-mgmt** | プロジェクト追加・ステータス設定・日付設定 | [.claude/skills/project-mgmt/SKILL.md](../project-mgmt/SKILL.md) |
| **repo-flow** | ブランチ作成・コミット・プッシュ・PR・マージ | [.claude/skills/repo-flow/SKILL.md](../repo-flow/SKILL.md) |

## ステータス遷移

```
Todo → In Progress → Done
  ↑         │
  └─────────┘
      (中断時)
```

## 注意点

1. **プライベートリポジトリ**: このフローを実行せず、通常の開発モードで作業
2. **プロジェクトID**: 固定IDに依存せず、動的に取得する
3. **サブイシュー**: `sub_issue_id` には Issue番号ではなく `databaseId` を使用する
4. **サブイシュー機能**: Organizationで有効化されている必要がある
5. **タスク粒度**: サブイシューは 1-2 日で完了できる粒度に分割
6. **日付設定**: Issue 作成後、必ず開始日と終了日を設定すること（YYYY-MM-DD形式）
7. **コミットメッセージ**: `Closes #番号` を含めると自動的にIssueがクローズされる

## 参照

詳細な使用例とトラブルシューティング:

- [references/EXAMPLES.md](references/EXAMPLES.md) - 完全実例とエラー解決策

GitHub プロジェクト管理のコマンド詳細は **`project-mgmt`** スキルを参照してください:

- [.claude/skills/project-mgmt/SKILL.md](../project-mgmt/SKILL.md) - プロジェクト管理スキル
- [.claude/skills/project-mgmt/references/COMMANDS.md](../project-mgmt/references/COMMANDS.md) - コマンド詳細
- [.claude/skills/project-mgmt/references/EXAMPLES.md](../project-mgmt/references/EXAMPLES.md) - 使用例

**`repo-manager` は各モジュールを組み合わせてタスク分割・進捗管理を行います。**
