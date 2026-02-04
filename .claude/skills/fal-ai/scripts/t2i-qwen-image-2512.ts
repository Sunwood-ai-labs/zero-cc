#!/usr/bin/env tsx
/**
 * t2i-qwen-image-2512.ts
 *
 * MODEL: fal-ai/qwen-image-2512/lora
 * TYPE: Text to Image (T2I)
 *
 * テキストプロンプトから画像を生成するスクリプト
 * 生成された画像は outputs/images/generated/ に保存されます
 *
 * 使用方法:
 *   node t2i-qwen-image-2512.ts "A beautiful sunset" --size landscape_16_9
 *   node t2i-qwen-image-2512.ts "A cat" --num 3 --format png
 *
 * パラメータ制約:
 *   --size: square_hd | square | portrait_4_3 | portrait_16_9 | landscape_4_3 | landscape_16_9
 *   --steps: 1-100 (デフォルト: 28)
 *   --scale: 1-20 (デフォルト: 4)
 *   --num: 1-4 (デフォルト: 1)
 *   --format: jpeg | png | webp
 *   --acceleration: none | regular | high
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
type ImageSize =
  | "square_hd"
  | "square"
  | "portrait_4_3"
  | "portrait_16_9"
  | "landscape_4_3"
  | "landscape_16_9"
  | { width: number; height: number };

type OutputFormat = "jpeg" | "png" | "webp";
type Acceleration = "none" | "regular" | "high";

interface GenerateImageOptions {
  prompt: string;
  negativePrompt?: string;
  imageSize?: ImageSize;
  numInferenceSteps?: number;
  guidanceScale?: number;
  seed?: number;
  numImages?: number;
  enableSafetyChecker?: boolean;
  outputFormat?: OutputFormat;
  acceleration?: Acceleration;
  loras?: Array<{ path: string; scale: number }>;
}

// コマンドライン引数の解析
function parseArgs(): GenerateImageOptions {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("使用方法: node generate-image.ts <prompt> [options]");
    console.error("");
    console.error("オプション:");
    console.error("  --size <size>              画像サイズ (square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9)");
    console.error("  --steps <number>           推論ステップ数 (デフォルト: 28)");
    console.error("  --scale <number>           ガイダンススケール (デフォルト: 4)");
    console.error("  --seed <number>            乱数シード");
    console.error("  --num <number>             生成する画像数 (デフォルト: 1)");
    console.error("  --format <format>          出力形式 (jpeg, png, webp)");
    console.error("  --acceleration <level>     加速レベル (none, regular, high)");
    console.error("  --negative <prompt>        ネガティブプロンプト");
    console.error("  --no-safety               セーフティチェッカーを無効化");
    console.error("");
    console.error("例:");
    console.error('  node generate-image.ts "A beautiful sunset" --size landscape_16_9');
    console.error('  node generate-image.ts "A cat" --num 3 --format png');
    process.exit(1);
  }

  const options: GenerateImageOptions = {
    prompt: args[0]
  };

  let i = 1;
  while (i < args.length) {
    switch (args[i]) {
      case "--size":
        options.imageSize = args[++i] as ImageSize;
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
      case "--num":
        options.numImages = parseInt(args[++i]);
        break;
      case "--format":
        options.outputFormat = args[++i] as OutputFormat;
        break;
      case "--acceleration":
        options.acceleration = args[++i] as Acceleration;
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

// プロンプトからファイル名を生成
function generateFilename(prompt: string, seed?: number, index: number = 0): string {
  const timestamp = Date.now();
  const seedSuffix = seed ? `_seed${seed}` : "";
  const indexSuffix = index > 0 ? `_${index}` : "";
  // プロンプトの先頭部分を抽出（ファイル名用）
  const promptSlug = prompt
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .split("_")
    .slice(0, 3)
    .join("_");
  return `${promptSlug}_${timestamp}${seedSuffix}${indexSuffix}.png`;
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

// 画像生成を実行
async function generateImage(options: GenerateImageOptions) {
  console.log("画像生成を開始します...");
  console.log(`プロンプト: ${options.prompt}`);

  try {
    const result = await fal.subscribe("fal-ai/qwen-image-2512/lora", {
      input: {
        prompt: options.prompt,
        negative_prompt: options.negativePrompt || "",
        image_size: options.imageSize || "landscape_4_3",
        num_inference_steps: options.numInferenceSteps || 28,
        guidance_scale: options.guidanceScale || 4,
        seed: options.seed,
        num_images: options.numImages || 1,
        enable_safety_checker: options.enableSafetyChecker !== false,
        output_format: options.outputFormat || "png",
        acceleration: options.acceleration || "regular",
        loras: options.loras || []
      },
      logs: true,
      onQueueUpdate: (update) => {
        if (update.status === "IN_PROGRESS") {
          update.logs.map((log) => log.message).forEach(console.log);
        }
      }
    });

    console.log("\n✓ 画像生成が完了しました！");
    console.log(`リクエストID: ${result.requestId}`);
    console.log(`シード: ${result.data.seed}`);

    // 出力ディレクトリを作成
    const outputDir = path.join(__dirname, "../../../outputs/images/generated");
    fs.mkdirSync(outputDir, { recursive: true });

    console.log("\n生成された画像:");

    for (let i = 0; i < result.data.images.length; i++) {
      const image = result.data.images[i];
      const filename = generateFilename(options.prompt, result.data.seed, i);
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
  await generateImage(options);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
