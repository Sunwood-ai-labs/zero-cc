# Google Drive API リファレンス

このドキュメントでは、Google Drive API v3の主なメソッドと検索クエリ構文について説明します。

## 目次

1. [主なAPIメソッド](#主なapiメソッド)
2. [検索クエリ構文](#検索クエリ構文)
3. [MIMEタイプ](#mimeタイプ)
4. [フィールド](#フィールド)

---

## 主なAPIメソッド

### Files: list

ファイルとフォルダの一覧を取得します。

```python
service.files().list(
    q="クエリ文字列",
    fields="files(id,name,mimeType,size)",
    pageSize=100,
    orderBy="modifiedTime desc"
).execute()
```

### Files: get

ファイルのメタデータを取得します。

```python
service.files().get(
    fileId="ファイルID",
    fields='id,name,mimeType,size,webViewLink'
).execute()
```

### Files: create

新しいファイルまたはフォルダを作成します。

```python
service.files().create(
    body={'name': 'ファイル名', 'parents': ['親フォルダID']},
    media_body=MediaFileUpload('ファイルパス')
).execute()
```

### Files: update

ファイルのメタデータを更新します。

```python
service.files().update(
    fileId="ファイルID",
    body={'trashed': True}
).execute()
```

### Files: delete

ファイルを完全に削除します。

```python
service.files().delete(fileId="ファイルID").execute()
```

### Files: get_media

ファイルの内容をダウンロードします。

```python
request = service.files().get_media(fileId="ファイルID")
```

### Files: export

Google Workspaceファイル（Docs/Sheets/Slides）をエクスポートします。

```python
request = service.files().export(
    fileId="ファイルID",
    mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
```

---

## 検索クエリ構文

### 基本構文

```
フィールド名 演算子 '値'
```

### フィールド名

| フィールド | 説明 | 例 |
|----------|------|-----|
| `name` | ファイル名 | `name contains 'report'` |
| `mimeType` | MIMEタイプ | `mimeType = 'application/pdf'` |
| `parents` | 親フォルダID | `'folder_id' in parents` |
| `trashed` | ゴミ箱にあるか | `trashed = false` |
| `modifiedTime` | 更新日時 | `modifiedTime > '2024-01-01T00:00:00'` |
| `createdTime` | 作成日時 | `createdTime > '2024-01-01T00:00:00'` |
| `owners` | オーナー | `owners = 'user@example.com'` |
| `sharedWithMe` | 共有されたファイル | `sharedWithMe = true` |

### 演算子

| 演算子 | 説明 | 例 |
|-------|------|-----|
| `contains` | 含む | `name contains 'invoice'` |
| `=` | 等しい | `name = 'document.pdf'` |
| `!=` | 等しくない | `mimeType != 'application/pdf'` |
| `<` | 小さい | `modifiedTime < '2024-01-01'` |
| `<=` | 以下 | `modifiedTime <= '2024-01-01'` |
| `>` | 大きい | `modifiedTime > '2024-01-01'` |
| `>=` | 以上 | `modifiedTime >= '2024-01-01'` |
| `in` | 配列に含まれる | `'folder_id' in parents` |

### 論理演算子

| 演算子 | 説明 | 例 |
|-------|------|-----|
| `and` | かつ | `name contains 'report' and mimeType = 'application/pdf'` |
| `or` | または | `name contains 'invoice' or name contains 'receipt'` |
| `not` | 否定 | `not trashed` |

### クエリ例

```python
# ファイル名で検索
"name contains 'report'"

# 特定のフォルダ内のPDFファイル
"'folder_id' in parents and mimeType = 'application/pdf' and trashed = false"

# 最近更新されたファイル
"modifiedTime > '2024-01-01T00:00:00' and trashed = false"

# Google Docsのみ
"mimeType = 'application/vnd.google-apps.document' and trashed = false"

# 共有されたファイル
"sharedWithMe = true"

# 複数の条件
"(name contains 'invoice' or name contains 'receipt') and modifiedTime > '2024-01-01T00:00:00'"
```

---

## MIMEタイプ

### Google Workspaceファイル

| MIMEタイプ | 説明 |
|-----------|------|
| `application/vnd.google-apps.document` | Google Docs |
| `application/vnd.google-apps.spreadsheet` | Google Sheets |
| `application/vnd.google-apps.presentation` | Google Slides |
| `application/vnd.google-apps.drawing` | Google Drawings |
| `application/vnd.google-apps.forms` | Google Forms |
| `application/vnd.google-apps.folder` | フォルダ |
| `application/vnd.google-apps.shortcut` | ショートカット |

### 一般的なファイルタイプ

| MIMEタイプ | 説明 | エクスポート形式 |
|-----------|------|----------------|
| `application/pdf` | PDF | - |
| `image/jpeg` | JPEG画像 | - |
| `image/png` | PNG画像 | - |
| `image/gif` | GIF画像 | - |
| `text/plain` | テキストファイル | - |
| `application/zip` | ZIPアーカイブ | - |
| `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Word (.docx) | - |
| `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | Excel (.xlsx) | - |
| `application/vnd.openxmlformats-officedocument.presentationml.presentation` | PowerPoint (.pptx) | - |

### エクスポート用MIMEタイプ

Google Workspaceファイルをダウンロードする際、以下のMIMEタイプでエクスポートできます：

| ファイルタイプ | エクスポートMIMEタイプ | 拡張子 |
|---------------|----------------------|--------|
| Google Docs | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | .docx |
| Google Docs | `application/pdf` | .pdf |
| Google Docs | `text/plain` | .txt |
| Google Sheets | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | .xlsx |
| Google Sheets | `application/pdf` | .pdf |
| Google Sheets | `text/csv` | .csv |
| Google Slides | `application/vnd.openxmlformats-officedocument.presentationml.presentation` | .pptx |
| Google Slides | `application/pdf` | .pdf |

---

## フィールド

### Filesリソースの主なフィールド

| フィールド | タイプ | 説明 |
|----------|--------|------|
| `id` | string | ファイルの一意のID |
| `name` | string | ファイル名 |
| `mimeType` | string | ファイルのMIMEタイプ |
| `description` | string | ファイルの説明 |
| `parents` | array | 親フォルダのID配列 |
| `size` | long | ファイルサイズ（バイト） |
| `createdTime` | datetime | 作成日時（RFC 3339） |
| `modifiedTime` | datetime | 更新日時（RFC 3339） |
| `trashed` | boolean | ゴミ箱にあるか |
| `webViewLink` | string | ブラウザで開くためのリンク |
| `webContentLink` | string | コンテンツをダウンロードするリンク |
| `owners` | array | ファイルオーナーの情報 |
| `shared` | boolean | 共有されているか |
| `capabilities` | object | 現在のユーザーの権限 |

### リクエスト用fieldsパラメータの例

```
# 最小限の情報
files(id,name)

# 基本的な情報
files(id,name,mimeType,size)

# 詳細な情報
files(id,name,mimeType,size,createdTime,modifiedTime,webViewLink,parents)

# 全ての情報
files(*)
```

---

## 日時フォーマット

日時は[RFC 3339](https://www.rfc-editor.org/rfc/rfc3339)形式で指定します。

```
2024-01-01T00:00:00
2024-01-01T00:00:00Z      # UTC
2024-01-01T09:00:00+09:00 # JST
```

### 日時クエリの例

```python
# 特定の日以降に更新されたファイル
"modifiedTime > '2024-01-01T00:00:00'"

# 特定の期間内に作成されたファイル
"createdTime >= '2024-01-01T00:00:00' and createdTime <= '2024-12-31T23:59:59'"

# 過去30日以内に更新されたファイル
"modifiedTime > '2024-01-05T00:00:00'"
```

---

## 関連ドキュメント

- [SETUP.md](SETUP.md) - Google Cloud Consoleでの認証設定手順
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - 各スクリプトの使用例
- [Google Drive API公式ドキュメント](https://developers.google.com/drive/api/v3/reference)
