---
name: google-sheets
description: Googleスプレッドシートへのアクセス、データの書き込み、読み込み、検索、シート管理を行うスキル。セルへの値書き込み、行の追加、シート全体の読み取り、特定条件での検索、シートの作成・削除・名前変更をサポート。レシートの記録、家計簿の管理、データの集計など、スプレッドシートを操作するタスク全般で使用する。
---

# Google Sheets 操作スキル

Googleスプレッドシートにアクセスして、データの読み書き・検索を行うスキルです。

## 認証設定

このスキルを使用する前に、Google Cloud Console で以下の設定が必要です。

### 方法1: サービスアカウント認証（バッチ処理向け）

サーバー側で自動実行する処理（バッチ、CLIツールなど）に適しています。

**設定手順:**

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクトを作成
2. 「APIとサービス」→「ライブラリ」から「Google Sheets API」を有効化
3. 「APIとサービス」→「認証情報」→「認証情報を作成」→「サービスアカウント」
4. サービスアカウントを作成し、「キー」タブから「鍵を追加」→「新しい鍵を作成」→ JSON形式でダウンロード
5. スプレッドシートを開き、「共有」ボタンからサービスアカウントのメールアドレスを招待（編集権限）

**環境変数の設定:**

```bash
export GOOGLE_SPREADSHEET_ID="your-spreadsheet-id"
```

**デフォルトのOAuth認証:**

このスキルはデフォルトでOAuth 2.0認証を使用します。

初回のみ以下の手順でトークンを取得してください：

```bash
# 初回認証（ブラウザで認証）
python3 -c "
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET_PATH = '/home/maki/.claude/skills/google-drive/config/credentials.json'
TOKEN_PATH = '/home/maki/.config/google-sheets-token.json'

creds = None
if os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
    with open(TOKEN_PATH, 'wb') as token:
        pickle.dump(creds, token)

print('Token saved to', TOKEN_PATH)
"
```

トークンは以下に保存されます：
```
/home/maki/.config/google-sheets-token.json
```

**サービスアカウントを使用する場合:**

サービスアカウントを使用したい場合は、`--credentials` 引数または `GOOGLE_CREDENTIALS_PATH` 環境変数で指定してください。

```bash
export GOOGLE_CREDENTIALS_PATH="/home/maki/.claude/skills/google-drive/config/service-account.json"
```

### 方法2: OAuth 2.0 認証（Webアプリ・個人利用向け）

ユーザー権限で操作する場合（Webアプリ、個人アカウントでアクセスする場合など）に適しています。

**設定手順:**

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクトを作成
2. 「APIとサービス」→「ライブラリ」から「Google Sheets API」を有効化
3. 「APIとサービス」→「同意画面」を設定：
   - **外部**を選択
   - アプリ名、ユーザーサポートメール、開発者連絡先情報を入力
   - スコープは「追加または削除」から `.../auth/spreadsheets` を選択
   - テストユーザーに自分のメールアドレスを追加
4. 「APIとサービス」→「認証情報」→「認証情報を作成」→「OAuthクライアントID」
5. アプリケーションの種類を選択：
   - **デスクトップアプリ**: CLIツールなど（`http://127.0.0.1` へのコールバック）
   - **Webアプリ**: Webサーバー向け
   - **その他**: コマンドラインツール向け
6. 作成したクライアントIDとシークレットを保存

**OAuth 2.0 でのトークン取得（初回のみ）:**

初回のみブラウザで認証を行い、トークンファイルを保存します。

```bash
# Pythonスクリプトで初回認証（token.json が保存される）
python3 -c "
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None

if os.path.exists('token.json'):
    with open('token.json', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'wb') as token:
        pickle.dump(creds, token)

print('Token saved to token.json')
"
```

**スクリプトをOAuth対応に改造する場合:**

各スクリプトの `get_credentials` 関数を以下のように修正：

```python
def get_credentials(credentials_path=None, token_path="token.json", client_secret_path="client_secret.json"):
    """OAuth 2.0 または サービスアカウントで認証情報を取得"""
    from google.oauth2 import service_account
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # OAuthトークンがあれば使用
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        if creds.valid:
            return creds
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            return creds

    # クライアントシークレットがあればOAuthフローを実行
    if os.path.exists(client_secret_path):
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        return creds

    # サービスアカウントにフォールバック
    if credentials_path is None:
        credentials_path = os.environ.get("GOOGLE_CREDENTIALS_PATH")
    if credentials_path and os.path.exists(credentials_path):
        return service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)

    raise Exception("No valid credentials found")
```

### 認証方法の選択ガイド

| 方法 | メリット | デメリット | 使い道 |
|------|----------|------------|--------|
| サービスアカウント | ユーザー操作不要、自動化に最適 | スプレッドシートへの共有設定が必要 | バッチ処理、CLIツール、サーバー処理 |
| OAuth 2.0 | ユーザー権限でアクセス、共有不要 | トークンの有効期限あり、更新が必要 | Webアプリ、個人利用ツール |

**環境変数の設定（共通）:**

```bash
export GOOGLE_SPREADSHEET_ID="your-spreadsheet-id"

# サービスアカウントの場合
export GOOGLE_CREDENTIALS_PATH="/path/to/credentials.json"

# OAuthの場合
export GOOGLE_TOKEN_PATH="/path/to/token.json"
export GOOGLE_CLIENT_SECRET_PATH="/path/to/client_secret.json"
```

## スプレッドシートIDの取得

スプレッドシートを開いたときのURLから取得できます：
```
https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit#gid=0
```

## スクリプト一覧

### write_cell.py - セルに値を書き込み

指定したセルに値を書き込みます。

