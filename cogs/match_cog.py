
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from data import champion_pool

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
            name = "banchamp",
            description = "bans a champ from champ select"
            )
    async def ban_champ(self,interaction:discord.Interaction,
                        champ:str):
        if champ.title() not in [c for c in champion_pool]:
            await interaction.response.send_message(f"The champion {champ} doesn't exist")
        else:
            await interaction.response.send_message(f"champion has been banned")

    @app_commands.command(
            name = "unbanchamp",
            description = "unbans a champ from champ select"
            )
    async def unban_champ(self,interaction:discord.Interaction,
                          champ:str):
        if champ.title() not in champion_pool:
            await interaction.response.send_message(f"The champion {champ.title()} doesn't exist")
        else:
            await interaction.response.send_message(f"champion has been unbanned")

    @app_commands.command(
            name = "banlist",
            description = "gets banlist"
            )
    async def banlist(self,interaction:discord.Interaction):
        await interaction.response.send_message("poo")

    @app_commands.command(
            name = "creatematch",
            description = "creates match"
            )
    async def creatematch(self,interaction:discord.Interaction):
        await interaction.response.send_message("poo")


    
             
        
async def setup(bot: commands.Bot):
    await bot.add_cog(MatchCog(bot))
