import os
import discord
import asyncio
import traceback
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path
import time

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_LOG_CHANNEL_ID", "0"))

def format_uptime(seconds: float) -> str:
    mins, sec = divmod(int(seconds), 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs}h {mins}m {sec}s"

async def report_exception_to_discord(exc_info, context="Runtime Exception", startup_time=None):
    if not DISCORD_TOKEN or not CHANNEL_ID:
        print("Discord logging not configured properly.")
        return

    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        try:
            channel = client.get_channel(CHANNEL_ID)
            if not channel:
                print("Log channel not found.")
                await client.close()
                return

            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

            # Calculate uptime if available
            uptime_msg = ""
            if startup_time:
                uptime_seconds = round(time.time() - startup_time)
                hours, remainder = divmod(uptime_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime_msg = f"\n⏱ Uptime: {hours:02}:{minutes:02}:{seconds:02}"

            if isinstance(exc_info, str):
                # Custom string message (e.g., shutdown signal)
                message = f"🛑 **{exc_info}**{uptime_msg}\n📟 Status: Offline\n📅 {timestamp}"
            else:
                # Full traceback
                tb = ''.join(traceback.format_exception(*exc_info))
                message = f"❗ **{context}**{uptime_msg}\n```{tb[-1800:]}```\n📅 {timestamp}"

            await channel.send(message)

        except Exception as e:
            print("Failed to report to Discord:", e)
        finally:
            await client.close()

    await client.start(DISCORD_TOKEN)
    if not DISCORD_TOKEN or not CHANNEL_ID:
        print("Discord logging not configured properly.")
        return

    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        try:
            channel = client.get_channel(CHANNEL_ID)
            if channel:
                tb = ''.join(traceback.format_exception(*exc_info)) if isinstance(exc_info, tuple) else str(exc_info)
                timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

                msg = f"❗ **{context} in Murray**"

                if isinstance(exc_info, tuple):
                    msg += f"\n```{tb[-1800:]}```"
                else:
                    msg += f"\n💬 {tb}"

                if startup_time:
                    uptime = format_uptime(time.time() - startup_time)
                    msg += f"\n🕒 Uptime before event: `{uptime}`"

                msg += f"\n📅 {timestamp}"
                await channel.send(msg)
        except Exception as e:
            print("Failed to report to Discord:", e)
        finally:
            await client.close()

    await client.start(DISCORD_TOKEN)