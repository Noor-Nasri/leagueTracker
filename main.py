from pyrebase import pyrebase
from keys import firebase_config, discord_token
import discord
from discord.ext import commands, tasks

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(help = "[username] creates a new folder for this user")
    async def add_player(self, ctx, arg):
        await ctx.channel.send("WIP")

if __name__ == "__main__":
    # connect to firebase and initialize discord bot
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

    client = commands.Bot(command_prefix="/lol_tracker ")

    @client.event
    async def on_ready():
        await client.change_presence(activity = discord.Game(name = '/lol_tracker help for a list of commands'))

        print("Done")