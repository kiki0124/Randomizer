import discord
from discord.ext import commands
from discord import app_commands

class bot(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        try:
            synced = await self.client.tree.sync()
        except discord.HTTPException as e:
            return await ctx.reply(f"There was an error while syncing commands...\n`{e.code}`, `{e.response}`, `{e.status}`, {e.text}`.")
        await ctx.reply(content=f"Successfully synced {len(synced)} slash command(s)")

    @commands.Cog.listener('on_command_error')
    async def handle_prefix_errors(self, ctx: commands.Context, error: commands.CommandError):
        match error:
            case commands.MissingPermissions:
                return
            case commands.BadArgument:
                await ctx.reply(content=f"You have parsed a bad argument... Please try again later.", mention_author=False)
            case _:
                raise error

async def setup(client):
    await client.add_cog(bot(client))