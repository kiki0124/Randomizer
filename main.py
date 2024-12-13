import discord
from discord.ext import commands
import os
import json

with open("config.json", 'r') as file:
    data = json.load(file)

client = commands.Bot(command_prefix=data["Prefixes"], help_command=None, intents=discord.Intents.all())

@client.event("on_ready")
async def on_ready():
    print(f"Bot is ready.\nLogged in as {client.user.name} | {client.user.id}")

@client.event("setup_hook")
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded extension: {filename}")
        else:
            print(f"Skipped loading extension: {filename}")

client.run(token=data["Token"])