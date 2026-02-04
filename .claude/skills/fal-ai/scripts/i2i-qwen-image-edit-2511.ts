#!/usr/bin/env tsx
/**
 * i2i-qwen-image-edit-2511.ts
 *
 * MODEL: fal-ai/qwen-image-edit-2511/lora
 * TYPE: Image to Image (I2I)
 *
 * 既存の画像を編集するスクリプト
 * 編集された画像は outputs/images/edited/ に保存されます
 *
 * 使用方法:
 *   node i2i-qwen-image-edit-2511.ts input.jpg "Make the sky blue"
 *   node i2i-qwen-image-edit-2511.ts input.png "Add clouds" --strength 0.7
 *
 * パラメータ制約:
 *   入力画像: ローカルファイル または URL
 *   image_urls: 配列形式で指定（内部処理）
 *   --strength: 0.0-1.0 (デフォルト: 0.8)
 *   --steps: 1-100 (デフォルト: 28)
 *   --scale: 1-20 (デフォルト: 4)
 *   --format: jpeg | png | webp
 *
 * 重要: モデルは image_urls (配列) を要求します
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
type OutputFormat = "jpeg" | "png" | "webp";

interface EditImageOptions {
  imageUrl: string;
  prompt: string;
  negativePrompt?: string;
  strength?: number;
  numInferenceSteps?: number;
  guidanceScale?: number;
  seed?: number;
  enableSafetyChecker?: boolean;
  outputFormat?: OutputFormat;
}

// コマンドライン引数の解析
function parseArgs(): EditImageOptions {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error("使用方法: node edit-image.ts <input_image> <prompt> [options]");
    console.error("");
    console.error("オプション:");
    console.error("  --strength <number>        編集の強さ 0-1 (デフォルト: 0.8)");
    console.error("  --steps <number>           推論ステップ数 (デフォルト: 28)");
    console.error("  --scale <number>           ガイダンススケール (デフォルト: 4)");
    console.error("  --seed <number>            乱数シード");
    console.error("  --format <format>          出力形式 (jpeg, png, webp)");
    console.error("  --negative <prompt>        ネガティブプロンプト");
    console.error("  --no-safety               セーフティチェッカーを無効化");
    console.error("");
    console.error("例:");
    console.error('  node edit-image.ts photo.jpg "Make the sky blue"');
    console.error('  node edit-image.ts portrait.png "Add sunglasses" --strength 0.6');
    process.exit(1);
  }

  const options: EditImageOptions = {
    imageUrl: args[0],
    prompt: args[1]
  };

  let i = 2;
  while (i < args.length) {
    switch (args[i]) {
      case "--strength":
        options.strength = parseFloat(args[++i]);
        break;
      case "--steps":
        options.numInferenceSteps = parseInt(args[++i]);
        break;
      case "--scale":
        options.guidanceScale = parseFloat(args[++i]);
        break;
      case "--seed":
        options.seed = parseInt(args[++i]);
        break;
      case "--format":
        options.outputFormat = args[++i] as OutputFormat;
        break;
      case "--negative":
        options.negativePrompt = args[++i];
        break;
      case "--no-safety":
        options.enableSafetyChecker = false;
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

// 編集後のファイル名を生成
function generateFilename(originalPath: string, prompt: string, index: number = 0): string {
  const timestamp = Date.now();
  const originalName = path.basename(originalPath, path.extname(originalPath));
  const indexSuffix = index > 0 ? `_${index}` : "";
  return `${originalName}_edited_${timestamp}${indexSuffix}.png`;
}

// 画像をダウンロードして保存
async function downloadImage(url: string, outputPath: string): Promise<void> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to download image: ${response.statusText}`);
  }
  const buffer = await response.arrayBuffer();
  fs.writeFileSync(outputPath, Buffer.from(buffer));
}

// 画像編集を実行
async function editImage(options: EditImageOptions) {
  console.log("画像編集を開始します...");
  console.log(`プロンプト: ${options.prompt}`);

  try {
    // 画像のアップロード（必要な場合）
    const imageUrl = await uploadImage(options.imageUrl);

    const result = await fal.subscribe("fal-ai/qwen-image-edit-2511", {
      input: {
        image_urls: [imageUrl],
        prompt: options.prompt,
        negative_prompt: options.negativePrompt || "",
        num_inference_steps: options.numInferenceSteps || 28,
        guidance_scale: options.guidanceScale || 4.5,
        seed: options.seed,
        enable_safety_checker: options.enableSafetyChecker !== false,
        output_format: options.outputFormat || "png"
      },
      logs: true,
      onQueueUpdate: (update) => {
        if (update.status === "IN_PROGRESS") {
          update.logs.map((log) => log.message).forEach(console.log);
        }
      }
    });

    console.log("\n✓ 画像編集が完了しました！");
    console.log(`リクエストID: ${result.requestId}`);
    console.log(`シード: ${result.data.seed}`);

    // 出力ディレクトリを作成
    const outputDir = path.join(__dirname, "../../../outputs/images/edited");
    fs.mkdirSync(outputDir, { recursive: true });

    console.log("\n編集された画像:");

    for (let i = 0; i < result.data.images.length; i++) {
      const image = result.data.images[i];
      const filename = generateFilename(options.imageUrl, options.prompt, i);
      const outputPath = path.join(outputDir, filename);

      // 画像をダウンロード
      await downloadImage(image.url, outputPath);

      console.log(`  [${i + 1}] ${filename}`);
      console.log(`      パス: ${outputPath}`);
      console.log(`      サイズ: ${image.width}x${image.height}`);
      console.log(`      形式: ${image.content_type}`);
      console.log(`      URL: ${image.url}`);
    }

    // NSFWチェック
    if (result.data.has_nsfw_concepts && result.data.has_nsfw_concepts.some((c: boolean) => c)) {
      console.warn("\n⚠️ 警告: いずれかの画像にNSFWコンテンツが検出されました");
    }

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
  await editImage(options);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
