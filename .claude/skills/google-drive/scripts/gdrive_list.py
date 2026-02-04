#!/usr/bin/env python3
"""
Google Drive 一覧スクリプト

Google Driveのフォルダ内のファイル・フォルダ一覧を表示します。

使用方法:
    python gdrive_list.py [--folder FOLDER_ID] [--recursive] [--limit N]

オプション:
    --folder: フォルダID (省略時はルートディレクトリ 'root')
    --recursive: サブフォルダも再帰的に表示
    --limit: 1フォルダあたりの最大表示数 (デフォルト: 50)
    --json: JSON形式で出力
    --folders-only: フォルダのみを表示
    --files-only: ファイルのみを表示

例:
    # ルートディレクトリの内容を表示
    python gdrive_list.py

    # 特定のフォルダの内容を表示
    python gdrive_list.py --folder 1ABC123xyz

    # 再帰的に全てのファイルを表示
    python gdrive_list.py --recursive

    # フォルダのみを表示
    python gdrive_list.py --folders-only
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

try:
    from googleapiclient.discovery import build
except ImportError:
    print("エラー: 必要なライブラリがインストールされていません")
    print("以下のコマンドでインストールしてください:")
    print("  pip install google-api-python-client google-auth-oauthlib")
    sys.exit(1)

from auth_helper import get_credentials


def format_size(size_bytes):
    """バイト単位を人間が読みやすい形式に変換"""
    if size_bytes is None:
        return "N/A"

    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def format_date(date_str):
    """日付文字列を整形"""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return date_str


def get_file_type_name(mime_type):
    """MIMEタイプを日本語のファイルタイプに変換"""
    type_map = {
        'application/vnd.google-apps.document': 'Google Docs',
        'application/vnd.google-apps.spreadsheet': 'Google Sheets',
        'application/vnd.google-apps.presentation': 'Google Slides',
        'application/vnd.google-apps.folder': 'フォルダ',
        'application/pdf': 'PDF',
        'application/zip': 'ZIP',
        'image/jpeg': 'JPEG画像',
        'image/png': 'PNG画像',
        'image/gif': 'GIF画像',
        'text/plain': 'テキスト',
    }

    return type_map.get(mime_type, mime_type)


def list_folder(folder_id='root', service=None, token_file='../config/token.pickle',
                limit=50, folders_only=False, files_only=False):
    """
    フォルダ内のファイル・フォルダ一覧を取得します。

    Args:
        folder_id: フォルダID ('root'でルートディレクトリ)
        service: Drive APIサービスオブジェクト (省略時は新規作成)
        token_file: トークンファイルのパス
        limit: 最大取得数
        folders_only: フォルダのみを取得
        files_only: ファイルのみを取得

    Returns:
        ファイル・フォルダのリスト
    """
    # サービスが未指定の場合は新規作成
    if service is None:
        creds = get_credentials(token_file)
        service = build('drive', 'v3', credentials=creds)

    # クエリを構築
    query = f"'{folder_id}' in parents and trashed = false"

    if folders_only:
        query += " and mimeType = 'application/vnd.google-apps.folder'"
    elif files_only:
        query += " and mimeType != 'application/vnd.google-apps.folder'"

    try:
        # フォルダ情報も取得
        folder_info = None
        if folder_id != 'root':
            folder_info = service.files().get(
                fileId=folder_id,
                fields='id,name'
            ).execute()

        # ファイル一覧を取得
        results = service.files().list(
            q=query,
            fields="files(id,name,mimeType,size,createdTime,modifiedTime,webViewLink)",
            pageSize=limit,
            orderBy="name"
        ).execute()

        items = results.get('files', [])

        # フォルダ情報を含めて返す
        return {
            'folder': folder_info,
            'items': items
        }

    except Exception as e:
        print(f"エラー: ファイル一覧の取得に失敗しました: {e}")
        raise


def list_recursive(folder_id='root', token_file='../config/token.pickle',
                   limit=50, indent=0, folders_only=False, files_only=False):
    """
    フォルダを再帰的に表示します。

    Args:
        folder_id: 開始フォルダID
        token_file: トークンファイルのパス
        limit: 最大取得数
        indent: インデントレベル
        folders_only: フォルダのみを取得
        files_only: ファイルのみを取得
    """
    creds = get_credentials(token_file)
    service = build('drive', 'v3', credentials=creds)

    # フォルダ情報を取得
    if folder_id == 'root':
        folder_name = 'マイドライブ'
    else:
        folder_info = service.files().get(
            fileId=folder_id,
            fields='name'
        ).execute()
        folder_name = folder_info.get('name', folder_id)

    indent_str = "  " * indent
    print(f"{indent_str}📁 {folder_name} ({folder_id})")

    # 内容を取得
    result = list_folder(
        folder_id=folder_id,
        service=service,
        token_file=token_file,
        limit=limit,
        folders_only=folders_only,
        files_only=files_only
    )

    items = result['items']

    # ファイル/フォルダを表示
    for item in items:
        mime_type = item.get('mimeType')
        name = item.get('name')

        if mime_type == 'application/vnd.google-apps.folder':
            print(f"{indent_str}  📂 {name} ({item.get('id')})")

            # 再帰的にサブフォルダを表示
            if not files_only:
                list_recursive(
                    folder_id=item.get('id'),
                    token_file=token_file,
                    limit=limit,
                    indent=indent + 2,
                    folders_only=folders_only,
                    files_only=files_only
                )
        else:
            type_name = get_file_type_name(mime_type)
            size = format_size(item.get('size'))
            print(f"{indent_str}  📄 {name}")
            print(f"{indent_str}     タイプ: {type_name}, サイズ: {size}")


def print_result(result, show_details=False):
    """検索結果を表示"""
    folder = result.get('folder')
    items = result.get('items', [])

    # フォルダ名を表示
    if folder:
        print(f"\nフォルダ: {folder.get('name')} (ID: {folder.get('id')})")
    else:
        print(f"\nフォルダ: マイドライブ (ルート)")

    # ファイル数を表示
    folder_count = sum(1 for i in items if i.get('mimeType') == 'application/vnd.google-apps.folder')
    file_count = len(items) - folder_count

    print(f"フォルダ: {folder_count}, ファイル: {file_count}")

    if not items:
        print("(空のフォルダです)")
        return

    # 各アイテムを表示
    for i, item in enumerate(items, 1):
        mime_type = item.get('mimeType')
        name = item.get('name')

        if mime_type == 'application/vnd.google-apps.folder':
            icon = "📂"
            type_name = "フォルダ"
        else:
            icon = "📄"
            type_name = get_file_type_name(mime_type)

        print(f"\n{i}. {icon} {name}")
        print(f"   ID: {item.get('id')}")
        print(f"   タイプ: {type_name}")

        if show_details:
            if item.get('size'):
                print(f"   サイズ: {format_size(int(item.get('size')))}")
            if item.get('modifiedTime'):
                print(f"   更新日時: {format_date(item.get('modifiedTime'))}")
            if item.get('webViewLink'):
                print(f"   リンク: {item.get('webViewLink')}")


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='Google Driveのフォルダ内のファイル・フォルダ一覧を表示'
    )
    parser.add_argument(
        '--folder',
        default='root',
        help='フォルダID (省略時はルートディレクトリ)'
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='サブフォルダも再帰的に表示'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='1フォルダあたりの最大表示数 (デフォルト: 50)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='JSON形式で出力'
    )
    parser.add_argument(
        '--folders-only',
        action='store_true',
        help='フォルダのみを表示'
    )
    parser.add_argument(
        '--files-only',
        action='store_true',
        help='ファイルのみを表示'
    )
    parser.add_argument(
        '--details',
        action='store_true',
        help='詳細情報を表示'
    )
    parser.add_argument(
        '--token',
        default='../config/token.pickle',
        help='トークンファイルのパス'
    )

    args = parser.parse_args()

    try:
        if args.recursive:
            # 再帰的表示
            list_recursive(
                folder_id=args.folder,
                token_file=args.token,
                limit=args.limit,
                folders_only=args.folders_only,
                files_only=args.files_only
            )
        else:
            # 通常のリスト表示
            result = list_folder(
                folder_id=args.folder,
                token_file=args.token,
                limit=args.limit,
                folders_only=args.folders_only,
                files_only=args.files_only
            )

            if args.json:
                # JSON形式で出力
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                # 人間が読みやすい形式で出力
                print_result(result, show_details=args.details)

    except Exception as e:
        print(f"\nエラー: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
