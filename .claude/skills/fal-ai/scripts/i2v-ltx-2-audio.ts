#!/usr/bin/env tsx
/**
 * i2v-ltx-2-audio.ts
 *
 * MODEL: fal-ai/ltx-2-19b/distilled/image-to-video/lora
 * TYPE: Image to Video with Audio (I2V + Audio)
 *
 * 画像から音声付き動画を生成するスクリプト
 * 生成された動画は outputs/videos/generated/ に保存されます
 *
 * 使用方法:
 *   node i2v-ltx-2-audio.ts input.jpg
 *   node i2v-ltx-2-audio.ts input.png --prompt "Camera zooms in" --frames 121
 *   node i2v-ltx-2-audio.ts input.jpg --no-audio --camera dolly_in
 *
 * パラメータ制約:
 *   入力画像: ローカルファイル または URL
 *   --frames: フレーム数 (デフォルト: 121)
 *   --fps: フレームレート (デフォルト: 25)
 *   --size: auto | square_hd | square | portrait_4_3 | portrait_16_9 | landscape_4_3 | landscape_16_9
 *   --camera: dolly_in | dolly_out | dolly_left | dolly_right | jib_up | jib_down | static | none
 *   --camera-scale: 0.0-2.0 (デフォルト: 1.0)
 *   --acceleration: none | regular | high | full
 *
 * 音声生成:
 *   --no-audio: 音声生成を無効化
 *   --no-multiscale: マルチスケール生成を無効化
 */

import { fal } from "@fal-ai/client";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

// .envファイルを読み込む（プロジェクトルートから）
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, "../../../../");
const envPath = path.resolve(projectRoot, ".env");
dotenv.config({ path: envPath });

// 環境変数からAPIキーを取得
const FAL_KEY = process.env.FAL_KEY;

if (!FAL_KEY) {
  console.error("エラー: FAL_KEY環境変数が設定されていません");
  console.error("プロジェクトルートの .env ファイルを確認してください");
  process.exit(1);
}

fal.config({
  credentials: FAL_KEY
});

// 型定義
type VideoSize = "auto" | "square_hd" | "square" | "portrait_4_3" | "portrait_16_9" | "landscape_4_3" | "landscape_16_9";
type Acceleration = "none" | "regular" | "high" | "full";
type CameraLoRA = "dolly_in" | "dolly_out" | "dolly_left" | "dolly_right" | "jib_up" | "jib_down" | "static" | "none";
type VideoOutputType = "X264 (.mp4)" | "VP9 (.webm)" | "PRORES4444 (.mov)" | "GIF (.gif)";
type VideoQuality = "low" | "medium" | "high" | "maximum";
type VideoWriteMode = "fast" | "balanced" | "small";

interface ImageToVideoAudioOptions {
  imageUrl: string;
  prompt?: string;
  numFrames?: number;
  videoSize?: VideoSize;
  generateAudio?: boolean;
  useMultiscale?: boolean;
  fps?: number;
  acceleration?: Acceleration;
  cameraLoRA?: CameraLoRA;
  cameraLoRAScale?: number;
  negativePrompt?: string;
  enablePromptExpansion?: boolean;
  enableSafetyChecker?: boolean;
  videoOutputType?: VideoOutputType;
  videoQuality?: VideoQuality;
  videoWriteMode?: VideoWriteMode;
}

// コマンドライン引数の解析
function parseArgs(): ImageToVideoAudioOptions {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("使用方法: node image-to-video-audio.ts <input_image> [options]");
    console.error("");
    console.error("オプション:");
    console.error("  --prompt <prompt>           動画生成のプロンプト");
    console.error("  --frames <number>           フレーム数 (デフォルト: 121)");
    console.error("  --size <size>               動画サイズ (auto, square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9)");
    console.error("  --no-audio                  音声を生成しない");
    console.error("  --no-multiscale             マルチスケール生成を無効化");
    console.error("  --fps <number>              フレームレート (デフォルト: 25)");
    console.error("  --acceleration <level>      加速レベル (none, regular, high, full)");
    console.error("  --camera <type>             カメラLoRA (dolly_in, dolly_out, dolly_left, dolly_right, jib_up, jib_down, static, none)");
    console.error("  --camera-scale <scale>      カメラLoRAスケール (デフォルト: 1.0)");
    console.error("  --negative <prompt>         ネガティブプロンプト");
    console.error("  --no-prompt-expansion       プロンプト拡張を無効化");
    console.error("  --no-safety                 セーフティチェッカーを無効化");
    console.error("  --output-type <type>        出力タイプ (X264 (.mp4), VP9 (.webm), PRORES4444 (.mov), GIF (.gif))");
    console.error("  --quality <quality>         品質 (low, medium, high, maximum)");
    console.error("  --write-mode <mode>         書き込みモード (fast, balanced, small)");
    console.error("");
    console.error("例:");
    console.error('  node image-to-video-audio.ts photo.jpg');
    console.error('  node image-to-video-audio.ts landscape.png --prompt "Camera slowly pans right"');
    console.error('  node image-to-video-audio.ts portrait.jpg --camera dolly_in --camera-scale 1.5');
    console.error('  node image-to-video-audio.ts scene.jpg --frames 169 --fps 24 --size landscape_16_9');
    process.exit(1);
  }

  const options: ImageToVideoAudioOptions = {
    imageUrl: args[0],
    generateAudio: true,
    useMultiscale: true,
    enableSafetyChecker: true
  };

  let i = 1;
  while (i < args.length) {
    switch (args[i]) {
      case "--prompt":
        options.prompt = args[++i];
        break;
      case "--frames":
        options.numFrames = parseInt(args[++i]);
        break;
      case "--size":
        options.videoSize = args[++i] as VideoSize;
        break;
      case "--no-audio":
        options.generateAudio = false;
        break;
      case "--no-multiscale":
        options.useMultiscale = false;
        break;
      case "--fps":
        options.fps = parseFloat(args[++i]);
        break;
      case "--acceleration":
        options.acceleration = args[++i] as Acceleration;
        break;
      case "--camera":
        options.cameraLoRA = args[++i] as CameraLoRA;
        break;
      case "--camera-scale":
        options.cameraLoRAScale = parseFloat(args[++i]);
        break;
      case "--negative":
        options.negativePrompt = args[++i];
        break;
      case "--no-prompt-expansion":
        options.enablePromptExpansion = false;
        break;
      case "--no-safety":
        options.enableSafetyChecker = false;
        break;
      case "--output-type":
        options.videoOutputType = args[++i] as VideoOutputType;
        break;
      case "--quality":
        options.videoQuality = args[++i] as VideoQuality;
        break;
      case "--write-mode":
        options.videoWriteMode = args[++i] as VideoWriteMode;
        break;
      default:
        console.error(`不明なオプション: ${args[i]}`);
        process.exit(1);
    }
    i++;
  }

  return options;
}

