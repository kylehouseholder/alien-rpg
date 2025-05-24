import os, sys, asyncio, warnings
import discord
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_LOG_CHANNEL_ID", "0"))

async def send_message(prefix: str, startup_time: int = None):
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        try:
            channel = client.get_channel(CHANNEL_ID)
            if not channel:
                print("[WARN] Log channel not found.")
                await client.close()
                return

            now = datetime.now(timezone.utc)
            ts = now.strftime("%Y-%m-%d %H:%M:%S UTC")

            # Build one-line message
            parts = [
                prefix,                    # e.g. "🛑 **Murray has shut down.**"
                "📟 Status: Offline"
            ]

            # Uptime
            if startup_time:
                delta = int(now.timestamp()) - int(startup_time)
                hrs, rem = divmod(delta, 3600)
                mins, secs = divmod(rem, 60)
                parts.append(f"⏱ Uptime: {hrs:02}:{mins:02}:{secs:02}")
            else:
                parts.append("⏱ Uptime: Unavailable")

            parts.append(f"📅 {ts}")

            final_msg = "  ".join(parts)
            await channel.send(final_msg)

        except Exception as e:
            print("[ERROR] Failed to send log message:", e)
        finally:
            await client.close()

    await client.start(TOKEN)

if __name__ == "__main__":
    prefix = sys.argv[1] if len(sys.argv) > 1 else "🛠 Bot log message."
    try:
        startup = int(sys.argv[2]) if len(sys.argv) > 2 else None
    except ValueError:
        startup = None

    # suppress aiohttp warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        asyncio.run(send_message(prefix, startup))
