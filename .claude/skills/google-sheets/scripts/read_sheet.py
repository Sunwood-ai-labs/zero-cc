#!/usr/bin/env python3
"""Google Spreadsheetからデータを読み込むスクリプト"""

import argparse
import json
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


def read_sheet(spreadsheet_id, sheet_name=None, range_name=None, skip_header=False, credentials_path=None):
    """シートのデータを読み込む"""
    credentials = get_credentials(credentials_path)
    service = build("sheets", "v4", credentials=credentials)

    # rangeが指定されていなければsheet_nameから作成
    if range_name is None:
        if sheet_name is None:
            sheet_name = "シート1"
        range_name = sheet_name

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()

    values = result.get("values", [])

    if not values:
        print("No data found.")
        return []

    # ヘッダーをスキップ
    if skip_header and len(values) > 1:
        values = values[1:]

    # 結果を表示
    print(f"📊 Read {len(values)} row(s) from {range_name}")
    for row in values:
        print("\t".join(row))

    return values


def main():
    parser = argparse.ArgumentParser(description="Read data from a Google Sheet")
    parser.add_argument("--spreadsheet-id", help="Spreadsheet ID (default: GOOGLE_SPREADSHEET_ID env var)")
    parser.add_argument("--sheet-name", help="Sheet name (not used if --range is specified)")
    parser.add_argument("--range", help="A1 notation range (e.g., 'シート1!A1:D10')")
    parser.add_argument("--skip-header", action="store_true", help="Skip header row")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--credentials", help="Path to credentials JSON (default: GOOGLE_CREDENTIALS_PATH env var)")

    args = parser.parse_args()

    spreadsheet_id = args.spreadsheet_id or os.environ.get("GOOGLE_SPREADSHEET_ID")

    if not spreadsheet_id:
        print("Error: --spreadsheet-id argument or GOOGLE_SPREADSHEET_ID environment variable required")
        sys.exit(1)

    values = read_sheet(
        spreadsheet_id=spreadsheet_id,
        sheet_name=args.sheet_name,
        range_name=args.range,
        skip_header=args.skip_header,
        credentials_path=args.credentials
    )

    if args.json:
        print(json.dumps(values, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
