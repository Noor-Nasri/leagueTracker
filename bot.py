from pyrebase import pyrebase
from keys import firebase_config, discord_token
import discord
from discord import app_commands
from discord.ext import commands, tasks
import os
from DAO import DAO_Object

class TrackerBot(commands.Bot):
    def __init__(self):
        super().__init__(
                command_prefix = "!",
                intents = discord.Intents.all())
    async def setup_hook(self):
        print("setup")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        try:
            print("syncing commands")
            synced = await self.tree.sync()
            print(f"Synced {synced} commands")
        except Exception as e:
            print(e)
    async def on_ready(self):
        print(f'{bot.user.name} has connected to Discord!')

bot = TrackerBot()
    
bot.run(discord_token)
