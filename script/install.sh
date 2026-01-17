#!/usr/bin/env bash
set -euo pipefail

# zero-cc installer (uv-style: curl | bash)
#
# What it does:
#  - Installs Claude Code if `claude` is missing (official native installer)
#  - Ensures ~/.local/bin is in PATH (via ~/.bashrc.d/10-path-localbin.sh)
#  - Writes:
#      ~/.bashrc.d/00-llm-secrets.sh
#      ~/.bashrc.d/60-claude-modes.sh
#    and ensures ~/.bashrc sources ~/.bashrc.d/*.sh
#
# Usage (examples):
#   curl -fsSL https://raw.githubusercontent.com/Sunwood-ai-labs/zero-cc/main/script/install.sh | bash
#   ZAI_API_KEY="xxx" CC_NONROOT_USER="aslan" curl -fsSL .../install.sh | bash -s -- --force --perms

FORCE=0
NO_BASHRC=0
WRITE_PERMS=0
SKIP_CLAUDE_INSTALL=0

while [ $# -gt 0 ]; do
  case "$1" in
    --force) FORCE=1 ;;
    --no-bashrc) NO_BASHRC=1 ;;
    --perms) WRITE_PERMS=1 ;;
    --skip-claude-install) SKIP_CLAUDE_INSTALL=1 ;;
    -h|--help)
      cat <<'HELP'
Options:
  --force                overwrite existing files (creates backups)
  --no-bashrc            do not modify ~/.bashrc
  --perms                create ./.claude/settings.local.json (permissions template)
  --skip-claude-install  do not install Claude Code even if missing

Env:
  ZAI_API_KEY        Z.AI API key (optional; prompts if TTY, else placeholder)
  CC_NONROOT_USER    user for ccd-* downgrade when running as root (default: current user)
HELP
      exit 0
      ;;
    *)
      echo "[install] unknown option: $1" >&2
      exit 2
      ;;
  esac
  shift
done

timestamp() { date +%Y%m%d-%H%M%S; }
has_tty() { [ -t 0 ] && [ -t 1 ]; }

backup_if_exists() {
  local f="$1"
  if [ -e "$f" ]; then
    cp -a "$f" "${f}.bak.$(timestamp)"
  fi
}

write_file_strict() {
  # $1=path $2=content $3=mode
  local path="$1" content="$2" mode="$3"

  if [ -e "$path" ] && [ "$FORCE" -ne 1 ]; then
    echo "[install] exists (skip; use --force to overwrite): $path" >&2
    return 0
  fi

  backup_if_exists "$path"
  umask 077
  printf '%s' "$content" > "$path"
  chmod "$mode" "$path"
}

ensure_bashrc_loader() {
  local bashrc="$1"
  local marker="user snippets (modular)"

  [ -e "$bashrc" ] || touch "$bashrc"

  if grep -q "$marker" "$bashrc"; then
    return 0
  fi

  cat >> "$bashrc" <<'BLOCK'

# ---- user snippets (modular) ----
if [ -d "$HOME/.bashrc.d" ]; then
  for f in "$HOME/.bashrc.d/"*.sh; do
    [ -e "$f" ] || continue
    . "$f"
  done
fi
BLOCK
}

pick_zai_key() {
  if [ -n "${ZAI_API_KEY:-}" ]; then
    echo "$ZAI_API_KEY"
    return 0
  fi

  if has_tty; then
    printf "ZAI_API_KEY: " >&2
    # shellcheck disable=SC2162
    read -s key
    echo >&2
    echo "$key"
    return 0
  fi

  echo "YOUR_ZAI_API_KEY"
}

pick_nonroot_user() {
  if [ -n "${CC_NONROOT_USER:-}" ]; then
    echo "$CC_NONROOT_USER"
    return 0
  fi
  # default: current user (works for typical non-root usage)
  id -un
}

install_claude_if_missing() {
  if [ "$SKIP_CLAUDE_INSTALL" -eq 1 ]; then
    return 0
  fi

  if command -v claude >/dev/null 2>&1; then
    return 0
  fi

  echo "[install] Claude Code not found. Installing via official installer..." >&2
  # Official native install (macOS/Linux/WSL)
  # curl -fsSL https://claude.ai/install.sh | bash
  # Installs symlink to ~/.local/bin/claude (ensure PATH includes ~/.local/bin)
  curl -fsSL https://claude.ai/install.sh | bash

  if ! command -v claude >/dev/null 2>&1; then
    echo "[install] Claude Code install finished but 'claude' is still not in PATH." >&2
    echo "[install] You may need to reload your shell or ensure ~/.local/bin is in PATH." >&2
  fi
}

