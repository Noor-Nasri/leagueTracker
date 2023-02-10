from pyrebase import pyrebase
from keys import firebase_config, discord_token
import discord
from discord.ext import commands, tasks
from data import champion_pool
from typing import List, Dict

def sign_up(ctx, nickname: str) -> bool:
    # Creates a new folder for the player and links it to the discord tag
    # returns false if it already exists

    all_player_ids = db.child("users").shallow().get()
    player_id = str(ctx.message.author.id)
    if player_id in all_player_ids.val():
        return False

    data = {"name": nickname, "wins": 0, "losses": 0}
    db.child("users").child(player_id).set(data)
    return True


def ban_champ(db, name: str) -> bool:
    # Returns true on success, false on champ not found

    name = name.upper()
    if not name in champion_pool:
        return False
    
    banlist = db.child("banlist").get().val()
    if not name in banlist:
        banlist.append(name)
        db.child("banlist").set(banlist)

    print(banlist)
    return True


def unban_champ(db, name: str) -> bool:
    # Returns true on success, false on champ not found

    name = name.upper()
    banlist = db.child("banlist").get().val()
    if not name in banlist:
        return False

    banlist.remove(name)
    db.child("banlist").set(banlist)
    print(banlist)
    return True


def get_banlist(db) -> List[str]:
    # Returns a list of champion names

    return db.child("banlist").get().val()[1:]


def generate_matchup(ctx) -> List[Dict[str, str]]:
    # Generates a valid matchup and returns it in [{"ziadom" : "Yorick"}, {team 2}]
    # If -1 is returned, display "ERROR: You are not connected to a voice channel"
    # If -2 is returned, display "Uneven number of players in voice channel"

    if not (ctx.author.voice and ctx.author.voice.channel):
        return []

    channel = ctx.author.voice.channel
    member_ids = channel.voice_states.keys()
    print(member_ids)
    return []

def accept_matchup(teams: List[Dict[str, str]]) -> int:
    # Saves the matchup and remembers the integer 
    pass

def conclude_match(match_id: int, winner_index: int) -> bool:
    # Saves winner of the match, returns false if id or index is invalid
    pass
    

if __name__ == "__main__":
    # connect to firebase and initialize discord bot
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

    print(unban_champ(db, "zoe"))
    #db.child("banlist").set(["Init"])

    """
    client = commands.Bot(command_prefix="!")

    @client.event
    async def on_ready():
        await client.change_presence(activity = discord.Game(name = '!help for a list of commands'))

        print("Running")

    @client.command()
    async def test(ctx):
        print("Got call")
        await generate_matchup(ctx)
    
    @client.command()
    async def test2(ctx):
        print("Got call2")
        await add_player(ctx, "ziadom")
        
    client.run(discord_token)

    """