from sre_parse import FLAGS
from sys import flags
import nextcord
from nextcord.ext import commands
import os
import json
import sqlite3
from nextcord.utils import get


intents = nextcord.Intents.default()
intents.members = True



if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix":"."}
    
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

TOKEN = os.getenv("DISCORD_TOKEN")
        
#TOKEN = "OTU2MzQyNzI2OTEwMTgxNDI2.Yju1kg.QVCzfdMpFinbYq5455Z8jowxosI"

#token = configData["Token"]
prefix = configData["Prefix"]

client = commands.Bot(command_prefix=prefix, intents=intents)





@client.event
async def on_ready():
    # db = sqlite3.connect('welcome.sqlite')
    # cursor = db.cursor()
    # cursor.execute('''
    #                CREATE TABLE IF NOT EXISTS main(
    #                    guild_id TEXT,
    #                    channel_id TEXT,
    #                    welcome_message TEXT
    #                )
    #                ''')
    print("Bot is ready.")
    game = nextcord.Game("Watching Commands")
    await client.change_presence(status=nextcord.Status.online, activity=game)
    
#For ticket system
@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "🗑️":
        channel = client.get_channel(payload.channel_id)
        if channel.category.name == "Support-Category":
            message = await channel.fetch_message(payload.message_id)
            reaction = get(message.reactions, emoji = payload.emoji.name)
            if reaction and reaction.count > 1:
                await channel.delete()

#################################


#For cog system
#@client.command()
#async def load(ctx, extension):
 #   client.load_extension(f'cogs.{extension}')
  #  await ctx.message.delete()
#@client.command()
#async def unload(ctx, extension):
 #   client.unload_extension(f'cogs.{extension}')
  #  await ctx.message.delete()
#@client.command()
#async def reload(ctx, extension):
 #   client.reload_extension(f'cogs.{extension}')
  #  await ctx.message.delete()

#for fn in os.listdir("./cogs"):
 #   if fn.endswith(".py"):
  #      client.load_extension(f"cogs.{fn[:-3]}")
#################################


if __name__ == "__main__":
    client.run(TOKEN)