write_path_snippet() {
  local bashrc_d="$HOME/.bashrc.d"
  mkdir -p "$bashrc_d"
  chmod 700 "$bashrc_d"

  local path_file="$bashrc_d/10-path-localbin.sh"
  local content
  content=$(
    cat <<'EOF'
# Ensure ~/.local/bin is on PATH (Claude Code installer links here)
# Only run in bash
[ -n "$BASH_VERSION" ] || return 0
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) export PATH="$HOME/.local/bin:$PATH" ;;
esac
EOF
  )
  write_file_strict "$path_file" "$content" 600
}

write_secrets_and_modes() {
  local bashrc_d="$HOME/.bashrc.d"
  mkdir -p "$bashrc_d"
  chmod 700 "$bashrc_d"

  local zai_key nonroot_user
  zai_key="$(pick_zai_key)"
  nonroot_user="$(pick_nonroot_user)"

  local secrets_path="$bashrc_d/00-llm-secrets.sh"
  local secrets_content
  secrets_content=$(
    cat <<EOF
# LLM Secrets (DO NOT SHARE)

# --- Z.AI (Anthropic-compatible endpoint for Claude Code) ---
ZAI_API_KEY="${zai_key}"

# --- OpenRouter (keep for reference) ---
# OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY"

# ccd-* を root で実行した場合に降格するユーザー（dangerous mode対策）
CC_NONROOT_USER="${nonroot_user}"
EOF
  )
  write_file_strict "$secrets_path" "$secrets_content" 600

  local modes_path="$bashrc_d/60-claude-modes.sh"
  local modes_content
  modes_content=$(
    cat <<'EOF'
# ===== Claude Code: mode switching =====
# Only run in bash
[ -n "$BASH_VERSION" ] || return 0

# --- Z.AI Anthropic-compatible endpoint ---
# Z.AI docs:
#   ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
#   ANTHROPIC_AUTH_TOKEN=your_zai_api_key
#   API_TIMEOUT_MS=3000000 (optional)
ZAI_ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"

# Model mapping (as requested)
ZAI_DEFAULT_HAIKU_MODEL="glm-4.5-air"
ZAI_DEFAULT_SONNET_MODEL="glm-4.7"
ZAI_DEFAULT_OPUS_MODEL="glm-4.7"

# --- OpenRouter config (kept as comments for reference) ---
# OPENROUTER_BASE_URL="https://openrouter.ai/api"
# OPENROUTER_GLM_FREE_MODEL="z-ai/glm-4.5-air:free"
# export ANTHROPIC_BASE_URL="$OPENROUTER_BASE_URL"
# export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
# export ANTHROPIC_API_KEY=""
# export ANTHROPIC_DEFAULT_OPUS_MODEL="$OPENROUTER_GLM_FREE_MODEL"
# export ANTHROPIC_DEFAULT_SONNET_MODEL="$OPENROUTER_GLM_FREE_MODEL"
# export ANTHROPIC_DEFAULT_HAIKU_MODEL="$OPENROUTER_GLM_FREE_MODEL"


# --- internal helper: if root, re-exec as non-root for dangerous mode ---
_ccd_reexec_as_nonroot_if_root() {
  [ "${EUID:-$(id -u)}" -eq 0 ] || return 1

  # shellcheck disable=SC1090
  . "$HOME/.bashrc.d/00-llm-secrets.sh"

  if [ -z "${CC_NONROOT_USER:-}" ]; then
    echo "[ccd] CC_NONROOT_USER が未設定です: ~/.bashrc.d/00-llm-secrets.sh" >&2
    exit 2
  fi

  if ! id "$CC_NONROOT_USER" >/dev/null 2>&1; then
    echo "[ccd] 指定ユーザーが存在しません: CC_NONROOT_USER=$CC_NONROOT_USER" >&2
    exit 2
  fi

  exec sudo -u "$CC_NONROOT_USER" -H bash -lc 'source ~/.bashrc; '"$1"' "$@"' bash "$@"
}

# 1) 通常（Anthropic 側ログイン/サブスク運用想定）
cc_std() (
  unset ANTHROPIC_BASE_URL
  unset ANTHROPIC_AUTH_TOKEN
  unset ANTHROPIC_DEFAULT_OPUS_MODEL
  unset ANTHROPIC_DEFAULT_SONNET_MODEL
  unset ANTHROPIC_DEFAULT_HAIKU_MODEL
  unset ANTHROPIC_API_KEY
  unset API_TIMEOUT_MS
  command claude "$@"
)

# 2) GLM (Z.AI Anthropic endpoint)
cc_glm() (
  # shellcheck disable=SC1090
  . "$HOME/.bashrc.d/00-llm-secrets.sh"

  if [ -z "${ZAI_API_KEY:-}" ]; then
    echo "[cc_glm] ZAI_API_KEY が未設定です: ~/.bashrc.d/00-llm-secrets.sh を編集してください" >&2
    exit 2
  fi

  export ANTHROPIC_BASE_URL="$ZAI_ANTHROPIC_BASE_URL"
  export ANTHROPIC_AUTH_TOKEN="$ZAI_API_KEY"
  export ANTHROPIC_API_KEY=""

  # optional, but recommended by Z.AI docs
  export API_TIMEOUT_MS="${API_TIMEOUT_MS:-3000000}"

  export ANTHROPIC_DEFAULT_HAIKU_MODEL="$ZAI_DEFAULT_HAIKU_MODEL"
  export ANTHROPIC_DEFAULT_SONNET_MODEL="$ZAI_DEFAULT_SONNET_MODEL"
  export ANTHROPIC_DEFAULT_OPUS_MODEL="$ZAI_DEFAULT_OPUS_MODEL"

  command claude "$@"
)

# 3) Dangerous（root/sudo では Claude Code 側で拒否されるため、rootなら自動で非rootに降格）
ccd_std() (
  _ccd_reexec_as_nonroot_if_root ccd_std "$@" || true

  unset ANTHROPIC_BASE_URL
  unset ANTHROPIC_AUTH_TOKEN
  unset ANTHROPIC_DEFAULT_OPUS_MODEL
  unset ANTHROPIC_DEFAULT_SONNET_MODEL
  unset ANTHROPIC_DEFAULT_HAIKU_MODEL
  unset ANTHROPIC_API_KEY
  unset API_TIMEOUT_MS

  command claude --dangerously-skip-permissions "$@"
)

ccd_glm() (
  _ccd_reexec_as_nonroot_if_root ccd_glm "$@" || true

  # shellcheck disable=SC1090
  . "$HOME/.bashrc.d/00-llm-secrets.sh"

  if [ -z "${ZAI_API_KEY:-}" ]; then
    echo "[ccd_glm] ZAI_API_KEY が未設定です: ~/.bashrc.d/00-llm-secrets.sh を編集してください" >&2
    exit 2
  fi

  export ANTHROPIC_BASE_URL="$ZAI_ANTHROPIC_BASE_URL"
  export ANTHROPIC_AUTH_TOKEN="$ZAI_API_KEY"
  export ANTHROPIC_API_KEY=""
  export API_TIMEOUT_MS="${API_TIMEOUT_MS:-3000000}"

  export ANTHROPIC_DEFAULT_HAIKU_MODEL="$ZAI_DEFAULT_HAIKU_MODEL"
  export ANTHROPIC_DEFAULT_SONNET_MODEL="$ZAI_DEFAULT_SONNET_MODEL"
  export ANTHROPIC_DEFAULT_OPUS_MODEL="$ZAI_DEFAULT_OPUS_MODEL"

  command claude --dangerously-skip-permissions "$@"
)

alias cc-st='cc_std'
alias cc-glm='cc_glm'
alias ccd-st='ccd_std'
alias ccd-glm='ccd_glm'
EOF
  )
  write_file_strict "$modes_path" "$modes_content" 600
}

