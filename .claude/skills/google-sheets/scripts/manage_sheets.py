#!/usr/bin/env python3
"""シートを作成・削除・管理するスクリプト"""

import argparse
import os
import sys

try:
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
except ImportError:
    print("Error: Required libraries not installed.")
    print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)


def get_credentials(credentials_path=None):
    """認証情報を取得 (OAuth 2.0 または サービスアカウント)"""
    # OAuth 2.0 トークンパス（デフォルト）
    DEFAULT_TOKEN_PATH = "/home/maki/.config/google-sheets-token.json"
    # サービスアカウントパス（環境変数または引数で指定）
    DEFAULT_SERVICE_ACCOUNT_PATH = "/home/maki/.claude/skills/google-drive/config/service-account.json"

    # サービスアカウントが明示的に指定された場合
    if credentials_path is not None:
        if not os.path.exists(credentials_path):
            print(f"Error: Credentials file not found: {credentials_path}")
            sys.exit(1)
        return service_account.Credentials.from_service_account_file(credentials_path)

    # 環境変数でサービスアカウントが指定された場合
    service_account_path = os.environ.get("GOOGLE_CREDENTIALS_PATH")
    if service_account_path:
        if not os.path.exists(service_account_path):
            print(f"Error: Service account file not found: {service_account_path}")
            sys.exit(1)
        return service_account.Credentials.from_service_account_file(service_account_path)

    # OAuth 2.0 トークンを使用（デフォルト）
    token_path = os.environ.get("GOOGLE_TOKEN_PATH", DEFAULT_TOKEN_PATH)

    if os.path.exists(token_path):
        import pickle
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

        if creds.valid:
            return creds

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            return creds

    # トークンが見つからない場合
    print(f"Error: OAuth token not found: {token_path}")
    print("Please run the initial OAuth setup:")
    print("  python3 -c \"")
    print("  from google_auth_oauthlib.flow import InstalledAppFlow")
    print("  from google.auth.transport.requests import Request")
    print("  import pickle, os")
    print("  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']")
    print("  flow = InstalledAppFlow.from_client_secrets_file('/home/maki/.claude/skills/google-drive/config/credentials.json', SCOPES)")
    print("  creds = flow.run_local_server(port=0)")
    print("  with open('/home/maki/.config/google-sheets-token.json', 'wb') as f:")
    print("    pickle.dump(creds, f)")
    print("  \"")
    sys.exit(1)


def list_sheets(spreadsheet_id, credentials_path=None):
    """シート一覧を取得"""
    creds = get_credentials(credentials_path)
    service = build("sheets", "v4", credentials=creds)

    spreadsheet = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id
    ).execute()

    print("📋 Sheets:")
    for sheet in spreadsheet['sheets']:
        props = sheet['properties']
        sheet_id = props['sheetId']
        title = props['title']
        index = props.get('index', 0)
        print(f"   [{index}] {title} (ID: {sheet_id})")

    return spreadsheet['sheets']


def create_sheet(spreadsheet_id, sheet_name, credentials_path=None):
    """新しいシートを作成"""
    creds = get_credentials(credentials_path)
    service = build("sheets", "v4", credentials=creds)

    body = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": sheet_name
                    }
                }
            }
        ]
    }

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    sheet_id = result['replies'][0]['addSheet']['properties']['sheetId']
    print(f"✅ Created sheet: {sheet_name} (ID: {sheet_id})")
    return sheet_id


def delete_sheet(spreadsheet_id, sheet_id, credentials_path=None):
    """シートを削除"""
    creds = get_credentials(credentials_path)
    service = build("sheets", "v4", credentials=creds)

    body = {
        "requests": [
            {
                "deleteSheet": {
                    "sheetId": sheet_id
                }
            }
        ]
    }

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    print(f"✅ Deleted sheet (ID: {sheet_id})")
    return result


def rename_sheet(spreadsheet_id, sheet_id, new_name, credentials_path=None):
    """シート名を変更"""
    creds = get_credentials(credentials_path)
    service = build("sheets", "v4", credentials=creds)

    body = {
        "requests": [
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "title": new_name
                    },
                    "fields": "title"
                }
            }
        ]
    }

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    print(f"✅ Renamed sheet to: {new_name}")
    return result


def duplicate_sheet(spreadsheet_id, sheet_id, new_name, credentials_path=None):
    """シートをコピー"""
    creds = get_credentials(credentials_path)
    service = build("sheets", "v4", credentials=creds)

    body = {
        "requests": [
            {
                "duplicateSheet": {
                    "sourceSheetId": sheet_id,
                    "insertSheetIndex": 0,
                    "newSheetName": new_name
                }
            }
        ]
    }

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    new_sheet_id = result['replies'][0]['duplicateSheet']['properties']['sheetId']
    print(f"✅ Duplicated sheet as: {new_name} (ID: {new_sheet_id})")
    return new_sheet_id


def main():
    parser = argparse.ArgumentParser(description="Manage Google Sheets")
    parser.add_argument("--spreadsheet-id", help="Spreadsheet ID (default: GOOGLE_SPREADSHEET_ID env var)")
    parser.add_argument("--credentials", help="Path to credentials JSON (default: GOOGLE_CREDENTIALS_PATH env var)")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # list コマンド
    subparsers.add_parser("list", help="List all sheets")

    # create コマンド
    create_parser = subparsers.add_parser("create", help="Create a new sheet")
    create_parser.add_argument("--name", required=True, help="Sheet name")

    # delete コマンド
    delete_parser = subparsers.add_parser("delete", help="Delete a sheet")
    delete_parser.add_argument("--sheet-id", type=int, required=True, help="Sheet ID to delete")

    # rename コマンド
    rename_parser = subparsers.add_parser("rename", help="Rename a sheet")
    rename_parser.add_argument("--sheet-id", type=int, required=True, help="Sheet ID to rename")
    rename_parser.add_argument("--name", required=True, help="New sheet name")

    # duplicate コマンド
    dup_parser = subparsers.add_parser("duplicate", help="Duplicate a sheet")
    dup_parser.add_argument("--sheet-id", type=int, required=True, help="Sheet ID to duplicate")
    dup_parser.add_argument("--name", required=True, help="Name for the duplicated sheet")

    args = parser.parse_args()

    spreadsheet_id = args.spreadsheet_id or os.environ.get("GOOGLE_SPREADSHEET_ID")

    if not spreadsheet_id:
        print("Error: --spreadsheet-id argument or GOOGLE_SPREADSHEET_ID environment variable required")
        sys.exit(1)

    if args.command == "list":
        list_sheets(spreadsheet_id, args.credentials)
    elif args.command == "create":
        create_sheet(spreadsheet_id, args.name, args.credentials)
    elif args.command == "delete":
        delete_sheet(spreadsheet_id, args.sheet_id, args.credentials)
    elif args.command == "rename":
        rename_sheet(spreadsheet_id, args.sheet_id, args.name, args.credentials)
    elif args.command == "duplicate":
        duplicate_sheet(spreadsheet_id, args.sheet_id, args.name, args.credentials)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
