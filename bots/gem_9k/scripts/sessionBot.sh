#!/bin/bash

SESSION="gem9k-bot"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PATH="$SCRIPT_DIR/../venv/bin/activate"
BOT_CMD="python3 -u $SCRIPT_DIR/../main.py"
LOG_PATH="$SCRIPT_DIR/bot.log"

unset DISCORD_TOKEN  # <--- Add this line

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already exists."
    sleep 0.25
    echo "Use: tmux attach -t $SESSION"
    echo "Or:  tmux a (if no other sessions exist)"
    exit 0
fi

tmux new-session -d -s "$SESSION" \
    "source $VENV_PATH && exec $BOT_CMD 2>&1 | tee -a $LOG_PATH" 