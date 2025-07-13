# TenhoBot

A locally-run bot for Discord with a variety of commands, built using the [Discord.py](https://github.com/Rapptz/discord.py) API wrapper

Configure as per the [Discord documentation](https://discord.com/developers/docs/intro).

Additionally, configure *config.json* file in the following format:
```yaml
{
    "token": "", # your bot's token here, sourced from the discord developer portal
    "whitelist": [
        "" # discord usernames here to whitelist as admins
    ]
}
```

Finally, run *main.py* to start the bot.