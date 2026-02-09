---
name: fal-ai
description: fal.ai APIを使って画像生成・画像編集・動画生成を行うワークスペーススキル
allowed-tools:
  - Bash(node .claude/skills/fal-ai/scripts/*)
triggers:
  - "画像を作"
  - "画像を生成"
  - "generate.*image"
  - "画像を編集"
  - "edit.*image"
  - "動画を作"
  - "動画を生成"
  - "image.*video"
  - "video.*generat"
  - "音声付き動画"
  - "audio.*video"
---

# fal-ai Workspace Skill

fal.ai APIを使ってマルチメディアコンテンツを作成するワークスペーススキル。

## 機能

- **画像生成**: テキストプロンプトから画像を生成（Nano Banana Pro、Qwen Image 2512）
- **画像編集**: 既存の画像を編集
- **動画生成**: 画像から動画を生成
- **音声付き動画生成**: 画像から音声付き動画を生成（LTX-2 19B Distilled）

### 利用可能なモデル

| モデル | タイプ | 特徴 |
|--------|------|------|
| **Nano Banana Pro** | T2I | Google Gemini 3 Pro Image、高度なテキスト描画、キャラクターの一貫性 |
| **Qwen Image 2512** | T2I | 改善されたテキスト描画、自然なテクスチャ |
| **Qwen Image Edit 2511** | I2I | 画像編集 |
| **LTX-2** | I2V | 高速動画生成 |
| **LTX-2 19B Distilled** | I2V | 音声付き動画生成 |

## 使用方法

### 画像生成（Nano Banana Pro）

```
「マーケティングバナーを作って、テキスト『SUMMER SALE』入りで」
「1960s aesthetic portrait（1960年代風ポートレート）の画像を」
「プロフェッショナルなインフォグラフィックを生成して」
「Multi-language text rendering, Japanese calligraphy style（多言語テキスト、日本の書道スタイル）の画像を」
```

### 画像生成（Qwen Image 2512）

```
「夕日の山脈の画像を作って」
「猫のイラストを生成して」
「A cyberpunk city at night, neon lights（サイバーパンクな夜の街）の画像を」
```

### 画像編集

```
「この写真の空を青くして」
「画像を編集して、くっきりさせる」
```

### 動画生成

```
「この写真から動画を作って」
「5秒間のアニメーションを生成して」
```

### 音声付き動画生成

```
「この写真から音声付き動画を作って」
「カメラをズームインする動画を生成して」
```


## ワークフロー

### 1. 画像生成

1. ユーザーからプロンプトを受け取る
2. 必要に応じてプロンプトを改善・補完
3. `generate-image.ts` を実行
4. `outputs/images/generated/` に保存
5. 結果を確認・共有

### 2. 画像編集

1. 編集元の画像パスを確認
2. 編集内容のプロンプトを確認
3. `edit-image.ts` を実行
4. `outputs/images/edited/` に保存
5. 結果を確認・共有

### 3. 動画生成

1. 元画像のパスを確認
2. 動画パラメータ（長さ、FPS等）を確認
3. `image-to-video.ts` を実行
4. `outputs/videos/generated/` に保存
5. 結果を確認・共有

### 4. 音声付き動画生成

1. 元画像のパスを確認
2. 動画パラメータ（フレーム数、FPS、カメラ移動等）を確認
3. `image-to-video-audio.ts` を実行
4. `outputs/videos/generated/` に保存
5. 結果を確認・共有

## スクリプト実行例

```bash
# Nano Banana Pro による画像生成（高度なテキスト描画対応）
node .claude/skills/fal-ai/scripts/t2i-nano-banana-pro.ts "Marketing banner with text" --size 16:9 --resolution 2k
node .claude/skills/fal-ai/scripts/t2i-nano-banana-pro.ts "A beautiful sunset" --size 16:9
node .claude/skills/fal-ai/scripts/t2i-nano-banana-pro.ts "A cat" --num 3 --format png

# Qwen Image 2512 による画像生成
node .claude/skills/fal-ai/scripts/t2i-qwen-image-2512.ts "A beautiful sunset" --size landscape_16_9

# 画像編集
node .claude/skills/fal-ai/scripts/i2i-qwen-image-edit-2511.ts photo.jpg "Make the sky blue"

# 動画生成
node .claude/skills/fal-ai/scripts/i2v-ltx-2.ts photo.jpg --duration 5

# 音声付き動画生成
node .claude/skills/fal-ai/scripts/i2v-ltx-2-audio.ts photo.jpg
node .claude/skills/fal-ai/scripts/i2v-ltx-2-audio.ts photo.jpg --prompt "Camera slowly zooms in" --camera dolly_in
node .claude/skills/fal-ai/scripts/i2v-ltx-2-audio.ts photo.jpg --frames 169 --fps 24 --size landscape_16_9
```

## 出力先

生成物は以下のディレクトリに保存されます：

- 画像生成: `outputs/images/generated/`
- 画像編集: `outputs/images/edited/`
- 動画生成: `outputs/videos/generated/`
