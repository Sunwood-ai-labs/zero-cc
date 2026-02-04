#!/usr/bin/env python3
"""
Google Drive フォルダ作成スクリプト

Google Driveに新しいフォルダを作成します。

使用方法:
    python gdrive_mkdir.py <FOLDER_NAME> [--parent FOLDER_ID]

オプション:
    --parent: 親フォルダのID (省略時はルートディレクトリ)

例:
    # ルートにフォルダを作成
    python gdrive_mkdir.py "プロジェクト資料"

    # 特定のフォルダの中に作成
    python gdrive_mkdir.py "2024年度" --parent 1ABC123xyz
"""

import sys
import argparse
from pathlib import Path

try:
    from googleapiclient.discovery import build
except ImportError:
    print("エラー: 必要なライブラリがインストールされていません")
    print("以下のコマンドでインストールしてください:")
    print("  pip install google-api-python-client google-auth-oauthlib")
    sys.exit(1)

from auth_helper import get_credentials


def create_folder(folder_name, parent_folder_id=None, token_file='../config/token.pickle'):
    """
    Google Driveに新しいフォルダを作成します。

    Args:
        folder_name: フォルダ名
        parent_folder_id: 親フォルダのID (Noneならルート)
        token_file: トークンファイルのパス

    Returns:
        作成したフォルダの情報
    """
    # 認証
    creds = get_credentials(token_file)
    service = build('drive', 'v3', credentials=creds)

    # フォルダメタデータ
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    # 親フォルダが指定されている場合
    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]

    print(f"フォルダを作成中: {folder_name}")
    if parent_folder_id:
        print(f"  親フォルダID: {parent_folder_id}")

    try:
        folder = service.files().create(
            body=folder_metadata,
            fields='id,name,webViewLink'
        ).execute()

        print(f"\nフォルダを作成しました！")
        print(f"  フォルダID: {folder.get('id')}")
        print(f"  フォルダ名: {folder.get('name')}")
        print(f"  リンク: {folder.get('webViewLink')}")

        return folder

    except Exception as e:
        print(f"エラー: フォルダの作成に失敗しました: {e}")
        raise


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='Google Driveにフォルダを作成'
    )
    parser.add_argument('folder_name', help='作成するフォルダ名')
    parser.add_argument(
        '--parent',
        help='親フォルダのID (省略時はルートディレクトリ)'
    )
    parser.add_argument(
        '--token',
        default='../config/token.pickle',
        help='トークンファイルのパス'
    )

    args = parser.parse_args()

    try:
        create_folder(
            args.folder_name,
            parent_folder_id=args.parent,
            token_file=args.token
        )
    except Exception as e:
        print(f"\nエラー: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
