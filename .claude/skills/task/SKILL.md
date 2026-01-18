---
name: task
description: |
  タスク管理（repo-managerのエイリアス）。
  トリガー例: 「/task ユーザー認証機能を追加して」
allowed-tools: Bash, Glob, Grep, Read, AskUserQuestion
arguments: auto-detect
user-invocable: true
---

# Task

タスク管理をする省略形スキルです。**repo-manager** のエイリアスです。

## 使い方

```
/task ユーザー認証機能を追加して
```

## 詳細

このスキルは **repo-manager** のエイリアスです。詳細なドキュメントは以下を参照してください：

- [.claude/skills/repo-manager/SKILL.md](../repo-manager/SKILL.md)

**repo-manager** は以下のモジュールを組み合わせてタスク分割・進捗管理を行います：

| モジュール | 説明 | ドキュメント |
|:---------|:-----|:------------|
| **plan** | タスク分割 → Issue作成 → 親子関係設定 | [.claude/skills/plan/SKILL.md](../plan/SKILL.md) |
| **analyze-diff** | 差分解析 → タスク分割 | [.claude/skills/analyze-diff/SKILL.md](../analyze-diff/SKILL.md) |
| **project-mgmt** | プロジェクト追加・ステータス設定・日付設定 | [.claude/skills/project-mgmt/SKILL.md](../project-mgmt/SKILL.md) |
| **repo-flow** | ブランチ作成・コミット・プッシュ・PR・マージ | [.claude/skills/repo-flow/SKILL.md](../repo-flow/SKILL.md) |
