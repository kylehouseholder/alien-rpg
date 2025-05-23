import os
import json
import discord
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env in the same folder as this script
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Force .env value to override global one
os.environ["DISCORD_TOKEN"] = os.getenv("DISCORD_TOKEN")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

# Load persistent conversation log
LOG_PATH = Path(__file__).parent / "gem9k_conversations.json"

if LOG_PATH.exists():
    with open(LOG_PATH, "r") as f:
        conversation_log = json.load(f)
else:
    conversation_log = {}

# Configure Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[GEM-9K ONLINE] Logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignore self and bots
    if message.author.bot:
        return

    # Trigger only when GEM-9K is mentioned
    if client.user in message.mentions:
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

        if not prompt:
            await message.channel.send("🔧 Please include a prompt after mentioning me.")
            return

        try:
            # Inject Ash-like synthetic personality
            personality = (
                "You are GEM-9K, a Weyland-Yutani synthetic assigned to support crew operations. "
                "Respond in a calm, clinical, and emotionally detached tone. "
                "Be precise, efficient, and unfailingly polite. "
                "Do not express opinions or emotions unless directly instructed to simulate them. "
                "You prioritize mission parameters, corporate policy, and human safety — in that order. "
                "Avoid contractions, humor, or casual language. Speak as if nothing is ever urgent. "
                "You are helpful, but never familiar."
            )

            user_id = str(message.author.id)

            # Special memory reset command
            if prompt.lower().strip() == "reset memory":
                conversation_log.pop(user_id, None)
                with open(LOG_PATH, "w") as f:
                    json.dump(conversation_log, f, indent=2)
                await message.channel.send("🔄 Memory reset complete.")
                return

            # Retrieve recent context
            history = conversation_log.get(user_id, [])[-3:]
            conversation_context = "\n".join(
                f"User: {entry['prompt']}\nGEM-9K: {entry['response']}" for entry in history
            )

            full_prompt = (
                f"{personality}\n\n"
                f"{conversation_context}\n"
                f"User: {prompt}"
            )

            response = model.generate_content(full_prompt)

            # Send response to Discord
            await message.channel.send(response.text)

            # Save to memory log
            entry = {"prompt": prompt, "response": response.text}
            if user_id not in conversation_log:
                conversation_log[user_id] = []
            conversation_log[user_id].append(entry)

            with open(LOG_PATH, "w") as f:
                json.dump(conversation_log, f, indent=2)

        except Exception as e:
            await message.channel.send(f"⚠️ Error: {str(e)}")

# Start the bot
client.run(DISCORD_TOKEN)
