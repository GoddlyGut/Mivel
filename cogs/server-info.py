from code import interact
from unicodedata import name
import nextcord
from nextcord.ext import commands, tasks
from datetime import datetime
from nextcord.utils import get
import roblox
roblox_client = roblox.Client()
import pymongo
from pymongo import MongoClient




class server_info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.refresh.start()
        
    @commands.group(invoke_without_command=True)
    async def server_info(self, ctx):
        embed=nextcord.Embed(
            title="Server Info",
            colour= nextcord.Colour.blurple(),
            description="Available Setup Commands: \n`m!server_info setup_members`\n`m!server_info disable_members`\n`m!server_info setup_bots`\n`m!server_info disable_bots`\n`m!server_info setup_game <UniverseId>`\n`m!server_info disable_game`\n`m!server_info setup_group <GroupId>`\n`m!server_info disable_group`",
            
        )      
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    
    
    @server_info.command()
    async def setup_members(self, ctx):
        if ctx.author.guild_permissions.administrator:
            
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            
            member_channel = None
            bot_channel = None
            game_channel = None
            group_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                
            if member_channel is None:
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                 
                if bot_channel is None and game_channel is None and group_channel is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else: 
                    if bot_channel != None:
                        category = self.client.get_channel(bot_channel).category
                        
                    if game_channel != None:
                        category = self.client.get_channel(game_channel).category
                        
                    if group_channel != None:
                        category = self.client.get_channel(group_channel).category
                        
                        
                channel = await ctx.guild.create_voice_channel(name=f"Members: {ctx.guild.member_count}", category=category)
                
                channel_info = {"_id":ctx.guild.id, "member_channel":channel.id, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None}
                
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"member_channel":channel.id}})
                    
                embed=nextcord.Embed(
                    title="Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Member Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
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
    @setup_members.error
    async def members_error(self,ctx, error):
        embed=nextcord.Embed(
            title="Error",
            colour= nextcord.Colour.red(),
            description=error
        )
                    
        embed.timestamp = datetime.now()
        
        await ctx.reply(embed=embed)
            
            
            
    @server_info.command()
    async def disable_members(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            
            member_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                
            if member_channel is None:
                embed_error_disable=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description="This feature is already disabled!"
                )
                        
                embed_error_disable.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_disable)
            else:
                channel = self.client.get_channel(member_channel)
                channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
                await channel.delete()
                all_channels = channel_category.channels
                if len(all_channels) == 0:
                    await channel_category.delete()
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None}   
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"member_channel":None}})
                
                embed=nextcord.Embed(
                    title="Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Members has been disabled!'
                )
                
                embed.timestamp = datetime.now()    
                
                await ctx.reply(embed=embed)
            
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
            
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            
            member_channel = None
            bot_channel = None
            game_channel = None
            group_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                
            if bot_channel is None:
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                 
                if member_channel is None and game_channel is None and group_channel is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else: 
                    if member_channel != None:
                        category = self.client.get_channel(member_channel).category
                        
                    if game_channel != None:
                        category = self.client.get_channel(game_channel).category
                        
                    if group_channel != None:
                        category = self.client.get_channel(group_channel).category
                        
                        
                members = ctx.guild.members
                bot_count = 0
                for i in members:
                    member = i.bot
                    if member == True:
                        bot_count += 1
                
                channel = await ctx.guild.create_voice_channel(name=f"Bots: {bot_count}", category=category)
                
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":channel.id,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None}
                
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"bot_channel":channel.id}})
                    
                embed=nextcord.Embed(
                    title="Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Bot Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
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
            
    @setup_bots.error
    async def bots_error(self,ctx, error):
        embed=nextcord.Embed(
            title="Error",
            colour= nextcord.Colour.red(),
            description=error
        )
                    
        embed.timestamp = datetime.now()
        
        await ctx.reply(embed=embed)
            

    @server_info.command()
    async def disable_bots(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            
            bot_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                
            if bot_channel is None:
                embed_error_disable=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description="This feature is already disabled!"
                )
                        
                embed_error_disable.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_disable)
            else:
                channel = self.client.get_channel(bot_channel)
                channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
                await channel.delete()
                all_channels = channel_category.channels
                if len(all_channels) == 0:
                    await channel_category.delete()
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None}   
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"bot_channel":None}})
                
                embed=nextcord.Embed(
                    title="Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Bots has been disabled!'
                )
                
                embed.timestamp = datetime.now()    
                
                await ctx.reply(embed=embed)
            
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
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            
            member_channel = None
            bot_channel = None
            game_channel = None
            group_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                
            if game_channel is None:
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                 
                if member_channel is None and bot_channel is None and group_channel is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else: 
                    if member_channel != None:
                        category = self.client.get_channel(member_channel).category
                        
                    if bot_channel != None:
                        category = self.client.get_channel(bot_channel).category
                        
                    if group_channel != None:
                        category = self.client.get_channel(group_channel).category
                        
                        

                game_info = universe.playing
                channel = await ctx.guild.create_voice_channel(name=f"Players: {game_info}", category=category)
                
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":channel.id,"game_id":id,"group_channel":None, "group_id":None}
                
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_channel":channel.id}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_id":id}})
                    
                embed=nextcord.Embed(
                    title="Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Game Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
            else:
                embed_error=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Game has already been setup!'
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
    @setup_game.error
    async def game_error(self,ctx, error):
        embed=nextcord.Embed(
            title="Error",
            colour= nextcord.Colour.red(),
            description=error
        )
                    
        embed.timestamp = datetime.now()
        
        await ctx.reply(embed=embed)
            
            
    @server_info.command()
    async def disable_game(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            
            game_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                
            if game_channel is None:
                embed_error_disable=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description="This feature is already disabled!"
                )
                        
                embed_error_disable.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_disable)
            else:
                channel = self.client.get_channel(game_channel)
                channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
                await channel.delete()
                all_channels = channel_category.channels
                if len(all_channels) == 0:
                    await channel_category.delete()
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None}   
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_channel":None}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_id":None}})
                
                embed=nextcord.Embed(
                    title="Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Game has been disabled!'
                )
                
                embed.timestamp = datetime.now()    
                
                await ctx.reply(embed=embed)
            
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
                    description="No group found! Make sure it is the `GroupId`!"
                )
                        
                embed_error_none.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_none)
                return
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            
            member_channel = None
            bot_channel = None
            game_channel = None
            group_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                
            if group_channel is None:
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                 
                if member_channel is None and bot_channel is None and game_channel is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else: 
                    if member_channel != None:
                        category = self.client.get_channel(member_channel).category
                        
                    if bot_channel != None:
                        category = self.client.get_channel(bot_channel).category
                        
                    if game_channel != None:
                        category = self.client.get_channel(game_channel).category
                        
                        

                group_info = group.member_count
                channel = await ctx.guild.create_voice_channel(name=f"Group: {group_info}", category=category)
                
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":channel.id, "group_id":id}
                
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"group_channel":channel.id}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"group_id":id}})
                    
                embed=nextcord.Embed(
                    title="Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Group Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
            else:
                embed_error=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Group has already been setup!'
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
            
    @setup_group.error
    async def group_error(self,ctx, error):
        embed=nextcord.Embed(
            title="Error",
            colour= nextcord.Colour.red(),
            description=error
        )
                    
        embed.timestamp = datetime.now()
        
        await ctx.reply(embed=embed)
            
    @server_info.command()
    async def disable_group(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            
            group_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                
            if group_channel is None:
                embed_error_disable=nextcord.Embed(
                    title="Server Info Error",
                    colour= nextcord.Colour.red(),
                    description="This feature is already disabled!"
                )
                        
                embed_error_disable.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_disable)
            else:
                channel = self.client.get_channel(group_channel)
                channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
                await channel.delete()
                all_channels = channel_category.channels
                if len(all_channels) == 0:
                    await channel_category.delete()
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None}   
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"group_channel":None}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"group_id":None}})
                
                embed=nextcord.Embed(
                    title="Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Group has been disabled!'
                )
                
                embed.timestamp = datetime.now()    
                
                await ctx.reply(embed=embed)
            
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
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            
            member_channel = None
            bot_channel = None
            game_channel = None
            group_channel = None
            
            for x in collection.find({"_id": guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                game_id = x["game_id"]
                group_channel = x["group_channel"]
                group_id = x["group_id"]
            
            if member_channel != None:
                channel_member = self.client.get_channel(member_channel)
            else:
                channel_member = None

            if bot_channel != None:
                channel_bot = self.client.get_channel(bot_channel)
            else:
                channel_bot = None
                
            if game_channel != None:
                channel_game = self.client.get_channel(game_channel)
            else:
                channel_game = None
                
            if group_channel != None:
                channel_group = self.client.get_channel(group_channel)
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
                universe = await roblox_client.get_universe(game_id)
                
                text_split = channel_game.name.split(": ")

                if int(universe.playing) != int(text_split[1]):
                    await channel_game.edit(name=f"Players: {universe.playing}")
            
            if channel_group != None:

                group = await roblox_client.get_group(group_id)
                
                text_split_group = channel_group.name.split(": ")
                
                if group.get_members != int(text_split_group[1]):
                    await channel_group.edit(name=f"Group: {group.get_members}")
                    
            
                
            
                
    

    
        
        
def setup(client):
    client.add_cog(server_info(client))
        