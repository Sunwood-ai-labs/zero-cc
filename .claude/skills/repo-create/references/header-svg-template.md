# Header SVG Template

リポジトリ用のアニメーション付きヘッダーSVGテンプレート。

## デザイン原則

1. **タイトルは中央に大きく表示** - プロジェクト名が目立つように
2. **エレガントなフォント** - `Segoe UI`, `Roboto`, `Helvetica`, `Arial` など
3. **リポジトリ内容に合わせた配色** - プロジェクトの特性に応じたカラーマップを使用

## 変数プレースホルダー

| プレースホルダー | 説明 | デフォルト値 |
|:--|:--|:--|
| `{PROJECT_NAME}` | プロジェクト名（大文字） | - |
| `{SUBTITLE}` | サブタイトル/説明文 | - |
| `{FONT_SIZE}` | フォントサイズ（長さで自動調整） | 90 |
| `{LETTER_SPACING}` | 文字間隔（長さで自動調整） | 8 |
| `{WIDTH}` | 画像幅 | 1200 |
| `{HEIGHT}` | 画像高さ | 300 |
| `{BG_COLOR_1}` | 背景グラデーション色1 | `#0f0c29` |
| `{BG_COLOR_2}` | 背景グラデーション色2 | `#302b63` |
| `{BG_COLOR_3}` | 背景グラデーション色3 | `#24243e` |
| `{TEXT_COLOR_1}` | テキストグラデーション色1 | `#00d4ff` |
| `{TEXT_COLOR_2}` | テキストグラデーション色2 | `#7b2cbf` |
| `{TEXT_COLOR_3}` | テキストグラデーション色3 | `#ff6b6b` |
| `{ACCENT_COLOR_1}` | アクセント色1 | `#00d4ff` |
| `{ACCENT_COLOR_2}` | アクセント色2 | `#7b2cbf` |
| `{ACCENT_COLOR_3}` | アクセント色3 | `#ff6b6b` |

## リポジトリタイプ別カラーマップ

### AI/ML プロジェクト
- 背景: `#0a0e27`, `#1a1f3a`, `#0f1525`
- テキスト: `#00d4ff`, `#7b2cbf`, `#ff6b6b`
- アクセント: `#00d4ff`, `#7b2cbf`, `#ff6b6b`

### Web フロントエンド
- 背景: `#1a1a2e`, `#16213e`, `#0f3460`
- テキスト: `#00d9ff`, `#00ff88`, `#ffcc00`
- アクセント: `#00d9ff`, `#00ff88`, `#ffcc00`

### バックエンド/API
- 背景: `#0d1b2a`, `#1b263b`, `#1b3a4b`
- テキスト: `#4cc9f0`, `#4361ee`, `#3f37c9`
- アクセント: `#4cc9f0`, `#4361ee`, `#3f37c9`

### モバイルアプリ
- 背景: `#1a0a0a`, `#2d1810`, `#1f1410`
- テキスト: `#ff9800`, `#ff5722`, `#ffc107`
- アクセント: `#ff9800`, `#ff5722`, `#ffc107`

### データ/インフラ
- 背景: `#0a1628`, `#0f2040`, `#0a1f35`
- テキスト: `#00bcd4`, `#0097a7`, `#4dd0e1`
- アクセント: `#00bcd4`, `#0097a7`, `#4dd0e1`

### セキュリティ/ハッキング
- 背景: `#0d0d0d`, `#1a1a1a`, `#0f0f0f`
- テキスト: `#00ff00`, `#39ff14`, `#7fff00`
- アクセント: `#00ff00`, `#39ff14`, `#7fff00`

### ゲーム開発
- 背景: `#1a0a20`, `#2d1028`, `#1f0a25`
- テキスト: `#e91e63`, `#9c27b0`, `#ff5722`
- アクセント: `#e91e63`, `#9c27b0`, `#ff5722`

### 緑/環境系
- 背景: `#0a1a0f`, `#142015`, `#0f1a12`
- テキスト: `#4caf50`, `#8bc34a`, `#cddc39`
- アクセント: `#4caf50`, `#8bc34a`, `#cddc39`

