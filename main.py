from pyrebase import pyrebase
from keys import firebase_config, discord_token
import discord
from discord.ext import commands, tasks
from data import champion_pool
from typing import List, Dict
from random import shuffle

def sign_up(author, nickname: str) -> bool:
    # Creates a new folder for the player and links it to the discord tag
    # returns false if it already exists

    all_player_ids = db.child("users").shallow().get().val()
    if str(author.id) in all_player_ids:
        return False

    data = {"name": nickname, "wins": 0, "losses": 0}
    db.child("users").child(author.id).set(data)
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


def generate_matchup(db, author) -> List[Dict[str, str]]:
    # Generates a valid matchup and returns it in [{"ziadom" : "Yorick"}, 
    # {team 2}, {"ziadom" : "_id_"}]
    # If -1 is returned, display "You are not connected to a voice channel"
    # If -2 is returned, display "Uneven number of players in voice channel"
    # If -3 is returned, display "No league players found in vc"

    if not (author.voice and author.voice.channel):
        return -1

    channel = author.voice.channel
    member_ids = channel.voice_states.keys()
    all_player_ids = db.child("users").shallow().get().val()
    player_ids = []
    for member_id in member_ids:
        if member_id in all_player_ids:
            player_ids.append(member_id)
    
    if not player_ids: return -3
    if len(player_ids) % 2 != 0: return -2

    teams = [{}, {}]
    banlist = get_banlist(db)
    champs = champion_pool[:]
    shuffle(champs)
    shuffle(player_ids)

    for i in range(len(player_ids)):
        username = db.child("users").child(player_ids[i]).get().val().get("name")
        while champs[i] in banlist:
            champs.pop(i)

        teams[i % 2][username] = champs[i] 
        banlist.append(champs[i])

    print(teams)
    return teams

def accept_matchup(teams: List[Dict[str, str]]) -> int:
    # Saves the matchup and remembers the integer 

    num_matches = len(db.child("matches").shallow().get().val())
    data = {"Team 0": [teams[2][e] for e in teams[0].keys()], 
            "Team 1": [teams[2][e] for e in teams[1].keys()], 
            "Winner": -1}
    
    db.child("matches").child(num_matches).set(data)
    return num_matches

def conclude_match(match_id: int, winner_index: int) -> bool:
    # Saves winner of the match, returns false if id or index is invalid

    matches = db.child("matches").shallow().get().val()
    if not str(match_id) in db.child("matches").shallow().get().val() or \
        winner_index != 0 and winner_index != 1:
        return False
    
    db.child("matches").child(match_id).update({"Winner": winner_index})
    return False
    

if __name__ == "__main__":
    # connect to firebase and initialize discord bot
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

    #print(db.child("users").child("1981").get().val().get("name"))
    #db.child("banlist").set(["Init"])
    #db.child("users").set({0 : {"name": "Default", "wins": 0, "losses": 0}})
    #db.child("matches").set([{"Team 0": ["Default"], "Team 1": ["Default"], "Winner": 1}])

    #db.child("users").child(0).update({"wins": 2})
    
    #print(accept_matchup([
    #    {"Ziadom": "Nunu"}, 
    #    {"Pop": "Yorick"}, 
    #    {"Ziadom": 1022, "Pop": 1829}]))
    
    #print(conclude_match(1, 0))
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