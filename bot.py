import discord
from discord import Interaction
from discord.ext import commands, tasks
import json
import datetime
import random
import os
import databaseManipulation
import operationLogging

#TODO: make sure logging is actually done at each function

def runDiscordBot():
    TOKEN = loadConfig('token')
    intents = discord.Intents.all()
    #intents = discord.Intents.default()
    bot = commands.Bot(command_prefix = '!', intents=intents)
    operationLogging.init()

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        operationLogging.log(f'{bot.user} is now running!')

    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return
        username =      str(message.author)
        userMessage =   str(message.content)
        channel =       str(message.channel)
        
        if userMessage != '':
            operationLogging.log(f'{username} said: "{userMessage}" on #{channel}')
        if userMessage.lower().startswith('hello'):
            await message.channel.send('YO!')

    @bot.event
    # catch 'repostimiespate'
    async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
        try:
            if reaction.is_custom_emoji():
                if reaction.emoji.name == 'repostimies':
                    operationLogging.log(f'{user.name} reacted with repostimies to a message on #{reaction.message.channel}')
                    databaseManipulation.incrementUser(user.name)
        except Exception as e:
            operationLogging.log(e)

    @bot.tree.command(name='hello', description='Greet the bot and get a "witty" response')
    async def hello(interaction: discord.Interaction):
        dbResponse = await databaseManipulation.fetchResponse()
        await interaction.response.send_message(dbResponse[1])

    @bot.tree.command(name='add_response', description="Add a command to the bot's list of responses used in the /hello command")
    async def add_response(interaction: discord.Interaction, response: str):
        try:
            response = str(response)
            if response == None or len(response) >= 255:
                raise Exception
        except Exception as e:
            operationLogging.log(e)
            embed = embedDecorator(interaction)
            embed.add_field(name='Use a proper response, dumbass', value='')
            await interaction.response.send_message(embed=embed)
            return
        databaseManipulation.addEntry((interaction.user.name, response), 'Responses')

        embed = embedDecorator(interaction)
        embed.add_field(name="Thanks for your input, sucker\nThis one's going in my cringe compilation", value='')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='keep_company', description="Get Tenho to keep you company on a voice channel")
    async def keep_company(interaction: discord.Interaction):
        embed = embedDecorator(interaction)
        if not interaction.user.voice:
            embed.add_field(name="Join a voice channel first, fool", value='')
            return await interaction.response.send_message(embed=embed)

        voiceChannel: discord.VoiceChannel = interaction.user.voice.channel
        voiceClient: discord.VoiceClient = await voiceChannel.connect()
        embed.add_field(name=f"Connected to voice channel {voiceChannel.name}", value='')
        await interaction.response.send_message(embed=embed)

        @tasks.loop(seconds=20.0, count=3)
        async def speak():
            # actually need to install ffmpeg also
            randomFile = random.choice(os.listdir('media/sound'))
            print(f'media/sound/{randomFile}')
            voiceClient.play(discord.FFmpegPCMAudio(f'media/sound/{randomFile}'))

        @speak.after_loop
        async def after_speak():
            await voiceClient.disconnect()
            voiceClient.cleanup()

        speak.start()

    @bot.tree.command(name='leave_company', description="Tell Tenho to go back home to Varissuo")
    async def leave_company(interaction: discord.Interaction):
        embed = embedDecorator(interaction)
        if interaction.user.voice and bot.voice_clients:
            for voiceClient in bot.voice_clients:
                if voiceClient.guild == interaction.guild:
                    await voiceClient.disconnect()
                    voiceClient.cleanup()
                   
                    embed.add_field(name=f"Disconnected from {voiceClient.channel.name}", value='')
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed.add_field(name="Join a voice channel with me in it first, fool", value='')
            return await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='tapan_ittes', description="Make the bot sad and tell it to shut down")
    async def tapan_ittes(interaction: discord.Interaction):
        operationLogging.log(f'{interaction.user} used: "{interaction.command}" on #{interaction.channel}')
        embed = embedDecorator(interaction)
        if await bot.is_owner(interaction.user) or interaction.user.name in loadConfig('whitelist'):
            operationLogging.log('Shutting down...')
            embed.add_field(name='kuolen nyt', value='')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await bot.close()
        else:
            #TODO: Do something fun here (read: permaban their ass)
            embed.add_field(name='kuolet nyt', value='')
            await interaction.response.send_message(embed=embed)

            randomFile = random.choice(os.listdir('media/image'))
            with open(f'media/image/{randomFile}', 'rb') as f:
                pic = discord.File(f)
                await interaction.channel.send(file=pic)
                await interaction.guild.create_scheduled_event(
                    name='Laugh at this dumbass',
                    description=f'Laugh at {interaction.user.display_name} for being a dumbass and trying to kill me lmao hahaaa',
                    start_time=discord.utils.utcnow() + datetime.timedelta(0, 300),
                    end_time=discord.utils.utcnow() + datetime.timedelta(0, 600),
                    #image=pic, should probably fix this
                    entity_type=discord.EntityType.external,
                    privacy_level=discord.PrivacyLevel.guild_only,
                    location=f"{interaction.user.display_name}'s mom's house",
                    reason=f'To laugh at {interaction.user.display_name} for being a dumbass and trying to kill me lmao hahaaa'
                    )

    @bot.tree.command(name='sync', description="Update the bot's list of commands")
    @commands.guild_only()
    @commands.is_owner()
    async def sync(interaction: discord.Interaction):
        try:
            synced = await bot.tree.sync()
            operationLogging.log(f'Synced {len(synced)} commands')
            embed = embedDecorator(interaction)
            embed.add_field(name=f'Synced {len(synced)} commands', value='')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except commands.NotOwner as e:
            operationLogging.log(f'{interaction.user.name} tried to use /sync on #{interaction.channel}')

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