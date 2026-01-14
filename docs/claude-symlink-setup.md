# Claude Code ユーザー全体設定を `zero-cc/.claude` を正として同期する（Symlink運用）

## 目的
- `~/aslan_prj/zero-cc/.claude/` を **ユーザー全体設定の正本（Single Source of Truth）**にする
- `~/.claude/` 側は **シンボリックリンクで参照**させる
- 正本は **Git で管理**して、複数端末でも同じ設定を再現できるようにする

本ドキュメントでは、以下の 2 つを同期対象とします。

- `settings.json`（Claude Code のユーザー全体設定）
- `skills/`（任意の運用資産ディレクトリ）

> 注意：`~/.claude` 配下の `cache/` や `history.jsonl` などの状態・キャッシュ類は同期しません（Git 管理しない）。

---

## 前提
- OS は Linux（bash 想定）
- 正本のリポジトリは以下
  - `REPO=~/aslan_prj/zero-cc`
  - 正本ディレクトリ：`$REPO/.claude/`

---

## 最終形（期待する状態）
`readlink -f` の結果が **必ず `zero-cc/.claude` を指す**状態になっていればOKです。

- `~/.claude/settings.json` → `~/aslan_prj/zero-cc/.claude/settings.json`
- `~/.claude/skills` → `~/aslan_prj/zero-cc/.claude/skills`

確認コマンド：
```bash
ls -l ~/.claude/settings.json ~/.claude/skills
readlink -f ~/.claude/settings.json
readlink -f ~/.claude/skills
```

---

## セットアップ（初回のみ）

### 1. 変数定義

```bash
REPO=~/aslan_prj/zero-cc
SRC="$REPO/.claude"
TS=$(date +%Y%m%d-%H%M%S)
```

### 2. バックアップ（必須）

既存のユーザー設定があれば退避します。

```bash
mkdir -p ~/.claude/backup-$TS

[ -f ~/.claude/settings.json ] && mv ~/.claude/settings.json ~/.claude/backup-$TS/
[ -d ~/.claude/skills ] && mv ~/.claude/skills ~/.claude/backup-$TS/
```

### 3. 正本ディレクトリの用意

```bash
mkdir -p "$SRC"
```

### 4. 正本ファイルを用意

* `settings.json` が未作成なら作成（最低限空でも動きますが、運用上は中身を入れる想定）

```bash
# 未作成なら作る（既にあるなら不要）
[ -f "$SRC/settings.json" ] || echo '{}' > "$SRC/settings.json"

# skills も未作成なら作る（既にあるなら不要）
[ -d "$SRC/skills" ] || mkdir -p "$SRC/skills"
```

### 5. `~/.claude` へ symlink を張る

```bash
rm -f ~/.claude/settings.json
rm -f ~/.claude/skills

ln -s "$SRC/settings.json" ~/.claude/settings.json
ln -s "$SRC/skills" ~/.claude/skills
```

### 6. 動作確認

```bash
ls -l ~/.claude/settings.json ~/.claude/skills
readlink -f ~/.claude/settings.json
readlink -f ~/.claude/skills
```

---

## Git 管理（正本をコミットする）

### 1. 追跡対象

* `zero-cc/.claude/settings.json`
* `zero-cc/.claude/skills/` 配下（必要なもの）

### 2. `.gitignore` 推奨

ローカル専用・生成物を誤って入れないための最低限です。

```gitignore
# Claude Code local overrides / personal scratch
.claude/settings.local.json
CLAUDE.local.md

# 万一 repo 配下にキャッシュができた場合に弾く（必要に応じて）
.claude/cache/
```

### 3. コミット

```bash
cd ~/aslan_prj/zero-cc
git add .claude/settings.json .claude/skills .gitignore
git commit -m "Manage Claude user-wide config via zero-cc/.claude symlinks"
```

---

## 日常運用（同期の考え方）

### 変更は常に「正本」に対して行う

* 変更する場所：`~/aslan_prj/zero-cc/.claude/settings.json` と `~/aslan_prj/zero-cc/.claude/skills/`
* `~/.claude/settings.json` はリンクなので、編集しても実体は正本が更新されます（どちらで編集しても同じ）。

### 変更を他端末へ反映

* `zero-cc` を `git push` → 他端末で `git pull`
* 他端末は symlink を張り直す必要は基本ありません（初回セットアップ済みなら `pull` だけで追従）。

---

## 新しい端末での再現手順（最短）

1. `zero-cc` を所定のパスに clone（同じパスが望ましい）
2. 「セットアップ（初回のみ）」の symlink 作成手順（上記の 1〜6）を実行

> パスを変える場合：symlink は絶対パスで作っているため、clone 先が変わるとリンクが切れます。
> その場合は `rm` → `ln -s` をやり直してください。

---

## トラブルシューティング

### リンクが切れている（No such file）

```bash
readlink -f ~/.claude/settings.json
```

で存在しないパスが出る場合、以下で貼り直し：

```bash
REPO=~/aslan_prj/zero-cc
SRC="$REPO/.claude"

rm -f ~/.claude/settings.json ~/.claude/skills
ln -s "$SRC/settings.json" ~/.claude/settings.json
ln -s "$SRC/skills" ~/.claude/skills
```

### `~/.claude` 全体を repo にしたくなった

推奨しません（状態・キャッシュが混ざりやすい）。同期対象は「宣言的設定」に限定してください。

---

## ロールバック（元に戻す）

バックアップを取っている前提で戻します。

```bash
# リンクを削除
rm -f ~/.claude/settings.json ~/.claude/skills

# 退避したものを戻す（最新の backup-* を選んでください）
# 例：
TS=YYYYMMDD-HHMMSS
mv ~/.claude/backup-$TS/settings.json ~/.claude/ 2>/dev/null || true
mv ~/.claude/backup-$TS/skills ~/.claude/ 2>/dev/null || true
```

---

## 補足（運用ルール）

* 秘密情報（APIキー等）は Git に入れない方針を推奨
* 端末固有の差分を持ちたい場合は、ユーザー側（`~/.claude`）に別ファイルで持つ、または暗号化管理する
* `settings.local.json` は「プロジェクトのローカル上書き」用途なので、ユーザー全体同期の正本には通常不要
