import nextcord
from nextcord.ext import commands
from datetime import datetime
import sqlite3
class welcome_system(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.group(invoke_without_command=True)
    async def welcome_settings(self, ctx):
        embed=nextcord.Embed(
            title="Welcome Settings Info",
            colour= nextcord.Colour.blurple(),
            description="Available Setup Commands:\n`[m!]welcome_settings channel <#channel>`\n`[m!]welcome_settings message <'message'>`\n`[m!]welcome_settings disable`\n`[m!]welcome_settings enable`"
        )      
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    @welcome_settings.command()
    async def channel(self, ctx, channel:nextcord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:

            db = sqlite3.connect('welcome.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
                
                
            embed=nextcord.Embed(
                title="Welcome Info Updated",
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
        
        
    @welcome_settings.command()
    async def disable(self,ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('welcome.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT Enabled FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
            embed=nextcord.Embed(
                title="Welcome System Updated",
                colour= nextcord.Colour.green(),
                description=f"Welcome system has been disabled!"
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
            
            
            

    @welcome_settings.command()
    async def enable(self,ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('welcome.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT Enabled FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
            embed=nextcord.Embed(
                title="Welcome System Updated",
                colour= nextcord.Colour.green(),
                description=f"Welcome system has been enabled!"
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
            
    @welcome_settings.command()
    async def message(self, ctx,*, message:str):
        if ctx.message.author.guild_permissions.manage_messages:

            db = sqlite3.connect('welcome.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT welcome_message FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
                
                
            embed=nextcord.Embed(
                title="Welcome Info Updated",
                colour= nextcord.Colour.green(),
                description=f"Welcome message has been set to '{message}'"
            )
                    
            embed.timestamp = datetime.now()
                
            if result is None:
                sql = ("INSERT INTO main(guild_id, welcome_message) VALUES(?,?)")
                val = (ctx.guild.id, message)
                await ctx.reply(embed=embed)
            elif result is not None:
                sql = ("UPDATE main SET welcome_message = ? WHERE guild_id = ?")
                val = (message, ctx.guild.id)
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
        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('welcome.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        
        cursor_message = db.cursor()
        cursor_message.execute(f"SELECT welcome_message FROM main WHERE guild_id = {member.guild.id}")
        result_message = cursor_message.fetchone()
        
        cursor_enabled = db.cursor()
        cursor_enabled.execute(f"SELECT Enabled FROM main WHERE guild_id = {member.guild.id}")
        result_enabled = cursor_enabled.fetchone()
        
        if result is None:
            return
        else:
            if result_enabled[0] == "False":
                return
            else:
                channel = self.client.get_channel(int(result[0])) #suggestion-channel
                
                if result_message[0] is None:
                    welcome_description = "Welcome to this server!" #if no data is saved, use default message
                else:
                    welcome_description = result_message[0]
                
                embed_joined=nextcord.Embed(
                    title="New User!",
                    colour= nextcord.Colour.blurple(),
                    description=f"Hello {member.mention}, {welcome_description}"
                    
                )
                embed_joined.set_thumbnail(url=member.display_avatar.url)
                embed_joined.timestamp = datetime.now()
                
                await channel.send(embed=embed_joined)
            
            
            


            
            
    
    

def setup(client):
    client.add_cog(welcome_system(client))
        