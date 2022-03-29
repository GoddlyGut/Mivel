import sqlite3
from nextcord.ext import commands
import nextcord
import os
import json
from nextcord import Embed, Role, TextChannel, embeds
from nextcord.abc import GuildChannel
from nextcord import Interaction, SlashOption, ChannelType
from datetime import datetime

class suggestions(commands.Cog):
    def __init__(self, client):
        self.client = client
    
   
    
    testServerId = 907299002586894367
    
  

  
  
    
    @nextcord.slash_command(name="suggest",description="Use this command to send a suggestion!",guild_ids=[testServerId])
    async def suggest(self, interaction: Interaction, suggestion = nextcord.SlashOption(description="Please fill out a suggestion here!", required=True)):
        
        db = sqlite3.connect('suggest.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()
        
        if result is None:
            await interaction.response.send_message("Please finish setting up the suggestion bot!", ephemeral=True)
        else:
           
            
            channel = self.client.get_channel(int(result[0])) #suggestion-channel
            embed=nextcord.Embed(
                title="Suggestion",
                colour= nextcord.Colour.blurple()
             )
                
            embed.set_footer(text="Type /suggest to send a suggestion!")
            embed.add_field(name="User", value=interaction.user.mention,inline=False)
            embed.add_field(name="Suggestion Text", value=suggestion, inline=False)
            
            
            
            msg = await channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            
            
            embed_success=nextcord.Embed(
                title="Suggestion Sent",
                colour= nextcord.Colour.green(),
                description=f"Suggestion submitted to {channel.mention}"
            )
                    
            embed_success.timestamp = datetime.now()
                
            await interaction.response.send_message(embed=embed_success, ephemeral=True)
    
    
    @commands.group(invoke_without_command=True)
    async def suggest_settings(self, ctx):
        embed=nextcord.Embed(
            title="Suggest Settings Info",
            colour= nextcord.Colour.blurple(),
            description="Available Setup Commands: `[.]suggest_settings channel <#channel>`"
        )      
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    @suggest_settings.command()
    async def channel(self, ctx, channel:nextcord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:

            db = sqlite3.connect('suggest.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
                
                
            embed=nextcord.Embed(
                title="Suggest Info Updated",
                colour= nextcord.Colour.green(),
                description=f"Channel has been set to {channel.mention}"
            )
                    
            embed.timestamp = datetime.now()
                
            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.reply(embed=embed)
            elif result is not None:
                sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
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
    
    @channel.error
    async def channel_error(self,ctx, error):
        embed=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description=error
        )
                    
        embed.timestamp = datetime.now()
        
        await ctx.reply(embed=embed)
        
        



def setup(client):
    client.add_cog(suggestions(client))
    