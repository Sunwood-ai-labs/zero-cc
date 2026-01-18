---
name: reg-commit
description: |
  差分からIssueを作成 + プロジェクトに登録 + コミット＆プッシュ（analyze-diff + plan + project-mgmt + repo-flow）。
  トリガー例: 「/reg-commit」
allowed-tools: Bash, Glob, Grep, Read, AskUserQuestion
arguments: auto-detect
user-invocable: true
---

# Reg Commit (Register & Commit)

差分からIssueを作成してプロジェクトに登録し、コミット＆プッシュまで行う省略形スキルです。

**フロー**: `analyze-diff` → `plan` → `project-mgmt` → `repo-flow`

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
│  4. repo-flow モジュール                                      │
│     - ブランチ作成                                             │
│     - コミット（Issue番号を含める）                            │
│     - プッシュ                                                 │
│     - PR 作成                                                 │
│     - develop へマージ                                        │
│     - クリーンアップ                                           │
└─────────────────────────────────────────────────────────────┘
```

## 詳細

このスキルは以下のモジュールを組み合わせたものです：

- [.claude/skills/analyze-diff/SKILL.md](../analyze-diff/SKILL.md) - 差分解析 → タスク分割
- [.claude/skills/plan/SKILL.md](../plan/SKILL.md) - タスク分割 → Issue作成 → 親子関係設定
- [.claude/skills/project-mgmt/SKILL.md](../project-mgmt/SKILL.md) - プロジェクト追加・ステータス設定・日付設定
- [.claude/skills/repo-flow/SKILL.md](../repo-flow/SKILL.md) - ブランチ作成・コミット・プッシュ・PR・マージ

詳細なドキュメントは各モジュールを参照してください。
