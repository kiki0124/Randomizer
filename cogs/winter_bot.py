import discord
from discord.ext import commands, tasks
from functions import get_config_data, add_user_item, get_user_item_count, decrease_user_item_count
from discord import ui, app_commands
import random

class guess_modal(ui.Modal):
    def __init__(self, answer: str):
        self.answer = answer
        super().__init__(title="Make your guess here!", timeout=30, custom_id="Guess_modal")
    guess = ui.TextInput(label="What is your guess?", style=discord.TextStyle.short, custom_id="Guess_modal_guess_input", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        if self.guess.value.lower() == self.answer.lower() and interaction.message.components[0]:
            await add_user_item(user_id=interaction.user.id, item=self.answer)
            await interaction.message.edit(content=f"{interaction.user.mention} Got it right!\nIt was `{self.answer}`", view=None)
            await interaction.response.send_message(content="Nice, you got it!", ephemeral=True)
        else:
            await interaction.response.send_message(content=f"You got it wrong... Try again!", ephemeral=True)

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

    @commands.hybrid_command(name="get-user-item-count", with_app_command=True, description="Get the amount of an item that a specific user has")
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(user="What user?", item="What item?")
    async def get_user_item_count(self, interaction: discord.Interaction, item: str, user: discord.User = None):
        await interaction.response.defer(ephemeral=True)
        if item in await get_config_data["Items"]:
            if user == None: user = interaction.user
            count = await get_user_item_count(user_id=user.id, item=item)
            await interaction.followup.send(content=f"{user.mention} has `{count}` of `{item}`!")
        else:
            await interaction.followup.send(content=f"`{item}` is not a valid item...\nPlease try again later", ephemeral=True)

    @commands.hybrid_command(name="remove-user-item", with_app_command=True, description="Remove x amount of specified item from specified user")
    @app_commands.guild_only()
    @commands.guild_only()
    @app_commands.describe(user="What user?", item="What item?", amount="How many of the item? Defaults to 1")
    async def remove_user_item(self, ctx: commands.Context, user: discord.Member, item: str, amount: int = 1):
        await ctx.defer(ephemeral=True)
        if ctx.channel.permissions_for(ctx.author).administrator or ctx.channel.permissions_for(ctx.author).manage_guild:
            if item in await get_config_data["Items"]:
                if amount >= get_user_item_count(user.id, item):
                    await decrease_user_item_count(user.id, item, amount)
                else:
                    await ctx.reply(content=f"{user.name} doesn't have `{amount}` of {item} and they cannot have a negative of any item...", ephemeral=True)
            else:
                await ctx.reply(content=f"`{item}` is not a valid item...", ephemeral=True)
        else:
            raise commands.MissingPermissions(missing_permissions=["Administrator", "Manage Guild"])

async def setup(client: commands.Bot):
    await client.add_cog(winter_bot(client))