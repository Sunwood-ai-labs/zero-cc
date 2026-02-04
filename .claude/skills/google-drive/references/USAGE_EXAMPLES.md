# Google Drive スクリプト 使用例

このドキュメントでは、各スクリプトの使用例を紹介します。

## 目次

1. [認証設定](#認証設定)
2. [アップロード](#アップロード)
3. [ダウンロード](#ダウンロード)
4. [検索](#検索)
5. [一覧](#一覧)
6. [削除](#削除)
7. [フォルダ作成](#フォルダ作成)
8. [実践的なワークフロー](#実践的なワークフロー)

---

## 認証設定

### 初回認証

```bash
cd /prj/zero-cc/.claude/skills/google-drive/scripts
python auth_setup.py
```

**出力例:**
```
Google Drive API 認証を開始します...
ブラウザが開き、Googleアカウントへの許可を求められます

認証に成功しました！
トークンファイル: ../config/token.pickle

これでGoogle Drive APIを使用する準備が整いました。
```

---

## アップロード

### 基本的な使い方

```bash
# ルートディレクトリにアップロード
python gdrive_upload.py ./document.pdf
```

### 特定のフォルダにアップロード

```bash
# フォルダIDを指定
python gdrive_upload.py ./photo.jpg --parent 1ABC123xyz
```

### ファイル名を指定してアップロード

```bash
# 保存時のファイル名を変更
python gdrive_upload.py ./data.txt --name "backup_data.txt"
```

**出力例:**
```
アップロード中: document.pdf
  MIMEタイプ: application/pdf

アップロード完了！
  ファイルID: 1a2b3c4d5e6f
  ファイル名: document.pdf
  リンク: https://drive.google.com/file/d/1a2b3c4d5e6f/view?usp=drivesdk
```

---

## ダウンロード

### ファイルIDでダウンロード

```bash
python gdrive_download.py --id 1a2b3c4d5e6f --output ./downloads/
```

### ファイル名で検索してダウンロード

```bash
python gdrive_download.py --name "report.pdf"
```

### 特定フォルダ内のファイルを検索してダウンロード

```bash
python gdrive_download.py --name "invoice.pdf" --parent 1ABC123xyz
```

### Google DocsをWord形式でダウンロード

```bash
# ファイルID指定
python gdrive_download.py --id 1doc123xyz --output ./my_report.docx

# ファイル名検索
python gdrive_download.py --name "Proposal Doc" --output ./downloads/
```

**出力例:**
```
ファイル名で検索中: report.pdf
ファイルが見つかりました (ID: 1a2b3c4d5e6f)
ダウンロード中: report.pdf
  ファイルID: 1a2b3c4d5e6f
  MIMEタイプ: application/pdf
  進捗: 50%
  進捗: 100%

ダウンロード完了！
  保存先: /home/user/downloads/report.pdf
```

---

## 検索

### ファイル名で検索

```bash
python gdrive_search.py "report"
```

### 特定のフォルダ内で検索

```bash
python gdrive_search.py "invoice" --parent 1ABC123xyz
```

### MIMEタイプでフィルタ

```bash
# PDFファイルのみ
python gdrive_search.py "document" --mime-type application/pdf

# 画像ファイル
python gdrive_search.py "photo" --mime-type image/jpeg

# Google Docs
python gdrive_search.py "proposal" --mime-type application/vnd.google-apps.document
```

### JSON形式で出力

```bash
python gdrive_search.py "report" --json > results.json
```

**出力例:**
```
検索クエリ: trashed = false and name contains 'report'
検索中...

見つかりました: 3件

--- 1 ---
名前: Monthly Report.pdf
ID: 1report123
タイプ: PDF
サイズ: 1.2 MB
更新日時: 2024-01-15 10:30
リンク: https://drive.google.com/file/d/1report123/view
```

---

## 一覧

### ルートディレクトリの内容を表示

```bash
python gdrive_list.py
```

### 特定のフォルダの内容を表示

```bash
python gdrive_list.py --folder 1ABC123xyz
```

### 詳細情報を表示

```bash
python gdrive_list.py --details
```

### フォルダのみを表示

```bash
python gdrive_list.py --folders-only
```

### ファイルのみを表示

```bash
python gdrive_list.py --files-only
```

### 再帰的に全てのファイルを表示

```bash
python gdrive_list.py --recursive
```

**出力例:**
```
フォルダ: プロジェクト資料 (ID: 1ABC123xyz)
フォルダ: 2, ファイル: 5

1. 📂 画像
   ID: 1folder456
   タイプ: フォルダ

2. 📄 report.pdf
   ID: 1doc789
   タイプ: PDF

3. 📄 data.csv
   ID: 1csv123
   タイプ: テキスト
   サイズ: 45.2 KB
   更新日時: 2024-01-20 14:30
   リンク: https://drive.google.com/file/d/1csv123/view
```

---

## 削除

### ファイルIDでゴミ箱へ移動

```bash
python gdrive_delete.py --id 1a2b3c4d5e6f
```

### ファイル名で検索して削除

```bash
python gdrive_delete.py --name "old_file.txt"
```

### ドライラン（確認のみ）

```bash
# 実際には削除せず、確認のみ
python gdrive_delete.py --id 1a2b3c4d5e6f --dry-run
```

### 完全に削除

```bash
# ゴミ箱を経由せずに完全削除
python gdrive_delete.py --id 1a2b3c4d5e6f --permanent
```

**出力例:**
```
ファイルIDで削除: 1a2b3c4d5e6f

ファイルをゴミ箱へ移動します:
  名前: old_file.txt
  ID: 1a2b3c4d5e6f

よろしいですか？ (yes/no): yes

ファイルをゴミ箱へ移動しました
```

---

## フォルダ作成

### ルートにフォルダを作成

```bash
python gdrive_mkdir.py "新しいプロジェクト"
```

### 特定のフォルダの中に作成

```bash
python gdrive_mkdir.py "2024年度" --parent 1ABC123xyz
```

**出力例:**
```
フォルダを作成中: 新しいプロジェクト

フォルダを作成しました！
  フォルダID: 1newfolder123
  フォルダ名: 新しいプロジェクト
  リンク: https://drive.google.com/drive/u/0/folders/1newfolder123
```

---

## 実践的なワークフロー

### ワークフロー1: バックアップ

ローカルファイルをGoogle Driveにバックアップする:

```bash
# バックアップ用フォルダを作成
python gdrive_mkdir.py "Backup_2024"

# フォルダIDをメモ
# FOLDER_ID="1backup123"

# ファイルをアップロード
python gdrive_upload.py ./important.docx --parent $FOLDER_ID
python gdrive_upload.py ./data.xlsx --parent $FOLDER_ID
```

### ワークフロー2: フォルダ整理

古いファイルを検索してゴミ箱へ移動:

```bash
# 古いPDFを検索
python gdrive_search.py "old" --mime-type application/pdf

# ドライランで確認
python gdrive_delete.py --name "old_report.pdf" --dry-run

# 削除実行
python gdrive_delete.py --name "old_report.pdf"
```

### ワークフロー3: 共有フォルダのダウンロード

共有フォルダの内容をローカルにダウンロード:

```bash
# フォルダIDを指定（共有フォルダのID）
FOLDER_ID="1sharedfolder123"

# 内容を一覧表示
python gdrive_list.py --folder $FOLDER_ID

# 必要なファイルをダウンロード
python gdrive_download.py --name "shared_doc.pdf" --parent $FOLDER_ID --output ./
```

### ワークフロー4: 定期レポートの作成とアップロード

```bash
# 日付付きのレポート名
DATE=$(date +%Y%m%d)
REPORT_NAME="report_${DATE}.pdf"

# レポートをアップロード
python gdrive_upload.py ./reports/$REPORT_NAME --parent 1reports123

# アップロード確認
python gdrive_search.py "$REPORT_NAME"
```

---

## 環境変数の使用

頻繁に使用するフォルダIDは環境変数に設定すると便利です:

```bash
# ~/.bashrc または ~/.zshrc に追加
export DRIVE_WORK_FOLDER="1workfolder123"
export DRIVE_BACKUP_FOLDER="1backupfolder123"

# 使用例
python gdrive_upload.py ./file.pdf --parent $DRIVE_WORK_FOLDER
python gdrive_list.py --folder $DRIVE_BACKUP_FOLDER
```

---

## トラブルシューティング

### 認証エラー

```
エラー: credentials.json が見つかりません
```

**解決策:** [SETUP.md](SETUP.md) を参照して、認証設定を行ってください。

### ファイルが見つからない

```
ファイルが見つかりません: report.pdf
```

**解決策:** 検索クエリを緩めてみてください:

```bash
# 部分一致で検索
python gdrive_search.py "report"

# 全てのPDFを表示
python gdrive_search.py "" --mime-type application/pdf
```

### アップロード失敗

```
エラー: アップロードに失敗しました
```

**解決策:**
- ファイルサイズが上限を超えていないか確認
- インターネット接続を確認
- 認証トークンの有効期限を確認

---

## 関連ドキュメント

- [SETUP.md](SETUP.md) - Google Cloud Consoleでの認証設定手順
- [API_REFERENCE.md](API_REFERENCE.md) - Google Drive APIの主なメソッドと検索クエリ構文
