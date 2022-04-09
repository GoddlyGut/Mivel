from turtle import title
import nextcord
from nextcord import Color, Guild, Member, member
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord import Interaction, SlashOption, ChannelType
from datetime import datetime, timedelta




class embed_system(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @nextcord.slash_command(name="embed", description="What text would you like to embed?")
    async def embed_command(self, interaction:Interaction, text:str):
        embed = nextcord.Embed(
            title="",
            color=nextcord.Color.blurple(),
            description=text
        )

        await interaction.response.send_message(embed=embed)
        

def setup(client):
    client.add_cog(embed_system(client))