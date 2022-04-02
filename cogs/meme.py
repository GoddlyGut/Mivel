from nextcord import Member
from nextcord.ext import commands
import nextcord
from nextcord import GuildSticker, Interaction
from nextcord.ext.commands import MissingPermissions, has_permissions
from datetime import datetime
import aiohttp
import random

class memes(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name="meme", description="Use this command to show a meme!")
    async def meme(self, interaction:Interaction):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.reddit.com/r/memes.json") as r:
                memes = await r.json()
                embed = nextcord.Embed(
                    color=nextcord.Color.magenta()
                )
                
                embed.set_image(url=memes["data"]["children"][random.randint(0,25)]["data"]["url"])
                embed.set_footer(text=f"Managed & Operated by r/Memes")
                await interaction.response.send_message(embed=embed)
         
        
def setup(client):
    client.add_cog(memes(client))