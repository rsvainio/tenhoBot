import discord
import json

def loadToken():
    with open("bot.json") as f:
        data = json.load(f)
        return data['token']


def runDiscordBot():
    TOKEN = loadToken()
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
        print(f"{username} said: '{userMessage}' on {channel}")

        if userMessage.lower().startswith("hello"):
            await message.channel.send("YO!")

    @client.event
    async def on_raw_reaction_add(reaction):
        try:
            emoji = reaction.emoji
            print(emoji.name)
        except Exception as e:
            print(e)

    client.run(TOKEN)