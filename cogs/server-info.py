from turtle import position
from unicodedata import name
import nextcord
from nextcord.ext import commands, tasks
from datetime import datetime
import sqlite3
from nextcord.utils import get


class server_info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.refresh.start()
        
    @commands.group(invoke_without_command=True)
    async def server_info(self, ctx):
        embed=nextcord.Embed(
            title="Server Info",
            colour= nextcord.Colour.blurple(),
            description="Available Setup Commands: \n`[.]server_info setup`\n`[.]server_info disable`"
        )      
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    @server_info.command()
    async def setup(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()

                
            embed=nextcord.Embed(
                title="Server Info Updated",
                colour= nextcord.Colour.blurple(),
                description=f'Server Info Channel Created! Note that the channel updates every 30 minutes.'
            )
            
            embed.timestamp = datetime.now()
                        
            category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0)
            
            channel = await ctx.guild.create_voice_channel(name=f"Members: {ctx.guild.member_count}", category=category)
            
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
    
    @server_info.command()
    async def disable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
            
            embed=nextcord.Embed(
                title="Server Info Disabled",
                colour= nextcord.Colour.blurple(),
                description=f'Server Info has been disabled!'
            )
            
            embed.timestamp = datetime.now()
                

            channel = self.client.get_channel(int(result[0]))
    
            channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
            
            await channel.delete()
            await channel_category.delete()
            
            await ctx.reply(embed=embed)
        else:
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
        


    
    
    
    @tasks.loop(minutes=30)
    async def refresh(self):
        for guild in self.client.guilds:
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {guild.id}")
            result = cursor.fetchone()
            
            
            channel = self.client.get_channel(int(result[0]))
            
            if channel is None:
                return
            else:
                await channel.edit(name=f"Members: {guild.member_count}")
    

    
        
        
        

def setup(client):
    client.add_cog(server_info(client))
        