#!/usr/bin/env python3
"""
Google Drive API 認証設定スクリプト

このスクリプトは、Google Drive APIを使用するためのOAuth2認証をセットアップします。
Google Cloud Consoleで取得したcredentials.jsonを使用して、最初の認証を行い、
token.pickleを保存します。

使用方法:
    python auth_setup.py [--credentials CREDENTIALS_FILE] [--token TOKEN_FILE]

オプション:
    --credentials: credentials.jsonのパス (デフォルト: ../config/credentials.json)
    --token: token.pickleの保存先パス (デフォルト: ../config/token.pickle)
"""

import os
import pickle
import argparse
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
except ImportError:
    print("エラー: 必要なライブラリがインストールされていません")
    print("以下のコマンドでインストールしてください:")
    print("  pip install google-auth-oauthlib google-auth-httplib2")
    exit(1)

# Google Drive APIのスコープ
# 読み取りと書き込みの両方を許可
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
]


def authenticate(credentials_file: str, token_file: str) -> Credentials:
    """
    OAuth2認証を行い、Credentialsオブジェクトを返します。

    Args:
        credentials_file: credentials.jsonのパス
        token_file: token.pickleのパス

    Returns:
        認証されたCredentialsオブジェクト
    """
    creds = None

    # 保存されたトークンがあれば読み込む
    token_path = Path(token_file)
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # トークンがない、または有効期限切れの場合は再認証
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("トークンを更新しました")
            except Exception as e:
                print(f"トークンの更新に失敗しました: {e}")
                creds = None

        if not creds:
            # credentials.jsonから認証フローを作成
            if not Path(credentials_file).exists():
                raise FileNotFoundError(
                    f"{credentials_file} が見つかりません。\n"
                    "Google Cloud ConsoleでOAuth2クライアントIDを作成し、\n"
                    "credentials.jsonをダウンロードしてください。\n"
                    "詳細は references/SETUP.md を参照してください。"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # トークンを保存
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        print(f"トークンを {token_file} に保存しました")

    return creds


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='Google Drive API 認証設定')
    parser.add_argument(
        '--credentials',
        default='../config/credentials.json',
        help='credentials.jsonのパス (デフォルト: ../config/credentials.json)'
    )
    parser.add_argument(
        '--token',
        default='../config/token.pickle',
        help='token.pickleのパス (デフォルト: ../config/token.pickle)'
    )

    args = parser.parse_args()

    try:
        print("Google Drive API 認証を開始します...")
        print("ブラウザが開き、Googleアカウントへの許可を求められます")

        creds = authenticate(args.credentials, args.token)

        print("\n認証に成功しました！")
        print(f"トークンファイル: {args.token}")
        print("\nこれでGoogle Drive APIを使用する準備が整いました。")

    except FileNotFoundError as e:
        print(f"\nエラー: {e}")
        exit(1)
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        exit(1)


if __name__ == '__main__':
    main()
