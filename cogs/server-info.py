from code import interact
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
            description="Available Setup Commands: \n`[m!]server_info setup_members`\n`[m!]server_info disable_members`\n`[m!]server_info setup_bots`\n`[m!]server_info disable_bots`",
            
        )      
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    
    
    @server_info.command()
    async def setup_members(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT member_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
            cursor_bot = db.cursor()
            cursor_bot.execute(f"SELECT bot_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_bot = cursor_bot.fetchone()

            
            
            if result != None:
                if result[0] is None:
                    channel_found = None
                else:
                    channel_found = self.client.get_channel(int(result[0]))
            else:
                channel_found = None 
            
            if channel_found is None:


                embed=nextcord.Embed(
                    title="Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                            
                if result_bot is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else:
                    if result_bot[0] != None:
                        if self.client.get_channel(int(result_bot[0])) is None:
                            category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                        else:
                            category = self.client.get_channel(int(result_bot[0])).category
                    else:
                        category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                
                channel = await ctx.guild.create_voice_channel(name=f"Members: {ctx.guild.member_count}", category=category)
                
                if result is None:
                    sql = ("INSERT INTO main(guild_id, member_channel_id) VALUES(?,?)")
                    val = (ctx.guild.id, channel.id)
                    await ctx.reply(embed=embed)
                elif result is not None:
                    sql = ("UPDATE main SET member_channel_id = ? WHERE guild_id = ?")
                    val = (channel.id, ctx.guild.id)
                    await ctx.reply(embed=embed)
                    

                    
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
                
            else:
                embed_error=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Members has already been setup!'
                )
                
                await ctx.reply(embed=embed_error)
        else:
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
    
    @server_info.command()
    async def disable_members(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT member_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
            if result != None:
                if result[0] != None:
                    channel = self.client.get_channel(int(result[0]))
                else:
                    channel = None
                
            else:
                channel = None
            
            if channel != None:
                embed=nextcord.Embed(
                    title="Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info has been disabled!'
                )
                
                embed.timestamp = datetime.now()
                    

        
                channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
                
                
                
                
                
                await channel.delete()
                all_channels = channel_category.channels
                if len(all_channels) == 0:
                    await channel_category.delete()
                
                await ctx.reply(embed=embed)
            else:
                embed_error_disable=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description="This feature is already disabled!"
                )
                        
                embed_error_disable.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_disable)   
        else:
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
            
            
            
    @server_info.command()
    async def setup_bots(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT bot_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
            cursor_member = db.cursor()
            cursor_member.execute(f"SELECT member_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_member = cursor_member.fetchone()

            if result != None:
                if result[0] is None:
                    channel_found = None
                else:
                    channel_found = self.client.get_channel(int(result[0]))
            else:
                channel_found = None  
            
            if channel_found is None:
                
                embed=nextcord.Embed(
                    title="Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Bot Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                
                if result_member is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else:
                    if result_member[0] != None:
                        if self.client.get_channel(int(result_member[0])) is None:
                            category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                        else:
                            category = self.client.get_channel(int(result_member[0])).category
                    else:
                        category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                
                members = ctx.guild.members
                bot_count = 0
                for i in members:
                    member = i.bot
                    if member == True:
                        bot_count += 1
                
                channel = await ctx.guild.create_voice_channel(name=f"Bots: {bot_count}", category=category)
                
                if result is None:
                    sql = ("INSERT INTO main(guild_id, bot_channel_id) VALUES(?,?)")
                    val = (ctx.guild.id, channel.id)
                    await ctx.reply(embed=embed)
                elif result is not None:
                    sql = ("UPDATE main SET bot_channel_id = ? WHERE guild_id = ?")
                    val = (channel.id, ctx.guild.id)
                    await ctx.reply(embed=embed)
                    

                    
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
            else:
                embed_error=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Bots has already been setup!'
                )
                
                await ctx.reply(embed=embed_error)
        else:
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
    
    @server_info.command()
    async def disable_bots(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT bot_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
            if result != None:
                if result[0] != None:
                    channel = self.client.get_channel(int(result[0]))
                else:
                    channel = None
                
            else:
                channel = None
            
            if channel != None:
            
                embed=nextcord.Embed(
                    title="Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Bots has been disabled!'
                )
                
                embed.timestamp = datetime.now()
                    

                channel = self.client.get_channel(int(result[0]))
        
                channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
                
                
                
                
                
                await channel.delete()
                all_channels = channel_category.channels
                if len(all_channels) == 0:
                    await channel_category.delete()
                
                await ctx.reply(embed=embed)
            else:
                embed_error_disable=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description="This feature is already disabled!"
                )
                        
                embed_error_disable.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_disable)   
        else:
            embed_error_perms=nextcord.Embed(
                title="Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
        


    
    
    
    @tasks.loop(hours=1)
    async def refresh(self):
        for guild in self.client.guilds:
            db = sqlite3.connect('server_info.sqlite')
            cursor_member = db.cursor()
            cursor_member.execute(f"SELECT member_channel_id FROM main WHERE guild_id = {guild.id}")
            result_member = cursor_member.fetchone()
            
            cursor_bot = db.cursor()
            cursor_bot.execute(f"SELECT bot_channel_id FROM main WHERE guild_id = {guild.id}")
            result_bot = cursor_bot.fetchone()
            
            
            channel_member = self.client.get_channel(int(result_member[0]))
            channel_bot = self.client.get_channel(int(result_bot[0]))
            
            if channel_bot != None:
                members = guild.members
                bot_count = 0
                for i in members:
                    member = i.bot
                    if member == True:
                        bot_count += 1
                await channel_bot.edit(name=f"Bots: {bot_count}")
                
            if channel_member != None:
                await channel_member.edit(name=f"Members: {guild.member_count}")
                
    

    
        
        
def setup(client):
    client.add_cog(server_info(client))
        