import discord
from discord.ext import commands
import os
from functions import get_config_data

config = get_config_data()

client = commands.Bot(command_prefix=config["Prefixes"], help_command=None, intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"Bot is ready.\nLogged in as {client.user.name} | {client.user.id}")

@client.event
async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(f"cogs.{filename[:-3]}")
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded extension: {filename}")
        else:
            print(f"Skipped loading extension: {filename}")
client.run(token=config["Token"])