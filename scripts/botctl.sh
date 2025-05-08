#!/bin/bash

SESSION="alien-bot"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSION_PATH="$SCRIPT_DIR/sessionBot.sh"
LOG_PATH="$SCRIPT_DIR/bot.log"
LINES=10

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
        log INFO "Starting $SESSION..."
        bash "$SESSION_PATH" &
        sleep 0.2  # Give the bot a moment to start writing logs
        timeout 15s tail -n 0 -F "$LOG_PATH" | while read -r line; do
            echo "$line"
            if [[ "$line" =~ Synced\ [0-9]+\ commands ]]; then
                break
            fi
        done
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
            tail -100 "$LOG_PATH" | awk 'NF' | awk '
                /Synced [0-9]+ commands/ {lastsync=NR}
                {lines[NR]=$0}
                END {
                    if (lastsync) {
                        for (i=1; i<=lastsync; i++) print lines[i]
                    } else {
                        for (i=1; i<=NR; i++) print lines[i]
                    }
                }'
        else
            log INFO "No log file found."
        fi
        ;;
    *)
        log INFO "Usage: $0 {start|stop|log}"
        ;;
esac 