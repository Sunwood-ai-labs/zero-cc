---
name: repo-flow
description: |
  Git Flow ワークフローで開発からマージまでを実行。
  「フィーチャーブランチ作って」「PR出して」「コードレビューして」「マージして」などのリクエスト時に使用。
  開発中の差分がある状態からブランチを作成します。
  develop → main のリリースフローもサポート。
allowed-tools: Bash, Glob, Grep, Read, Write
user-invocable: true
---

# Repo Flow

Git Flow ワークフローでフィーチャーブランチの作成からマージ・クリーンアップまでを支援します。

**前提: 開発で差分がある状態から開始します**

## ワークフロー

### Step 1: 現状確認（差分チェック）

```bash
git status
git diff --stat
git branch --show-current
```

- カレントブランチの確認
- 未コミット変更の有無と内容
- 変更されたファイル一覧

### Step 2: フィーチャーブランチ作成（差分を含めて）

**重要: 開発中の差分がある状態でブランチを作成します**

```bash
# 現在のブランチを確認
git branch --show-current

# develop からブランチ作成（差分は新しいブランチに引き継がれる）
git checkout develop 2>/dev/null || git checkout main
git pull

# 変更を一時退避（必要な場合）
git stash push -m "WIP: <description>"

# フィーチャーブランチ作成
git checkout -b feature/<name>

# 変更を戻す（一時退避していた場合）
git stash pop
```

**ブランチ名の決定:**
```
feature/<description>

例:
feature/repo-create-refs
feature/add-auth-system
feature/fix-login-bug
```

### Step 3: 差分をコミット

**現在の差分を確認:**
```bash
git status
git diff
```

**コミットメッセージ形式:**
```
<type>: <subject>

[optional body]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**タイプ:**
- `feat` - 新機能
- `fix` - バグ修正
- `docs` - ドキュメント
- `style` - フォーマット
- `refactor` - リファクタリング
- `test` - テスト
- `chore` - その他

**コミット例:**
```bash
# 全ての変更をコミット
git add .
git commit -m "feat: add user authentication

- Implement JWT-based authentication
- Add login/logout endpoints
- Include password hashing

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 4: プッシュ

```bash
git push -u origin feature/<name>
```

### Step 5: プルリクエスト作成

**タイトル形式:**
```
<type>: <subject>

例:
feat(repo-create): add comprehensive reference templates
fix(auth): resolve JWT token expiration issue
```

**PR 作成:**
```bash
# develop に対してPRを作成
gh pr create --base develop \
  --title "feat(scope): description" \
  --body "PR body here"
```

**PR ボディンテンプレート:**
```markdown
## Summary

[1-2行で変更内容を説明]

## Changes

- 変更点1
- 変更点2

## Test plan

- [x] テスト項目1
- [x] テスト項目2

---

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Step 6: コードレビュー対応

**gemini-code-assist などのレビュー確認:**
```bash
# レビューコメントを確認
gh pr view <number> --json comments

# gemini-code-assist のレビューを抽出
gh api repos/:owner/:repo/pulls/:number/comments --jq '.[] | select(.user.login == "gemini-code-assist[bot]")'
```

**修正コミット:**
```bash
# 修正をコミット（同じブランチにプッシュ）
git add <files>
git commit -m "fix: resolve review feedback"
git push
```

### Step 7: develop へのマージ

**Git Flow の正しい順序:**
```
feature → develop → main
```

```bash
# develop に切り替え
git checkout develop
git pull

# feature ブランチをマージ
git merge feature/<name> --no-ff
git push origin develop
```

### Step 8: main へのリリースマージ

**リリース時のみ実行:**

```bash
# main に切り替え
git checkout main
git pull

# develop をマージ（--no-ff または --squash）
git merge develop --no-ff
git push origin main

# タグ付け（任意、repo-maintain スキルでも可）
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Step 9: クリーンアップ

```bash
# ローカルブランチ削除
git branch -d feature/<name>

# リモートブランチ削除
git push origin --delete feature/<name>

# リモートの追跡ブランチをクリーンアップ
git fetch --prune
```

## ブランチ構造

```
main           ← 本番環境（リリース時のみ更新）
  ↑
develop        ← 開発統合ブランチ
  ↑
feature/*      ← フィーチャーブランチ（各機能開発）
```

## 開発ワークフロー図

```
1. 開発（ファイル修正）
   ↓
2. feature/<name> ブランチ作成
   ↓ (差分を引き継ぐ)
3. コミット & プッシュ
   ↓
4. PR 作成 (feature → develop)
   ↓
5. レビュー & 修正
   ↓
6. develop にマージ
   ↓ (リリース時)
7. main にマージ
   ↓
8. ブランチ削除
```

## クイックリファレンス

### コマンド一覧

| 操作 | コマンド |
|:--|:--|
| 差分確認 | `git status`, `git diff` |
| ブランチ作成 | `git checkout -b feature/<name>` |
| 一時退避 | `git stash push -m "message"` |
| 復元 | `git stash pop` |
| コミット | `git add . && git commit` |
| プッシュ | `git push -u origin feature/<name>` |
| PR 作成 | `gh pr create --base develop` |
| develop へマージ | `git merge feature/<name> --no-ff` |
| ブランチ削除 | `git branch -d feature/<name>` |

### develop が存在しない場合

```bash
# main から develop を作成
git checkout main
git pull
git checkout -b develop
git push -u origin develop
```

## ベストプラクティス

✅ **やるべきこと:**
- develop から feature ブランチを作成
- Conventional Commits 形式でコミット
- PR ボディに詳細な説明を記載
- PR は develop に対して作成
- コードレビューを受けてからマージ
- マージ済みブランチは削除

❌ **やるべきでないこと:**
- feature ブランチを直接 main にマージ
- リモートの main に直接プッシュ
- マージせずにブランチを放置
- `git push --force` を使用（緊急時のみ）

## 使用例

```bash
# 開発中の差分からブランチ作成
/repo-flow フィーチャーブランチ作って
↓
1. 差分を確認します
2. ブランチ名を決定します
3. feature/<name> を作成して差分を移動

# コミット & プッシュ & PR
/repo-flow PR出して
↓
1. 変更をコミット
2. プッシュ
3. develop への PR を作成

# マージ
/repo-flow マージして
↓
feature → develop にマージ

# クリーンアップ
/repo-flow ブランチ削除して
↓
マージ済みブランチを削除
```

## 関連スキル

| スキル | 用途 |
|:------|:------|
| **repo-maintain** | リリース、変更履歴、Issue |
| **repo-create** | 新規リポジトリ作成 |
