
import discord
from discord import app_commands
from discord.ext import commands

class MatchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name = "introduce",
            description = "Intro")
    async def introduce(self,interaction:discord.Interaction,
                    name:str,
                    age:int) -> None:
        await interaction.response.send_message("poo")

async def setup(bot: commands.Bot):
    await bot.add_cog(MatchCog(bot))
