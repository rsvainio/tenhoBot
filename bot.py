import discord
from discord import Interaction
from discord.ext import commands
import json
import databaseManipulation

#TODO: Implement logging

def runDiscordBot():
    TOKEN = loadConfig('token')
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix = '!', intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username =      str(message.author)
        userMessage =   str(message.content)
        channel =       str(message.channel)
        print(f'{username} said: "{userMessage}" on #{channel}')

        if userMessage.lower().startswith('hello'):
            await message.channel.send('YO!')

    @client.event
    # catch 'repostimiespate'
    async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
        try:
            if reaction.is_custom_emoji():
                if reaction.emoji.name == 'Tenho':
                    databaseManipulation.queryDatabase(user.name)
            else:
                print('non-custom')
        except Exception as e:
            print(e)

    @client.tree.command(name='hello')
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message('stfu')

    @client.tree.command(name='add_response')
    async def add_response(interaction: discord.Interaction, response: str):
        try:
            response = str(response)
            if response == None:
                raise Exception
        except Exception as e:
            print(e)
            await interaction.response.send_message('Use a proper response dumbass')
            return

        with open('responses.json') as f:
            responses = json.load(f)
        responses.append({
            "author": interaction.user.name,
            "response": response})
        with open('responses.json', 'w') as f:
            json.dump(responses, f)

        await interaction.response.send_message('Thanks for your input, sucker\nThis is going in my cringe compilation')

    @client.tree.command(name='tapan_ittes')
    async def tapan_ittes(interaction: discord.Interaction):
        print(f'{interaction.user} used: "{interaction.command}" on #{interaction.channel}')
        if await client.is_owner(interaction.user) or interaction.user.name in loadConfig('whitelist'):
            print('Shutting down...')
            await interaction.response.send_message('kuolen nyt')
            await client.close()
        else:
            #TODO: Do something fun here (permaban their ass)
            await interaction.response.send_message('kuolet nyt')

    @client.tree.command(name='sync')
    @commands.guild_only()
    @commands.is_owner()
    async def sync(interaction: discord.Interaction):
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} commands')
        await interaction.response.send_message(f'Synced {len(synced)} commands')

    client.run(TOKEN)

def loadConfig(field):
    with open('config.json') as f:
        configs = json.load(f)
        return configs[field]