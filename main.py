import nextcord
from nextcord.ext import commands
import os
import json
from nextcord.utils import get


intents = nextcord.Intents.all()
intents.members = True



if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix":"."}
    
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)


TOKEN = "OTU2MzQyNzI2OTEwMTgxNDI2.Yju1kg.QVCzfdMpFinbYq5455Z8jowxosI"

#TOKEN = os.getenv("DISCORD_TOKEN")

#token = configData["Token"]
prefix = configData["Prefix"]

client = commands.Bot(command_prefix=prefix, intents=intents)





@client.event
async def on_ready():
    # db = sqlite3.connect('roblox_userid.sqlite')
    # cursor = db.cursor()
    # cursor.execute('''
    #                CREATE TABLE IF NOT EXISTS main(
    #                    guild_id TEXT,
    #                    role TEXT,
    #                    Enabled TEXT
    #                )
    #                ''')
    print("Bot is ready.")
    client.remove_command('help')
    game = nextcord.Game("Watching Commands")
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="Commands"))


#################################


#For cog system
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.message.delete()
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.message.delete()
@client.command()
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    await ctx.message.delete()

for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        client.load_extension(f"cogs.{fn[:-3]}")
#################################


client.run(TOKEN)
