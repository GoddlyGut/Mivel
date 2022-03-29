from nextcord.ext import commands
import nextcord
from nextcord import Guild, Member, Role, RoleTags, member
from nextcord import GuildSticker, Interaction
from nextcord.ext.commands import MissingPermissions, has_guild_permissions
from nextcord.abc import GuildChannel
from nextcord import Interaction, SlashOption, ChannelType
from nextcord import components
from nextcord.utils import get
from datetime import datetime
import sqlite3
import os
import json


   

class ticket_system(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    testServerId = 907299002586894367
    
    @commands.group(invoke_without_command=True)
    async def ticket_settings(self, ctx):
        embed=nextcord.Embed(
            title="Ticket Settings Info",
            colour= nextcord.Colour.blurple(),
            description="Available Setup Commands:\n`[.]ticket_settings role <@role>`\n`[.]ticket_settings message <'message'>`\n`[.]ticket_settings disable`\n`[.]ticket_settings enable`"
            
        )

        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    @ticket_settings.command()
    async def role(self, ctx,*, ticket_support_role:nextcord.Role):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('ticket.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT staff_role FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
                
                
            embed=nextcord.Embed(
                title="Ticket Info Updated",
                colour= nextcord.Colour.green(),
                description=f"Ticket support role has been set to {ticket_support_role.mention}"
            )
                    
            embed.timestamp = datetime.now()
                
            
            if result is None:
                sql = ("INSERT INTO main(guild_id, staff_role) VALUES(?,?)")
                val = (ctx.guild.id, ticket_support_role.id)
                    
                    
                await ctx.reply(embed=embed)
            elif result is not None:
                sql = ("UPDATE main SET staff_role = ? WHERE guild_id = ?")
                val = (ticket_support_role.id, ctx.guild.id)
                await ctx.reply(embed=embed)
                
                
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
    
    @role.error
    async def channel_error(self,ctx, error):
        embed=nextcord.Embed(
            title="Error",
            colour= nextcord.Colour.red(),
            description=error
        )
                    
        embed.timestamp = datetime.now()
        
        await ctx.reply(embed=embed)
        
        
    @ticket_settings.command()
    async def disable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            
            db = sqlite3.connect('ticket.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT Enabled FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()

            embed=nextcord.Embed(
                title="Ticket Settings Updated",
                colour= nextcord.Colour.green(),
                description=f'Ticket system has been disabled!'
            )
            
            embed.timestamp = datetime.now()
            
            if result is None:
                sql = ("INSERT INTO main(guild_id, Enabled) VALUES(?,?)")
                val = (ctx.guild.id, "False")
                await ctx.reply(embed=embed)
            elif result is not None:
                sql = ("UPDATE main SET Enabled = ? WHERE guild_id = ?")
                val = ("False", ctx.guild.id)
                await ctx.reply(embed=embed)
                
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
        
    @ticket_settings.command()
    async def enable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('ticket.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT Enabled FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()

            embed=nextcord.Embed(
                title="Ticket Settings Updated",
                colour= nextcord.Colour.green(),
                description=f'Ticket system has been enabled!'
            )
            
            embed.timestamp = datetime.now()
            
            if result is None:
                sql = ("INSERT INTO main(guild_id, Enabled) VALUES(?,?)")
                val = (ctx.guild.id, "True")
                await ctx.reply(embed=embed)
            elif result is not None:
                sql = ("UPDATE main SET Enabled = ? WHERE guild_id = ?")
                val = ("True", ctx.guild.id)
                await ctx.reply(embed=embed)
                
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)

    @ticket_settings.command()
    async def message(self, ctx, *,ticket_message_new: str):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('ticket.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT ticket_message FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
            embed=nextcord.Embed(
                title="Ticket Info Updated",
                colour= nextcord.Colour.blurple(),
                description=f'Ticket message has been set to "{ticket_message_new}"'
            )
                    
            embed.timestamp = datetime.now()
            
            if result is None:
                sql = ("INSERT INTO main(guild_id, ticket_message) VALUES(?,?)")
                val = (ctx.guild.id, ticket_message_new)
                await ctx.reply(embed=embed)
            elif result is not None:
                sql = ("UPDATE main SET ticket_message = ? WHERE guild_id = ?")
                val = (ticket_message_new, ctx.guild.id)
                await ctx.reply(embed=embed)
                
                
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms) 
    
    @message.error
    async def message_error(self,ctx, error):
        embed=nextcord.Embed(
            title="Error",
            colour= nextcord.Colour.red(),
            description=error
        )
                    
        embed.timestamp = datetime.now()
        
        await ctx.reply(embed=embed)
    
        
    
    @nextcord.slash_command(name="ticket", description="Use this command to create a ticket",guild_ids=[testServerId])
    async def ticket(self, interaction: Interaction):
           
        db = sqlite3.connect('ticket.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT staff_role FROM main WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()
        
        cursor_message = db.cursor()
        cursor_message.execute(f"SELECT ticket_message FROM main WHERE guild_id = {interaction.guild.id}")
        result_message = cursor_message.fetchone()
        
        cursor_enabled = db.cursor()
        cursor_enabled.execute(f"SELECT Enabled FROM main WHERE guild_id = {interaction.guild.id}")
        result_enabled = cursor_enabled.fetchone()
        
        if result is None or result_message is None:
            embed_error=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="Please setup the ticket bot before use!"
            )
                        
            embed_error.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error, ephemeral=True)
        else:
            if result_enabled[0] == "False":
                embed_not_enabled=nextcord.Embed(
                    title="Ticket System",
                    colour= nextcord.Colour.red(),
                    description="Ticket system has been disabled!"
                )   
                    
                embed_not_enabled.timestamp = datetime.now()
        
                await interaction.response.send_message(embed=embed_not_enabled, ephemeral=True)
            else:
                support_role = result[0]
                ticket_message = result_message[0]
                if get(interaction.guild.categories, name="Support-Category"):
                    SupportCategory = get(interaction.guild.categories, name="Support-Category")
                    admin_role = get(interaction.guild.roles, id=int(support_role))

                    
                    if admin_role is None:
                        newRole = await interaction.guild.create_role(name="Support")
                        admin_role = newRole.name
                        
                    overwrites={
                        interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                        interaction.user: nextcord.PermissionOverwrite(view_channel=True),
                        admin_role: nextcord.PermissionOverwrite(view_channel=True),
                    }
                    
                    channel = await interaction.guild.create_text_channel(f"support~{interaction.user.name}", category=SupportCategory, overwrites=overwrites)
                    
                    
                else:
                    newCategory = await interaction.guild.create_category("Support-Category")
                    admin_role = get(interaction.guild.roles, name=support_role)
                    overwrites={
                        interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                        interaction.user: nextcord.PermissionOverwrite(view_channel=True),
                        admin_role: nextcord.PermissionOverwrite(view_channel=True),
                    }
                    
                    channel = await interaction.guild.create_text_channel(f"support~{interaction.user.name}", category=newCategory, overwrites=overwrites)
                
                embed = nextcord.Embed(
                    title="Ticket",
                    colour= nextcord.Colour.blurple()
                )
                        
                embed.timestamp=datetime.now()
                embed.add_field(name="User", value=interaction.user.mention)
                embed.add_field(name="Support", value=ticket_message, inline=False)
                msg = await channel.send(embed=embed)
                await msg.add_reaction("🗑️")
                await interaction.response.send_message(f"Created message in {channel.mention}", ephemeral=True)
        





def setup(client):
    client.add_cog(ticket_system(client))