## SVGテンプレート

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <!-- Gradient Background -->
    <linearGradient id="bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{BG_COLOR_1}">
        <animate attributeName="stop-color" values="{BG_COLOR_1};{BG_COLOR_2};{BG_COLOR_1}" dur="8s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" style="stop-color:{BG_COLOR_2}">
        <animate attributeName="stop-color" values="{BG_COLOR_2};{BG_COLOR_3};{BG_COLOR_2}" dur="8s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" style="stop-color:{BG_COLOR_3}">
        <animate attributeName="stop-color" values="{BG_COLOR_3};{BG_COLOR_1};{BG_COLOR_3}" dur="8s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <!-- Animated Text Gradient -->
    <linearGradient id="text-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{TEXT_COLOR_1}">
        <animate attributeName="stop-color" values="{TEXT_COLOR_1};{TEXT_COLOR_2};{TEXT_COLOR_1}" dur="4s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" style="stop-color:{TEXT_COLOR_2}">
        <animate attributeName="stop-color" values="{TEXT_COLOR_2};{TEXT_COLOR_3};{TEXT_COLOR_2}" dur="4s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" style="stop-color:{TEXT_COLOR_3}">
        <animate attributeName="stop-color" values="{TEXT_COLOR_3};{TEXT_COLOR_1};{TEXT_COLOR_3}" dur="4s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <!-- Glow Effect -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="coloredBlur">
        <animate attributeName="stdDeviation" values="3;5;3" dur="2s" repeatCount="indefinite"/>
      </feGaussianBlur>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Animated Grid Pattern -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <g>
        <animateTransform attributeName="transform" type="translate" from="0 0" to="40 40" dur="20s" repeatCount="indefinite"/>
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>
      </g>
    </pattern>
  </defs>

  <style>
    @keyframes float {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-10px); }
    }
    @keyframes pulse {
      0%, 100% { opacity: 0.3; }
      50% { opacity: 0.7; }
    }
    @keyframes spin {
      from { transform-origin: center; transform: rotate(0deg); }
      to { transform-origin: center; transform: rotate(360deg); }
    }
    @keyframes blink {
      0%, 100% { opacity: 0.3; r: 4; }
      50% { opacity: 1; r: 6; }
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .main-text { animation: float 3s ease-in-out infinite; }
    .subtitle { animation: fadeIn 1s ease-out forwards; }
    .bracket-left { animation: pulse 2s ease-in-out infinite; }
    .bracket-right { animation: pulse 2s ease-in-out infinite 0.5s; }
    .circle-spin { animation: spin 30s linear infinite; transform-origin: center; }
    .dot-blink-1 { animation: blink 1.5s ease-in-out infinite; }
    .dot-blink-2 { animation: blink 1.5s ease-in-out infinite 0.3s; }
    .dot-blink-3 { animation: blink 1.5s ease-in-out infinite 0.6s; }
    .dot-blink-4 { animation: blink 1.5s ease-in-out infinite 0.9s; }
    .dot-blink-5 { animation: blink 1.5s ease-in-out infinite 1.2s; }
    .dot-blink-6 { animation: blink 1.5s ease-in-out infinite 0.2s; }
  </style>

  <!-- Background -->
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg-gradient)"/>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#grid)"/>

  <!-- Decorative Circles with Animation -->
  <circle cx="100" cy="150" r="80" fill="none" stroke="rgba(0,212,255,0.1)" stroke-width="2" class="circle-spin"/>
  <circle cx="1100" cy="150" r="100" fill="none" stroke="rgba(123,44,191,0.1)" stroke-width="2" class="circle-spin" style="animation-direction: reverse;"/>
  <circle cx="600" cy="280" r="150" fill="none" stroke="rgba(255,107,107,0.05)" stroke-width="1">
    <animate attributeName="r" values="150;160;150" dur="4s" repeatCount="indefinite"/>
  </circle>

  <!-- Floating Particles -->
  <circle cx="150" cy="200" r="2" fill="{ACCENT_COLOR_1}" opacity="0.6">
    <animate attributeName="cy" values="200;50;200" dur="10s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.6;0;0.6" dur="10s" repeatCount="indefinite"/>
  </circle>
  <circle cx="1050" cy="100" r="2" fill="{ACCENT_COLOR_3}" opacity="0.6">
    <animate attributeName="cy" values="100;250;100" dur="12s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.6;0;0.6" dur="12s" repeatCount="indefinite"/>
  </circle>
  <circle cx="300" cy="80" r="1.5" fill="{ACCENT_COLOR_2}" opacity="0.5">
    <animate attributeName="cy" values="80;220;80" dur="8s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.5;0;0.5" dur="8s" repeatCount="indefinite"/>
  </circle>
  <circle cx="900" cy="250" r="1.5" fill="{ACCENT_COLOR_1}" opacity="0.5">
    <animate attributeName="cy" values="250;50;250" dur="9s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.5;0;0.5" dur="9s" repeatCount="indefinite"/>
  </circle>

  <!-- Code Brackets Left -->
  <g fill="none" stroke="rgba(0,212,255,0.3)" stroke-width="3" stroke-linecap="round" class="bracket-left">
    <path d="M 200 120 Q 180 150 200 180"/>
    <path d="M 180 100 Q 150 150 180 200"/>
  </g>

  <!-- Code Brackets Right -->
  <g fill="none" stroke="rgba(255,107,107,0.3)" stroke-width="3" stroke-linecap="round" class="bracket-right">
    <path d="M 1000 120 Q 1020 150 1000 180"/>
    <path d="M 1020 100 Q 1050 150 1020 200"/>
  </g>

  <!-- Main Text: Project Name (中央に大きく表示) -->
  <text x="600" y="175" text-anchor="middle" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="{FONT_SIZE}" font-weight="900" fill="url(#text-gradient)" filter="url(#glow)" letter-spacing="{LETTER_SPACING}" class="main-text">{PROJECT_NAME}</text>

  <!-- Subtitle -->
  <text x="600" y="220" text-anchor="middle" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="18" font-weight="400" fill="rgba(255,255,255,0.6)" letter-spacing="4" class="subtitle">{SUBTITLE}</text>

  <!-- Decorative Dots -->
  <circle cx="300" cy="260" r="4" fill="{ACCENT_COLOR_1}" class="dot-blink-1"/>
  <circle cx="330" cy="260" r="3" fill="{ACCENT_COLOR_2}" class="dot-blink-2"/>
  <circle cx="355" cy="260" r="2" fill="{ACCENT_COLOR_3}" class="dot-blink-3"/>
  <circle cx="845" cy="260" r="2" fill="{ACCENT_COLOR_3}" class="dot-blink-4"/>
  <circle cx="870" cy="260" r="3" fill="{ACCENT_COLOR_2}" class="dot-blink-5"/>
  <circle cx="900" cy="260" r="4" fill="{ACCENT_COLOR_1}" class="dot-blink-6"/>
</svg>
```

## フォントサイズ自動計算

プロジェクト名の文字数に応じてフォントサイズと文字間隔を調整（中央配置を維持）:

```python
# 文字数に応じた調整例
name_len = len(project_name)
font_size = max(50, min(90, 90 - (name_len - 8) * 3))
letter_spacing = max(2, 8 - (name_len - 8) * 0.3)
```

| 文字数 | フォントサイズ | 文字間隔 |
|:--:|:--:|:--:|
| 5-8 | 90 | 8.0 |
| 9-12 | 78 | 6.8 |
| 13-16 | 66 | 5.6 |
| 17-20 | 54 | 4.4 |
| 21+ | 50 | 2.0 |

## 生成手順

1. リポジトリの内容を分析して適切なカラーマップを選択
2. プロジェクト名の長さに応じてフォントサイズを計算
3. テンプレートの変数を置換して `assets/header.svg` に出力
