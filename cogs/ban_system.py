from optparse import Option
import nextcord
from nextcord import Guild, Member, member
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord import Interaction, SlashOption, ChannelType

testServerId = 907299002586894367

class ban_system(commands.Cog):
    def __init__(self, client):
        self.client = client


    @nextcord.slash_command(name="kick",description="Use this command to kick members!",guild_ids=[testServerId])
    async def kick(self, interaction: Interaction,member: Member = nextcord.SlashOption(description="Please select a member", required=True),reason=nextcord.SlashOption(description="Please type a valid reason", required=True)):
        if interaction.user.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await interaction.response.send_message(f'User {member.mention} has been kicked')
        else:
            await interaction.response.send_message(f"You do not have the required permissions!", ephemeral=True) 
        
        
    @nextcord.slash_command(name="ban",description="Use this command to ban members!",guild_ids=[testServerId])
    async def ban(self, interaction: Interaction,member: Member = nextcord.SlashOption(description="Please select a member", required=True),reason=nextcord.SlashOption(description="Please type a valid reason", required=True)):
        if interaction.user.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await interaction.response.send_message(f'User {member.mention} has been banned')
        else:
            await interaction.response.send_message(f"You do not have the required permissions!", ephemeral=True) 

    @nextcord.slash_command(name="unban",description="Use this command to unban members!",guild_ids=[testServerId])
    async def unban(self, interaction: Interaction,member:str= nextcord.SlashOption(description="Please type the members username", required=True)):
        if interaction.user.guild_permissions.ban_members:
            banned_users = await interaction.guild.bans()
            member_name, member_hash_code = member.split("#")
        
            for ban_entry in banned_users:
                user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_hash_code):
                await interaction.guild.unban(user)
                await interaction.response.send_message(f'User {user.mention} has been unbanned!')
        else:
            await interaction.response.send_message(f"You do not have the required permissions!", ephemeral=True) 
            

def setup(client):
    client.add_cog(ban_system(client))