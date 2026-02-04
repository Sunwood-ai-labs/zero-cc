#!/usr/bin/env python3
"""
Google Drive アップロードスクリプト

ローカルファイルをGoogle Driveにアップロードします。

使用方法:
    python gdrive_upload.py <file_path> [--parent FOLDER_ID] [--name FILE_NAME]

オプション:
    --parent: 親フォルダのID (省略時はルートディレクトリ)
    --name: 保存時のファイル名 (省略時は元のファイル名)

例:
    # ファイルをルートにアップロード
    python gdrive_upload.py ./document.pdf

    # 特定のフォルダにアップロード
    python gdrive_upload.py ./photo.jpg --parent 1ABC123xyz

    # ファイル名を指定してアップロード
    python gdrive_upload.py ./data.txt --name "backup_data.txt"
"""

import os
import sys
import argparse
import mimetypes
from pathlib import Path

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    import google.auth
except ImportError:
    print("エラー: 必要なライブラリがインストールされていません")
    print("以下のコマンドでインストールしてください:")
    print("  pip install google-api-python-client google-auth-oauthlib")
    sys.exit(1)

from auth_helper import get_credentials


def get_mime_type(file_path):
    """ファイルのMIMEタイプを取得"""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        # 判別できない場合はバイナリとして扱う
        mime_type = 'application/octet-stream'
    return mime_type


def upload_file(file_path, parent_folder_id=None, new_file_name=None, token_file='../config/token.pickle'):
    """
    ファイルをGoogle Driveにアップロードします。

    Args:
        file_path: アップロードするファイルのパス
        parent_folder_id: 親フォルダのID (Noneならルート)
        new_file_name: 保存時のファイル名 (Noneなら元のファイル名)
        token_file: トークンファイルのパス

    Returns:
        アップロードされたファイルの情報
    """
    # ファイルの存在確認
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    # 認証
    creds = get_credentials(token_file)
    service = build('drive', 'v3', credentials=creds)

    # ファイルメタデータ
    file_name = new_file_name or file_path.name
    mime_type = get_mime_type(file_path)

    file_metadata = {
        'name': file_name
    }

    # 親フォルダが指定されている場合
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    # ファイルのアップロード
    media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)

    print(f"アップロード中: {file_path.name}")
    print(f"  MIMEタイプ: {mime_type}")
    if parent_folder_id:
        print(f"  親フォルダID: {parent_folder_id}")

    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink,webContentLink'
        ).execute()

        print(f"\nアップロード完了！")
        print(f"  ファイルID: {file.get('id')}")
        print(f"  ファイル名: {file.get('name')}")
        print(f"  リンク: {file.get('webViewLink')}")

        return file

    except Exception as e:
        print(f"エラー: アップロードに失敗しました: {e}")
        raise


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='Google Driveにファイルをアップロード'
    )
    parser.add_argument('file_path', help='アップロードするファイルのパス')
    parser.add_argument(
        '--parent',
        help='親フォルダのID (省略時はルートディレクトリ)'
    )
    parser.add_argument(
        '--name',
        help='保存時のファイル名 (省略時は元のファイル名)'
    )
    parser.add_argument(
        '--token',
        default='../config/token.pickle',
        help='トークンファイルのパス'
    )

    args = parser.parse_args()

    try:
        upload_file(
            args.file_path,
            parent_folder_id=args.parent,
            new_file_name=args.name,
            token_file=args.token
        )
    except Exception as e:
        print(f"\nエラー: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
