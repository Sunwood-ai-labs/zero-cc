---
name: repo-maintain
description: |
  既存GitHubリポジトリのメンテナンス（リリース、変更履歴、Issue等）。ghコマンド使用。
  トリガー例: 「リリースノート」「リリース」「issue」「repo-maintain」
  ※ PR 作成・マージは git-flow-workflow スキルを使用
allowed-tools: Bash, Read, Write, Glob, Grep
arguments: auto-detect
user-invocable: true
---

# GitHub Repository Maintainer

既存のGitHubリポジトリのメンテナンス作業を支援します。

## 前提条件

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み
- Gitリポジトリ内であること

## ワークフロー

### 引数解析
`$ARGUMENTS` から操作タイプを特定:

| 操作 | 引数パターン | 説明 |
|:----|:-------------|:------|
| **release** | `release [ver]`, `rl [ver]`, `publish [ver]` | リリース作成 |
| **changelog** | `changelog`, `changes`, `history` | 変更履歴生成 |
| **issue** | `issue [title]` | イシュー作成 |
| **status** | `status`, `st` | 状態確認 |

---

## release - リリース作成

Git タグと GitHub リリースを作成します。

### 手順

1. **現在の状態確認**
   ```bash
   git fetch --tags
   git tag -l | tail -5
   git log --oneline -10
   ```

2. **バージョン決定**
   - 引数指定 → 使用
   - 未指定 → 現在のタグから自動推奨（例: v1.0.0 → v1.0.1）

3. **変更内容収集**
   ```bash
   PREV_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
   git log ${PREV_TAG}..HEAD --pretty=format:"%h %s" --reverse
   ```

4. **リリースノート生成**

   まず `references/RELEASE_NOTES.md` のフォーマットを参照:
   ```
   .claude/skills/repo-maintain/references/RELEASE_NOTES.md
   ```

   コミットメッセージを解析して分類:

   | プレフィックス | カテゴリ |
   |:---------------|:----------|
   | `feat:` | 新機能 |
   | `fix:` | バグ修正 |
   | `refactor:` | リファクタリング |
   | `perf:` | パフォーマンス |
   | `docs:` | ドキュメント |
   | `test:` | テスト |
   | `chore:` | その他 |
   | なし | 変更 |

   **ステップ:**
   1. `RELEASE_NOTES.md` をプロジェクトルートに生成（テンプレートを参照）
   2. 必要に応じてヘッダー画像を作成:
      - `references/release-header.svg` があれば参照
      - なければ `references/header.svg` をベースに作成

5. **リリース実行（gh コマンド）**

   生成した `RELEASE_NOTES.md` を使用して GitHub リリースを作成:

   ```bash
   # マークダウンファイルを指定してリリース
   gh release create v[version] \
     --title "v[version] - YYYY-MM-DD" \
     --notes-file RELEASE_NOTES.md \
     --verify-tag

   # タグが存在しない場合は先に作成
   git tag -a v[version] -m "v[version]"
   git push origin v[version]
   gh release create v[version] \
     --title "v[version] - YYYY-MM-DD" \
     --notes-file RELEASE_NOTES.md
   ```

   **ポイント:**
   - `--notes-file` で生成済みのマークダウンを直接指定
   - `--verify-tag` でタグの存在確認（オプション）

6. **完了メッセージ**
   - リリースURL
   - 次のステップ

---

## changelog - 変更履歴生成

直近の変更履歴を生成・表示します。

```bash
PREV_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
git log ${PREV_TAG}..HEAD --pretty=format:"%h %s" --reverse
```

カテゴリ別に分類して表示

---

## issue - イシュー作成

GitHub イシューを作成します。

```bash
gh issue create --title "[title]" --body "[description]" --label "bug,enhancement"
```

**イシューテンプレート:**
```markdown
## 概要
[問題の概要]

## 再現手順
1. 手順1
2. 手順2

## 期待する動作
[期待]

## 実際の動作
[現状]

## 環境
- OS:
- Version:
```

---

## status - リポジトリ状態確認

リポジトリの状態をサマリー表示します。

```bash
echo "=== Git Status ==="
git status --short
echo ""
echo "=== Branch ==="
git branch --show-current
echo ""
echo "=== Recent Commits ==="
git log --oneline -5
echo ""
echo "=== GitHub Info ==="
gh repo view --json name,url,visibility,latestRelease 2>/dev/null
echo ""
echo "=== Open PRs ==="
gh pr list --state open --limit 5 2>/dev/null
echo ""
echo "=== Open Issues ==="
gh issue list --state open --limit 5 2>/dev/null
```

---

## 使用例

```bash
/repo-maintain release 1.0.0
/repo-maintain changelog
/repo-maintain issue "Bug: Login fails"
/repo-maintain status
```

---

## 関連スキル

| スキル | 用途 |
|:------|:------|
| **git-flow-workflow** | フィーチャーブランチ作成、PR作成、マージ |
| **repo-create** | 新規リポジトリ作成 |
