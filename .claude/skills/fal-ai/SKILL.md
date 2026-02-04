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

- **画像生成**: テキストプロンプトから画像を生成
- **画像編集**: 既存の画像を編集
- **動画生成**: 画像から動画を生成
- **音声付き動画生成**: 画像から音声付き動画を生成（LTX-2 19B Distilled）

## 使用方法

### 画像生成

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
# 画像生成
node .claude/skills/fal-ai/scripts/generate-image.ts "A beautiful sunset" --size landscape_16_9

# 画像編集
node .claude/skills/fal-ai/scripts/edit-image.ts photo.jpg "Make the sky blue"

# 動画生成
node .claude/skills/fal-ai/scripts/image-to-video.ts photo.jpg --duration 5

# 音声付き動画生成
node .claude/skills/fal-ai/scripts/image-to-video-audio.ts photo.jpg
node .claude/skills/fal-ai/scripts/image-to-video-audio.ts photo.jpg --prompt "Camera slowly zooms in" --camera dolly_in
node .claude/skills/fal-ai/scripts/image-to-video-audio.ts photo.jpg --frames 169 --fps 24 --size landscape_16_9
```

## 出力先

生成物は以下のディレクトリに保存されます：

- 画像生成: `outputs/images/generated/`
- 画像編集: `outputs/images/edited/`
- 動画生成: `outputs/videos/generated/`
