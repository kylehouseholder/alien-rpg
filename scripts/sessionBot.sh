#!/bin/bash

SESSION="alien-bot"
VENV_PATH="venv/bin/activate"
BOT_CMD="python -u main.py"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_PATH="$SCRIPT_DIR/bot.log"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION already exists."
	sleep 0.25
    echo "Use: tmux attach -t $SESSION"
    echo "Or:  tmux a (if no other sessions exist)"
    exit 0
fi

tmux new-session -d -s "$SESSION" \
    "source $VENV_PATH && exec $BOT_CMD 2>&1 | tee -a $LOG_PATH"