#!/usr/bin/env python3
"""
Google Drive 削除スクリプト

Google Driveからファイルを削除（ゴミ箱へ移動または完全削除）します。

使用方法:
    # ファイルIDで指定してゴミ箱へ移動
    python gdrive_delete.py --id FILE_ID

    # ファイル名で検索してゴミ箱へ移動
    python gdrive_delete.py --name FILE_NAME [--parent FOLDER_ID]

    # 完全に削除
    python gdrive_delete.py --id FILE_ID --permanent

オプション:
    --id: ファイルID (--nameとのどちらか必須)
    --name: ファイル名 (--idとのどちらか必須)
    --parent: 検索時の親フォルダID (--name使用時)
    --permanent: 完全削除（省略時はゴミ箱へ移動）
    --dry-run: 削除せずに確認のみ

例:
    # ファイルIDでゴミ箱へ移動
    python gdrive_delete.py --id 1ABC123xyz

    # 完全に削除
    python gdrive_delete.py --id 1ABC123xyz --permanent

    # ファイル名で検索して削除確認
    python gdrive_delete.py --name "old_file.txt" --dry-run
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


def find_file_by_name(service, file_name, parent_folder_id=None):
    """
    ファイル名でファイルを検索します。

    Args:
        service: Drive APIサービスオブジェクト
        file_name: 検索するファイル名
        parent_folder_id: 親フォルダのID

    Returns:
        ファイル情報の辞書、見つからない場合はNone
    """
    query = f"name = '{file_name}' and trashed = false"

    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"

    try:
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType, size)",
            pageSize=10
        ).execute()

        files = results.get('files', [])

        if not files:
            return None

        if len(files) > 1:
            print(f"注意: {len(files)}個のファイルが見つかりました。最初のものを削除します。")

        return files[0]

    except Exception as e:
        print(f"エラー: ファイルの検索に失敗しました: {e}")
        raise


def delete_file(file_id, permanent=False, dry_run=False, token_file='../config/token.pickle'):
    """
    Google Driveからファイルを削除します。

    Args:
        file_id: ファイルID
        permanent: 完全削除フラグ（Falseならゴミ箱へ移動）
        dry_run: ドライランフラグ（確認のみ）
        token_file: トークンファイルのパス

    Returns:
        削除が成功したかどうか
    """
    # 認証
    creds = get_credentials(token_file)
    service = build('drive', 'v3', credentials=creds)

    # ファイル情報を取得
    try:
        file_info = service.files().get(
            fileId=file_id,
            fields='id,name,mimeType,size'
        ).execute()
    except Exception as e:
        print(f"エラー: ファイル情報の取得に失敗しました: {e}")
        return False

    file_name = file_info.get('name')
    mime_type = file_info.get('mimeType')

    # Google Workspaceフォルダ
    folder_types = {
        'application/vnd.google-apps.folder': 'フォルダ',
        'application/vnd.google-apps.document': 'Google Docs',
        'application/vnd.google-apps.spreadsheet': 'Google Sheets',
        'application/vnd.google-apps.presentation': 'Google Slides',
    }

    type_name = folder_types.get(mime_type, 'ファイル')

    # 確認メッセージ
    if permanent:
        action = "完全に削除"
    else:
        action = "ゴミ箱へ移動"

    print(f"\n{type_name}を{action}します:")
    print(f"  名前: {file_name}")
    print(f"  ID: {file_id}")

    if file_info.get('size'):
        size_mb = int(file_info.get('size')) / (1024 * 1024)
        print(f"  サイズ: {size_mb:.2f} MB")

    if dry_run:
        print("\n[ドライラン] 実際の削除は行いません")
        return True

    # 確認
    response = input("\nよろしいですか？ (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("キャンセルしました")
        return False

    try:
        if permanent:
            # 完全削除
            service.files().delete(fileId=file_id).execute()
        else:
            # ゴミ箱へ移動
            service.files().update(
                fileId=file_id,
                body={'trashed': True}
            ).execute()

        print(f"\n{type_name}を{action}しました")
        return True

    except Exception as e:
        print(f"\nエラー: 削除に失敗しました: {e}")
        return False


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='Google Driveからファイルを削除'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--id', help='ファイルID')
    group.add_argument('--name', help='ファイル名')

    parser.add_argument(
        '--parent',
        help='親フォルダのID (--name使用時、フォルダ内のみ検索)'
    )
    parser.add_argument(
        '--permanent',
        action='store_true',
        help='完全削除（省略時はゴミ箱へ移動）'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='削除せずに確認のみ'
    )
    parser.add_argument(
        '--token',
        default='../config/token.pickle',
        help='トークンファイルのパス'
    )

    args = parser.parse_args()

    try:
        if args.name:
            # ファイル名で検索
            print(f"ファイル名で検索中: {args.name}")
            creds = get_credentials(args.token)
            service = build('drive', 'v3', credentials=creds)

            file_info = find_file_by_name(
                service,
                args.name,
                parent_folder_id=args.parent
            )

            if not file_info:
                print(f"ファイルが見つかりません: {args.name}")
                sys.exit(1)

            file_id = file_info['id']
            print(f"ファイルが見つかりました (ID: {file_id})")
        else:
            file_id = args.id

        success = delete_file(
            file_id,
            permanent=args.permanent,
            dry_run=args.dry_run,
            token_file=args.token
        )

        if not success:
            sys.exit(1)

    except Exception as e:
        print(f"\nエラー: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
