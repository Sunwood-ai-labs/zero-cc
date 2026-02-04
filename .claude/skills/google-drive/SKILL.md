---
name: google-drive
description: "Google Drive APIを使用してファイルのアップロード、ダウンロード、検索、一覧、削除を行うスキル。使用タイミング: (1) Google Driveにファイルをアップロードするとき、(2) Google Driveからファイルをダウンロードするとき、(3) Google Driveのファイルを検索・一覧するとき、(4) Google Driveのファイルを削除・移動するとき"
---

# Google Drive Operations

## Quick Start

### 1. 認証設定（初回のみ）

Google Drive APIを使用するには、事前にOAuth2認証の設定が必要です。

```bash
# 必要なライブラリをインストール
pip install google-api-python-client google-auth-oauthlib

# Google Cloud ConsoleでOAuth2クライアントIDを作成
# （詳細は references/SETUP.md を参照）

# 認証設定を実行
python -c "
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRET_PATH = '/path/to/credentials.json'

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
creds = flow.run_local_server(port=0)

with open('~/.config/google-drive-token.json', 'wb') as f:
    pickle.dump(creds, f)
"
```

**認証ファイルの配置:**
- トークンファイル: `~/.config/google-drive-token.json`
- スクリプトは自動的にこのファイルを読み込みます

詳細は[SETUP.md](references/SETUP.md)を参照してください。

### 2. 基本的な使用方法

```bash
# ファイルをアップロード
python gdrive_upload.py ./file.pdf

# ファイルをダウンロード
python gdrive_download.py --id FILE_ID --output ./

# ファイルを検索
python gdrive_search.py "report"

# フォルダの内容を一覧表示
python gdrive_list.py

# ファイルを削除（ゴミ箱へ）
python gdrive_delete.py --id FILE_ID

# フォルダを作成
python gdrive_mkdir.py "新しいフォルダ"
```

---

## Scripts

### Upload

ファイルをGoogle Driveにアップロードします。

**スクリプト:** `scripts/gdrive_upload.py`

**基本的な使い方:**
```bash
python gdrive_upload.py <ファイルパス> [--parent フォルダID] [--name ファイル名]
```

**例:**
```bash
# ルートにアップロード
python gdrive_upload.py ./document.pdf

# 特定のフォルダにアップロード
python gdrive_upload.py ./photo.jpg --parent 1ABC123xyz

# ファイル名を指定してアップロード
python gdrive_upload.py ./data.txt --name "backup_2024.txt"
```

---

### Download

Google Driveからファイルをダウンロードします。

**スクリプト:** `scripts/gdrive_download.py`

**基本的な使い方:**
```bash
# ファイルIDで指定
python gdrive_download.py --id ファイルID [--output 保存先]

# ファイル名で検索してダウンロード
python gdrive_download.py --name ファイル名 [--parent フォルダID]
```

**例:**
```bash
# ファイルIDでダウンロード
python gdrive_download.py --id 1a2b3c4d5e6f --output ./downloads/

# ファイル名で検索してダウンロード
python gdrive_download.py --name "report.pdf"

# Google DocsをWord形式でダウンロード
python gdrive_download.py --id 1doc123xyz --output ./report.docx
```

**注意:** Google Workspaceファイル（Docs/Sheets/Slides）は自動的に適切な形式（.docx/.xlsx/.pptx）でエクスポートされます。

---

### Search

Google Drive内のファイルを検索します。

**スクリプト:** `scripts/gdrive_search.py`

**基本的な使い方:**
```bash
python gdrive_search.py <クエリ> [--mime-type MIMEタイプ] [--parent フォルダID]
```

**例:**
```bash
# ファイル名で検索
python gdrive_search.py "invoice"

# 特定のフォルダ内のPDFを検索
python gdrive_search.py "contract" --parent 1ABC123xyz --mime-type application/pdf

# Google Docsを検索
python gdrive_search.py "proposal" --mime-type application/vnd.google-apps.document

# JSON形式で出力
python gdrive_search.py "report" --json
```