// 画像をアップロード
async function uploadImage(imagePath: string): Promise<string> {
  // ローカルファイルの場合、アップロードが必要
  if (fs.existsSync(imagePath)) {
    console.log(`画像をアップロード中: ${imagePath}`);
    const fileData = fs.readFileSync(imagePath);
    const file = new File([fileData], imagePath.split("/").pop() || "image.png", {
      type: "image/png"
    });
    const url = await fal.storage.upload(file);
    console.log(`✓ アップロード完了: ${url}`);
    return url;
  }

  // URLの場合はそのまま返す
  return imagePath;
}

// 動画ファイル名を生成
function generateFilename(originalPath: string, hasAudio: boolean): string {
  const timestamp = Date.now();
  const originalName = path.basename(originalPath, path.extname(originalPath));
  const audioSuffix = hasAudio ? "_audio" : "";
  return `${originalName}${audioSuffix}_video_${timestamp}.mp4`;
}

// 動画をダウンロードして保存
async function downloadVideo(url: string, outputPath: string): Promise<void> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to download video: ${response.statusText}`);
  }
  const buffer = await response.arrayBuffer();
  fs.writeFileSync(outputPath, Buffer.from(buffer));
}

// 動画生成を実行
async function generateVideo(options: ImageToVideoAudioOptions) {
  console.log("音声付き動画生成を開始します...");

  if (options.prompt) {
    console.log(`プロンプト: ${options.prompt}`);
  }

  try {
    // 画像のアップロード（必要な場合）
    const imageUrl = await uploadImage(options.imageUrl);

    const input: Record<string, any> = {
      image_url: imageUrl,
      prompt: options.prompt || "Continue the scene naturally, maintaining the same style and motion.",
      num_frames: options.numFrames || 121,
      video_size: options.videoSize || "auto",
      generate_audio: true,
      use_multiscale: true,
      fps: options.fps || 25
    };

    // オプションパラメータを追加
    if (options.acceleration) input.acceleration = options.acceleration;
    if (options.cameraLoRA) input.camera_lora = options.cameraLoRA;
    if (options.cameraLoRAScale !== undefined) input.camera_lora_scale = options.cameraLoRAScale;
    if (options.negativePrompt) input.negative_prompt = options.negativePrompt;
    if (options.enablePromptExpansion !== undefined) input.enable_prompt_expansion = options.enablePromptExpansion;
    if (options.enableSafetyChecker !== undefined) input.enable_safety_checker = options.enableSafetyChecker;
    if (options.videoOutputType) input.video_output_type = options.videoOutputType;
    if (options.videoQuality) input.video_quality = options.videoQuality;
    if (options.videoWriteMode) input.video_write_mode = options.videoWriteMode;

    const result = await fal.subscribe("fal-ai/ltx-2-19b/distilled/image-to-video", {
      input,
      logs: true,
      onQueueUpdate: (update) => {
        if (update.status === "IN_PROGRESS") {
          update.logs.map((log) => log.message).forEach(console.log);
        }
      }
    });

    console.log("\n✓ 動画生成が完了しました！");
    console.log(`リクエストID: ${result.requestId}`);

    // 出力ディレクトリを作成
    const outputDir = path.join(__dirname, "../../../outputs/videos/generated");
    fs.mkdirSync(outputDir, { recursive: true });

    const filename = generateFilename(options.imageUrl, options.generateAudio !== false);
    const outputPath = path.join(outputDir, filename);

    // 動画をダウンロード
    await downloadVideo(result.data.video.url, outputPath);

    console.log("\n生成された動画:");
    console.log(`  ファイル名: ${filename}`);
    console.log(`  パス: ${outputPath}`);
    console.log(`  URL: ${result.data.video.url}`);
    console.log(`  サイズ: ${result.data.video.width}x${result.data.video.height}`);
    console.log(`  コンテンツタイプ: ${result.data.video.content_type}`);
    console.log(`  長さ: ${result.data.video.duration}秒`);
    console.log(`  FPS: ${result.data.video.fps}`);
    console.log(`  フレーム数: ${result.data.video.num_frames}`);
    console.log(`  音声: ${options.generateAudio !== false ? "あり" : "なし"}`);

    return result;
  } catch (error: any) {
    console.error("\n✗ エラーが発生しました:");
    if (error instanceof Error) {
      console.error(error.message);
      // エラー詳細を表示
      if (error.body && error.body.detail) {
        console.error("詳細:", JSON.stringify(error.body.detail, null, 2));
      }
    }
    throw error;
  }
}

// メイン処理
async function main() {
  const options = parseArgs();
  await generateVideo(options);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
