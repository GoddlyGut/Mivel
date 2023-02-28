import nextcord
from nextcord.ext import commands
import os
import json
from nextcord.utils import get
from nextcord import Embed, Member
from datetime import datetime
from nextcord.ui import Button, View

intents = nextcord.Intents.all()
intents.members = True



if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix":"."}
    
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)



TOKEN = os.getenv("DISCORD_TOKEN")

prefix = configData["Prefix"]

client = commands.Bot(command_prefix=prefix, intents=intents)





@client.event
async def on_ready():
    print("Bot is ready.")
    client.remove_command('help')
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="/help"))


    

        
@client.event
async def on_command_error(ctx, error):
    embed=nextcord.Embed(
        title="❌ Error",
        colour= nextcord.Colour.red(),
        description=f"{error} | To see a list of available commands, please use `/help`!"
    )
    
    view = View()
    link = Button(label="Support Server", url="https://discord.gg/HvPTFMfPRy")
    view.add_item(link)   
    embed.timestamp = datetime.now()
            
    await ctx.reply(embed=embed, view=view)


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
