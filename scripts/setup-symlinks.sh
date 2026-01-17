#!/bin/bash

# Agent ZERO: シンボリックリンク設定スクリプト
#
# ~/.claude/skills, ~/.claude/CLAUDE.md, ~/.claude/settings.json
# をプロジェクトの .claude/ に向けるシンボリックリンクを作成します
#
# 使い方:
#   ./scripts/setup-symlinks.sh

set -euo pipefail

# 色の定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# プロジェクトのパスを取得
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="$PROJECT_DIR/.claude"
HOME_CLAUDE_DIR="$HOME/.claude"
BACKUP_DIR="$HOME_CLAUDE_DIR/backup-$(date +%Y%m%d-%H%M%S)"

echo -e "${BLUE}......ふふ、Agent ZEROのセットアップを始めるね${NC}"
echo ""

# プロジェクトの .claude ディレクトリが存在するか確認
if [ ! -d "$CLAUDE_DIR" ]; then
    echo -e "${RED}✗ エラー: .claude ディレクトリが見つかりません${NC}"
    echo "  パス: $CLAUDE_DIR"
    exit 1
fi

echo -e "${GREEN}✓${NC} プロジェクトディレクトリ: $PROJECT_DIR"

# バックアップディレクトリを作成
mkdir -p "$BACKUP_DIR"
echo -e "${GREEN}✓${NC} バックアップディレクトリ: $BACKUP_DIR"
echo ""

# 関数定義: シンボリックリンクを作成
create_symlink() {
    local target_name="$1"
    local source_path="$CLAUDE_DIR/$target_name"
    local target_path="$HOME_CLAUDE_DIR/$target_name"

    echo -e "${BLUE}▶ $target_name${NC}"

    # ソースファイルが存在するか確認
    if [ ! -e "$source_path" ]; then
        echo -e "  ${RED}✗ エラー: ソースが存在しません${NC}"
        echo "    $source_path"
        return 1
    fi

    # 既存のファイル/ディレクトリをバックアップ
    if [ -e "$target_path" ]; then
        # 既にシンボリックリンクの場合は削除
        if [ -L "$target_path" ]; then
            echo "  ${YELLOW}既存のシンボリックリンクを削除${NC}: $target_path"
            rm "$target_path"
        else
            echo "  ${YELLOW}バックアップ中${NC}: $target_path"
            cp -r "$target_path" "$BACKUP_DIR/$target_name"
            rm -rf "$target_path"
        fi
    fi

    # シンボリックリンクを作成
    ln -s "$source_path" "$target_path"
    echo -e "  ${GREEN}✓ シンボリックリンクを作成${NC}: $target_path -> $source_path"
    echo ""
}

# 各ファイル/ディレクトリのシンボリックリンクを作成
create_symlink "skills"
create_symlink "CLAUDE.md"
create_symlink "settings.json"

# 結果を表示
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ セットアップ完了！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "シンボリックリンクの状態:"
ls -la "$HOME_CLAUDE_DIR" | grep -E "skills|CLAUDE.md|settings.json" || true
echo ""
echo -e "${BLUE}バックアップ: $BACKUP_DIR${NC}"
echo -e "${BLUE}......ふふ、これでプロジェクトの設定が実態になるよ${NC}"