```bash
python3 scripts/write_cell.py \
  --spreadsheet-id "your-id" \
  --sheet-name "シート1" \
  --cell "A1" \
  --value "Hello"
```

**引数:**
- `--spreadsheet-id`: スプレッドシートID（環境変数 `GOOGLE_SPREADSHEET_ID` 也可）
- `--sheet-name`: シート名（デフォルト: "シート1"）
- `--cell`: セル番地（例: A1, B2）
- `--value`: 書き込む値
- `--credentials`: 認証JSONのパス（環境変数 `GOOGLE_CREDENTIALS_PATH` 也可）

### append_row.py - 行を追加

シートの最後に行を追加します。レシートの記録などに最適です。

```bash
python3 scripts/append_row.py \
  --spreadsheet-id "your-id" \
  --sheet-name "シート1" \
  --values "2024-01-01,コンビニ,1200,食費"
```

**引数:**
- `--spreadsheet-id`: スプレッドシートID
- `--sheet-name`: シート名
- `--values`: カンマ区切りの値（例: "日付,店舗,金額,カテゴリ"）
- `--credentials`: 認証JSONのパス

### read_sheet.py - シートを読み込み

シートのデータを読み込みます。

```bash
# 全データを読み込み
python3 scripts/read_sheet.py \
  --spreadsheet-id "your-id" \
  --sheet-name "シート1"

# 特定の範囲を読み込み
python3 scripts/read_sheet.py \
  --spreadsheet-id "your-id" \
  --range "シート1!A1:D10"

# ヘッダー行を除外して読み込み
python3 scripts/read_sheet.py \
  --spreadsheet-id "your-id" \
  --sheet-name "シート1" \
  --skip-header
```

**引数:**
- `--spreadsheet-id`: スプレッドシートID
- `--sheet-name`: シート名（`--range` 指定時は不要）
- `--range`: A1記法の範囲（例: "シート1!A1:D10"）
- `--skip-header`: ヘッダー行を除外
- `--credentials`: 認証JSONのパス

### search.py - データを検索

シート内のデータを検索します。

```bash
# 値で検索
python3 scripts/search.py \
  --spreadsheet-id "your-id" \
  --sheet-name "シート1" \
  --value "コンビニ"

# 列を指定して検索
python3 scripts/search.py \
  --spreadsheet-id "your-id" \
  --sheet-name "シート1" \
  --column "B" \
  --value "コンビニ"

# 正規表現で検索
python3 scripts/search.py \
  --spreadsheet-id "your-id" \
  --sheet-name "シート1" \
  --column "C" \
  --pattern "^[0-9]+$"
```

**引数:**
- `--spreadsheet-id`: スプレッドシートID
- `--sheet-name`: シート名
- `--column`: 検索対象の列（A, B, C...）
- `--value`: 検索する値
- `--pattern`: 正規表現パターン（`--value` より優先）
- `--credentials`: 認証JSONのパス

### manage_sheets.py - シート管理

シートの作成、削除、名前変更、コピーを行います。

```bash
# シート一覧
python3 scripts/manage_sheets.py \
  --spreadsheet-id "your-id" \
  list

# シート作成
python3 scripts/manage_sheets.py \
  --spreadsheet-id "your-id" \
  create --name "家計簿2024"

# シート削除（シートID指定）
python3 scripts/manage_sheets.py \
  --spreadsheet-id "your-id" \
  delete --sheet-id 123456789

# シート名変更
python3 scripts/manage_sheets.py \
  --spreadsheet-id "your-id" \
  rename --sheet-id 0 --name "新しい名前"

# シートコピー
python3 scripts/manage_sheets.py \
  --spreadsheet-id "your-id" \
  duplicate --sheet-id 0 --name "コピー"
```

**コマンド:**
- `list`: シート一覧を表示
- `create --name NAME`: 新しいシートを作成
- `delete --sheet-id ID`: シートを削除
- `rename --sheet-id ID --name NAME`: シート名を変更
- `duplicate --sheet-id ID --name NAME`: シートをコピー

## 依存ライブラリ

このスキルを使用するには、以下のライブラリが必要です：

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## 使用例

### レシートの記録

```bash
python3 scripts/append_row.py \
  --spreadsheet-id "abc123..." \
  --sheet-name "家計簿" \
  --values "2024-01-01,コンビニ,1200,食費,おにぎりと飲み物"
```

### 家計簿の集計

まずデータを読み込み、その後に必要な集計を行います。

```bash
python3 scripts/read_sheet.py \
  --spreadsheet-id "abc123..." \
  --sheet-name "家計簿" \
  --skip-header
```

### 特定のカテゴリを検索

```bash
python3 scripts/search.py \
  --spreadsheet-id "abc123..." \
  --sheet-name "家計簿" \
  --column "D" \
  --value "食費"
```

## エラーハンドリング

### サービスアカウント認証の場合
- **認証エラー**: サービスアカウントのJSONファイルパスが正しいか確認
- **権限エラー**: スプレッドシートにサービスアカウント（メールアドレス）を共有しているか確認
- **シートが見つからない**: シート名が正しいか確認

### OAuth 2.0 認証の場合
- **認証エラー**: `token.json` または `client_secret.json` のパスを確認
- **トークン期限切れ**: トークンを再取得するか、リフレッシュトークンを確認
- **リダイレクトエラー**: OAuthアプリのリダイレクトURIが正しく設定されているか確認
- **権限スコープエラー**: 同意画面で `.../auth/spreadsheets` スコープが有効になっているか確認

### 共通のエラー
- **スプレッドシートIDが無効**: URLから正しくIDをコピーしているか確認
- **APIが有効になっていない**: Google Cloud Consoleで Google Sheets API を有効化
- **クォータ超過**: APIリクエスト回数が制限を超えていないか確認
