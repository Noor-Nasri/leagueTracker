from pyrebase import pyrebase
from keys import firebase_config
from data import champion_pool
from typing import List, Dict
from random import shuffle

class DAO_Object():
    def __init__(self):
        firebase = pyrebase.initialize_app(firebase_config)
        self.db = firebase.database()
        self.current_matchup = None

    def sign_up(self, author, nickname: str) -> bool:
        # Creates a new folder for the player and links it to the discord tag
        # returns false if it already exists

        all_player_ids = self.db.child("users").shallow().get().val()
        if str(author.id) in all_player_ids:
            return False

        data = {"name": nickname, "wins": 0, "losses": 0}
        self.db.child("users").child(author.id).set(data)
        return True


    def ban_champ(self, name: str) -> bool:
        # Returns true on success, false on champ not found

        name = name.title()
        if not name in champion_pool:
            return False
        
        banlist = self.db.child("banlist").get().val()
        if not name in banlist:
            banlist.append(name)
            self.db.child("banlist").set(banlist)

        print(banlist)
        return True


    def unban_champ(self, name: str) -> bool:
        # Returns true on success, false on champ not found

        name = name.title()
        banlist = self.db.child("banlist").get().val()
        if not name in banlist:
            return False

        banlist.remove(name)
        self.db.child("banlist").set(banlist)
        print(banlist)
        return True


    def get_banlist(self) -> List[str]:
        # Returns a list of champion names

        return self.db.child("banlist").get().val()[1:]


    def generate_matchup(self, author) -> List[Dict[str, str]]:
        # Generates a valid matchup and returns it in [{"ziadom" : "Yorick"}, 
        # {team 2}, {"ziadom" : "_id_"}]
        # If -1 is returned, display "You are not connected to a voice channel"
        # If -2 is returned, display "Uneven number of players in voice channel"
        # If -3 is returned, display "No league players found in vc"

        if not (author.voice and author.voice.channel):
            return -1

        channel = author.voice.channel
        member_ids = channel.voice_states.keys()
        all_player_ids = self.db.child("users").shallow().get().val()
        player_ids = []
        for member_id in member_ids:
            if str(member_id) in all_player_ids:
                player_ids.append(member_id)
        
        if not player_ids: return -3
        if len(player_ids) % 2 != 0: return -2

        teams = [{}, {}]
        banlist = self.get_banlist()
        champs = champion_pool[:]
        shuffle(champs)
        shuffle(player_ids)

        for i in range(len(player_ids)):
            username = self.db.child("users").child(player_ids[i]).get().val().get("name")
            while champs[i] in banlist:
                champs.pop(i)

            teams[i % 2][username] = champs[i] 
            banlist.append(champs[i])

        print(teams)
        self.current_matchup = teams
        return teams

    def accept_matchup(self) -> int:
        # Saves the matchup and remembers the integer 

        num_matches = len(self.db.child("matches").shallow().get().val())
        data = {"Team 0": [self.current_matchup[2][e] for e in self.current_matchup[0].keys()], 
                "Team 1": [self.current_matchup[2][e] for e in self.current_matchup[1].keys()], 
                "Winner": -1}
        
        self.db.child("matches").child(num_matches).set(data)
        self.current_match_id = num_matches

        return num_matches

    def conclude_match(self, winner_index: int) -> bool:
        # Saves winner of the match, returns false if id or index is invalid

        matches = self.db.child("matches").shallow().get().val()
        if not str(self.current_match_id) in matches or winner_index != 0 and winner_index != 1:
            return False
        
        self.db.child("matches").child(self.current_match_id).update({"Winner": winner_index})
        return True

dao = DAO_Object()
