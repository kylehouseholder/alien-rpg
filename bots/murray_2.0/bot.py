import os

# Ensure no globally exported DISCORD_TOKEN interferes
os.environ.pop("DISCORD_TOKEN", None)

import discord
import openai
from dotenv import load_dotenv
import time
import sys
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from dotenv import dotenv_values

from scripts.runtime_error_logger import report_exception_to_discord
# Record startup timestamp
startup_time = time.time()

# Explicitly load .env from local directory and override system vars
env_path = Path(__file__).resolve().parent / ".env"
env_vars = dotenv_values(env_path)
os.environ["DISCORD_TOKEN"] = env_vars.get("DISCORD_TOKEN", "")
os.environ["OPENAI_API_KEY"] = env_vars.get("OPENAI_API_KEY", "")

openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_LOG_CHANNEL_ID = env_vars.get("DISCORD_LOG_CHANNEL_ID")

print(f"[DEBUG] Loaded Discord Token: {os.getenv('DISCORD_TOKEN')[:10]}...")
print(f"[DEBUG] Final token used: {os.environ.get('DISCORD_TOKEN')[:10]}")

intents = discord.Intents.default()
intents.message_content = True  # Must be enabled in Discord Developer Portal too

client = discord.Client(intents=intents)

with open("prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

@client.event
async def on_ready():
    # Console log
    print(f"[Murray Online] Logged in as {client.user}")

    # One-line startup message to Discord log channel
    log_channel_id = os.getenv("DISCORD_LOG_CHANNEL_ID")
    if log_channel_id:
        try:
            channel = client.get_channel(int(log_channel_id))
            if not channel:
                print("[WARN] Could not find log channel.")
                return
            now = datetime.now(timezone.utc)
            ts = now.strftime("%Y-%m-%d %H:%M:%S UTC")
            parts = [
                "🧪 **Murray is now online.**",
                f"📅 {ts}",
                "📡 Status: Operational"
            ]
            await channel.send("  ".join(parts))
        except Exception as e:
            print(f"[ERROR] Failed to send startup message: {e}")

@client.event
async def on_message(message):
    if message.author == client.user or not message.content.startswith("!murray"):
        return

    user_input = message.content[len("!murray"):].strip()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        await message.channel.send(response["choices"][0]["message"]["content"])
    except Exception as e:
        await message.channel.send(f"Error: {e}")
        await report_exception_to_discord(e, context="!murray command failure", startup_time=startup_time)

# Run bot with shutdown and error handlers
try:
    client.run(DISCORD_TOKEN)
except KeyboardInterrupt:
    # Graceful shutdown
    print("[Shutdown] Murray received KeyboardInterrupt")
    asyncio.run(
        report_exception_to_discord(
            "Shutdown requested by user",
            context="Graceful Shutdown",
            startup_time=startup_time
        )
    )
except Exception:
    # Fatal startup error
    asyncio.run(
        report_exception_to_discord(
            sys.exc_info(),
            context="Startup failure",
            startup_time=startup_time
        )
    )
    raise  # propagate traceback
