#!/usr/bin/env tsx
/**
 * t2i-nano-banana-pro.ts
 *
 * MODEL: fal-ai/nano-banana-pro
 * TYPE: Text to Image (T2I)
 *
 * Google Nano Banana Pro (Gemini 3 Pro Image) による画像生成スクリプト
 * 高度なテキスト描画とキャラクターの一貫性に対応
 * 生成された画像は outputs/images/generated/ に保存されます
 *
 * 使用方法:
 *   node t2i-nano-banana-pro.ts "A beautiful sunset" --size landscape_16_9
 *   node t2i-nano-banana-pro.ts "A cat" --num 3 --resolution 2k
 *   node t2i-nano-banana-pro.ts "Marketing banner with text" --format png
 *
 * パラメータ制約:
 *   --size: 21:9 | 16:9 | 3:2 | 4:3 | 5:4 | 1:1 | 4:5 | 3:4 | 2:3 | 9:16
 *   --resolution: 1k | 2k | 4k (デフォルト: 1k)
 *   --num: 1-10 (デフォルト: 1)
 *   --format: jpeg | png | webp
 *   --negative: ネガティブプロンプト
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
type AspectRatio =
  | "21:9"
  | "16:9"
  | "3:2"
  | "4:3"
  | "5:4"
  | "1:1"
  | "4:5"
  | "3:4"
  | "2:3"
  | "9:16";

type Resolution = "1k" | "2k" | "4k";
type OutputFormat = "jpeg" | "png" | "webp";

interface GenerateImageOptions {
  prompt: string;
  negativePrompt?: string;
  aspectRatio?: AspectRatio;
  resolution?: Resolution;
  numImages?: number;
  outputFormat?: OutputFormat;
  enableSafetyChecker?: boolean;
  seed?: number;
  outputDir?: string;
}

// コマンドライン引数の解析
function parseArgs(): GenerateImageOptions {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("使用方法: node t2i-nano-banana-pro.ts <prompt> [options]");
    console.error("");
    console.error("オプション:");
    console.error("  --size <ratio>             アスペクト比 (21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16)");
    console.error("  --resolution <res>         解像度 (1k, 2k, 4k) - デフォルト: 1k");
    console.error("  --num <number>             生成する画像数 (デフォルト: 1)");
    console.error("  --format <format>          出力形式 (jpeg, png, webp)");
    console.error("  --negative <prompt>        ネガティブプロンプト");
    console.error("  --seed <number>            乱数シード（再現性のため）");
    console.error("  --no-safety               セーフティチェッカーを無効化");
    console.error("  --output <dir>             出力ディレクトリ (デフォルト: outputs/images/generated)");
    console.error("");
    console.error("例:");
    console.error('  node t2i-nano-banana-pro.ts "A beautiful sunset" --size 16:9');
    console.error('  node t2i-nano-banana-pro.ts "Marketing banner with text" --resolution 2k');
    console.error('  node t2i-nano-banana-pro.ts "A cat" --num 3 --format png');
    process.exit(1);
  }

  const options: GenerateImageOptions = {
    prompt: args[0]
  };

  let i = 1;
  while (i < args.length) {
    switch (args[i]) {
      case "--size":
        options.aspectRatio = args[++i] as AspectRatio;
        break;
      case "--resolution":
        options.resolution = args[++i] as Resolution;
        break;
      case "--num":
        options.numImages = parseInt(args[++i]);
        break;
      case "--format":
        options.outputFormat = args[++i] as OutputFormat;
        break;
      case "--negative":
        options.negativePrompt = args[++i];
        break;
      case "--seed":
        options.seed = parseInt(args[++i]);
        break;
      case "--no-safety":
        options.enableSafetyChecker = false;
        break;
      case "--output":
        options.outputDir = args[++i];
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
  return `nano_banana_${promptSlug}_${timestamp}${seedSuffix}${indexSuffix}.png`;
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
  console.log("Nano Banana Pro で画像生成を開始します...");
  console.log(`プロンプト: ${options.prompt}`);

  try {
    // パラメータを構築（オプションパラメータは条件付きで追加）
    const inputParams: Record<string, any> = {
      prompt: options.prompt
    };

    // オプションパラメータを追加（設定されている場合のみ）
    if (options.negativePrompt) inputParams.negative_prompt = options.negativePrompt;
    if (options.aspectRatio) inputParams.aspect_ratio = options.aspectRatio;
    if (options.numImages) inputParams.num_images = options.numImages;
    if (options.outputFormat) inputParams.output_format = options.outputFormat;
    if (options.enableSafetyChecker !== undefined) inputParams.enable_safety_checker = options.enableSafetyChecker;
    if (options.seed) inputParams.seed = options.seed;

    console.log("リクエストパラメータ:", JSON.stringify(inputParams, null, 2));

    const result = await fal.subscribe("fal-ai/nano-banana-pro", {
      input: inputParams,
      logs: true,
      onQueueUpdate: (update) => {
        if (update.status === "IN_PROGRESS") {
          update.logs.map((log) => log.message).forEach(console.log);
        }
      }
    });

    console.log("\n✓ 画像生成が完了しました！");
    console.log(`リクエストID: ${result.requestId}`);

    // 出力ディレクトリを作成
    const outputDir = options.outputDir
      ? path.resolve(options.outputDir)
      : path.join(__dirname, "../../../outputs/images/generated");
    fs.mkdirSync(outputDir, { recursive: true });

    console.log("\n生成された画像:");

    // 結果の構造に対応
    const images = result.data?.images || result.images || [];

    for (let i = 0; i < images.length; i++) {
      const image = images[i];
      const filename = generateFilename(options.prompt, options.seed, i);
      const outputPath = path.join(outputDir, filename);

      // 画像をダウンロード
      await downloadImage(image.url, outputPath);

      console.log(`  [${i + 1}] ${filename}`);
      console.log(`      パス: ${outputPath}`);
      if (image.width) {
        console.log(`      サイズ: ${image.width}x${image.height}`);
      }
      if (image.content_type) {
        console.log(`      形式: ${image.content_type}`);
      }
      console.log(`      URL: ${image.url}`);
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
