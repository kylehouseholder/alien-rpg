#!/bin/bash

SESSION="murray-bot"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_PATH="$SCRIPT_DIR/../.env"
VENV_PATH="../../venv/bin/activate"
BOT_CMD="python3 bot.py"
LOG_PATH="$SCRIPT_DIR/bot.log"

# Export environment variables
set -a
source <(grep -v '^#' "$ENV_PATH" | sed -E 's/ *= */=/' | sed -E 's/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/\1=\2/' | sed -E 's/^([^=]+)="(.*)"$/\1=\2/')
set +a

# Record startup time silently (no “no server running…” warning)
tmux set-environment startup_time "$(date +%s)" 2>/dev/null
STARTUP_TIME=$(date +%s)
echo "$STARTUP_TIME" > "$SCRIPT_DIR/startup_time.txt"

# Launch tmux session running the bot
tmux new-session -d -s "$SESSION" \
  "bash -c 'cd $SCRIPT_DIR/.. && source $VENV_PATH && exec $BOT_CMD 2>&1 | tee -a $LOG_PATH'"
  