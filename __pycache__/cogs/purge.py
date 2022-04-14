from nextcord import Member
from nextcord.ext import commands
import nextcord
from nextcord import GuildSticker, Interaction
from nextcord.ext.commands import MissingPermissions, has_permissions
from datetime import datetime

class purge(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
    @nextcord.slash_command(name="purge-member", description="Use this command to purge a specific users messages")
    async def purge_member(self, interaction: Interaction,user:Member = nextcord.SlashOption(description="Which user do you want to select?", required=True), amount: int = nextcord.SlashOption(description="How many messages do you want to purge?", required=True)):
        if interaction.user.guild_permissions.manage_messages:
            channel = interaction.channel
        
        
            embed_success=nextcord.Embed(
                title="Successful Purge",
                colour= nextcord.Colour.green(),
                description=f"Successfully purged {amount} messages from {user.mention}!"
            )
                    
            embed_success.timestamp = datetime.now()
        
            messages = []

            async for message in channel.history(limit=amount):
                if message.author.name == user.name:
                    messages.append(message)
            await channel.purge(limit=amount+1, check=lambda message: message.author == user)
            if amount > 1:
                await interaction.response.send_message(embed=embed_success, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed_success, ephemeral=True)
        else:
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms,ephemeral=True)
    
    @nextcord.slash_command(name="purge",description="Use this command to delete messages!")
    async def purge(self, interaction: Interaction, amount: int = nextcord.SlashOption(description="How many messages do you want to purge?", required=True)):
        if interaction.user.guild_permissions.manage_messages:
            channel = interaction.channel
        
        
            embed_success=nextcord.Embed(
                title="Successful Purge",
                colour= nextcord.Colour.green(),
                description=f"Successfully purged {amount} messages!"
            )
                    
            embed_success.timestamp = datetime.now()
        
            messages = []

            async for message in channel.history(limit=amount):
                messages.append(message)
            await channel.purge(limit=amount)
            if amount > 1:
                await interaction.response.send_message(embed=embed_success, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed_success, ephemeral=True)
        else:
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms,ephemeral=True)
            
    

    

def setup(client):
    client.add_cog(purge(client))