write_project_permissions_template() {
  local dir="$PWD/.claude"
  local path="$dir/settings.local.json"

  mkdir -p "$dir"

  if [ -e "$path" ] && [ "$FORCE" -ne 1 ]; then
    echo "[install] exists (skip; use --force to overwrite): $path" >&2
    return 0
  fi

  backup_if_exists "$path"
  umask 077
  cat > "$path" <<'JSON'
{
  "permissions": {
    "allow": [
      "Bash(pwd)",
      "Bash(ls)",
      "Bash(ls:*)",
      "Bash(tree:*)",
      "Bash(find:*)",
      "Bash(grep:*)",
      "Bash(rg:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(cd:*)",
      "Bash(mkdir:*)",
      "Bash(mv:*)",
      "Bash(cp:*)",
      "Bash(touch:*)",
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(uv:*)"
    ],
    "deny": [
      "Bash(sudo:*)",
      "Bash(su:*)",
      "Bash(rm -rf:*)",
      "Bash(rm:*)",
      "Bash(dd:*)",
      "Bash(mkfs:*)",
      "Bash(chmod:*)",
      "Bash(chown:*)",
      "Bash(mount:*)",
      "Bash(umount:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  }
}
JSON
  chmod 600 "$path"
  echo "[install] wrote: $path"
}

main() {
  install_claude_if_missing
  write_path_snippet
  write_secrets_and_modes

  if [ "$NO_BASHRC" -ne 1 ]; then
    ensure_bashrc_loader "$HOME/.bashrc"
  fi

  if [ "$WRITE_PERMS" -eq 1 ]; then
    write_project_permissions_template
  fi

  echo "[install] done. Run: source ~/.bashrc"
  echo "[install] commands: cc-st / cc-glm / ccd-st / ccd-glm"
  echo "[install] verify: claude doctor"
}

main
