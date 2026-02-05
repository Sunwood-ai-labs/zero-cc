---
name: voicevox
description: VOICEVOX Engineを使って日本語音声合成を行うスキル。テキストから自然な日本語音声を生成する。
triggers:
  - "音声を作"
  - "音声を生成"
  - "音声合成"
  - "voicevox"
  - "VOICEVOX"
  - "ナレーション"
  - "読み上げ"
---

# VOICEVOX Skill

VOICEVOX Engineを使って日本語音声を合成するスキル。テキストから自然な日本語音声（WAV形式）を生成します。

## 機能

- **テキスト読み上げ**: 日本語テキストから音声を生成
- **話者選択**: 複数のキャラクター（四国めたん、ずんだもん等）から選択可能
- **パラメータ調整**: 速度、ピッチ、音量、イントネーションを調整
- **話者一覧**: 利用可能な話者とスタイルの一覧表示

## クイックスタート

### 前提条件

VOICEVOX EngineがDockerコンテナで実行されている必要があります：

```bash
docker-compose up -d
```

Engineは `http://127.0.0.1:50021` で利用可能になります。

### 基本的な使用方法

```
「この文章を読み上げて」
「音声を生成して」
「『こんにちは、世界』という音声を作って」
```

## 使用方法

### 1. 音声生成

基本の音声生成：

```bash
python3 .claude/skills/voicevox/scripts/voicevox_client.py "こんにちは、世界" -o output.wav
```

話者を指定して生成：

```bash
python3 .claude/skills/voicevox/scripts/voicevox_client.py "こんにちは" -s 1 -o output.wav
```

### 2. パラメータ調整

速度、ピッチ、音量を調整：

```bash
python3 .claude/skills/voicevox/scripts/voicevox_client.py "テスト" \
  --speed 1.2 \
  --pitch 0.1 \
  --volume 1.5 \
  -o output.wav
```

### 3. 話者一覧の表示

利用可能な話者を確認：

```bash
python3 .claude/skills/voicevox/scripts/voicevox_client.py --list-speakers
```

## スクリプトオプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `text` | 読み上げるテキスト（必須） | - |
| `-o, --output` | 出力ファイルパス | `output.wav` |
| `-s, --speaker` | 話者ID | `0` |
| `--speed` | 速度（0.5-2.0程度） | `1.0` |
| `--pitch` | ピッチ（-0.5〜0.5程度） | `0.0` |
| `--volume` | 音量 | `1.0` |
| `--host` | VOICEVOX Engineのホスト | `127.0.0.1` |
| `--port` | VOICEVOX Engineのポート | `50021` |
| `--list-speakers` | 話者一覧を表示 | - |

## 主な話者（デフォルト）

| ID | 名前 | スタイル |
|----|------|----------|
| 0 | 四国めたん | 普通 |
| 1 | ずんだもん | 普通 |
| 2 | 水瀬いのり | 普通 |
| 3 | 春日部つむぎ | 普通 |
| 4 | 波音リツ | 普通 |

*注: 話者一覧は `--list-speakers` で確認してください*

## 使用例

### シンプルな音声生成

```bash
python3 .claude/skills/voicevox/scripts/voicevox_client.py "こんにちは、無重星来です" -o greeting.wav
```

### キャラクターを変える

```bash
# ずんだもん（話者ID: 1）
python3 .claude/skills/voicevox/scripts/voicevox_client.py "なのだ" -s 1 -o zundamon.wav

# 水瀬いのり（話者ID: 2）
python3 .claude/skills/voicevox/scripts/voicevox_client.py "はじめまして" -s 2 -o inori.wav
```

### パラメータ調整

```bash
# 少し速く、高めの声
python3 .claude/skills/voicevox/scripts/voicevox_client.py "さあ、始めよう" \
  --speed 1.3 --pitch 0.2 -o cheerful.wav

# ゆっくり、落ち着いた声
python3 .claude/skills/voicevox/scripts/voicevox_client.py "じっくり考えよう" \
  --speed 0.8 --pitch -0.1 -o calm.wav
```

### Pythonプログラムから使用

```python
from .claude.skills.voicevox.scripts.voicevox_client import VoicevoxClient

client = VoicevoxClient()

# 音声生成
client.text_to_speech(
    "こんにちは、世界",
    "output.wav",
    speaker=0,
    speed_scale=1.0,
    pitch_scale=0.0,
    volume_scale=1.0
)

# 話者一覧を取得
speakers = client.get_speakers()
for speaker in speakers:
    print(f"{speaker['name']}: {speaker['styles']}")
```

## 出力先

音声ファイルは指定したパスに保存されます。デフォルトはカレントディレクトリの `output.wav` です。

## エラー対処

### 接続エラー

```
エラー: VOICEVOX Engineに接続できません: http://127.0.0.1:50021
docker-compose up -d でEngineを起動してください
```

VOICEVOX Engineが起動していない場合は、Dockerコンテナを起動してください：

```bash
docker-compose up -d
```

## リソース

- **スクリプト**: `.claude/skills/voicevox/scripts/voicevox_client.py`
- **VOICEVOX Engine**: https://github.com/VOICEVOX/voicevox_engine
- **VOICEVOX 公式サイト**: https://voicevox.hiroshiba.jp/
