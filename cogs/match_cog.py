
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

class MatchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name = "signup",
            description = "sign up a league player")
    async def signup(self,interaction:discord.Interaction,
                    ign:str) -> None:
        await interaction.response.send_message(f"User {interaction.user.name} has been linked with {ign}")

    @app_commands.command(
            name = "ban_champ",
            description = "bans a champ from being picked"
            )
    # @app_commands.choices(champ = [
    async def ban_champ(self,interaction:discord.Interaction,
                        champ:str):
        await interaction.response.send_message("ppooy")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(MatchCog(bot))
