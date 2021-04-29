import discord
from discord.ext import commands
class Lobby():
    def __init__(self, lobbyName):
        self.lobbyName = lobbyName
        self.lobbyNumber = "".join(filter(str.isdigit, lobbyName))
        self.lobbyid = 0 #The channel Lobby ID
        self.players =[] # A list of players in this lobby
        self.team_one = [] #Players on team 1 'Blue'
        self.team_two = [] #Players on team 2 'Orange
        self.game_cred = {} #The credentials used to create the game
        self.game_mode = "random"
    def addPlayer(self, player :discord.Member):
        #Do a check if player already in THIS lobby
        if player in self.players:
            print("Player already in lobby.")
        else:
            self.players.append(player)
    def removePlayer(self, player :discord.Member):
        self.players.remove(player)
    def setCredentials(self, user, password):
        self.game_cred = {user, password}
    def setLobbyID(self, lobbyID):
        self.id = lobbyID
    def display(self):
        return "Lobby Name: {0}\nLobby ID: {1}\nPlayers: {2} ".format(self.lobbyNumber, self.lobbyid, self.players)
    async def moveOnePlayersToChannel(self, member: discord.Member ):
        await member.move_to(self.lobbyid)
    async def moveAllPlayersToChannel(self):
        for player in self.players:
            await player.move_to(self.lobbyid)
    def author_on_list(self, author):
        """
            Checks if the author is on the player list
        """
        for player in self.players:
            if player == author:
                return True
        return False
    def reportResults(self, blue_score, orange_score):
        """
            Reports the results of a lobby match
        """
        if blue_score > orange_score:
            for player in self.team_one:
                pass
                #insert +1 win or new player record
            for player in self.team_two:
                pass
                #insert -1 for loss or new player record
        else:
            for player in self.team_two:
                pass
                #insert +1 win or new player record
            for player in self.team_one:
                pass
                #insert -1 for loss or new player record
    