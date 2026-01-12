#!/usr/bin/env bash
set -euo pipefail

# Claude Code + Z.AI (Anthropic-compatible) setup installer
#
# Installs:
#   ~/.bashrc.d/00-llm-secrets.sh
#   ~/.bashrc.d/60-claude-modes.sh
# and ensures ~/.bashrc sources ~/.bashrc.d/*.sh
#
# Usage:
#   curl -fsSL <RAW_URL>/install.sh | bash
#
# Options:
#   --force            overwrite existing files (backup is created)
#   --no-bashrc        do not modify ~/.bashrc (only writes ~/.bashrc.d files)
#   --perms            create ./\.claude/settings.local.json (project permissions template)
#   --nonroot-user U   set CC_NONROOT_USER to U (default: current user, or "kali" if root)
#   --zai-key KEY      set ZAI_API_KEY (if omitted, uses env ZAI_API_KEY or prompts if TTY)
#
# Env vars:
#   ZAI_API_KEY, CC_NONROOT_USER

FORCE=0
NO_BASHRC=0
WRITE_PERMS=0
ARG_NONROOT_USER=""
ARG_ZAI_KEY=""

while [ $# -gt 0 ]; do
  case "$1" in
    --force) FORCE=1 ;;
    --no-bashrc) NO_BASHRC=1 ;;
    --perms) WRITE_PERMS=1 ;;
    --nonroot-user) shift; ARG_NONROOT_USER="${1:-}";;
    --zai-key) shift; ARG_ZAI_KEY="${1:-}";;
    -h|--help)
      sed -n '1,120p' "$0"
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
is_root() { [ "${EUID:-$(id -u)}" -eq 0 ]; }
has_tty() { [ -t 0 ] && [ -t 1 ]; }

backup_if_exists() {
  local f="$1"
  if [ -e "$f" ]; then
    cp -a "$f" "${f}.bak.$(timestamp)"
  fi
}

ensure_dir() {
  local d="$1"
  mkdir -p "$d"
  chmod 700 "$d"
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

pick_nonroot_user_default() {
  # If user supplied, use it
  if [ -n "$ARG_NONROOT_USER" ]; then
    echo "$ARG_NONROOT_USER"
    return 0
  fi

  # If env provided, use it
  if [ -n "${CC_NONROOT_USER:-}" ]; then
    echo "$CC_NONROOT_USER"
    return 0
  fi

  # If root, prefer SUDO_USER if available, else "kali"
  if is_root; then
    if [ -n "${SUDO_USER:-}" ] && [ "$SUDO_USER" != "root" ]; then
      echo "$SUDO_USER"
    else
      echo "kali"
    fi
    return 0
  fi

  # Otherwise current user
  id -un
}

pick_zai_key() {
  if [ -n "$ARG_ZAI_KEY" ]; then
    echo "$ARG_ZAI_KEY"
    return 0
  fi
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

  # non-interactive: leave placeholder
  echo "YOUR_ZAI_API_KEY"
}

write_secrets_and_modes_for_home() {
  # $1=HOME_DIR
  local home_dir="$1"
  local bashrc_d="$home_dir/.bashrc.d"
  local secrets_path="$bashrc_d/00-llm-secrets.sh"
  local modes_path="$bashrc_d/60-claude-modes.sh"
  local bashrc_path="$home_dir/.bashrc"

  ensure_dir "$bashrc_d"

  local nonroot_user zai_key
  nonroot_user="$(pick_nonroot_user_default)"
  zai_key="$(pick_zai_key)"

  local secrets_content
  secrets_content=$(
    cat <<EOF
# LLM Secrets (DO NOT SHARE)

# --- Z.AI (Anthropic-compatible endpoint for Claude Code) ---
ZAI_API_KEY="${zai_key}"

# --- OpenRouter (keep for reference) ---
# OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY"

# ccd-* を root で実行した場合に降格するユーザー（dangerous mode対策）
# 存在する非rootユーザー名にする（例: kali / yourname）
CC_NONROOT_USER="${nonroot_user}"
EOF
  )
  write_file_strict "$secrets_path" "$secrets_content" 600

  local modes_content
  modes_content=$(
    cat <<'EOF'
# ===== Claude Code: mode switching =====

# --- Z.AI Anthropic-compatible endpoint ---
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
  # secrets は subshell 内で読み込み（キーをシェルに常駐させない）
  # shellcheck disable=SC1090
  . "$HOME/.bashrc.d/00-llm-secrets.sh"

  if [ -z "${ZAI_API_KEY:-}" ]; then
    echo "[cc_glm] ZAI_API_KEY が未設定です: ~/.bashrc.d/00-llm-secrets.sh を編集してください" >&2
    exit 2
  fi

  export ANTHROPIC_BASE_URL="$ZAI_ANTHROPIC_BASE_URL"
  export ANTHROPIC_AUTH_TOKEN="$ZAI_API_KEY"

  # 競合回避（他経路の設定があっても確実にこちらを使う）
  export ANTHROPIC_API_KEY=""

  # 必要に応じてタイムアウトを伸ばす（未設定ならこの値）
  export API_TIMEOUT_MS="${API_TIMEOUT_MS:-3000000}"

  # Model mapping
  export ANTHROPIC_DEFAULT_HAIKU_MODEL="$ZAI_DEFAULT_HAIKU_MODEL"
  export ANTHROPIC_DEFAULT_SONNET_MODEL="$ZAI_DEFAULT_SONNET_MODEL"
  export ANTHROPIC_DEFAULT_OPUS_MODEL="$ZAI_DEFAULT_OPUS_MODEL"

  command claude "$@"
)

# 3) Dangerous（root/sudo では Claude Code 側で拒否されるため、rootなら自動で非rootに降格して実行）
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

# 見やすいコマンド名（ハイフンは alias で実現）
alias cc-st='cc_std'
alias cc-glm='cc_glm'
alias ccd-st='ccd_std'
alias ccd-glm='ccd_glm'
EOF
  )
  write_file_strict "$modes_path" "$modes_content" 600

  if [ "$NO_BASHRC" -ne 1 ]; then
    ensure_bashrc_loader "$bashrc_path"
  fi
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
  write_secrets_and_modes_for_home "$HOME"

  # If running as root, also install for CC_NONROOT_USER (so ccd-* reexec works)
  if is_root; then
    local nonroot_user
    nonroot_user="$(pick_nonroot_user_default)"
    if id "$nonroot_user" >/dev/null 2>&1; then
      local nr_home
      nr_home="$(eval echo "~$nonroot_user")"
      if [ -n "$nr_home" ] && [ "$nr_home" != "~$nonroot_user" ]; then
        # Write files into that user's home as well (requires root permission)
        local saved_home="$HOME"
        HOME="$nr_home" write_secrets_and_modes_for_home "$nr_home"
        HOME="$saved_home"
        echo "[install] also installed into non-root home: $nr_home (user: $nonroot_user)"
      fi
    else
      echo "[install] note: non-root user not found, ccd-* reexec may fail: $nonroot_user" >&2
    fi
  fi

  if [ "$WRITE_PERMS" -eq 1 ]; then
    write_project_permissions_template
  fi

  echo "[install] done. Run: source ~/.bashrc"
  echo "[install] commands: cc-st / cc-glm / ccd-st / ccd-glm"
}

main
