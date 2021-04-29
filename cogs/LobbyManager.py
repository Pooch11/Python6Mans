from cogs.Lobby import Lobby
import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(LobbyManager(bot))

class LobbyManager(commands.Cog, name="LobbyManager"):
    def __init__(self, bot = "LobbyManager"):
            self.lobby_list = [] 
            self.bot = bot
    def find_in_list(self, find_number :int):
        """
            Finds the lobby based on the number passed in
            Returns the lobby object if found, None if not found
        """
        for lobby in self.lobby_list:
            if lobby.lobbyNumber == find_number:
                return lobby
        return None
    def add_lobby(self, lobby : Lobby):
        """
            Add lobby to the queue.
        """
        self.lobby_list.append(lobby)
    def lobby_size(self):
        """
            Report the lobby length
        """
        return (len(self.lobby_list))
    def remove_lobby(self, lobby_number):
        """
            Remove a lobby to the queue.
        """
        for lobby in self.lobby_list:
            if lobby.lobbyNumber == lobby_number:
                self.lobby_list.remove(lobby)
            else:
                print("Could not find lobby {0}".format(lobby_number))
    def configure_lobby(self, settings :dict):
        """
            Configure lobby for pick and team size options (Captians, Random, KOTH)
        """
        pass
    def report_match(self, number, blue, orange):
        """
            Process once a match has been flagged to report
        """
        print("Reporting Lobby {0} Blue:{1} - Orange:{2}".format(number, blue, orange))
        #use Lobby number to find this lobby
        for lobby in self.lobby_list:
            if lobby.lobbyNumber == number:
                try:
                    lobby.reportResults(blue, orange)
                except Exception as e:
                    print(e)
            else:
                print("Specified Lobby not found.")
        
    def player_in_queue(self):
        """
            Finds if the player is already part of a lobby
        """
        pass
    def message_to_players(self, lobby_number, message):
        """
            Sends a direct message to players in a lobby
        """
        for lobby in self.lobby_list:
            if lobby.lobbyNumber == lobby_number:
                for player in lobby.players:
                    print("Send {0} to {1}".format(message, player)) 

_LobbyManager = LobbyManager()
        