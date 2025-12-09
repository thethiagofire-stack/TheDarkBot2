import discord
import os
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
USER_ID_TO_TRACK = int(os.getenv("USER_ID_TO_TRACK"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_status = None
last_custom = None

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_presence_update(before, after):
    global last_status, last_custom
    if after.id != USER_ID_TO_TRACK:
        return

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    if after.status != last_status:
        last_status = after.status
        await channel.send(f"**{after.name}** → `{after.status}`")

    before_custom = before.activity.state if before.activity else None
    after_custom = after.activity.state if after.activity else None

    if after_custom != last_custom:
        last_custom = after_custom
        await channel.send(f"**{after.name}** custom status → `{after_custom}`")

bot.run(TOKEN)
