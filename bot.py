import discord
from discord import Interaction
from discord.ext import commands
import json
import random
import databaseManipulation

#TODO: Implement logging

def runDiscordBot():
    TOKEN = loadConfig('token')
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix = '!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return
        username =      str(message.author)
        userMessage =   str(message.content)
        channel =       str(message.channel)
        print(f'{username} said: "{userMessage}" on #{channel}')

        if userMessage.lower().startswith('hello'):
            await message.channel.send('YO!')

    @bot.event
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

    @bot.tree.command(name='hello', description='Greet the bot and get a "witty" response')
    async def hello(interaction: discord.Interaction):
        with open('responses.json') as f:
            responses = json.load(f)
            response = random.choice(responses)
        embed = embedDecorator(interaction)
        embed.add_field(name=response['response'], value='')
        embed.set_footer(text=f"Author: {response['author']}")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='add_response', description="Add a command to the bot's list of responses used in the /hello command")
    async def add_response(interaction: discord.Interaction, response: str):
        try:
            response = str(response)
            if response == None:
                raise Exception
        except Exception as e:
            print(e)
            embed = embedDecorator(interaction)
            embed.add_field(name='Use a proper response, dumbass', value='')
            await interaction.response.send_message(embed=embed)
            return

        with open('responses.json') as f:
            responses = json.load(f)
        responses.append({
            "author": interaction.user.name,
            "response": response})
        with open('responses.json', 'w') as f:
            json.dump(responses, f)

        embed = embedDecorator(interaction)
        embed.add_field(name="Thanks for your input, sucker\nThis is going straight in my cringe collection", value='')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='tapan_ittes', description="Make the bot sad and tell it to shut down")
    async def tapan_ittes(interaction: discord.Interaction):
        print(f'{interaction.user} used: "{interaction.command}" on #{interaction.channel}')
        embed = embedDecorator(interaction)

        if await bot.is_owner(interaction.user) or interaction.user.name in loadConfig('whitelist'):
            print('Shutting down...')
            embed.add_field(name='kuolen nyt', value='')
            await interaction.response.send_message(embed=embed)
            await bot.close()
        else:
            #TODO: Do something fun here (read: permaban their ass)
            embed.add_field(name='kuolet nyt', value='')
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='sync', description="Update the bot's list of commands")
    @commands.guild_only()
    @commands.is_owner()
    async def sync(interaction: discord.Interaction):
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
        embed = embedDecorator(interaction)
        embed.add_field(name=f'Synced {len(synced)} commands', value='')
        await interaction.response.send_message(embed=embed, ephemeral=True)

    bot.run(TOKEN)

def loadConfig(field):
    with open('config.json') as f:
        configs = json.load(f)
        return configs[field]

# general decorator for embeds that can be expanded upon later
def embedDecorator(context: discord.Interaction) -> discord.Embed:
    embed = discord.Embed()
    embed.set_author(name=context.user.display_name, icon_url=context.user.display_avatar.url)
    return embed