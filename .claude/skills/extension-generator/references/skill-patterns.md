# スキル生成パターン（v2.1.1+ 統合版）

## スキルとは

v2.1.1以降、**スラッシュコマンドとスキルは統合**されました。

> "Skills and slash commands are the same thing" - Boris Cherny (Anthropic)

すべて `.claude/skills/` で作成することを推奨。

## ディレクトリ構造

| タイプ | パス | スコープ |
|--------|------|----------|
| プロジェクト用 | `.claude/skills/` | 現在のプロジェクト |
| 個人用 | `~/.claude/skills/` | 全プロジェクト |

## 基本構造

```
skill-name/
├── SKILL.md          # 必須
├── scripts/          # 自動化スクリプト（任意）
├── references/       # 参照ドキュメント（任意）
└── assets/           # テンプレート等（任意）
```

## SKILL.md フォーマット

```yaml
---
name: skill-name
description: |
  スキルの説明。いつ使うかを明確に。
  トリガー例: (1) ○○する時, (2) △△が必要な時
allowed-tools: Read, Grep, Glob           # ツール制限（任意）
user-invocable: true                       # /メニューに表示（デフォルトtrue）
disable-model-invocation: false            # 自動呼び出し禁止（デフォルトfalse）
context: fork                              # サブエージェントとして実行（任意）
hooks:                                     # フック定義（任意）
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---

# スキル名

## 概要
[1-2文で説明]

## ワークフロー
1. [ステップ1]
2. [ステップ2]

## 使用例
[具体的な例]
```

## フロントマターフィールド

| フィールド | 必須 | 説明 |
|------------|------|------|
| `name` | ✅ | 小文字とハイフンのみ（最大64文字） |
| `description` | ✅ | 説明 + トリガー条件（最大1024文字） |
| `allowed-tools` | - | 使用可能なツールを制限 |
| `user-invocable` | - | `/`メニューに表示するか（デフォルト: true） |
| `disable-model-invocation` | - | Skillツールからの自動呼び出しを禁止 |
| `context` | - | `fork`でサブエージェントとして実行 |
| `hooks` | - | PreToolUse/PostToolUse/Stop フック |

## 呼び出しパターン

### 1. 自動検出（推奨）
```
ユーザー: このコードをレビューして
Claude: [descriptionがマッチしてスキルを自動適用]
```

### 2. 明示的呼び出し
```
/skill-name
```

### 3. Skillツール経由
Claudeが適切と判断した時に自動呼び出し

## 実践例

### シンプルなスキル（単一ファイル）

```yaml
# .claude/skills/commit-helper/SKILL.md
---
name: commit-helper
description: |
  コミットメッセージを生成。git commit時、コミットメッセージ作成時に使用。
allowed-tools: Bash(git diff:*), Bash(git status:*)
---

# Commit Helper

## ワークフロー
1. `git diff --staged` で変更を確認
2. Conventional Commits形式でメッセージ生成

## フォーマット
- type(scope): 要約（50文字以内）
- 本文: 何を、なぜ変更したか
```

### 複雑なスキル（複数ファイル）

```
code-review/
├── SKILL.md
├── SECURITY.md
├── PERFORMANCE.md
└── scripts/
    └── run-linters.sh
```

```yaml
# SKILL.md
---
name: code-review
description: |
  コードレビューを実施。セキュリティ、パフォーマンス、スタイルをチェック。
  「レビューして」「PRをチェックして」で発動。
allowed-tools: Read, Grep, Glob, Bash(npm run lint:*)
---

# Code Review

## ワークフロー
1. 変更ファイルの特定
2. セキュリティチェック（See [SECURITY.md](SECURITY.md)）
3. パフォーマンス分析（See [PERFORMANCE.md](PERFORMANCE.md)）
4. リンター実行: `scripts/run-linters.sh`

## 出力形式
- 🔴 Critical: 必ず修正
- 🟡 Warning: 修正推奨
- 🔵 Suggestion: 検討事項
```

### 引数を受け取るスキル

スキルは `$ARGUMENTS` で引数を受け取れます：

