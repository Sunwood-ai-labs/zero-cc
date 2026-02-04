#!/usr/bin/env python3
"""
Google Drive ダウンロードスクリプト

Google Driveからファイルをダウンロードします。

使用方法:
    # ファイルIDで指定
    python gdrive_download.py --id FILE_ID [--output OUTPUT_PATH]

    # ファイル名で検索してダウンロード
    python gdrive_download.py --name FILE_NAME [--parent FOLDER_ID] [--output OUTPUT_PATH]

オプション:
    --id: ファイルID (--nameとのどちらか必須)
    --name: ファイル名 (--idとのどちらか必須)
    --parent: 検索時の親フォルダID (--name使用時)
    --output: 保存先パス (省略時はカレントディレクトリに元の名前で保存)

例:
    # ファイルIDでダウンロード
    python gdrive_download.py --id 1ABC123xyz --output ./downloaded.pdf

    # ファイル名で検索してダウンロード
    python gdrive_download.py --name "report.pdf" --output ./downloads/

    # 特定フォルダ内のファイルを名前で検索
    python gdrive_download.py --name "data.csv" --parent 1ABC123xyz
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    import google.auth
except ImportError:
    print("エラー: 必要なライブラリがインストールされていません")
    print("以下のコマンドでインストールしてください:")
    print("  pip install google-api-python-client google-auth-oauthlib")
    sys.exit(1)

import io
from auth_helper import get_credentials


def find_file_by_name(service, file_name, parent_folder_id=None):
    """
    ファイル名でファイルを検索します。

    Args:
        service: Drive APIサービスオブジェクト
        file_name: 検索するファイル名
        parent_folder_id: 親フォルダのID (指定するとフォルダ内のみ検索)

    Returns:
        ファイル情報の辞書、見つからない場合はNone
    """
    # 検索クエリを構築
    query = f"name = '{file_name}' and trashed = false"

    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"

    try:
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType, size, parents)",
            pageSize=10
        ).execute()

        files = results.get('files', [])

        if not files:
            return None

        # 複数見つかった場合は最初のものを返す
        if len(files) > 1:
            print(f"注意: {len(files)}個のファイルが見つかりました。最初のものをダウンロードします。")

        return files[0]

    except Exception as e:
        print(f"エラー: ファイルの検索に失敗しました: {e}")
        raise


def download_file(file_id, output_path=None, token_file='../config/token.pickle'):
    """
    Google Driveからファイルをダウンロードします。

    Args:
        file_id: ファイルID
        output_path: 保存先パス (省略時はカレントディレクトリ)
        token_file: トークンファイルのパス

    Returns:
        ダウンロードしたファイルのパス
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
        raise

    file_name = file_info.get('name')
    mime_type = file_info.get('mimeType')

    # Google Workspaceファイル（Docs, Sheets, Slides）の場合
    # これらはexport APIを使用してダウンロード
    export_mime_types = {
        'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.google-apps.presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    }

    # 保存先パスを決定
    if output_path:
        output_path = Path(output_path)
        if output_path.is_dir():
            # ディレクトリ指定の場合
            output_file = output_path / file_name
        else:
            # ファイルパス指定の場合
            output_file = output_path

            # Google Workspaceファイルの場合、拡張子を変更
            if mime_type in export_mime_types and not output_file.suffix:
                # 拡張子を付与
                ext_map = {
                    'application/vnd.google-apps.document': '.docx',
                    'application/vnd.google-apps.spreadsheet': '.xlsx',
                    'application/vnd.google-apps.presentation': '.pptx',
                }
                output_file = output_file.with_suffix(ext_map[mime_type])
    else:
        output_file = Path(file_name)
        if mime_type in export_mime_types:
            ext_map = {
                'application/vnd.google-apps.document': '.docx',
                'application/vnd.google-apps.spreadsheet': '.xlsx',
                'application/vnd.google-apps.presentation': '.pptx',
            }
            output_file = output_file.with_suffix(ext_map[mime_type])

    print(f"ダウンロード中: {file_name}")
    print(f"  ファイルID: {file_id}")
    print(f"  MIMEタイプ: {mime_type}")

    try:
        if mime_type in export_mime_types:
            # Google Workspaceファイルのエクスポート
            export_mime = export_mime_types[mime_type]
            request = service.files().export_media(
                fileId=file_id,
                mimeType=export_mime
            )

            with io.BytesIO() as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"  進捗: {int(status.progress() * 100)}%")

                # ファイルに書き込み
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, 'wb') as f:
                    f.write(fh.getvalue())

        else:
            # 通常のファイルのダウンロード
            request = service.files().get_media(fileId=file_id)

            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"  進捗: {int(status.progress() * 100)}%")

        print(f"\nダウンロード完了！")
        print(f"  保存先: {output_file.absolute()}")

        return str(output_file.absolute())

    except Exception as e:
        print(f"エラー: ダウンロードに失敗しました: {e}")
        raise


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='Google Driveからファイルをダウンロード'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--id', help='ファイルID')
    group.add_argument('--name', help='ファイル名')

    parser.add_argument(
        '--parent',
        help='親フォルダのID (--name使用時、フォルダ内のみ検索)'
    )
    parser.add_argument(
        '--output',
        help='保存先パス (省略時はカレントディレクトリに元の名前で保存)'
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

        download_file(
            file_id,
            output_path=args.output,
            token_file=args.token
        )

    except Exception as e:
        print(f"\nエラー: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
