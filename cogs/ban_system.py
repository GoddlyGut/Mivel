from optparse import Option
from async_timeout import timeout
import nextcord
from nextcord import Guild, Member, member
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord import Interaction, SlashOption, ChannelType
from datetime import datetime

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
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)
    
    @nextcord.slash_command(name="ban",description="Use this command to ban members!",guild_ids=[testServerId])
    async def ban(self, interaction: Interaction,member: Member = nextcord.SlashOption(description="Please select a member", required=True),reason=nextcord.SlashOption(description="Please type a valid reason", required=True)):
        if interaction.user.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await interaction.response.send_message(f'User {member.mention} has been banned')
        else:
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)

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
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)
            

def setup(client):
    client.add_cog(ban_system(client))