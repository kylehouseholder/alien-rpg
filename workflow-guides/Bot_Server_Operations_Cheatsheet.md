
# 📦 BOT SERVER OPERATIONS CHEATSHEET

This document describes how to operate, maintain, and manage the Discord bot on the remote server.

## 🚀 DAILY OPERATION (WORKING WITH THE BOT)

### Connect and check on the bot

```
ssh botserver
tmux attach -t bot
```

You are now watching the live bot logs.

### Detach and leave bot running

```
Ctrl + B
D
```

This detaches tmux and leaves the bot running in the background.

### Stop the bot

Inside tmux (while watching the bot):

```
Ctrl + C
```

This stops the bot.

### Exit tmux session (optional)

After stopping the bot:

```
exit
```

This closes the tmux session.

### Start bot manually (if needed)

```
cd ~/alien_rpg_bot
./start_bot.sh
```

This starts tmux and runs the bot in the `bot` session.

## 🖥️ SERVER REBOOT (AUTOMATIC OPERATION)

If the server reboots, crontab automatically runs:

```
@reboot /home/ztrob/alien_rpg_bot/start_bot.sh
```

The bot will launch automatically in tmux.

Check after reboot:

```
ssh botserver
tmux attach -t bot
```

## 📦 DEVELOPMENT / GIT

Project uses git for version control.

To commit changes:

```
git status
git add filename
git commit -m "Description of change"
git push
```

## ✅ VIRTUALENV REFERENCE

Bot always runs inside virtualenv. Script handles this automatically.  
To manually run:

```
source venv/bin/activate
python main.py
```

## ✅ FINAL NOTES

| Where you work | tmux needed? |
|----------------|--------------|
| Cursor (Remote SSH Terminal) | Yes (Cursor may auto-use tmux, manual tmux recommended for long runs) |
| SSH (Windows Terminal or CLI) | Yes (Always manual tmux required) |

Always use tmux when running bot. It prevents duplicate instances and keeps bot running safely.

## ✅ COMPLETION

This setup is production-grade:

✅ SSH + remote dev
✅ Virtualenv isolation
✅ tmux management and detachment
✅ Crontab auto-start
✅ Git versioning

This server and bot are now safe, automatic, and ready for long-term operation.
