#!/usr/bin/env python3
"""
認証ヘルパー - OAuth2とサービスアカウントの両方に対応

使用方法:
    from auth_helper import get_credentials

    # サービスアカウントを使用
    creds = get_credentials(service_account='config/service-account.json')

    # OAuthトークンを使用
    creds = get_credentials(token='config/token.pickle')
"""

import os
import pickle
from pathlib import Path

try:
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    from google.oauth2.credentials import Credentials as OAuthCredentials
    from google.auth.transport.requests import Request
except ImportError:
    print("エラー: 必要なライブラリがインストールされていません")
    print("以下のコマンドでインストールしてください:")
    print("  pip install google-api-python-client google-auth-oauthlib")
    raise ImportError


def get_service_account_credentials(service_account_file=None):
    """
    サービスアカウントの認証情報を取得

    Args:
        service_account_file: サービスアカウントJSONのパス

    Returns:
        サービスアカウントのCredentialsオブジェクト
    """
    if service_account_file is None:
        service_account_file = os.environ.get(
            'GOOGLE_SERVICE_ACCOUNT_PATH',
            '/home/maki/.config/google-service-account.json'
        )

    service_account_path = Path(service_account_file)
    if not service_account_path.exists():
        # スキル内のconfigもチェック
        skill_path = Path(__file__).parent.parent / 'config' / 'service-account.json'
        if skill_path.exists():
            service_account_path = skill_path
        else:
            raise FileNotFoundError(
                f"サービスアカウントファイルが見つかりません: {service_account_file}\n"
                "Google Cloud Consoleでサービスアカウントを作成し、"
                "JSONキーをダウンロードしてください。"
            )

    # Drive APIのスコープを指定
    SCOPES = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
    ]

    creds = ServiceAccountCredentials.from_service_account_file(
        service_account_path,
        scopes=SCOPES
    )

    return creds


def get_oauth_credentials(token_file=None):
    """
    OAuthトークンの認証情報を取得

    Args:
        token_file: トークンファイルのパス

    Returns:
        OAuthのCredentialsオブジェクト
    """
    if token_file is None:
        token_file = os.environ.get(
            'GOOGLE_TOKEN_PATH',
            '/home/maki/.config/google-drive-token.json'
        )

    token_path = Path(token_file)
    if not token_path.exists():
        raise FileNotFoundError(
            f"トークンファイルが見つかりません: {token_file}\n"
            "まず認証設定を行ってください。"
        )

    with open(token_path, 'rb') as token:
        creds = pickle.load(token)

    # トークンの有効期限チェック
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # 更新したトークンを保存
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        else:
            raise Exception("トークンが無効です。再認証してください。")

    return creds


def get_credentials(service_account=None, token=None, prefer_service_account=False):
    """
    認証情報を取得（サービスアカウントまたはOAuth）

    Args:
        service_account: サービスアカウントJSONのパス
        token: OAuthトークンファイルのパス
        prefer_service_account: サービスアカウントを優先するか（デフォルト: False）

    Returns:
        Credentialsオブジェクト
    """
    # OAuthを優先（デフォルト）
    if not prefer_service_account:
        try:
            return get_oauth_credentials(token)
        except FileNotFoundError:
            # OAuthトークンが見つからない場合はサービスアカウントを試す
            if service_account is not None:
                return get_service_account_credentials(service_account)
            raise

    # サービスアカウントを優先
    if service_account is not None:
        return get_service_account_credentials(service_account)

    # どちらも指定されていない場合はOAuthを試す
    return get_oauth_credentials(token)
