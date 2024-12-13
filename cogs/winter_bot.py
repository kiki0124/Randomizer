import discord
from discord.ext import commands, tasks
from functions import get_config_data
from discord import ui

class guess_button(ui.DynamicItem[ui.Button], template="guess-.*"):
    def __init__(self, item, *, row = None):
        super().__init__(item, row=row)

class winter_bot(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @tasks.loop(seconds=get_config_data()["Seconds"], minutes=get_config_data()["Minutes"], hours=get_config_data()["Hours"])
    async def send_guess_message(self):
        pass

async def setup(client: commands.Bot):
    await client.add_cog(winter_bot(client))