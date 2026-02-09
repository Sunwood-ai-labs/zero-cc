#!/usr/bin/env python3
"""
VOICEVOX Engine Client

音声合成用のシンプルなクライアント。
VOICEVOX EngineのHTTP APIを使って音声を生成する。
"""

import requests
import json
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, List


class VoicevoxClient:
    """VOICEVOX Engineへのクライアント"""

    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 50021

    def __init__(self, host: str = None, port: int = None):
        self.host = host or self.DEFAULT_HOST
        self.port = port or self.DEFAULT_PORT
        self.base_url = f"http://{self.host}:{self.port}"

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """HTTPリクエストを送信"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                f"VOICEVOX Engineに接続できません: {self.base_url}\n"
                "docker-compose up -d でEngineを起動してください"
            )
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTPエラー: {e}")

    def get_version(self) -> str:
        """VOICEVOX Engineのバージョンを取得"""
        response = self._request("GET", "/version")
        return response.text

    def get_speakers(self) -> List[Dict]:
        """利用可能な話者一覧を取得"""
        response = self._request("GET", "/speakers")
        return response.json()

    def get_speaker_info(self, speaker_uuid: str) -> Dict:
        """話者の詳細情報を取得"""
        response = self._request("GET", f"/speaker_info?speaker_uuid={speaker_uuid}")
        return response.json()

    def audio_query(
        self,
        text: str,
        speaker: int = 0,
        speed_scale: float = 1.0,
        pitch_scale: float = 0.0,
        intonation_scale: float = 1.0,
        volume_scale: float = 1.0,
        pre_phoneme_length: float = 0.1,
        post_phoneme_length: float = 0.1,
    ) -> Dict:
        """
        音声合成用のクエリを作成

        Args:
            text: 読み上げるテキスト
            speaker: 話者ID（デフォルト: 0 = 四国めたん）
            speed_scale: 速度（1.0が基準、0.5-2.0程度）
            pitch_scale: ピッチ（0.0が基準、-0.5〜0.5程度）
            intonation_scale: イントネーション（1.0が基準）
            volume_scale: 音量（1.0が基準）
            pre_phoneme_length: 前無音時間（秒）
            post_phoneme_length: 後無音時間（秒）
        """
        params = {"text": text, "speaker": speaker}
        response = self._request("POST", "/audio_query", params=params)
        query = response.json()

        # パラメータを更新
        query["speedScale"] = speed_scale
        query["pitchScale"] = pitch_scale
        query["intonationScale"] = intonation_scale
        query["volumeScale"] = volume_scale
        query["prePhonemeLength"] = pre_phoneme_length
        query["postPhonemeLength"] = post_phoneme_length

        return query

    def synthesis(self, query: Dict, speaker: int = 0) -> bytes:
        """
        音声合成を実行

        Args:
            query: audio_queryで取得したクエリ
            speaker: 話者ID

        Returns:
            WAV形式の音声データ（バイナリ）
        """
        params = {"speaker": speaker}
        headers = {"Content-Type": "application/json"}
        response = self._request(
            "POST", "/synthesis", params=params, headers=headers, data=json.dumps(query)
        )
        return response.content

    def text_to_speech(
        self,
        text: str,
        output_path: str,
        speaker: int = 0,
        speed_scale: float = 1.0,
        pitch_scale: float = 0.0,
        intonation_scale: float = 1.0,
        volume_scale: float = 1.0,
    ) -> None:
        """
        テキストから音声を生成して保存

        Args:
            text: 読み上げるテキスト
            output_path: 出力ファイルパス（.wav）
            speaker: 話者ID
            speed_scale: 速度
            pitch_scale: ピッチ
            intonation_scale: イントネーション
            volume_scale: 音量
        """
        query = self.audio_query(
            text,
            speaker=speaker,
            speed_scale=speed_scale,
            pitch_scale=pitch_scale,
            intonation_scale=intonation_scale,
            volume_scale=volume_scale,
        )
        audio = self.synthesis(query, speaker=speaker)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(audio)

        print(f"音声を保存しました: {output_path}")


def list_speakers(client: VoicevoxClient) -> None:
    """利用可能な話者を一覧表示"""
    speakers = client.get_speakers()
    print("\n=== 利用可能な話者 ===")
    for speaker in speakers:
        print(f"\n{speaker['name']} (supported: {speaker['supported_features']})")
        for style in speaker["styles"]:
            print(f"  ID: {style['id']:3d} - {style['name']}")


def main():
    parser = argparse.ArgumentParser(description="VOICEVOX音声合成クライアント")
    parser.add_argument("text", nargs="?", help="読み上げるテキスト")
    parser.add_argument("-o", "--output", default="output.wav", help="出力ファイルパス")
    parser.add_argument("-s", "--speaker", type=int, default=0, help="話者ID")
    parser.add_argument("--speed", type=float, default=1.0, help="速度（デフォルト: 1.0）")
    parser.add_argument("--pitch", type=float, default=0.0, help="ピッチ（デフォルト: 0.0）")
    parser.add_argument("--volume", type=float, default=1.0, help="音量（デフォルト: 1.0）")
    parser.add_argument("--host", default="127.0.0.1", help="VOICEVOX Engineのホスト")
    parser.add_argument("--port", type=int, default=50021, help="VOICEVOX Engineのポート")
    parser.add_argument("--list-speakers", action="store_true", help="話者一覧を表示")

    args = parser.parse_args()

    client = VoicevoxClient(host=args.host, port=args.port)

    # バージョンチェック
    try:
        version = client.get_version()
        print(f"VOICEVOX Engine {version}")
    except RuntimeError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)

    # 話者一覧
    if args.list_speakers:
        list_speakers(client)
        return

    # 音声合成
    if not args.text:
        parser.error("テキストが指定されていません")

    client.text_to_speech(
        args.text,
        args.output,
        speaker=args.speaker,
        speed_scale=args.speed,
        pitch_scale=args.pitch,
        volume_scale=args.volume,
    )


if __name__ == "__main__":
    main()
