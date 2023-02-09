from pyrebase import pyrebase
from keys import firebase_config, discord_token
import discord
from discord.ext import commands, tasks
from data import champion_pool
from typing import List

def add_player(nickname: str, discord_tag:str) -> bool:
    # Creates a new folder for the player and links it to the discord tag
    # True on success and False when nickname in use OR invalid tag

    pass

def ban_champ(name: str) -> bool:
    # Returns true on success, false on champ not found

    pass

def unban_champ(name: str) -> bool:
    # Returns true on success, false on champ not found

    pass

def get_banlist() -> List[str]:
    # Returns a list of champion names

    pass

async def generate_matchup(ctx): 
    # Still figuring out return

    if not (ctx.author.voice and ctx.author.voice.channel):
        await ctx.send("You are not connected to a voice channel")
        return 

    channel = ctx.author.voice.channel

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
