import discord
from discord.ext import commands, tasks
import json
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1461040942420066566

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "counter.json"

def load_days():
    if not os.path.exists(DATA_FILE):
        return 0
    with open(DATA_FILE, "r") as f:
        return json.load(f)["days"]

def save_days(days):
    with open(DATA_FILE, "w") as f:
        json.dump({"days": days}, f)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    daily_counter.start()

@tasks.loop(hours=24)
async def daily_counter():
    days = load_days() + 1
    save_days(days)

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"{days} dias desde el último hackeo al Erick.")

@bot.command()
@commands.has_permissions(administrator=True)
async def reset(ctx):
    save_days(0)
    await ctx.send("Contador reseteado.")

bot.run(TOKEN)
