#!/bin/bash

SESSION="alien-bot"
SESSION_SCRIPT="sessionBot.sh"
SESSION_PATH="$(dirname "$0")/$SESSION_SCRIPT"
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
        while read -r line; do
            echo "$line"
            if [[ "$line" =~ Synced\ [0-9]+\ commands ]]; then
                break
            fi
        done < <(tail -F -n 0 bot.log)
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
        if [ -f bot.log ]; then
            tail -100 bot.log | awk 'NF' | awk '
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