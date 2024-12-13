import discord
from discord.ext import commands, tasks
from functions import get_config_data
from discord import ui
import random

class guess_modal(ui.Modal):
    def __init__(self, answer: str):
        self.answer = answer
        super().__init__(title="Make your guess here!", timeout=30, custom_id="Guess_modal")
    guess = ui.TextInput(label="What is your guess?", style=discord.TextStyle.short, custom_id="Guess_modal_guess_input", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        if self.guess.value.lower() == self.answer.lower() and interaction.message.components[0]:
            await interaction.message.edit(content=f"{interaction.user.mention} Got it right!\nIt was `{self.answer}`", view=None)
            await interaction.response.send_message(content="Nice, you got it!", ephemeral=True)
        else:
            await interaction.response.send_message(content="")

class guess_button(ui.View):
    def __init__(self, answer: str):
        self.answer = answer
        super().__init__(timeout=180)
    
    @ui.Button(label="Click to guess!", style=discord.ButtonStyle.blurple, custom_id="guess_button")
    async def on_guess_button_click(self, interaction: discord.Interaction):
        await interaction.response.send_modal(guess_modal(answer=self.answer))

class winter_bot(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    async def send_error_to_owner(self, msg: str):
        owner = self.client.get_user(self.client.owner_id)
        await owner.send(content=msg)

    @tasks.loop(seconds=get_config_data()["Seconds"], minutes=get_config_data()["Minutes"], hours=get_config_data()["Hours"])
    async def send_guess_message(self):
        config = await get_config_data()
        channel = self.client.get_channel(config["Channel_ID"])
        if channel:
            items = config["Items"]
            item = random.choices(items)
            try:
                await channel.send(content=f"A new item has spawned! Click the button below to guess it!", view=guess_button(answer=item))
            except discord.HTTPException as e:
                await self.send_error_to_owner(msg=f"Couldn't send a message in <#{config["Channel_ID"]}>\n`{e.code}`, `{e.status}`, `{e.text}`, `{e.response}`")
                raise e
        else:
            await self.send_error_to_owner("You have inputted an invalid Channel_ID in `config.json`!\nPlease change it and restart the app.")
            raise ValueError("Invalid Channel_ID in config.json\nPlease update it immediately to a valid one and restart the app!")

async def setup(client: commands.Bot):
    await client.add_cog(winter_bot(client))