**検索クエリの詳細:** [API_REFERENCE.md](references/API_REFERENCE.md#検索クエリ構文)を参照してください。

---

### List

フォルダ内のファイル・フォルダ一覧を表示します。

**スクリプト:** `scripts/gdrive_list.py`

**基本的な使い方:**
```bash
python gdrive_list.py [--folder フォルダID] [--recursive] [--details]
```

**例:**
```bash
# ルートディレクトリの内容を表示
python gdrive_list.py

# 特定のフォルダの内容を表示
python gdrive_list.py --folder 1ABC123xyz

# 詳細情報を表示
python gdrive_list.py --details

# 再帰的に全てのファイルを表示
python gdrive_list.py --recursive

# フォルダのみを表示
python gdrive_list.py --folders-only

# ファイルのみを表示
python gdrive_list.py --files-only
```

---

### Delete

ファイルを削除（ゴミ箱へ移動または完全削除）します。

**スクリプト:** `scripts/gdrive_delete.py`

**基本的な使い方:**
```bash
# ファイルIDで指定してゴミ箱へ移動
python gdrive_delete.py --id ファイルID

# ファイル名で検索して削除
python gdrive_delete.py --name ファイル名 [--parent フォルダID]

# 完全に削除
python gdrive_delete.py --id ファイルID --permanent
```

**例:**
```bash
# ゴミ箱へ移動
python gdrive_delete.py --id 1a2b3c4d5e6f

# ドライラン（確認のみ）
python gdrive_delete.py --id 1a2b3c4d5e6f --dry-run

# 完全削除
python gdrive_delete.py --id 1a2b3c4d5e6f --permanent

# ファイル名で検索して削除
python gdrive_delete.py --name "old_file.txt"
```

**注意:** 完全削除は元に戻せません。慎重に使用してください。

---

### Make Directory

Google Driveに新しいフォルダを作成します。

**スクリプト:** `scripts/gdrive_mkdir.py`

**基本的な使い方:**
```bash
python gdrive_mkdir.py <フォルダ名> [--parent 親フォルダID]
```

**例:**
```bash
# ルートにフォルダを作成
python gdrive_mkdir.py "プロジェクト資料"

# 特定のフォルダの中に作成
python gdrive_mkdir.py "2024年度" --parent 1ABC123xyz
```

---

## Reference

### ドキュメント

- **[SETUP.md](references/SETUP.md)** - Google Cloud Consoleでの認証設定手順
- **[API_REFERENCE.md](references/API_REFERENCE.md)** - Google Drive APIの主なメソッドと検索クエリ構文
- **[USAGE_EXAMPLES.md](references/USAGE_EXAMPLES.md)** - 各スクリプトの使用例と実践的なワークフロー

### ディレクトリ構造

```
google-drive/
├── scripts/                   # 実行可能なスクリプト
│   ├── auth_helper.py         # 認証ヘルパー（OAuth2/サービスアカウント対応）
│   ├── auth_setup.py          # 認証設定（OAuth2用）
│   ├── gdrive_upload.py       # ファイルアップロード
│   ├── gdrive_download.py     # ファイルダウンロード
│   ├── gdrive_search.py       # ファイル検索
│   ├── gdrive_list.py         # ファイル一覧
│   ├── gdrive_delete.py       # ファイル削除
│   └── gdrive_mkdir.py        # フォルダ作成
└── references/                # ドキュメント
    ├── SETUP.md               # Google Cloud Consoleでの認証設定手順
    ├── API_REFERENCE.md       # Google Drive APIの主なメソッドと検索クエリ構文
    └── USAGE_EXAMPLES.md      # 各スクリプトの使用例と実践的なワークフロー
```

### 認証について

**デフォルト: OAuth2認証**
- トークンファイル: `~/.config/google-drive-token.json`
- 環境変数: `GOOGLE_TOKEN_PATH` で変更可能

**サービスアカウント（オプション）:**
- サービスアカウントJSON: `~/.config/google-service-account.json`
- スキル内の `config/service-account.json` も自動検出
- 環境変数: `GOOGLE_SERVICE_ACCOUNT_PATH` で変更可能

注意: サービスアカウントは共有ドライブ（Google Workspace）が必要です。

### 必要なライブラリ

```bash
pip install google-api-python-client google-auth-oauthlib
```

---

## 使用タイミング

このスキルは以下の状況で使用してください：

1. **Google Driveにファイルをアップロードするとき**
   - ローカルファイルをクラウドにバックアップ
   - プロジェクト資料を共有

2. **Google Driveからファイルをダウンロードするとき**
   - 共有されたファイルをローカルに保存
   - Google Docs/Sheets/Slidesをオフィス形式でエクスポート

3. **Google Driveのファイルを検索・一覧するとき**
   - 特定のファイルを探す
   - フォルダの内容を確認

4. **Google Driveのファイルを削除・整理するとき**
   - 古いファイルをゴミ箱へ移動
   - フォルダを作成して整理

---

## セキュリティに関する注意

- `config/credentials.json` と `config/token.pickle` は機密情報を含んでいます
- これらのファイルをGitリポジトリにコミットしないでください
- `.gitignore` に `config/credentials.json` と `config/token.pickle` を追加することを推奨します
