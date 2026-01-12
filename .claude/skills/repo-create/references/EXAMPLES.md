# 使用例

## 基本的な使用例

```bash
# パブリックリポジトリを作成
/repo-create my-awesome-project

# プライベートリポジトリを作成
/repo-create my-app --private

# 説明付きで作成
/repo-create my-lib --description "An awesome library"

# カレントディレクトリにクローン
/repo-create my-project --clone
```

## 実行例

### 例1: シンプルなプロジェクト

```bash
/repo-create hello-world
```

**出力:**
```
✓ GitHub repository "hello-world" created
  URL: https://github.com/username/hello-world

📝 Initial files created:
  - README.md
  - .gitignore
  - LICENSE (MIT)

🚀 Ready to code!
```

### 例2: プライベートリポジトリ

```bash
/repo-create secret-project --private --description "Internal tools"
```

**出力:**
```
✓ Private repository "secret-project" created
  URL: https://github.com/username/secret-project

📝 Initial files created:
  - README.md
  - .gitignore
  - LICENSE (Apache-2.0)

🔒 This is a private repository
```

### 例3: クローンして開始

```bash
/repo-create new-service --clone
```

**出力:**
```
✓ GitHub repository "new-service" created
  URL: https://github.com/username/new-service

📁 Cloned to: /current/directory/new-service

📝 Initial files created:
  - README.md
  - .gitignore
  - LICENSE
  - assets/.gitkeep

✓ Initial commit complete

🎯 Next steps:
  cd new-service
  # Start coding!
```
