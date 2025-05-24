#!/bin/bash

SESSION="murray-bot"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSION_PATH="$SCRIPT_DIR/sessionBot.sh"
LOG_PATH="$SCRIPT_DIR/bot.log"

log() {
    local level="$1"; shift
    local ts=$(date '+%Y-%m-%d %H:%M:%S')
    printf "[%s] [%-8s] %s\n" "$ts" "$level" "$*"
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
    ;;

  stop)
    if tmux has-session -t "$SESSION" 2>/dev/null; then
      log INFO "Stopping $SESSION..."

      # read (and delete) the file we wrote at launch
      if [ -f "$SCRIPT_DIR/startup_time.txt" ]; then
        STARTUP_TIME=$(<"$SCRIPT_DIR/startup_time.txt")
        rm "$SCRIPT_DIR/startup_time.txt"
      else
        STARTUP_TIME=""
      fi

      tmux kill-session -t "$SESSION"

      # define the shutdown prefix
      MESSAGE="🛑 **Murray has shut down.**"

      # fire off the logger in a fully detached subshell,
      # dropping both stdout and stderr so you never see
      # aiohttp "connector" warnings in your terminal
      (
        python3 "$SCRIPT_DIR/send_log_message.py" "$MESSAGE" "$STARTUP_TIME"
      ) > /dev/null 2>&1 & disown

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
