#!/usr/bin/env python3
"""Google Spreadsheetのデータを検索するスクリプト"""

import argparse
import os
import re
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


def column_letter_to_index(letter):
    """A, B, C... を 0, 1, 2... のインデックスに変換"""
    result = 0
    for char in letter:
        result = result * 26 + (ord(char.upper()) - ord("A") + 1)
    return result - 1


def search(spreadsheet_id, sheet_name, column=None, value=None, pattern=None, credentials_path=None):
    """シート内のデータを検索"""
    credentials = get_credentials(credentials_path)
    service = build("sheets", "v4", credentials=credentials)

    range_name = sheet_name

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()

    values = result.get("values", [])

    if not values:
        print("No data found.")
        return []

    matches = []
    col_index = None

    # 列が指定されている場合
    if column:
        col_index = column_letter_to_index(column)

    for row_idx, row in enumerate(values, start=1):
        # 列が指定されている場合
        if col_index is not None:
            if col_index < len(row):
                cell_value = row[col_index]
                # パターンマッチ（正規表現）
                if pattern:
                    if re.search(pattern, cell_value):
                        matches.append((row_idx, row))
                # 値マッチ
                elif value and value in cell_value:
                    matches.append((row_idx, row))
        # 列指定なし、行全体を検索
        else:
            for cell_value in row:
                if pattern:
                    if re.search(pattern, cell_value):
                        matches.append((row_idx, row))
                        break
                elif value and value in cell_value:
                    matches.append((row_idx, row))
                    break

    if matches:
        print(f"🔍 Found {len(matches)} match(es):")
        for row_idx, row in matches:
            print(f"  Row {row_idx}: {'\t'.join(row)}")
    else:
        print("No matches found.")

    return matches


def main():
    parser = argparse.ArgumentParser(description="Search for data in a Google Sheet")
    parser.add_argument("--spreadsheet-id", help="Spreadsheet ID (default: GOOGLE_SPREADSHEET_ID env var)")
    parser.add_argument("--sheet-name", default="シート1", help="Sheet name (default: シート1)")
    parser.add_argument("--column", help="Column letter to search (e.g., A, B, C)")
    parser.add_argument("--value", help="Value to search for")
    parser.add_argument("--pattern", help="Regex pattern to search for")
    parser.add_argument("--credentials", help="Path to credentials JSON (default: GOOGLE_CREDENTIALS_PATH env var)")

    args = parser.parse_args()

    spreadsheet_id = args.spreadsheet_id or os.environ.get("GOOGLE_SPREADSHEET_ID")

    if not spreadsheet_id:
        print("Error: --spreadsheet-id argument or GOOGLE_SPREADSHEET_ID environment variable required")
        sys.exit(1)

    if not args.value and not args.pattern:
        print("Error: --value or --pattern argument required")
        sys.exit(1)

    search(
        spreadsheet_id=spreadsheet_id,
        sheet_name=args.sheet_name,
        column=args.column,
        value=args.value,
        pattern=args.pattern,
        credentials_path=args.credentials
    )


if __name__ == "__main__":
    main()
