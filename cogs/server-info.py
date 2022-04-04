from code import interact
import imp
from unicodedata import name
import nextcord
from nextcord.ext import commands, tasks
from datetime import datetime
import sqlite3
from nextcord.utils import get
import roblox
import asyncio
roblox_client = roblox.Client()




class server_info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.refresh.start()
        
    @commands.group(invoke_without_command=True)
    async def server_info(self, ctx):
        embed=nextcord.Embed(
            title="Server Info",
            colour= nextcord.Colour.blurple(),
            description="Available Setup Commands: \n`m!server_info setup_members`\n`m!server_info disable_members`\n`m!server_info setup_bots`\n`m!server_info disable_bots`\n`m!server_info setup_game <UniverseId>`\n`m!server_info disable_game`",
            
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
            
            cursor_game_channel = db.cursor()
            cursor_game_channel.execute(f"SELECT game_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_game_channel = cursor_game_channel.fetchone()

            cursor_group = db.cursor()
            cursor_group.execute(f"SELECT group_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_group = cursor_group.fetchone()
            
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
                            
                if result_bot is None and result_game_channel is None and result_group is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else:
                    bot_found = True
                    game_found = True
                    group_found = False
                    
                    if result_bot[0] is None:
                        bot_found = False
                    else:
                        if self.client.get_channel(int(result_bot[0])) != None:
                            category = self.client.get_channel(int(result_bot[0]))
                        else:
                            bot_found = False
                            
                    if result_group[0] is None:
                        group_found = False
                    else:
                        if self.client.get_channel(int(result_group[0])) != None:
                            category = self.client.get_channel(int(result_group[0])).category
                        else:
                            group_found = False 
                    
                    if result_game_channel[0] is None:
                        game_found = False
                    else:
                        if self.client.get_channel(int(result_game_channel[0])) != None:
                            category = self.client.get_channel(int(result_game_channel[0])).category
                        else:
                            game_found = False
                        
                    if game_found != True and bot_found != True and group_found != True:
                        category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                    
                    
                    # if result_bot[0] != None or result_game_channel[0] != None:
                    #     if self.client.get_channel(int(result_bot[0])) is None and self.client.get_channel(int(result_game_channel[0])) is None:
                    #         category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                    #     elif self.client.get_channel(int(result_bot[0])) != None:
                    #         category = self.client.get_channel(int(result_bot[0])).category
                    #     elif self.client.get_channel(int(result_game_channel[0])) != None:
                    #         category = self.client.get_channel(int(result_game_channel[0])).categor
                    # else:
                    #     category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                
                
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

            cursor_game_channel = db.cursor()
            cursor_game_channel.execute(f"SELECT game_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_game_channel = cursor_game_channel.fetchone()

            cursor_group = db.cursor()
            cursor_group.execute(f"SELECT group_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_group = cursor_group.fetchone()

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
                
                if result_member is None and result_game_channel is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else:
                    member_found = True
                    game_found = True
                    group_found = True
                    
                    if result_member[0] is None:
                        member_found = False
                    else:
                        if self.client.get_channel(int(result_member[0])) != None:
                            category = self.client.get_channel(int(result_member[0]))
                            
                        else:
                            member_found = False
                            
                    if result_group[0] is None:
                        group_found = False
                    else:
                        if self.client.get_channel(int(result_group[0])) != None:
                            category = self.client.get_channel(int(result_group[0])).category
                        else:
                            group_found = False 
                    
                    
                    if result_game_channel[0] is None:
                        game_found = False
                    else:
                        if self.client.get_channel(int(result_game_channel[0])) != None:
                            category = self.client.get_channel(int(result_game_channel[0])).category
                        else:
                            game_found = False
                            
                    if game_found != True and member_found != True and group_found != True:
                        category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                    
                        
                    
                    # if result_member[0] != None or result_game_channel[0] != None:
                        
                    #     if self.client.get_channel(int(result_member[0])) is None and self.client.get_channel(int(result_game_channel[0])) is None:
                    #         category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                    #     elif self.client.get_channel(int(result_member[0])) != None:
                    #         category = self.client.get_channel(int(result_member[0])).category
                    #     elif self.client.get_channel(int(result_game_channel[0])) != None:
                    #         category = self.client.get_channel(int(result_game_channel[0])).category
                    # else:
                    #     category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                
                

                
                
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
            
            
            
            
            
            
    @server_info.command()
    async def setup_game(self, ctx,*, id:int):
        if ctx.author.guild_permissions.administrator:
            try:
                universe = await roblox_client.get_universe(id)
                
            except:
                embed_error_none=nextcord.Embed(
                    title="Error",
                    colour= nextcord.Colour.red(),
                    description="No experience found! Make sure it is the `ExperienceId` and not the `PlaceId`!"
                )
                        
                embed_error_none.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_none)
                return
            
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT game_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            
            cursor_game_id = db.cursor()
            cursor_game_id.execute(f"SELECT game_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_game_id = cursor_game_id.fetchone()
            
            cursor_group = db.cursor()
            cursor_group.execute(f"SELECT group_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_group = cursor_group.fetchone()
            
            cursor_member = db.cursor()
            cursor_member.execute(f"SELECT member_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_member = cursor_member.fetchone()
            
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
                    description=f'Server Info Bot Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                
                if result_member is None and result_bot is None and result_group is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else:
                    member_found = True
                    bot_found = True
                    group_found = True
                    if result_member is None:
                        member_found = False
                    else:             
                        if self.client.get_channel(int(result_member[0])) != None:
                            category = self.client.get_channel(int(result_member[0]))
                        else:
                            member_found = False
                         
                    if result_group[0] is None:
                        group_found = False
                    else:
                        if self.client.get_channel(int(result_group[0])) != None:
                            category = self.client.get_channel(int(result_group[0])).category
                        else:
                            group_found = False  
                            
                    if result_bot[0] is None:
                        bot_found = False
                    else:
                        if self.client.get_channel(int(result_bot[0])) != None:
                            category = self.client.get_channel(int(result_bot[0])).category
                        else:
                            bot_found = False
                            
                        
                    if bot_found != True and member_found != True and group_found != True:
                        category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                
                
                game_info = universe.playing
                
                
                channel = await ctx.guild.create_voice_channel(name=f"Players: {game_info}", category=category)
                
                if result is None:
                    sql = ("INSERT INTO main(guild_id, game_channel_id) VALUES(?,?)")
                    val = (ctx.guild.id, channel.id)
                    
                    
                    await ctx.reply(embed=embed)
                elif result is not None:
                    sql = ("UPDATE main SET game_channel_id = ? WHERE guild_id = ?")
                    val = (channel.id, ctx.guild.id)

                    
                    await ctx.reply(embed=embed)
                    
                    
                sql_id = ("UPDATE main SET game_id = ? WHERE guild_id = ?")
                val_id = (str(id), ctx.guild.id)
                    

                    
                cursor.execute(sql, val)
                cursor_game_id.execute(sql_id, val_id)
                db.commit()
                cursor.close()
                cursor_game_id.close()
                db.close()
            else:
                embed_error=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Game Players has already been setup!'
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
    async def disable_game(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT game_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
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
                    description=f'Server Info Game Players has been disabled!'
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
            
            
            
    @server_info.command()
    async def setup_group(self, ctx,*, id:int):
        if ctx.author.guild_permissions.administrator:
            try:
                group = await roblox_client.get_group(id)
                
            except:
                embed_error_none=nextcord.Embed(
                    title="Error",
                    colour= nextcord.Colour.red(),
                    description="No group found! Make sure it is the group id!"
                )
                        
                embed_error_none.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_none)
                return
            
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT group_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            

            cursor_game_channel = db.cursor()
            cursor_game_channel.execute(f"SELECT game_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_game_channel = cursor_game_channel.fetchone()
            
            cursor_game_id = db.cursor()
            cursor_game_id.execute(f"SELECT game_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_game_id = cursor_game_id.fetchone()
            
            cursor_member = db.cursor()
            cursor_member.execute(f"SELECT member_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result_member = cursor_member.fetchone()
            
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
                    description=f'Server Info Group Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                
                if result_member is None and result_bot is None and result_game_channel is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else:
                    member_found = True
                    game_found = True
                    bot_found = True
                    
                    
                    
                    if result_member is None:
                        member_found = False
                    else:             
                        if self.client.get_channel(int(result_member[0])) != None:
                            category = self.client.get_channel(int(result_member[0]))
                        else:
                            member_found = False
                            
                    if result_game_channel is None:
                        game_found = False
                    else:             
                        if self.client.get_channel(int(result_game_channel[0])) != None:
                            category = self.client.get_channel(int(result_game_channel[0]))
                        else:
                            game_found = False
                            
                            
                    if result_bot[0] is None:
                        bot_found = False
                    else:
                        if self.client.get_channel(int(result_bot[0])) != None:
                            category = self.client.get_channel(int(result_bot[0])).category
                        else:
                            bot_found = False
                            
                        
                    if bot_found != True and member_found != True and game_found != True:
                        category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                
                
                group_members = group.member_count
                
                
                channel = await ctx.guild.create_voice_channel(name=f"Group: {group_members}", category=category)
                
                if result is None:
                    sql = ("INSERT INTO main(guild_id, group_channel_id) VALUES(?,?)")
                    val = (ctx.guild.id, channel.id)
                    
                    
                    await ctx.reply(embed=embed)
                elif result is not None:
                    sql = ("UPDATE main SET group_channel_id = ? WHERE guild_id = ?")
                    val = (channel.id, ctx.guild.id)

                    
                    await ctx.reply(embed=embed)
                    
                    
                sql_id = ("UPDATE main SET group_id = ? WHERE guild_id = ?")
                val_id = (str(id), ctx.guild.id)
                    

                    
                cursor.execute(sql, val)
                cursor_game_id.execute(sql_id, val_id)
                db.commit()
                cursor.close()
                cursor_game_id.close()
                db.close()
            else:
                embed_error=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Group Members has already been setup!'
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
    async def disable_group(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('server_info.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT group_channel_id FROM main WHERE guild_id = {ctx.guild.id}")
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
                    description=f'Server Info Group Members has been disabled!'
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
            
            cursor_game_channel = db.cursor()
            cursor_game_channel.execute(f"SELECT game_channel_id FROM main WHERE guild_id = {guild.id}")
            result_game_channel = cursor_game_channel.fetchone()
            
            cursor_game_id = db.cursor()
            cursor_game_id.execute(f"SELECT game_id FROM main WHERE guild_id = {guild.id}")
            result_game_id = cursor_game_id.fetchone()
            
            cursor_group = db.cursor()
            cursor_group.execute(f"SELECT group_channel_id FROM main WHERE guild_id = {guild.id}")
            result_group = cursor_group.fetchone()
            
            cursor_group_id = db.cursor()
            cursor_group_id.execute(f"SELECT group_id FROM main WHERE guild_id = {guild.id}")
            result_group_id = cursor_group_id.fetchone()
            
            if result_member != None:
                if result_member[0] != None:
                    channel_member = self.client.get_channel(int(result_member[0]))
                else:
                    channel_member = None
            else:
                channel_member = None
                
            if result_bot != None:
                if result_bot[0] != None:
                    channel_bot = self.client.get_channel(int(result_bot[0]))
                else:
                    channel_bot = None
            else:
                channel_bot = None
                
            if result_game_channel != None:
                if result_game_channel[0] != None:
                    channel_game = self.client.get_channel(int(result_game_channel[0]))
                else:
                    channel_game = None
            else:
                channel_game = None
                
            if result_group != None:
                if result_group[0] != None:
                    channel_group = self.client.get_channel(int(result_group[0]))
                else:
                    channel_group = None
            else:
                channel_group = None
            
            if channel_bot != None:
                members = guild.members
                bot_count = 0
                for i in members:
                    member = i.bot
                    if member == True:
                        bot_count += 1
                        
                bot_text_split = channel_bot.name.split(": ")
                
                if int(bot_text_split[1]) != bot_count:
                    await channel_bot.edit(name=f"Bots: {bot_count}")
                
            if channel_member != None:
                member_text_split = channel_member.name.split(": ")
                
                if int(member_text_split[1]) != guild.member_count:
                    await channel_member.edit(name=f"Members: {guild.member_count}")
            if channel_game != None:
                universe = await roblox_client.get_universe(int(result_game_id[0]))
                
                text_split = channel_game.name.split(": ")
                
                
                if int(universe.playing) != int(text_split[1]):
                    await channel_game.edit(name=f"Players: {universe.playing}")
            
            if channel_group != None:
                
                
                group = await roblox_client.get_group(int(result_group_id[0]))
                
                text_split_group = channel_group.name.split(": ")
                
                if group.get_members != int(text_split_group[1]):
                    await channel_group.edit(fname="Group: {group.get_members}")
                    
            
                
            
                
    

    
        
        
def setup(client):
    client.add_cog(server_info(client))
        