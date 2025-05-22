import os
import discord
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env in the same folder as this script
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Debug print to confirm correct token is being used
print("DISCORD_TOKEN =", DISCORD_TOKEN)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Configure Discord bot client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[GEM-9K ONLINE] Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!gem9k "):
        prompt = message.content[len("!gem9k "):]
        try:
            response = model.generate_content(prompt)
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"Error: {str(e)}")

client.run(DISCORD_TOKEN)
