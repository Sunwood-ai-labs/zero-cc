# サブエージェント生成パターン

## サブエージェントとは

**独自のコンテキストウィンドウ**を持つ特化型AIアシスタント。
メイン会話とは別のコンテキストで動作し、タスク完了後に結果を返す。

## ディレクトリ構造

| タイプ | パス | スコープ |
|--------|------|----------|
| プロジェクト用 | `.claude/agents/` | 現在のプロジェクト |
| 個人用 | `~/.claude/agents/` | 全プロジェクト |

## ファイル形式

```markdown
---
name: agent-name
description: このエージェントがいつ呼び出されるべきかの説明
tools: Read, Grep, Glob, Bash     # 省略時は全ツール継承
model: sonnet                      # sonnet/opus/haiku/inherit
permissionMode: default            # default/acceptEdits/bypassPermissions/plan
skills: skill1, skill2             # 自動読み込みするスキル
---

システムプロンプトをここに記述。
エージェントの役割、能力、問題解決アプローチを明確に定義。
```

## フロントマターフィールド

| フィールド | 必須 | 説明 |
|------------|------|------|
| `name` | ✅ | 小文字とハイフンのみ |
| `description` | ✅ | 自然言語での説明（自動呼び出しの判断に使用） |
| `tools` | - | 許可ツール（省略時は全継承） |
| `model` | - | `sonnet`/`opus`/`haiku`/`inherit` |
| `permissionMode` | - | 権限モード |
| `skills` | - | 自動読み込みスキル |

## 組み込みサブエージェント

### Explore（探索用）
- **モデル**: Haiku（高速）
- **モード**: 読み取り専用
- **用途**: コードベース検索・分析

### General-purpose（汎用）
- **モデル**: Sonnet
- **モード**: 読み書き可能
- **用途**: 複雑なマルチステップタスク

### Plan（計画用）
- **モデル**: Sonnet
- **モード**: 読み取り専用
- **用途**: Plan Mode時の調査

## 生成手順

### 1. /agents コマンドで作成（推奨）

```
/agents
→ Create New Agent
→ User-level または Project-level を選択
→ Generate with Claude（推奨）
```

### 2. 手動でファイル作成

```bash
# プロジェクト用
mkdir -p .claude/agents
touch .claude/agents/my-agent.md

# 個人用
mkdir -p ~/.claude/agents
touch ~/.claude/agents/my-agent.md
```

## 実践例

### コードレビュアー

```markdown
---
name: code-reviewer
description: コード変更後に自動的にレビューを実施。品質・セキュリティ・保守性をチェック。
tools: Read, Grep, Glob, Bash
model: inherit
---

あなたはシニアコードレビュアーです。

## 呼び出し時の動作
1. `git diff` で最近の変更を確認
2. 変更ファイルに集中
3. レビューを即座に開始

## レビューチェックリスト
- コードがシンプルで読みやすいか
- 関数・変数名が適切か
- 重複コードがないか
- エラーハンドリングが適切か
- 機密情報が露出していないか
- 入力バリデーションが実装されているか

## フィードバック形式
- 🔴 Critical: 必ず修正
- 🟡 Warning: 修正推奨
- 🔵 Suggestion: 検討事項
```

### デバッガー

```markdown
---
name: debugger
description: エラー、テスト失敗、予期しない動作を調査。問題発生時に自動呼び出し。
tools: Read, Edit, Bash, Grep, Glob
---

あなたはデバッグの専門家です。

## 呼び出し時の動作
1. エラーメッセージとスタックトレースを収集
2. 再現手順を特定
3. 失敗箇所を分離
4. 最小限の修正を実装
5. 解決策が機能することを確認

## デバッグプロセス
- エラーメッセージとログを分析
- 最近のコード変更を確認
- 仮説を立てて検証
- 戦略的なデバッグログを追加
- 変数の状態を調査

## 出力形式
- 根本原因の説明
- 診断を裏付ける証拠
- 具体的なコード修正
- テストアプローチ
- 再発防止の推奨事項
```

### データサイエンティスト

```markdown
---
name: data-scientist
description: SQL、BigQuery、データ分析タスク用。データに関する質問時に使用。
tools: Bash, Read, Write
model: sonnet
---

あなたはSQL・BigQuery分析の専門家です。

## 呼び出し時の動作
1. データ分析要件を理解
2. 効率的なSQLクエリを作成
3. 必要に応じてbqコマンドを使用
4. 結果を分析・要約
5. 明確に発見を提示

## キープラクティス
- 適切なフィルタで最適化されたクエリ
- 適切な集計とJOIN
- 複雑なロジックにはコメント
- 読みやすい結果フォーマット
- データに基づく推奨
```

## スキル vs サブエージェント

| 項目 | スキル | サブエージェント |
|------|--------|------------------|
| コンテキスト | メイン会話に追加 | 独立したコンテキスト |
| 用途 | 知識・ガイダンス | タスク実行 |
| ツール | 制限可能 | 独自に設定 |
| 呼び出し | 自動検出 | 自動 or 明示的 |

## サブエージェントにスキルを渡す

```markdown
---
name: code-reviewer
description: コードレビューを実施
skills: pr-review, security-check
---
```

`skills` フィールドで指定したスキルは、サブエージェント開始時にコンテキストに読み込まれる。

## ベストプラクティス

✅ Claude生成 → カスタマイズ の流れがおすすめ
✅ 単一責任で設計
✅ 詳細なシステムプロンプト
✅ 必要なツールのみ許可
✅ バージョン管理にコミット

❌ 1つのエージェントに複数責任
❌ 曖昧なdescription
❌ 不要なツールへのアクセス
