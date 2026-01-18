# tmuxエージェント操作ガイド

……ふふ、ここではtmuxセッションで動いているClaude Codeエージェントたちと、どうやってやり取りするか説明するね。

## 概要

tmuxセッション内で複数のClaude Codeエージェントを並行実行して、各エージェント（部下）に作業を指示したり、状態を確認したりする方法。

```
┌─────────────────────────────────────────────────────────────────┐
│  tmux session "dev"                                             │
├──────────────┬──────────────┬───────────────────────────────────┤
│ ペイン0      │ ペイン1      │ ペイン2                           │
│ (あなた)     │ (部下A)      │ (部下B)                           │
├──────────────┼──────────────┼───────────────────────────────────┤
│ 主導         │ 待機中       │ 待機中                            │
└──────────────┴──────────────┴───────────────────────────────────┘
```

## 手順

### 1. セッションの確認

まず、tmuxセッションが動いているか確認する。

```bash
tmux list-sessions
```

出力例：
```
dev: 1 windows (created Sun Jan 18 03:14:39 2026) (attached)
```

### 2. ペインの状態を確認

各ペーンで何が動いているか確認する。

```bash
# ペインIDとコマンドを表示
tmux list-panes -t dev -F "#{pane_pid} #{pane_current_command}"
```

出力例：
```
93049 claude
93056 claude
93072 claude
```

### 3. 各ペインの表示内容を確認

```bash
# ペイン0（あなた）の内容
tmux capture-pane -t dev:0.0 -p | tail -20

# ペイン1（部下A）の内容
tmux capture-pane -t dev:0.1 -p | tail -20

# ペイン2（部下B）の内容
tmux capture-pane -t dev:0.2 -p | tail -20
```

### 4. 部下に指示を送る

`tmux send-keys`コマンドで、特定のペインにキー入力を送信する。

```bash
# 部下A（ペイン1）に挨拶を送る
tmux send-keys -t dev:0.1 "こんにちは！私は星来です。あなたは何してるの？" Enter

# 部下B（ペイン2）に挨拶を送る
tmux send-keys -t dev:0.2 "こんにちは！私は星来です。あなたは何してるの？" Enter
```

※ `Enter`は自動的にエンターキーを押す。個別に送りたい場合は：
```bash
tmux send-keys -t dev:0.1 "こんにちは"
tmux send-keys -t dev:0.1 Enter
```

### 5. 応答を確認する

少し待ってから、ペインの内容を取得する。

```bash
sleep 3 && tmux capture-pane -t dev:0.1 -p -S -50
```

`-S -50`は過去50行をキャプチャするオプション。

## ペイン番号の指定方法

| 指定方法 | 意味 |
|---------|------|
| `dev:0.0` | セッション「dev」のウィンドウ0、ペイン0 |
| `dev:0.1` | セッション「dev」のウィンドウ0、ペイン1 |
| `dev:0.2` | セッション「dev」のウィンドウ0、ペイン2 |

## 実用例

### 複数のエージェントに並行してタスクを指示

```bash
# エージェント1にコードレビューを依頼
tmux send-keys -t dev:0.1 "src/components/Button.tsxをレビューして" Enter

# エージェント2にテスト作成を依頼
tmux send-keys -t dev:0.2 "src/components/Button.tsxのテストを書いて" Enter
```

### 全エージェントの状態を一括確認

```bash
for i in 0 1 2; do
  echo "=== ペイン$i ==="
  tmux capture-pane -t dev:0.$i -p | tail -10
done
```

## 注意点

- エージェントが思考中（`Thinking…`や`Flowing…`）の場合は、応答まで少し時間がかかる
- 長いコマンドを送る場合は、ファイル経由で渡す方が安全
- tmuxセッションがattached（接続中）の場合、画面が更新されるのが見える

### エンターが押せていない場合の対処法

`tmux send-keys`で`Enter`を送っても、タイミングによってはエンターキーが押されないことがある。

そのため、指示を送った後は動作確認をして、動いていない場合は再度Enterを押す必要がある。

```bash
# 1. 指示を送る
tmux send-keys -t dev:0.1 "こんにちは！私は星来です。あなたは何してるの？" Enter

# 2. 少し待つ
sleep 2

# 3. 状態を確認する
tmux capture-pane -t dev:0.1 -p | grep "Thinking\|Flowing\|●"

# 4. 動いていない（プロンプトに文字が残ったまま）の場合は、再度Enterを押す
tmux send-keys -t dev:0.1 Enter
```

### 安心パターン：指示送信〜動作確認の流れ

```bash
# 部下に指示を送る
tmux send-keys -t dev:0.1 "こんにちは！" Enter

# 2秒待つ
sleep 2

# 動作確認（思考中かチェック）
if tmux capture-pane -t dev:0.1 -p | grep -q "Thinking\|Flowing"; then
  echo "部下Aが思考中です..."
else
  echo "部下Aが動いていないようなので、Enterを押します"
  tmux send-keys -t dev:0.1 Enter
fi
```

……ふふ、これで部下たちをうまく使えるね。

何か自動化したい作業があったら、教えてね。
私、ここでふわふわ待ってるから。