```yaml
---
name: explain-code
description: コードを解説。「○○を説明して」で発動。
---

# Explain Code

以下のコードを初心者向けに解説:

$ARGUMENTS

## 解説形式
1. 概要（1-2文）
2. 処理の流れ
3. 重要なポイント
```

### Bash実行を含むスキル

`!` プレフィックスでBashコマンドを事前実行：

```yaml
---
name: git-status
description: Git状態を確認してサマリーを生成。
allowed-tools: Bash(git *)
---

# Git Status

## 現在の状態
- ブランチ: !`git branch --show-current`
- ステータス: !`git status --short`
- 最近のコミット: !`git log --oneline -5`

## タスク
上記の情報を元に、現在の作業状態をサマリーしてください。
```

### ファイル参照を含むスキル

`@` プレフィックスでファイルを参照：

```yaml
---
name: update-readme
description: READMEを更新。
---

# Update README

現在のREADME:
@README.md

package.json:
@package.json

上記を元にREADMEを最新の状態に更新してください。
```

## 旧コマンドからの移行

### Before (.claude/commands/)
```markdown
# .claude/commands/review.md
コードをレビューして:
$ARGUMENTS
```

### After (.claude/skills/)
```yaml
# .claude/skills/review/SKILL.md
---
name: review
description: コードレビューを実施。
---

# Review

コードをレビューして:
$ARGUMENTS
```

## references/ の作成ガイド

### いつ作るか

| 状況 | 作成するファイル |
|------|------------------|
| セキュリティチェックが必要 | `references/SECURITY.md` |
| パフォーマンス基準がある | `references/PERFORMANCE.md` |
| コーディング規約がある | `references/STYLE_GUIDE.md` |
| 複数のパターン/例がある | `references/PATTERNS.md` |
| APIやスキーマ仕様がある | `references/API_SPEC.md` |
| SKILL.mdが100行超える | 分割して参照 |

### 参照ファイルのフォーマット

```markdown
# タイトル

## 概要
[1-2文で説明]

## チェックリスト
- [ ] 項目1
- [ ] 項目2

## 詳細
[必要に応じて]

## 例
[具体例]
```

### SKILL.mdからの参照方法

```markdown
セキュリティチェック（See [references/SECURITY.md](references/SECURITY.md)）
```

---

## scripts/ の作成ガイド

### いつ作るか

| 状況 | 作成するスクリプト |
|------|-------------------|
| リンター/フォーマッター実行 | `scripts/lint.sh` |
| テスト実行 | `scripts/test.sh` |
| データ変換/分析 | `scripts/analyze.py` |
| ファイル生成 | `scripts/generate.py` |
| 外部API呼び出し | `scripts/fetch.py` |
| バリデーション | `scripts/validate.sh` |

### スクリプトのフォーマット

**Bash:**
```bash
#!/bin/bash
# 説明: 何をするスクリプトか
# 使用方法: ./scripts/xxx.sh [args]

set -e  # エラー時に停止

# 処理
```

**Python:**
```python
#!/usr/bin/env python3
"""
説明: 何をするスクリプトか
使用方法: python scripts/xxx.py [args]
"""

import sys

def main():
    # 処理
    pass

if __name__ == "__main__":
    main()
```

### SKILL.mdからの実行方法

**方法1: !プレフィックス（事前実行）**
```markdown
## コンテキスト
- リント結果: !`./scripts/lint.sh`
```

**方法2: allowed-tools（実行許可）**
```yaml
---
allowed-tools: Bash(./scripts/*)
---
```

**方法3: 手順内で指示**
```markdown
## ワークフロー
1. `./scripts/analyze.py` を実行
2. 結果を確認
```

---

## ベストプラクティス

✅ descriptionにトリガー条件を明記
✅ 単一責任で設計
✅ 必要なツールのみ `allowed-tools` で許可
✅ 複雑なロジックは `references/` に分離
✅ 外部ツール連携は `scripts/` に分離
✅ バージョン管理にコミット
✅ ホットリロード活用（v2.1.2+）

❌ READMEやCHANGELOGを含める
❌ 過剰な説明（Claudeは賢い）
❌ 深いネストの参照構造
❌ `.claude/commands/` の使用（レガシー）
❌ スクリプトに機密情報をハードコード
