#!/usr/bin/env python3
"""
Google Drive 検索スクリプト

Google Drive内のファイルを検索します。

使用方法:
    python gdrive_search.py <QUERY> [--mime-type MIME] [--parent FOLDER_ID] [--limit N]

オプション:
    --mime-type: MIMEタイプでフィルタ (例: application/pdf, image/png)
    --parent: 親フォルダのIDでフィルタ
    --limit: 結果の最大数 (デフォルト: 20)
    --json: JSON形式で出力

クエリ構文:
    ファイル名の検索: name contains 'keyword'
    完全一致: name = 'filename'
    複数の単語: name contains 'word1' and name contains 'word2'
    日付範囲: modifiedTime > '2023-01-01T00:00:00'

例:
    # ファイル名で検索
    python gdrive_search.py "report"

    # 特定のフォルダ内でPDFを検索
    python gdrive_search.py "invoice" --parent 1ABC123xyz --mime-type application/pdf

    # Google Docsを検索
    python gdrive_search.py "proposal" --mime-type application/vnd.google-apps.document
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


def build_search_query(query, mime_type=None, parent_folder_id=None):
    """
    検索クエリ文字列を構築します。

    Args:
        query: 検索キーワード
        mime_type: MIMEタイプ
        parent_folder_id: 親フォルダID

    Returns:
        検索クエリ文字列
    """
    # 基本クエリ（ゴミ箱を除外）
    search_query = "trashed = false"

    # キーワードが含まれている場合
    if query:
        # クエリが演算子を含んでいる場合はそのまま使用
        if any(op in query for op in [' contains ', ' = ', ' > ', ' < ', ' >= ', ' <= ']):
            search_query += f" and ({query})"
        else:
            # 簡単なキーワード検索
            search_query += f" and name contains '{query}'"

    # MIMEタイプでフィルタ
    if mime_type:
        search_query += f" and mimeType = '{mime_type}'"

    # 親フォルダでフィルタ
    if parent_folder_id:
        search_query += f" and '{parent_folder_id}' in parents"

    return search_query


def search_files(query, mime_type=None, parent_folder_id=None, limit=20, token_file='../config/token.pickle'):
    """
    Google Drive内のファイルを検索します。

    Args:
        query: 検索クエリ
        mime_type: MIMEタイプ
        parent_folder_id: 親フォルダID
        limit: 最大結果数
        token_file: トークンファイルのパス

    Returns:
        検索結果のファイルリスト
    """
    # 認証
    creds = get_credentials(token_file)
    service = build('drive', 'v3', credentials=creds)

    # クエリを構築
    search_query = build_search_query(query, mime_type, parent_folder_id)

    print(f"検索クエリ: {search_query}")
    print("検索中...")

    try:
        results = service.files().list(
            q=search_query,
            fields="files(id,name,mimeType,size,createdTime,modifiedTime,webViewLink,parents)",
            pageSize=limit,
            orderBy="modifiedTime desc"
        ).execute()

        files = results.get('files', [])

        return files

    except Exception as e:
        print(f"エラー: 検索に失敗しました: {e}")
        raise


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
        'image/jpeg': 'JPEG画像',
        'image/png': 'PNG画像',
        'text/plain': 'テキスト',
    }

    return type_map.get(mime_type, mime_type)


def print_results(files):
    """検索結果を表示"""
    if not files:
        print("\nファイルが見つかりませんでした")
        return

    print(f"\n見つかりました: {len(files)}件")

    for i, file in enumerate(files, 1):
        print(f"\n--- {i} ---")
        print(f"名前: {file.get('name')}")
        print(f"ID: {file.get('id')}")
        print(f"タイプ: {get_file_type_name(file.get('mimeType'))}")

        if file.get('size'):
            print(f"サイズ: {format_size(int(file.get('size')))}")

        if file.get('modifiedTime'):
            print(f"更新日時: {format_date(file.get('modifiedTime'))}")

        if file.get('webViewLink'):
            print(f"リンク: {file.get('webViewLink')}")


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='Google Drive内のファイルを検索'
    )
    parser.add_argument('query', nargs='?', default='', help='検索キーワード')
    parser.add_argument(
        '--mime-type',
        help='MIMEタイプでフィルタ'
    )
    parser.add_argument(
        '--parent',
        help='親フォルダのIDでフィルタ'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=20,
        help='結果の最大数 (デフォルト: 20)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='JSON形式で出力'
    )
    parser.add_argument(
        '--token',
        default='../config/token.pickle',
        help='トークンファイルのパス'
    )

    args = parser.parse_args()

    try:
        files = search_files(
            args.query,
            mime_type=args.mime_type,
            parent_folder_id=args.parent,
            limit=args.limit,
            token_file=args.token
        )

        if args.json:
            # JSON形式で出力
            print(json.dumps(files, ensure_ascii=False, indent=2))
        else:
            # 人間が読みやすい形式で出力
            print_results(files)

    except Exception as e:
        print(f"\nエラー: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
