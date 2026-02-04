#!/usr/bin/env tsx
/**
 * i2v-ltx-2.ts
 *
 * MODEL: fal-ai/ltx-2/image-to-video/fast
 * TYPE: Image to Video (I2V)
 *
 * 画像から動画を生成するスクリプト
 * 生成された動画は outputs/videos/generated/ に保存されます
 *
 * 使用方法:
 *   node i2v-ltx-2.ts input.jpg
 *   node i2v-ltx-2.ts input.png --duration 8 --fps 25
 *
 * パラメータ制約:
 *   入力画像: ローカルファイル または URL
 *   --duration: 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 のみ (デフォルト: 4.0だが上記のみ有効)
 *   --fps: 25 | 50 のみ (デフォルト: 24だが上記のみ有効)
 *   --motion: 0.0-10.0 (デフォルト: 1.0)
 *
 * 重要: duration と fps は特定の値のみ受け付けます
 *   - duration: 6/8/10/12/14/16/18/20秒
 *   - fps: 25/50
 */

import { fal } from "@fal-ai/client";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

// .envファイルを読み込む
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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
interface ImageToVideoOptions {
  imageUrl: string;
  prompt?: string;
  duration?: number;
  fps?: number;
  motionScale?: number;
}

// コマンドライン引数の解析
function parseArgs(): ImageToVideoOptions {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("使用方法: node image-to-video.ts <input_image> [options]");
    console.error("");
    console.error("オプション:");
    console.error("  --prompt <prompt>          動画生成のプロンプト");
    console.error("  --duration <seconds>       動画の長さ（秒）(デフォルト: 4.0)");
    console.error("  --fps <number>             フレームレート (デフォルト: 24)");
    console.error("  --motion <scale>           動きのスケール (デフォルト: 1.0)");
    console.error("");
    console.error("例:");
    console.error('  node image-to-video.ts photo.jpg');
    console.error('  node image-to-video.ts landscape.png --prompt "Gentle camera movement" --duration 5');
    process.exit(1);
  }

  const options: ImageToVideoOptions = {
    imageUrl: args[0]
  };

  let i = 1;
  while (i < args.length) {
    switch (args[i]) {
      case "--prompt":
        options.prompt = args[++i];
        break;
      case "--duration":
        options.duration = parseFloat(args[++i]);
        break;
      case "--fps":
        options.fps = parseInt(args[++i]);
        break;
      case "--motion":
        options.motionScale = parseFloat(args[++i]);
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
function generateFilename(originalPath: string): string {
  const timestamp = Date.now();
  const originalName = path.basename(originalPath, path.extname(originalPath));
  return `${originalName}_video_${timestamp}.mp4`;
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
async function generateVideo(options: ImageToVideoOptions) {
  console.log("動画生成を開始します...");

  if (options.prompt) {
    console.log(`プロンプト: ${options.prompt}`);
  }

  try {
    // 画像のアップロード（必要な場合）
    const imageUrl = await uploadImage(options.imageUrl);

    const result = await fal.subscribe("fal-ai/ltx-2/image-to-video/fast", {
      input: {
        image_url: imageUrl,
        prompt: options.prompt || "",
        duration: options.duration || 4.0,
        fps: options.fps || 24,
        motion_scale: options.motionScale || 1.0
      },
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

    const filename = generateFilename(options.imageUrl);
    const outputPath = path.join(outputDir, filename);

    // 動画をダウンロード
    await downloadVideo(result.data.video.url, outputPath);

    console.log("\n生成された動画:");
    console.log(`  ファイル名: ${filename}`);
    console.log(`  パス: ${outputPath}`);
    console.log(`  URL: ${result.data.video.url}`);
    console.log(`  コンテンツタイプ: ${result.data.video.content_type}`);
    console.log(`  長さ: ${result.data.duration}秒`);
    console.log(`  FPS: ${result.data.fps}`);

    return result;
  } catch (error) {
    console.error("\n✗ エラーが発生しました:");
    if (error instanceof Error) {
      console.error(error.message);
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
