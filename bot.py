import discord
from discord.ext import commands
import logging
import sys
from config import Config

logging.basicConfig(level=logging.INFO)

config = Config()
prefix = config.command_prefix
token = config.bot_token
q_channel = config.queue_channel

startup_extensions = ['QueueHandler', 'admin', 'ChatCommands', 'LobbyManager']


if not prefix or not token:
    print("Confirm that you have set your command prefix and Discord bot token in the config.ini")
    sys.exit()

client = commands.Bot(command_prefix=prefix)


@client.event
async def on_command_error(ctx, error):

    print(f'\nCommand Error\nGuild:{ctx.guild.name}\nChannel:{ctx.channel.name}')
    print(f'{ctx.author.name}({ctx.author.id}) has tried to improperly use a command.')
    print(f'The error: {error}\n')


@client.event
async def on_ready():
    print(f'{client.user.name} has logged in.')
    await client.change_presence(activity=discord.Game(name="with my heart."))

if __name__ == '__main__':

    for extension in startup_extensions:
        try:
            client.load_extension(f'cogs.{extension}')
        except Exception as e:
            print(f'Failed to load extension: {extension}')
            print(f'\tError:{e}')
            continue
        print(f'Successfully loaded extension: {extension}')

    client.run(token)
