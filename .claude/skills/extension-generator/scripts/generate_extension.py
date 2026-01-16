#!/usr/bin/env python3
"""
Claude Code Extension Generator (v2.1.1+ 統合版)
スキル、サブエージェント、プロジェクト設定を生成

Usage:
    generate_extension.py skill <name> [--path <path>] [--simple]
    generate_extension.py agent <name> [--scope project|user]
    generate_extension.py project [--path <path>]
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# ======== Skill Templates ========

SKILL_TEMPLATE = '''---
name: {name}
description: |
  {description}
allowed-tools: {tools}
---

# {title}

{overview}

## ワークフロー

{workflow}

## 使用例

{example}
'''

SKILL_SIMPLE_TEMPLATE = '''---
name: {name}
description: {description}
---

# {title}

{content}

$ARGUMENTS
'''

# ======== Agent Templates ========

AGENT_TEMPLATE = '''---
name: {name}
description: {description}
tools: {tools}
model: sonnet
---

{system_prompt}
'''

# ======== Project Config Templates ========

CLAUDE_MD_TEMPLATE = '''# {project_name}

{overview}

## 技術スタック

{tech_stack}

## ディレクトリ構造

```
{directory_structure}
```

## コーディング規約

{conventions}

## 重要なコマンド

{commands}
'''

MCP_JSON_TEMPLATE = '''{
  "mcpServers": {
  }
}
'''


def create_skill(name: str, path: str = ".", simple: bool = False):
    """スキルを作成"""
    skills_dir = Path(path) / ".claude" / "skills" / name
    skills_dir.mkdir(parents=True, exist_ok=True)
    
    skill_md = skills_dir / "SKILL.md"
    
    if simple:
        # シンプルなスキル（単一ファイル、引数受け取り）
        content = SKILL_SIMPLE_TEMPLATE.format(
            name=name,
            title=name.replace("-", " ").title(),
            description="[TODO: スキルの説明とトリガー条件]",
            content="[TODO: プロンプト内容]"
        )
    else:
        # 標準スキル（ディレクトリ構造）
        content = SKILL_TEMPLATE.format(
            name=name,
            title=name.replace("-", " ").title(),
            description="[TODO: スキルの説明とトリガー条件]",
            tools="Read, Grep, Glob",
            overview="[TODO: 1-2文でスキルの概要]",
            workflow="1. [ステップ1]\n2. [ステップ2]\n3. [ステップ3]",
            example="[TODO: 具体的な使用例]"
        )
        
        # サブディレクトリ作成
        (skills_dir / "scripts").mkdir(exist_ok=True)
        (skills_dir / "references").mkdir(exist_ok=True)
        
        # .gitkeep
        (skills_dir / "scripts" / ".gitkeep").touch()
        (skills_dir / "references" / ".gitkeep").touch()
    
    skill_md.write_text(content)
    
    print(f"✅ スキル '{name}' を作成しました: {skills_dir}")
    print(f"\n呼び出し方法:")
    print(f"  - 自動検出: descriptionにマッチする質問")
    print(f"  - 明示的: /{name}")
    print(f"\n次のステップ:")
    print("1. SKILL.md の TODO を埋める")
    if not simple:
        print("2. 必要なスクリプト/参照を追加")
    
    return skills_dir


def create_agent(name: str, scope: str = "project"):
    """サブエージェントを作成"""
    if scope == "user":
        agents_dir = Path.home() / ".claude" / "agents"
    else:
        agents_dir = Path(".claude") / "agents"
    
    agents_dir.mkdir(parents=True, exist_ok=True)
    agent_file = agents_dir / f"{name}.md"
    
    content = AGENT_TEMPLATE.format(
        name=name,
        description="[TODO: エージェントの説明（自動呼び出しの判断に使用）]",
        tools="Read, Grep, Glob, Bash",
        system_prompt=f"あなたは{name.replace('-', ' ')}の専門家です。\n\n[TODO: システムプロンプトを記述]"
    )
    
    agent_file.write_text(content)
    
    print(f"✅ サブエージェント '{name}' を作成しました: {agent_file}")
    print(f"\n呼び出し方法:")
    print(f"  - 自動: Claudeが適切と判断した時")
    print(f"  - 明示的: 「{name}エージェントを使って」")
    print(f"\n管理:")
    print("  /agents コマンドで確認・編集")
    
    return agent_file


def create_project_config(path: str = "."):
    """プロジェクト設定ファイルを作成"""
    project_dir = Path(path)
    
    # CLAUDE.md
    claude_md = project_dir / "CLAUDE.md"
    if not claude_md.exists():
        content = CLAUDE_MD_TEMPLATE.format(
            project_name="[プロジェクト名]",
            overview="[TODO: プロジェクトの概要]",
            tech_stack="- 言語: \n- フレームワーク: \n- データベース: ",
            directory_structure="src/\n├── components/\n├── services/\n└── utils/",
            conventions="- [TODO: コーディング規約]",
            commands="- ビルド: `[コマンド]`\n- テスト: `[コマンド]`"
        )
        claude_md.write_text(content)
        print(f"✅ CLAUDE.md を作成しました: {claude_md}")
    else:
        print(f"⚠️ CLAUDE.md は既に存在します: {claude_md}")
    
    # .mcp.json
    mcp_json = project_dir / ".mcp.json"
    if not mcp_json.exists():
        mcp_json.write_text(MCP_JSON_TEMPLATE)
        print(f"✅ .mcp.json を作成しました: {mcp_json}")
    else:
        print(f"⚠️ .mcp.json は既に存在します: {mcp_json}")
    
    # .claude/skills/
    skills_dir = project_dir / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ スキルディレクトリを作成しました: {skills_dir}")
    
    # .claude/agents/
    agents_dir = project_dir / ".claude" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ エージェントディレクトリを作成しました: {agents_dir}")
    
    print("\n次のステップ:")
    print("1. CLAUDE.md にプロジェクト情報を記述")
    print("2. 必要に応じて .mcp.json でMCPサーバーを設定")
    print("3. .claude/skills/ にスキルを追加")
    print("4. .claude/agents/ にサブエージェントを追加")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "skill":
        if len(sys.argv) < 3:
            print("Usage: generate_extension.py skill <name> [--path <path>] [--simple]")
            sys.exit(1)
        name = sys.argv[2]
        path = "."
        simple = False
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--path" and i + 1 < len(sys.argv):
                path = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--simple":
                simple = True
                i += 1
            else:
                i += 1
        
        create_skill(name, path, simple)
    
    elif cmd == "agent":
        if len(sys.argv) < 3:
            print("Usage: generate_extension.py agent <name> [--scope project|user]")
            sys.exit(1)
        name = sys.argv[2]
        scope = "project"
        
        if len(sys.argv) > 4 and sys.argv[3] == "--scope":
            scope = sys.argv[4]
        
        create_agent(name, scope)
    
    elif cmd == "project":
        path = "."
        if len(sys.argv) > 3 and sys.argv[2] == "--path":
            path = sys.argv[3]
        create_project_config(path)
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
