---
name: reg-commit
description: |
  差分からIssueを作成 + プロジェクトに登録 + サブイシューごとのコミット + Gitフロー（analyze-diff + plan + project-mgmt）。
  トリガー例: 「/reg-commit」
allowed-tools: Bash, Glob, Grep, Read, AskUserQuestion
arguments: auto-detect
user-invocable: true
---

# Reg Commit (Register & Commit)

差分からIssueを作成してプロジェクトに登録し、サブイシューごとにコミットしてGitフローを実行する省略形スキルです。

**フロー**: `analyze-diff` → `plan` → `project-mgmt` → `サブイシューごとのコミット` → `Gitフロー`

**重要**: 各サブイシューは個別にコミットしてください。まとめてコミットしないこと。

## 使い方

```
/reg-commit
```

## ワークフロー

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
│  4. サブイシューごとのコミット                                 │
│     - 各サブイシューに対応するファイルを特定                    │
│     - サブイシューごとに個別にコミット                         │
│     - 各コミットメッセージに対応するIssue番号を含める          │
├─────────────────────────────────────────────────────────────┤
│  5. Gitフロー                                                 │
│     - ブランチ作成                                             │
│     - プッシュ                                                 │
│     - PR 作成                                                 │
│     - develop へマージ                                        │
│     - クリーンアップ                                           │
└─────────────────────────────────────────────────────────────┘
```

## 重要: サブイシューごとのコミット

**各サブイシューは個別にコミットする必要があります。**

### コミットの手順

1. **サブイシューとファイルの対応付け**
   ```
   サブイシュー #16 → .claude/skills/analyze-diff/
   サブイシュー #17 → .claude/skills/plan/
   サブイシュー #18 → .claude/skills/reg-commit/
   サブイシュー #19 → .claude/skills/reg-issue/
   サブイシュー #20 → .claude/skills/task/
   サブイシュー #21 → .claude/skills/repo-manager/SKILL.md
   ```

2. **各サブイシューごとにコミット**
   ```bash
   # サブイシュー #16
   git add .claude/skills/analyze-diff/
   git commit -m "✨ feat: analyze-diffモジュールの追加

   Closes #16

   Co-Authored-By: Claude <noreply@anthropic.com>"

   # サブイシュー #17
   git add .claude/skills/plan/
   git commit -m "✨ feat: planモジュールの追加

   Closes #17

   Co-Authored-By: Claude <noreply@anthropic.com>"

   # ... 以降同様に各サブイシューでコミット
   ```

3. **親Issueはクローズしない**
   - 親Issueはサブイシューがすべて完了した後に手動でクローズする
   - または、PRの説明で親Issueをクローズする

### 親Issueの作成例

```bash
gh issue create \
  --title "✨ refactor(repo-manager): モジュール化とドキュメント更新" \
  --body "## 概要

repo-managerスキルをモジュール構成にリファクタリングし、ドキュメントを更新します。

## サブイシュー

- #16: analyze-diffモジュールの追加
- #17: planモジュールの追加
- #18: reg-commitスキルの追加
- #19: reg-issueスキルの追加
- #20: taskスキルの追加
- #21: repo-managerドキュメントの更新

## タスク

- [ ] #16: analyze-diffモジュールの追加
- [ ] #17: planモジュールの追加
- [ ] #18: reg-commitスキルの追加
- [ ] #19: reg-issueスキルの追加
- [ ] #20: taskスキルの追加
- [ ] #21: repo-managerドキュメントの更新"
```

## 詳細

このスキルは以下のモジュールを組み合わせたものです：

- [.claude/skills/analyze-diff/SKILL.md](../analyze-diff/SKILL.md) - 差分解析 → タスク分割
- [.claude/skills/plan/SKILL.md](../plan/SKILL.md) - タスク分割 → Issue作成 → 親子関係設定
- [.claude/skills/project-mgmt/SKILL.md](../project-mgmt/SKILL.md) - プロジェクト追加・ステータス設定・日付設定

**注意**: `repo-flow` モジュールは使用しません。代わりに、各サブイシューごとに個別にコミットを作成してから、Gitフロー（ブランチ作成・プッシュ・PR・マージ）を実行します。

### なぜ repo-flow を使わないのか？

`repo-flow` モジュールは、すべての変更を1つのコミットにまとめてしまいます。しかし、サブイシューごとにIssueを作成した場合、各サブイシーに対して個別のコミットを作る必要があります。

したがって：
- **各サブイシュー**: 対応するファイルを個別にコミット（`Closes #番号`を含める）
- **Gitフロー**: コミットが完了した後に、ブランチ作成・プッシュ・PR・マージを実行

詳細なドキュメントは各モジュールを参照してください。

## 実例

### シナリオ: 6つのモジュールを追加する場合

```bash
# 1. 差分を解析
git status
git diff

# 2. Issueを作成（親子構造）
親Issue #15: ✨ refactor(repo-manager): モジュール化とドキュメント更新

## サブイシュー

- #16: analyze-diffモジュールの追加
- #17: planモジュールの追加
- #18: reg-commitスキルの追加
- #19: reg-issueスキルの追加
- #20: taskスキルの追加
- #21: repo-managerドキュメントの更新

# 3. プロジェクトに追加・ステータス設定
gh project item-add 2 --url "https://github.com/owner/repo/issues/16"
# ... 各サブイシューをプロジェクトに追加

# 4. 各サブイシューごとにコミット
git checkout -b feature/refactor-repo-manager-15 origin/develop

# サブイシュー #16
git add .claude/skills/analyze-diff/
git commit -m "✨ feat: analyze-diffモジュールの追加

差分を解析してタスク分割案を作成するモジュールを追加しました。

Closes #16

Co-Authored-By: Claude <noreply@anthropic.com>"

# サブイシュー #17
git add .claude/skills/plan/
git commit -m "✨ feat: planモジュールの追加

タスク分割・Issue作成・親子関係設定を行うモジュールを追加しました。

Closes #17

Co-Authored-By: Claude <noreply@anthropic.com>"

# ... 以降同様に各サブイシューでコミット

# 5. Gitフロー
git push -u origin feature/refactor-repo-manager-15

# PRを作成（親Issueをクローズ）
gh pr create \
  --title "✨ refactor(repo-manager): モジュール化とドキュメント更新" \
  --body "## 概要

repo-managerスキルをモジュール構成にリファクタリングしました。

## サブイシュー

- Closes #16: analyze-diffモジュールの追加
- Closes #17: planモジュールの追加
- Closes #18: reg-commitスキルの追加
- Closes #19: reg-issueスキルの追加
- Closes #20: taskスキルの追加
- Closes #21: repo-managerドキュメントの更新

## 親Issue

Closes #15

Co-Authored-By: Claude <noreply@anthropic.com>" \
  --base develop

# PRをマージ
gh pr merge --merge --delete-branch=true
```

## 注意点

1. **各サブイシューは個別にコミットする**: まとめてコミットしないこと
2. **コミットメッセージにIssue番号を含める**: `Closes #番号` を含めると自動的にIssueがクローズされる
3. **親Issueにはサブイシュー番号を記載する**:
   - 親Issueの説明に、すべてのサブイシュー番号を記載する
   - 親IssueをクローズするPRの説明にも、すべてのサブイシュー番号を記載する
   - 例:
     ```
     ## サブイシュー

     - Closes #16: analyze-diffモジュールの追加
     - Closes #17: planモジュールの追加
     - Closes #18: reg-commitスキルの追加
     ...
     ```
4. **親Issueのクローズタイミング**: 最後のサブイシューで親Issueもクローズするか、手動でクローズする
