# Google Drive API 認証設定手順

このガイドでは、Google Drive APIを使用するための認証設定の手順を説明します。

## 概要

Google Drive APIを使用するには、以下の手順が必要です：

1. Google Cloud Consoleでプロジェクトを作成
2. Drive APIを有効化
3. OAuth2同意画面を設定
4. OAuth2クライアントIDを作成
5. 認証スクリプトを実行

---

## 手順1: Google Cloud Consoleでプロジェクトを作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. Googleアカウントでログイン
3. プロジェクトを選択または新しいプロジェクトを作成
   - 上部のプロジェクトセレクタをクリック
   - 「新しいプロジェクト」をクリック
   - プロジェクト名を入力（例: `Google Drive API Tool`）
   - 「作成」をクリック

## 手順2: Drive APIを有効化

1. 左側のメニューから「APIとサービス」>「ライブラリ」を選択
2. 検索ボックスに「Google Drive API」と入力
3. 「Google Drive API」をクリック
4. 「有効にする」ボタンをクリック

## 手順3: OAuth同意画面を設定

1. 左側のメニューから「APIとサービス」>「OAuth同意画面」を選択
2. ユーザータイプを選択:
   - **外部**: 一般公開するアプリケーションの場合（個人利用はこちら）
   - **内部**: 組織内のみの利用の場合
3. 「作成」をクリック

### 必要な情報を入力

1. **アプリ情報**:
   - アプリ名（例: `My Drive Tool`）
   - ユーザーサポートメール（自分のメールアドレス）
   - デベロッパーの連絡先情報（自分のメールアドレス）

2. **スコープ**:
   - 「スコープを追加または削除」をクリック
   - `../drive.file` にチェック
   - `../drive` にチェック
   - 「更新」をクリック

3. **テストユーザー**:
   - 自分のメールアドレスを追加
   - 「保存」をクリック

## 手順4: OAuth2クライアントIDを作成

1. 左側のメニューから「APIとサービス」>「認証情報」を選択
2. 「+認証情報を作成」>「OAuthクライアントID」をクリック
3. アプリケーションの種類を選択:
   - **デスクトップアプリ**: コマンドラインスクリプトから使用する場合
4. 名前を入力（例: `Drive CLI Client`）
5. 「作成」をクリック

### 認証情報をダウンロード

1. 作成完了後、OAuthクライアントのポップアップが表示されます
2. 「JSONをダウンロード」をクリック
3. ダウンロードしたファイルを `credentials.json` にリネーム
4. スキルの `config/` ディレクトリに配置

```
google-drive/
├── config/
│   ├── credentials.json    ← 配置場所
│   └── token.pickle        ← 認証後に自動生成
├── scripts/
└── references/
```

## 手順5: 認証スクリプトを実行

1. 必要なライブラリをインストール:

```bash
pip install google-api-python-client google-auth-oauthlib
```

2. 認証スクリプトを実行:

```bash
cd /prj/zero-cc/.claude/skills/google-drive/scripts
python auth_setup.py
```

3. ブラウザが開き、Googleアカウントへの許可を求められます
4. 「許可」をクリック
5. 認証が成功すると、`token.pickle` が `config/` ディレクトリに保存されます

---

## 認証ファイルの配置構造

```
google-drive/
├── config/
│   ├── credentials.json    ← Google Cloud Consoleからダウンロード
│   └── token.pickle        ← auth_setup.py実行後に生成
├── scripts/
│   ├── auth_setup.py
│   ├── gdrive_upload.py
│   ├── gdrive_download.py
│   ├── gdrive_search.py
│   ├── gdrive_list.py
│   ├── gdrive_delete.py
│   └── gdrive_mkdir.py
└── references/
```

---

## トラブルシューティング

### エラー: "credentials.json が見つかりません"

`config/` ディレクトリに `credentials.json` が配置されているか確認してください。

### エラー: "トークンの更新に失敗しました"

古い `token.pickle` を削除して、再度 `auth_setup.py` を実行してください。

### エラー: "Redirect URI mismatch"

OAuthクライアントの設定で「デスクトップアプリ」を選択してください。

### エラー: "Access blocked"

OAuth同意画面で、自分のメールアドレスをテストユーザーに追加してください。

---

## セキュリティに関する注意

- `credentials.json` には機密情報が含まれています
- このファイルをGitリポジトリにコミットしないでください
- `.gitignore` に `config/credentials.json` を追加することを推奨します
- `token.pickle` もコミットしないでください

---

## 関連ドキュメント

- [API_REFERENCE.md](API_REFERENCE.md) - Google Drive APIの主なメソッドと検索クエリ構文
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - 各スクリプトの使用例
