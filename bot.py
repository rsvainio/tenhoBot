import discord
import json
import databaseManipulation


def loadConfig():
    with open('config.json') as f:
        data = json.load(f)
        return data['token']
    
def runDiscordBot():
    configs = loadConfig()
    TOKEN = configs['token']
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

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
    async def on_reaction_add(reaction, user):
        try:
            if reaction.is_custom_emoji():
                if reaction.emoji.name == 'Tenho':
                    databaseManipulation.queryDatabase(user.name)
            else:
                print('non-custom')
        except Exception as e:
            print(e)

    client.run(TOKEN)