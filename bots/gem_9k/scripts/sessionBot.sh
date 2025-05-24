#!/bin/bash

SESSION="gem9k-bot"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_PATH="$SCRIPT_DIR/../.env"
VENV_PATH="../../venv/bin/activate"
BOT_CMD="python3 main.py"
LOG_PATH="$SCRIPT_DIR/bot.log"

set -a
source <(grep -v '^#' "$ENV_PATH" | sed -E 's/ *= */=/' | sed -E 's/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/\1=\2/' | sed -E 's/^([^=]+)="(.*)"$/\1=\2/')
set +a

tmux new-session -d -s "$SESSION" \
  "cd $SCRIPT_DIR/.. && source $VENV_PATH && exec $BOT_CMD 2>&1 | tee -a $LOG_PATH"
