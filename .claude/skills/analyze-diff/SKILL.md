---
name: analyze-diff
description: |
  差分解析してタスク分割。
  トリガー例: 「/diff」
allowed-tools: Bash, Glob, Grep, Read, AskUserQuestion
arguments: auto-detect
user-invocable: true
---

# Analyze Diff

現在の差分を解析して、タスク分割案を出力します。

## 前提条件

- Git リポジトリ内であること
- 差分が存在すること

## ワークフロー

### 1. 現状確認

```bash
# 変更の確認
git status
git diff --stat

# カレントブランチの確認
git branch --show-current
```

- カレントブランチの確認
- 未コミット変更の有無と内容
- 変更されたファイル一覧

### 2. 差分の詳細解析

```bash
# 変更ファイルの詳細
git diff FILE_PATH

# 追加・変更・削除の行数
git diff --numstat
```

### 3. タスク分割案の作成

差分の内容を分析して、タスク分割案を作成:

1. **変更のカテゴライズ**: ファイルの種類や機能ごとにグループ化
2. **タスクの抽出**: 各変更を独立したタスクとして抽出
3. **優先順位付け**: 依存関係を考慮して順序を決定

### 4. 結果を出力

タスク分割案を出力:

```markdown
## タスク分割案

### 親タスク
- [親Issueのタイトル]

### サブタスク
1. [Sub-1] サブタスク1
2. [Sub-2] サブタスク2
3. [Sub-3] サブタスク3
```

## 使用例

```
ユーザー: 「/diff」

スキル:
1. 現在の差分を解析（git status, git diff）
2. 変更のカテゴライズ
3. タスク分割案の作成
4. 結果を出力

出力例:
```
## 差分解析結果

変更ファイル:
- src/auth/jwt.py (新規)
- src/auth/login.py (新規)
- src/auth/logout.py (新規)

## タスク分割案

親Issue: ユーザー認証機能の実装

サブタスク:
1. JWTモジュールの実装
2. ログインエンドポイントの実装
3. ログアウトエンドポイントの実装
```
```

## 注意点

1. **差分がない場合**: メッセージを表示して終了
2. **大量の変更**: 適切にグループ化してタスク数を調整
3. **関連性の高い変更**: 1つのタスクにまとめる

## 関連スキル

| スキル | 用途 |
|:------|:------|
| **plan** | タスク分割 → Issue作成 → 親子関係設定 |
| **project-mgmt** | プロジェクト追加・ステータス設定・日付設定 |
| **repo-flow** | ブランチ作成・コミット・プッシュ・PR・マージ |
| **repo-manager** | analyze-diff + plan + project-mgmt + repo-flow |
