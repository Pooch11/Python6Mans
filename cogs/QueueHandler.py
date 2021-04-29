import discord
from discord.ext import commands
import random
from datetime import datetime
from cogs.Lobby import *
from cogs.LobbyManager import _LobbyManager
from config import Config

config = Config()
MAX_QUEUE = int(config.lobby_size)
lobby_name = config.queue_channel



class QueueHandler(commands.Cog, name="Queue Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.blue_queue = []
        self.orange_queue = []
        self.lobby_queue = []
        self.team_one = []
        self.team_two = []

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction :discord.reaction, user :discord.user):
        channel = reaction.message.channel
        last_react_user = await reaction.users().flatten()
        if (reaction.message.author.name == 'RocketMan'): #Messages from the Bot
            if (str(reaction) == '🇶'): 
                print(reaction.message.embeds[0].title)
                if "queue" in (str(reaction.message.embeds[0].title)):
                    await channel.send("{0} You will be added to this queue.".format(user))                
                    await self.add_to_queue(last_react_user[-1])
            if (str(reaction) == '🧡'):
                if "Lobby" in (str(reaction.message.embeds[0].title)):
                    await channel.send("{0} Orange heart on message from {1}".format(last_react_user, reaction.message.author.name))
            if (str(reaction) == '💙'):
                if "Lobby" in (str(reaction.message.embeds[0].title)):
                    await channel.send("{0} Blue heart on message from {1}".format(last_react_user, reaction.message.author.name))

 

    
    @commands.command(name='q', aliases=['queue'], description='Allows a user to join the queue.')
    async def queue(self, ctx):
        if ctx.channel.name != lobby_name and ctx.channel.name != lobby_name:
            await ctx.send(f"No queueing in the {ctx.channel.name} channel.")
            return

        player = ctx.author

        if ctx.channel.name == lobby_name:
            if player in self.lobby_queue:
                #emb = ""
                await ctx.send('You are already in the 6mans queue!')
                return
            if len(self.lobby_queue) == MAX_QUEUE:
                return
            #Add player to the current queue 
            self.lobby_queue.append(player)
            curr_q_emb = (" ".join(player.mention for player in self.lobby_queue))
            if len(self.lobby_queue) < MAX_QUEUE:
                blue_embed = discord.Embed(title=f'{len(self.lobby_queue)} players are in the queue!')
                blue_embed.color = discord.Color.blue()
                blue_embed.description = f'{player.mention} has joined the queue.\n Current Queue: \n' + '{0}'.format(curr_q_emb)
                await ctx.send(embed=blue_embed)

            if len(self.lobby_queue) == MAX_QUEUE:
                user = random.randint(999, 9999)
                password = random.randint(999, 9999)
                credentials = f'**Here are your lobby details - {datetime.now()}**\n\t__Name__: {user}\n\t__Password__: {password}'
                bluepop_embed = discord.Embed(title=f'Queue has been popped! {MAX_QUEUE} players have queued up.')
                bluepop_embed.color = discord.Color.green()
                await ctx.send(embed=bluepop_embed)
                await ctx.send(" ".join(player.mention for player in self.lobby_queue))
                tempLobby = await self.create_lobby(ctx)
                for member in self.lobby_queue:
                    await member.send(credentials)
                    tempLobby.addPlayer(member)               
                await self.random_teams(ctx, self.lobby_queue, tempLobby) 
                _LobbyManager.add_lobby(tempLobby)
                self.lobby_queue = []
                new_queue = discord.Embed(title=f'Queue has been reset', color=discord.Color.blue())
                print("Queue has been Reset")
                await ctx.send(embed=new_queue)

    @commands.command(name="lobby", description="Creates a lobby if 6 players are ready to play.")
    async def manual_lobby(self, ctx):
        if ctx.channel.name != lobby_name:
            await ctx.send(f"Please go to correct channel to create/monitor a lobby")
            return
        tempLobby = await self.create_lobby(ctx)
        user = random.randint(999, 9999)
        password = random.randint(999, 9999)
        tempLobby.addPlayer(ctx.author)
        _LobbyManager.add_lobby(tempLobby)
        await ctx.send("A new lobby was created. (Total Lobbies: {0})".format(_LobbyManager.lobby_size()))
        credentials = f'**Here are your lobby details - {datetime.now()}**\n\t__Name__:{user}\n\t__Password__:{password}'
        await ctx.author.send(credentials)
        


    @commands.command(name="leave", description="Lets the user leave the queue.")
    async def leave_queue(self, ctx):
        if ctx.channel.name != lobby_name:
            await ctx.send(f"Please go to correct channels.")
            return
        player = ctx.author
        if ctx.channel.name == lobby_name:
            if player not in self.lobby_queue:
                await ctx.send("You are not currently in the queue.")
                return
            self.lobby_queue.remove(player)
            leave_embed = discord.Embed(title=f'{len(self.lobby_queue)} players are in the queue')
            leave_embed.description = f'{player.mention} has left.'
            leave_embed.color = discord.Color.dark_red()
            await ctx.send(embed=leave_embed)

    @commands.command(name="status", description="Displays current status of the queue.")
    async def queue_status(self, ctx):
        if ctx.channel.name != lobby_name:
            await ctx.send(f"Please go to correct channels.")
            return
        if ctx.channel.name == lobby_name:
            queue_embed = discord.Embed(title=f'{len(self.lobby_queue)} players are in the queue')
            queue_embed.description = (" ".join(player.mention for player in self.lobby_queue))
            queue_embed.color = discord.Color.blue()
            await ctx.send(embed=queue_embed)
            return
    @commands.command(name="join", aliases=['j'], description="Join an already existing Lobby.")
    async def join_lobby(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("You did not specify a lobby to join.")
            return
        else:
            try:
                int(args[0])
            except ValueError:
                await ctx.send("That is not a valid lobby number.")
                return
            print("Looking for lobbies")
            for lobby in _LobbyManager.lobby_list:  
                print(lobby.lobbyNumber)
                if (lobby.lobbyNumber == args[0]):
                    lobby.addPlayer(ctx.author)
                    await ctx.send("Added you to {0}".format(lobby.lobbyName))


    @commands.command(name="delete", aliases=['dl'], description="Deletes a lobby that was created previously.", hidden=True)
    @commands.has_permissions(manage_channels=True)
    async def delete_lobby(self, ctx, *args):
        server = ctx.guild
        await ctx.channel.purge(limit=1)
        if len(args) == 0:
            await ctx.send("You did not specify a room.")
            return
        try:
            int(args[0])
        except ValueError:
            await ctx.send("That is not a valid lobby number.")
            return

        lobby = f'Lobby {args[0]}'
        for category in server.categories:
            if category.name == lobby:
                for voice_channel in category.voice_channels:
                    await voice_channel.delete()
                await category.delete()
                print(f'\n{ctx.author} deleted {lobby}.\n')
                return
        #find lobby in manager and delete
        for lob in _LobbyManager.lobby_list:
            if lob.lobbyNumber == args[0]:
                _LobbyManager.remove_lobby(args[0])
                print(f'{lobby} has been removed.')
                return
        await ctx.send(f'Could not find {lobby}. My b.')
    
    @commands.command(name="report", aliases=['rp'], description="Report Match results from a finished lobby. Example: $report [lobby#] [bluescore] [orangescore]")
    async def report_match(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("You did not specify a room to report.")
            return
        try:
            for arg in args:
                int(arg[0])
        except ValueError:
            await ctx.send("That is not a valid number.")
            return
        lobby_num = args[0]
        score_blue = args[1]
        score_orange = args[2]
        print("This match is reporting results")
        ##Find lobby with this lobby#
        _LobbyManager.report_match(lobby_num, score_blue, score_orange)
        await ctx.send("Reporting Match for Lobby # {0}- score was {1} - {2}".format(args[0], args[1], args[2]))
        ##Lobby Await results (Reactions) from players
        print(ctx)
        print(args)
        await self.delete_lobby(ctx, args[0])

    @commands.command(name="remove", description="Removes a player from a queue", hidden=True)
    @commands.has_permissions(manage_channels=True)
    async def remove_from_queue(self, ctx, *, member: discord.Member):
        if member not in self.lobby_queue:
            await ctx.send(f"{member.display_name} is not in a queue right now.")
            return
        if member in self.lobby_queue:
            self.blue_queue.remove(member)
            await ctx.send(f'{member.display_name} has been successfully removed from the queue.')
            return
    @commands.command(name="lobprop", description="Returns the known properties for the given Lobby")
    async def lobprop(self, ctx, *args):
        for lob in _LobbyManager.lobby_list:
            await ctx.send(lob.display())

    @commands.command(hidden=True, name="addQueue")
    @commands.has_permissions(manage_channels=True)
    async def add_to_queue(self, member: discord.Member):
        # You will need to set your own ID here
        self.lobby_queue.append(member)
        print("Member successfully added to the queue")
        return

    @commands.command(name='moveP', description="Move player to specified lobby")
    async def move_player(self, ctx, lobby, member : discord.Member):
        await self.move_players_to_vclobby(ctx, member, lobby)


    @staticmethod
    async def create_lobby(ctx):
        server = ctx.guild
        lobby_num = str(random.randint(1, 1000))
        lobby = f'Lobby {lobby_num}'
        category_channel = await server.create_category_channel(lobby)
        lobby_embed = discord.Embed(title=f'New Lobby has been created', type="rich", color=discord.Color.green())
        lobby_embed.add_field(name=f'Please join {lobby}', value=f"Good Luck and Have Fun", inline=True)
        await ctx.send(embed=lobby_embed)
        await category_channel.create_voice_channel(lobby_num, user_limit=6)
        await category_channel.create_voice_channel("Team 1", user_limit=3)
        await category_channel.create_voice_channel("Team 2", user_limit=3)
        tempLobby = Lobby(lobby)
        return tempLobby

    async def random_teams(self, ctx, players, Lobby : Lobby):
        self.team_one = random.sample(players, (MAX_QUEUE /2))  
        for player in self.team_one:
            Lobby.team_one.append(player)
            await self.move_players_to_vclobby(ctx, player, Lobby)  
            players.remove(player)
        self.team_two = players
        for player in self.team_two:
            Lobby.team_two.append(player)
            await self.move_players_to_vclobby(ctx, player, Lobby)  
        teams_embed = discord.Embed(color=discord.Color.green())
        if (len(Lobby.team_one) > 0):
            teams_embed.add_field(name="**Team 1**", value=f'{" ".join(player.name for player in self.team_one)}',
                                inline=False)
        if (len(Lobby.team_two) > 0):
            teams_embed.add_field(name="**Team 2**", value=f'{" ".join(player.name for player in self.team_two)}',
                              inline=False)
        #await ctx.send(embed=teams_embed)
        print("Teams Have been made")
 
    
    async def move_players_to_vclobby(self, ctx,  member: discord.Member, lobby: Lobby):
        server = ctx.guild
        for category in server.categories:
            if category.name == lobby.lobbyName:
                for voice_channel in category.voice_channels:
                    channel_id = voice_channel.id
                    print(voice_channel.name)
                    print(lobby.lobbyName)
                    if voice_channel.name in lobby.lobbyName:
                        print("Moving {0} to {1}".format(member, channel_id))
                        try:
                            await member.move_to(voice_channel)
                        except:
                            print("Could not move member")

                    """
                    if voice_channel.name == "Team 1":
                        print(voice_channel.name)
                        print(lobby.team_one)
                        if any(x.name + '#' + x.discriminator == member for x in lobby.team_one):
                            
                    if voice_channel.name == "Team 2":
                        print(voice_channel.name)
                        if any(x.name + '#' + x.discriminator == member for x in lobby.team_two):
                            await member.move_to(channel_id)
                    """


def setup(bot):
    bot.add_cog(QueueHandler(bot))

