#!/bin/bash

SESSION="alien-bot"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSION_PATH="$SCRIPT_DIR/sessionBot.sh"
LOG_PATH="$SCRIPT_DIR/bot.log"

log() {
    local level="$1"
    shift
    local msg="$*"
    local ts
    ts=$(date '+%Y-%m-%d %H:%M:%S')
    printf "[%s] [%-8s] %s\n" "$ts" "$level" "$msg"
}

case "$1" in
    start)
        if tmux has-session -t "$SESSION" 2>/dev/null; then
            log INFO "$SESSION already running. Restarting..."
            tmux kill-session -t "$SESSION"
            sleep 0.25
        fi
        log INFO "Starting $SESSION from $SCRIPT_DIR..."
        bash "$SESSION_PATH" &
        ;;
    stop)
        if tmux has-session -t "$SESSION" 2>/dev/null; then
            log INFO "Stopping $SESSION..."
            tmux kill-session -t "$SESSION"
        else
            log INFO "$SESSION not running."
        fi
        ;;
    log)
        if [ -f "$LOG_PATH" ]; then
            tail -100 "$LOG_PATH"
        else
            log INFO "No log file found."
        fi
        ;;
    *)
        log ERROR "Usage: $0 {start|stop|log}"
        ;;
esac
