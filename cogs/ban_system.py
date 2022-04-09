import nextcord
from nextcord import Guild, Member, member
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord import Interaction, SlashOption, ChannelType
from datetime import datetime, timedelta




class ban_system(commands.Cog):
    def __init__(self, client):
        self.client = client


    @nextcord.slash_command(name="kick",description="Use this command to kick members!")
    async def kick(self, interaction: Interaction,member: Member = nextcord.SlashOption(required=True),reason:str=nextcord.SlashOption(required=True)):
        if interaction.user.guild_permissions.kick_members:
            if member.name != interaction.user.name:
                await member.kick(reason=reason)
                await interaction.response.send_message(f'✅ User {member.mention} has been kicked')
            else:
                embed_error_action=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description="You cannot do this action to yourself!"
                )
                    
                embed_error_action.timestamp = datetime.now()
                
                await interaction.response.send_message(embed=embed_error_action)   
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)
    
    @nextcord.slash_command(name="ban",description="Use this command to ban members!")
    async def ban(self, interaction: Interaction,member: Member = nextcord.SlashOption(description="Please select a member", required=True),reason=nextcord.SlashOption(description="Please type a valid reason", required=True)):
        if interaction.user.guild_permissions.ban_members:
            if member.name != interaction.user.name:
                
                await member.ban(reason=reason)
                await interaction.response.send_message(f'✅ User {member.mention} has been banned')
            else:
                embed_error_action=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description="You cannot do this action to yourself!"
                )
                    
                embed_error_action.timestamp = datetime.now()
                
                await interaction.response.send_message(embed=embed_error_action)   
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)


    @nextcord.slash_command(name="lockdown", description="Lockdown a channel")
    async def lockdown(self, interaction:Interaction):
        if interaction.user.guild_permissions.administrator:
            overwrite= interaction.channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            
            await interaction.channel.set_permissions(interaction.guild.default_role,overwrite=overwrite)
            
            embed = nextcord.Embed(
                title="Channel Lockdown",
                color=nextcord.Colour.green(),
                description=f"✅ {interaction.channel.mention} has been successfully locked down by {interaction.user.mention}!"
            )
            
            embed.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed)
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
            
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)
    @nextcord.slash_command(name="unlock", description="Unlock a channel")
    async def unlock(self, interaction:Interaction):
        if interaction.user.guild_permissions.administrator:
            overwrite= interaction.channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = True
            
            await interaction.channel.set_permissions(interaction.guild.default_role,overwrite=overwrite)
            
            embed = nextcord.Embed(
                title="Channel Unlocked",
                color=nextcord.Colour.green(),
                description=f"✅ {interaction.channel.mention} has been successfully unlocked by {interaction.user.mention}!"
            )
            
            embed.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed)
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
            
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)
    @nextcord.slash_command(name="timeout", description="Put a user in timeout")
    
    async def timeout(self, interaction:Interaction, member: Member=nextcord.SlashOption(required=True), days:int=nextcord.SlashOption(required=False),hours:int=nextcord.SlashOption(required=False),minutes:int=nextcord.SlashOption(required=False),seconds:int=nextcord.SlashOption(required=False), reason:str=nextcord.SlashOption(required=False)):
        if interaction.user.guild_permissions.kick_members:
            if member.name != interaction.user.name:
                
                if days == None:
                    days = 0
                if hours == None:
                    hours = 0
                if minutes == None:
                    minutes = 0
                if seconds == None:
                    seconds = 0

    
                duration = timedelta(days=days, hours=hours, minutes=minutes,seconds=seconds)
                await member.timeout(timeout=duration)
                embed_success_timeout=nextcord.Embed(
                    title="Timeout Success",
                    colour= nextcord.Colour.green(),
                    description=f"✅ {member.mention} has been successfully put in timeout by {interaction.user.mention} for {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"
                )
                        
                embed_success_timeout.timestamp = datetime.now()
                
                await interaction.response.send_message(embed=embed_success_timeout)
            else:
                embed_error_action=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description="You cannot do this action to yourself!"
                )
                    
                embed_error_action.timestamp = datetime.now()
                
                await interaction.response.send_message(embed=embed_error_action)   
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)
        
    @nextcord.slash_command(name="remove-timeout",description="Remove a users timeout")
    async def remove_timeout(self, interaction:Interaction, user: Member=nextcord.SlashOption(required=True)):
        if interaction.user.guild_permissions.kick_members:
            
            duration = timedelta(days=0, hours=0, minutes=0,seconds=0)
            await user.timeout(duration)
            embed_success_remove_timeout=nextcord.Embed(
                title="Timeout Success",
                colour= nextcord.Colour.green(),
                description=f"✅ {user.mention} has been successfully unmuted by {interaction.user.mention}"
            )
                        
            embed_success_remove_timeout.timestamp = datetime.now()
                
            await interaction.response.send_message(embed=embed_success_remove_timeout)

        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)   
    
    @nextcord.slash_command(name="unban",description="Use this command to unban members!")
    async def unban(self, interaction: Interaction,member:str= nextcord.SlashOption(description="Please type the members username", required=True)):
        if interaction.user.guild_permissions.ban_members:
            banned_users = await interaction.guild.bans()
            member_name, member_hash_code = member.split("#")
        
            for ban_entry in banned_users:
                user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_hash_code):
                await interaction.guild.unban(user)
                await interaction.response.send_message(f'✅ User {user.mention} has been unbanned!')
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error_perms)
            
    
            

def setup(client):
    client.add_cog(ban_system(client))