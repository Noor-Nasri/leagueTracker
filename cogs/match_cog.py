
import discord
from discord import app_commands,ui
from discord.app_commands import Choice
from discord.ext import commands
from data import champion_pool
from DAO import dao

class CreateMatchMenu(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label = "Accept")
    async def accept(self, interaction: discord.Interaction, Button: ui.Button):
        # dao.accept_matchup()
        await interaction.response.edit_message(view = SelectWinnerMenu())
    @ui.button(label = "Reroll")
    async def reroll(self, interaction: discord.Interaction, Button: ui.Button):
        await interaction.response.edit_message(content = dao.generate_matchup(interaction.user))
class SelectWinnerMenu(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label = "Team1")
    async def team1(self, interaction: discord.Interaction, Button: ui.Button):
        pass
    @ui.button(label = "Team2")
    async def team2(self, interaction:discord.Interaction, Button: ui.Button):
        pass

class MatchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name = "signup",
            description = "sign up a league player")
    async def signup(self,interaction:discord.Interaction,
                    ign:str) -> None:
        if dao.sign_up(interaction.user,ign):
            await interaction.response.send_message(f"User {interaction.user.name} has been linked with {ign}")
        else:
            await interaction.response.send_message(f"There was an error")

    @app_commands.command(
            name = "banchamp",
            description = "bans a champ from champ select"
            )
    async def ban_champ(self,interaction:discord.Interaction,
                        champ:str):
        if dao.ban_champ(champ): 
            await interaction.response.send_message(f"{champ} has been banned")
        else:
            await interaction.response.send_message(f"There was an error")

    @app_commands.command(
            name = "unbanchamp",
            description = "unbans a champ from champ select"
            )
    async def unban_champ(self,interaction:discord.Interaction,
                          champ:str):
        if dao.unban_champ(champ):
            await interaction.response.send_message(f"{champ} has been unbanned")
        else:
            await interaction.response.send_message(f"There was an error")

    @app_commands.command(
            name = "banlist",
            description = "gets banlist"
            )
    async def banlist(self,interaction:discord.Interaction):
        await interaction.response.send_message(str(dao.get_banlist()))


    @app_commands.command(
            name = "creatematch",
            description = "creates match"
            )
    async def creatematch(self,interaction:discord.Interaction):
        print("hello")
        await interaction.response.send_message(dao.generate_matchup(interaction.user),
                                                view = CreateMatchMenu())



    
             
        
async def setup(bot: commands.Bot):
    await bot.add_cog(MatchCog(bot))
