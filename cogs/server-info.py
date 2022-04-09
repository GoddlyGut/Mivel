import nextcord
from nextcord.ui import Button, View
from nextcord import Interaction
from nextcord.ext import commands, tasks
from datetime import datetime
from nextcord.utils import get
import roblox
<<<<<<< HEAD
import asyncio
=======

from cogs.buttons import Subscriptions

>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
roblox_client = roblox.Client("6E2C0CF7F4F7E2DCB1709C167EF155C4DCF29DCA9D9F2B91D9908D28B091941597004A87F31D06522D8BFAE02550F523549B290EEA74A2BB0FC9DC47B5818FA1625230B9C2D3F5C51DE9353670E1F5C34FE6D30A61E28EA6E4E7207C75D3BBBDA2956AAF252624EB2FAABA55F0986971AD106E8132ACCBB3C233F003B44BD55EEC52AE97843AD825B527BF29EA849115F7EFE9C3AEE89901BBE7CEB312FED484D9F633882C03111A6757E44C887845291CB3EB639ACFFD6CAE46554B76C8901A290C1BB20A11446C283C2145C3A2DC428399E5B4C6FA1E96331F9058B662734CD7254223304A56115A26216B1292216888383DED91236A6EAE291D85B7D6BA1AE020344B645A83D8C52B691FA3E82415794C4C9C198A97BAFFEE4733A6ECFCE8ED17296E455E7FBE10A5144555023E6BBA36708047CAEC2E016B4369CBFC9B54E333C2F4C27202F0F009A2EB51F6FAE5845F12CE1F3FF20AAC885B8BAD8D16AD473E9A3F")
import pymongo
from pymongo import MongoClient




class server_info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.refresh.start()
        
    @commands.group(invoke_without_command=True)
    async def stats(self, ctx):
        embed=nextcord.Embed(
            title="📦 Available Setup Commands:",
            colour= nextcord.Colour.blurple(),
<<<<<<< HEAD
            description="```m!stats setup_members```**Setup stats for server members**\n```m!stats disable_members```**Disable stats for server members**\n```m!stats setup_bots```**Setup stats for server bots**\n```m!stats disable_bots```**Disable stats for server bots**\n```m!stats setup_game```**Setup stats for a roblox game**\n```m!stats disable_game```**Disable stats for a roblox game**\n```m!stats setup_group```**Setup stats for a roblox group**\n```m!stats disable_group```**Disable stats for a roblox group**\n```m!stats setup_favorites```**Setup stats for a roblox game favorite count**\n```m!stats disable_favorites```**Disable stats for a roblox game favorite count**\n\n```m!stats return_game```**Returns the current tracked game**\n```m!stats return_group```**Returns the current tracked group**\n```m!stats return_favorites```**Returns the current tracked games favorite count**",
=======
            description="`m!stats setup_members`-**Setup stats for server members**\n`m!stats disable_members`-**Disable stats for server members**\n`m!stats setup_bots`-**Setup stats for server bots**\n`m!stats disable_bots`-**Disable stats for server bots**\n`m!stats setup_game <PlaceId>`-**Setup stats for a roblox game**\n`m!stats disable_game`-**Disable stats for a roblox game**\n`m!stats setup_group <GroupId>`-**Setup stats for a roblox group**\n`m!stats disable_group`-**Disable stats for a roblox group**\n`m!stats setup_favorites <PlaceId>`-**Setup stats for a roblox game favorite count**\n`m!stats disable_favorites`-**Disable stats for a roblox game favorite count**\n\n`m!stats return_game`-**Returns the current tracked game**\n`m!stats return_group`-**Returns the current tracked group**\n`m!stats return_favorite`-**Returns the current tracked games favorite count**",
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
            
        )      
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

    
    
    
    @stats.command()
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
            game_favorite_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                game_favorite_channel = x["game_favorite_channel"]
                
            if member_channel is None:
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                 
                if bot_channel is None and game_channel is None and group_channel is None and game_favorite_channel is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else: 
                    if bot_channel != None:
                        category = self.client.get_channel(bot_channel).category
                        
                    if game_channel != None:
                        category = self.client.get_channel(game_channel).category
                        
                    if group_channel != None:
                        category = self.client.get_channel(group_channel).category
                        
                    if game_favorite_channel != None:
                        category = self.client.get_channel(game_favorite_channel).category
                        
                        
                channel = await ctx.guild.create_voice_channel(name=f"Members: {ctx.guild.member_count}", category=category)
                
                channel_info = {"_id":ctx.guild.id, "member_channel":channel.id, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None, "game_favorite_channel":None,"game_favorite_id":None}
                
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"member_channel":channel.id}})
                    
                embed=nextcord.Embed(
                    title="✅ Server Info Updated",
                    colour= nextcord.Colour.green(),
                    description=f'Server Info Member Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
            else:
                embed_error=nextcord.Embed(
                    title="❌ Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Members has already been setup!'
                )
                
                await ctx.reply(embed=embed_error)
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)

            
            
            
    @stats.command()
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
                    title="❌ Server Info Error",
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
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None, "game_favorite_channel":None,"game_favorite_id":None}   
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"member_channel":None}})
                
                embed=nextcord.Embed(
                    title="✅ Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Members has been disabled!'
                )
                
                embed.timestamp = datetime.now()    
                
                await ctx.reply(embed=embed)
            
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
            
    @stats.command()
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
            game_favorite_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                game_favorite_channel = x["game_favorite_channel"]
                
            if bot_channel is None:
                overwrites={
                    ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                }
                 
                if member_channel is None and game_channel is None and group_channel is None and game_favorite_channel is None:    
                    category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                else: 
                    if member_channel != None:
                        category = self.client.get_channel(member_channel).category
                        
                    if game_channel != None:
                        category = self.client.get_channel(game_channel).category
                        
                    if group_channel != None:
                        category = self.client.get_channel(group_channel).category
                        
                    if game_favorite_channel != None:
                        category = self.client.get_channel(game_favorite_channel).category
                    
                        
                        
                members = ctx.guild.members
                bot_count = 0
                for i in members:
                    member = i.bot
                    if member == True:
                        bot_count += 1
                
                channel = await ctx.guild.create_voice_channel(name=f"Bots: {bot_count}", category=category)
                
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":channel.id,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None, "game_favorite_channel":None,"game_favorite_id":None}
                
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"bot_channel":channel.id}})
                    
                embed=nextcord.Embed(
                    title="✅ Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Bot Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
            else:
                embed_error=nextcord.Embed(
                    title="❌ Server Info Error",
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
            


    @stats.command()
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
                game_favorite_channel = x["game_favorite_channel"]
                
            if bot_channel is None:
                embed_error_disable=nextcord.Embed(
                    title="❌ Server Info Error",
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
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None, "game_favorite_channel":None,"game_favorite_id":None}   
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"bot_channel":None}})
                
                embed=nextcord.Embed(
                    title="✅ Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Bots has been disabled!'
                )
                
                embed.timestamp = datetime.now()    
                
                await ctx.reply(embed=embed)
            
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
            
            
    @stats.command()
<<<<<<< HEAD
    async def setup_game(self, ctx):
        if ctx.author.guild_permissions.administrator:
=======
    async def setup_game(self, ctx,*, id:int):
        if ctx.author.guild_permissions.administrator:
            try:
                place = await roblox_client.get_place(id)


            except:
                embed_error_none=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description="No place found! Make sure it is the `PlaceId`!"
                )
                        
                embed_error_none.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_none)
                return
            
            universe = await roblox_client.get_universe(place.universe.id)
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd

            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
                    
            member_channel = None
            bot_channel = None
            game_channel = None
            group_channel = None
            game_favorite_channel = None
            
            embed_setup_game= nextcord.Embed(
                title="" ,  
                colour=nextcord.Colour.blurple(),
                description=f"Please enter a `PlaceId` to setup this feature!"
            )

            embed_setup_game.timestamp = datetime.now()

            await ctx.send(embed=embed_setup_game)

            def check(m):
                return ctx.author == m.author

            while True:
                try:
                    msg = await self.client.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    embed_error_time = nextcord.Embed(
                        title="❌ Verification Error",
                        colour=nextcord.Colour.red(),
                        description=f"Your time has ran out!"
                    )

                    embed_error_time.timestamp = datetime.now()

                    await ctx.send(embed=embed_error_time)

                    break

                if msg and msg.author != "Mivel":
                    try:
                        place = await roblox_client.get_place(int(msg.content))
                    except:
                        embed_error_none=nextcord.Embed(
                            title="❌ Error",
                            colour= nextcord.Colour.red(),
                            description="No place found! Make sure it is the `PlaceId`!"
                        )
                                
                        embed_error_none.timestamp = datetime.now()
                        
                        await ctx.reply(embed=embed_error_none)
                        break

                    universe = await roblox_client.get_universe(place.universe.id)

                    embed_loading=nextcord.Embed(
                        title="",
                        colour= nextcord.Colour.blurple(),
                        description=f'🔎 Retrieving Game Data...'
                    )

                    message_temp = await ctx.reply(embed=embed_loading)
                    
                    for x in collection.find({"_id": ctx.guild.id}):
                        member_channel = x["member_channel"]
                        bot_channel = x["bot_channel"]
                        game_channel = x["game_channel"]
                        group_channel = x["group_channel"]
                        game_favorite_channel = x["game_favorite_channel"]
                        
                    if game_channel is None:
                        overwrites={
                            ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                        }
                        
                        if member_channel is None and bot_channel is None and group_channel is None and game_favorite_channel is None:    
                            category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                        else: 
                            if member_channel != None:
                                category = self.client.get_channel(member_channel).category
                                
                            if bot_channel != None:
                                category = self.client.get_channel(bot_channel).category
                                
                            if group_channel != None:
                                category = self.client.get_channel(group_channel).category
                            
                            if game_favorite_channel != None:
                                category = self.client.get_channel(game_favorite_channel).category
                                
                                

<<<<<<< HEAD
                        game_info = universe.playing
                        channel = await ctx.guild.create_voice_channel(name=f"Players: {game_info}", category=category)
                        
                        channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":channel.id,"game_id":int(msg.content),"group_channel":None, "group_id":None, "game_favorite_channel":None,"game_favorite_id":None}
                        
                        try:
                            collection.insert_one(channel_info)
                        except:
                            collection.update({"_id":ctx.guild.id},{"$set":{"game_channel":channel.id}})
                            collection.update({"_id":ctx.guild.id},{"$set":{"game_id":int(msg.content)}})
                            
                        await message_temp.delete()
                        
                        embed=nextcord.Embed(
                            title="✅ Server Info Updated",
                            colour= nextcord.Colour.blurple(),
                            description=f'Server Info Game Channel Created! **Now tracking {place.name}!** For more info on this game, run the command `m!stats return_game`! Note that the channel updates every 30 minutes.'
                        )
                        
                        embed.timestamp = datetime.now()
                        
                        await ctx.reply(embed=embed)

                        break
                    else:
                        embed_error=nextcord.Embed(
                            title="❌ Server Info Error",
                            colour= nextcord.Colour.red(),
                            description=f'Server Info Game has already been setup!'
                        )
                        
                        await ctx.reply(embed=embed_error)

                        break
                            
=======
                game_info = universe.playing
                channel = await ctx.guild.create_voice_channel(name=f"Players: {game_info}", category=category)
                
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":channel.id,"game_id":id,"group_channel":None, "group_id":None, "game_favorite_channel":None,"game_favorite_id":None}
                
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_channel":channel.id}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_id":id}})
                    
                embed=nextcord.Embed(
                    title="✅ Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Game Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
            else:
                embed_error=nextcord.Embed(
                    title="❌ Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Game has already been setup!'
                )
                
                await ctx.reply(embed=embed_error)
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)

            
            
    @stats.command()
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
                    title="❌ Server Info Error",
                    colour= nextcord.Colour.red(),
                    description="This feature is already disabled!"
                )
                        
                embed_error_disable.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_disable)
            else:
                embed_loading=nextcord.Embed(
                    title="",
                    colour= nextcord.Colour.blurple(),
                    description=f'🗑️ Caching Data...'
                )

                message_temp = await ctx.reply(embed=embed_loading)

                channel = self.client.get_channel(game_channel)
                channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
                await channel.delete()
                all_channels = channel_category.channels
                if len(all_channels) == 0:
                    await channel_category.delete()
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None, "game_favorite_channel":None,"game_favorite_id":None}   
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_channel":None}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_id":None}})
                
                await message_temp.delete()

                embed=nextcord.Embed(
                    title="✅ Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Game has been disabled!'
                )
                
                embed.timestamp = datetime.now()    
                
                await ctx.reply(embed=embed)
            
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
    
            
<<<<<<< HEAD
    @stats.command()
    async def setup_group(self, ctx):
        if ctx.author.guild_permissions.administrator:

=======

    
    
    @stats.command()
    async def setup_group(self, ctx,*, id:int):
        if ctx.author.guild_permissions.administrator:
            try:
                group = await roblox_client.get_group(id)
                
            except:
                embed_error_none=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description="No group found! Make sure it is the `GroupId`!"
                )
                        
                embed_error_none.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_none)
                return
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
                    
            member_channel = None
            bot_channel = None
            game_channel = None
            group_channel = None
            game_favorite_channel = None
            
            embed_setup_game= nextcord.Embed(
                title="" ,  
                colour=nextcord.Colour.blurple(),
                description=f"Please enter a `GroupId` to setup this feature!"
            )

            embed_setup_game.timestamp = datetime.now()

            await ctx.send(embed=embed_setup_game)

            def check(m):
                return ctx.author == m.author

            while True:
                try:
                    msg = await self.client.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    embed_error_time = nextcord.Embed(
                        title="❌ Verification Error",
                        colour=nextcord.Colour.red(),
                        description=f"Your time has ran out!"
                    )

                    embed_error_time.timestamp = datetime.now()

                    await ctx.send(embed=embed_error_time)

                    break

                if msg and msg.author != "Mivel":
                    try:
                        group = await roblox_client.get_group(int(msg.content))
                    except:
                        embed_error_none=nextcord.Embed(
                            title="❌ Error",
                            colour= nextcord.Colour.red(),
                            description="No group found! Make sure it is the `GroupId`!"
                        )
                                
                        embed_error_none.timestamp = datetime.now()
                        
                        await ctx.reply(embed=embed_error_none)
                        break



                    embed_loading=nextcord.Embed(
                        title="",
                        colour= nextcord.Colour.blurple(),
                        description=f'🔎 Retrieving Group Data...'
                    )

                    message_temp = await ctx.reply(embed=embed_loading)
                    
                    for x in collection.find({"_id": ctx.guild.id}):
                        member_channel = x["member_channel"]
                        bot_channel = x["bot_channel"]
                        game_channel = x["game_channel"]
                        group_channel = x["group_channel"]
                        game_favorite_channel = x["game_favorite_channel"]
                        
                    if group_channel is None:
                        overwrites={
                            ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                        }
                        
                        if member_channel is None and bot_channel is None and game_channel is None and game_favorite_channel is None:    
                            category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                        else: 
                            if member_channel != None:
                                category = self.client.get_channel(member_channel).category
                                
                            if bot_channel != None:
                                category = self.client.get_channel(bot_channel).category
                                
                            if game_channel != None:
                                category = self.client.get_channel(game_channel).category
                            
                            if game_favorite_channel != None:
                                category = self.client.get_channel(game_favorite_channel).category
                                
                                

                        group_info = group.member_count
                        channel = await ctx.guild.create_voice_channel(name=f"Group: {group.member_count}", category=category)
                        
                        channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":channel.id, "group_id":group.id, "game_favorite_channel":None,"game_favorite_id":None}
                        
                        try:
                            collection.insert_one(channel_info)
                        except:
                            collection.update({"_id":ctx.guild.id},{"$set":{"group_channel":channel.id}})
                            collection.update({"_id":ctx.guild.id},{"$set":{"group_id":group.id}})
                            
                        await message_temp.delete()
                        
                        embed=nextcord.Embed(
                            title="✅ Server Info Updated",
                            colour= nextcord.Colour.blurple(),
                            description=f'Server Info Group Channel Created! **Now tracking {group.name}!** For more info on this group, run the command `m!stats return_group`! Note that the channel updates every 30 minutes.'
                        )
                        
                        embed.timestamp = datetime.now()
                        
                        await ctx.reply(embed=embed)

<<<<<<< HEAD
                        break
                    else:
                        embed_error=nextcord.Embed(
                            title="❌ Server Info Error",
                            colour= nextcord.Colour.red(),
                            description=f'Server Info Group has already been setup!'
                        )
                        
                        await ctx.reply(embed=embed_error)

                        break
                            
=======
                group_info = group.member_count
                channel = await ctx.guild.create_voice_channel(name=f"Group: {group_info}", category=category)
                
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":channel.id, "group_id":id, "game_favorite_channel":None,"game_favorite_id":None}
                
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"group_channel":channel.id}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"group_id":id}})
                    
                embed=nextcord.Embed(
                    title="✅ Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Group Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
            else:
                embed_error=nextcord.Embed(
                    title="❌ Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Group has already been setup!'
                )
                
                await ctx.reply(embed=embed_error)
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)

    
    
            
<<<<<<< HEAD
=======
            
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
    @stats.command()
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
                game_favorite_channel = x["game_favorite_channel"]
                
            if group_channel is None:
                embed_error_disable=nextcord.Embed(
                    title="❌ Server Info Error",
                    colour= nextcord.Colour.red(),
                    description="This feature is already disabled!"
                )
                        
                embed_error_disable.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_disable)
            else:
                embed_loading=nextcord.Embed(
                    title="",
                    colour= nextcord.Colour.blurple(),
                    description=f'🗑️ Caching Data...'
                )

                message_temp = await ctx.reply(embed=embed_loading)

                channel = self.client.get_channel(group_channel)
                channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
                await channel.delete()
                all_channels = channel_category.channels
                if len(all_channels) == 0:
                    await channel_category.delete()
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None, "game_favorite_channel":None,"game_favorite_id":None}   
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"group_channel":None}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"group_id":None}})
                
                await message_temp.delete()

                embed=nextcord.Embed(
                    title="✅ Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Group has been disabled!'
                )
                
                embed.timestamp = datetime.now()    
                
                await ctx.reply(embed=embed)
            
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
            
<<<<<<< HEAD


    @stats.command()
    async def setup_favorites(self, ctx):
        if ctx.author.guild_permissions.administrator:

=======
    
    @stats.command()
    async def setup_favorites(self, ctx,*, id:int):
        if ctx.author.guild_permissions.administrator:
            try:
                place = await roblox_client.get_place(id)
                
            except:
                embed_error_none=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description="No game found! Make sure it is the `PlaceId`!"
                )
                        
                embed_error_none.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_none)
                return
            universe = await roblox_client.get_universe(place.universe.id)
            
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
                    
            member_channel = None
            bot_channel = None
            game_channel = None
            group_channel = None
            game_favorite_channel = None
            
            embed_setup_game= nextcord.Embed(
                title="" ,  
                colour=nextcord.Colour.blurple(),
                description=f"Please enter a `PlaceId` to setup this feature!"
            )

            embed_setup_game.timestamp = datetime.now()

            await ctx.send(embed=embed_setup_game)

            def check(m):
                return ctx.author == m.author

            while True:
                try:
                    msg = await self.client.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    embed_error_time = nextcord.Embed(
                        title="❌ Verification Error",
                        colour=nextcord.Colour.red(),
                        description=f"Your time has ran out!"
                    )

                    embed_error_time.timestamp = datetime.now()

                    await ctx.send(embed=embed_error_time)

                    break

                if msg and msg.author != "Mivel":
                    try:
                        place = await roblox_client.get_place(int(msg.content))
                    except:
                        embed_error_none=nextcord.Embed(
                            title="❌ Error",
                            colour= nextcord.Colour.red(),
                            description="No place found! Make sure it is the `PlaceId`!"
                        )
                                
                        embed_error_none.timestamp = datetime.now()
                        
                        await ctx.reply(embed=embed_error_none)
                        break

                    universe = await roblox_client.get_universe(place.universe.id)

                    embed_loading=nextcord.Embed(
                        title="",
                        colour= nextcord.Colour.blurple(),
                        description=f'🔎 Retrieving Game Favorites Data...'
                    )

                    message_temp = await ctx.reply(embed=embed_loading)
                    
                    for x in collection.find({"_id": ctx.guild.id}):
                        member_channel = x["member_channel"]
                        bot_channel = x["bot_channel"]
                        game_channel = x["game_channel"]
                        group_channel = x["group_channel"]
                        game_favorite_channel = x["game_favorite_channel"]
                        
                    if game_channel is None:
                        overwrites={
                            ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False),
                        }
                        
                        if member_channel is None and bot_channel is None and group_channel is None and game_channel is None:    
                            category = await ctx.guild.create_category(name=f"{ctx.guild.name} Info", position=0, overwrites=overwrites)
                        else: 
                            if member_channel != None:
                                category = self.client.get_channel(member_channel).category
                                
                            if bot_channel != None:
                                category = self.client.get_channel(bot_channel).category
                                
                            if group_channel != None:
                                category = self.client.get_channel(group_channel).category
                            
                            if game_channel != None:
                                category = self.client.get_channel(game_channel).category
                                
                                

                        game_info = universe.favorited_count
                        channel = await ctx.guild.create_voice_channel(name=f"Favorites: {game_info}", category=category)
                        
                        channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None, "game_favorite_channel":channel.id,"game_favorite_id":int(msg.content)}
                        
                        try:
                            collection.insert_one(channel_info)
                        except:
                            collection.update({"_id":ctx.guild.id},{"$set":{"game_favorite_channel":channel.id}})
                            collection.update({"_id":ctx.guild.id},{"$set":{"game_favorite_id":int(msg.content)}})
                            
                        await message_temp.delete()
                        
                        embed=nextcord.Embed(
                            title="✅ Server Info Updated",
                            colour= nextcord.Colour.blurple(),
                            description=f'Server Info Game Favorite Channel Created! **Now tracking {place.name}!** For more info on this game, run the command `m!stats return_favorites`! Note that the channel updates every 30 minutes.'
                        )
                        
                        embed.timestamp = datetime.now()
                        
                        await ctx.reply(embed=embed)

<<<<<<< HEAD
                        break
                    else:
                        embed_error=nextcord.Embed(
                            title="❌ Server Info Error",
                            colour= nextcord.Colour.red(),
                            description=f'Server Info Game Favorites has already been setup!'
                        )
                        
                        await ctx.reply(embed=embed_error)

                        break
                            
=======
                game_info = universe.favorited_count
                channel = await ctx.guild.create_voice_channel(name=f"Favorites: {game_info}", category=category)
                
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None, "game_favorite_channel":channel.id,"game_favorite_id":id}
                
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_favorite_channel":channel.id}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_favorite_id":id}})
                    
                embed=nextcord.Embed(
                    title="✅ Server Info Updated",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Game Favorites Channel Created! Note that the channel updates every 30 minutes.'
                )
                
                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
            else:
                embed_error=nextcord.Embed(
                    title="❌ Server Info Error",
                    colour= nextcord.Colour.red(),
                    description=f'Server Info Favorites has already been setup!'
                )
                
                await ctx.reply(embed=embed_error)
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
            


    @stats.command()
    async def disable_favorites(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["server_collection"]
            


            game_favorite_channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                group_channel = x["group_channel"]
                game_favorite_channel = x["game_favorite_channel"]
                
            if game_favorite_channel is None:
                embed_error_disable=nextcord.Embed(
                    title="❌ Server Info Error",
                    colour= nextcord.Colour.red(),
                    description="This feature is already disabled!"
                )
                        
                embed_error_disable.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error_disable)
            else:
                embed_loading=nextcord.Embed(
                    title="",
                    colour= nextcord.Colour.blurple(),
                    description=f'🗑️ Caching Data...'
                )

                message_temp = await ctx.reply(embed=embed_loading)

                channel = self.client.get_channel(game_favorite_channel)
                channel_category = nextcord.utils.get(ctx.guild.categories, id=channel.category_id)
                await channel.delete()
                all_channels = channel_category.channels
                if len(all_channels) == 0:
                    await channel_category.delete()
                channel_info = {"_id":ctx.guild.id, "member_channel":None, "bot_channel":None,"game_channel":None,"game_id":None,"group_channel":None, "group_id":None, "game_favorite_channel":None,"game_favorite_id":None}   
                try:
                    collection.insert_one(channel_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_favorite_channel":None}})
                    collection.update({"_id":ctx.guild.id},{"$set":{"game_favorite_id":None}})
                
                await message_temp.delete()

                embed=nextcord.Embed(
                    title="✅ Server Info Disabled",
                    colour= nextcord.Colour.blurple(),
                    description=f'Server Info Favorites has been disabled!'
                )
                
                embed.timestamp = datetime.now()    
                
                await ctx.reply(embed=embed)
            
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)
    class Subscriptions(nextcord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
            self.value = None
<<<<<<< HEAD
            

        
=======
        
        
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
    @stats.command()
    async def return_game(self, ctx):
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["server_collection"]
            
        member_channel = None
        bot_channel = None
        game_channel = None
        game_id = None
        group_channel = None
        group_id = None
        game_favorite_channel = None
        game_favorite_id = None
            
        for x in collection.find({"_id": ctx.guild.id}):
            member_channel = x["member_channel"]
            bot_channel = x["bot_channel"]
            game_channel = x["game_channel"]
            game_id = x["game_id"]
            group_channel = x["group_channel"]
            group_id = x["group_id"]
            game_favorite_channel = x["game_favorite_channel"]
            game_favorite_id = x["game_favorite_id"]
            
        if game_channel != None:
<<<<<<< HEAD
            embed_loading=nextcord.Embed(
                title="",
                colour= nextcord.Colour.blurple(),
                description=f'🔎 Retrieving Game Data...'
            )

            message_temp = await ctx.reply(embed=embed_loading)


=======
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
            game = await roblox_client.get_place(game_id)
            game_universe = await roblox_client.get_universe(game.universe.id)
            embed_stats = nextcord.Embed(
                title=game.name,
                color=nextcord.Colour.blurple(),
<<<<<<< HEAD
                description=f"⭐ Favorites: {game_universe.favorited_count}\n🧍 Players: {game_universe.playing}\n👨‍👨‍👦 Visits: {game_universe.visits}\n🛠 Creator: {game.builder}\n\n{nextcord.utils.escape_markdown(game.description)}"
            )
            embed_stats.timestamp = datetime.now()


            link = Button(label=f"Link to {game.name}", url=game.url, style=nextcord.ButtonStyle.blurple)
            view=View()
            view.add_item(link)
            
            embed_stats.set_image(url=f"https://www.roblox.com/asset-thumbnail/image?assetId={game.id}&width=768&height=432&format=png")
            await message_temp.delete()
            
            await ctx.reply(embed=embed_stats, view=view)
        else:
            embed=nextcord.Embed(
                title="❌ Server Info Error",
                colour= nextcord.Colour.red(),
                description=f'Server Info Game has not been setup!'
            )
                
            embed.timestamp = datetime.now()    
                
            await ctx.reply(embed=embed)
            
            
    @stats.command()
    async def return_group(self, ctx):
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["server_collection"]
            
        member_channel = None
        bot_channel = None
        game_channel = None
        game_id = None
        group_channel = None
        group_id = None
        game_favorite_channel = None
        game_favorite_id = None
            
        for x in collection.find({"_id": ctx.guild.id}):
            member_channel = x["member_channel"]
            bot_channel = x["bot_channel"]
            game_channel = x["game_channel"]
            game_id = x["game_id"]
            group_channel = x["group_channel"]
            group_id = x["group_id"]
            game_favorite_channel = x["game_favorite_channel"]
            game_favorite_id = x["game_favorite_id"]
            
        if group_channel != None:
            embed_loading=nextcord.Embed(
                title="",
                colour= nextcord.Colour.blurple(),
                description=f'🔎 Retrieving Group Data...'
            )

            message_temp = await ctx.reply(embed=embed_loading)

            group = await roblox_client.get_group(group_id)
            embed_stats = nextcord.Embed(
                title=group.name,
                color=nextcord.Colour.blurple(),
                description=f"👨‍👨‍👦 Members: {group.member_count}\n🛠 Creator: {group.owner.name}\n\n{nextcord.utils.escape_markdown(group.description)}"
            )
            embed_stats.timestamp = datetime.now()
            

            await message_temp.delete()
            
            await ctx.reply(embed=embed_stats)
        else:
            embed=nextcord.Embed(
                title="❌ Server Info Error",
                colour= nextcord.Colour.red(),
                description=f'Server Info Group has not been setup!'
            )
                
            embed.timestamp = datetime.now()    
                
            await ctx.reply(embed=embed)

    @stats.command()
    async def return_favorites(self, ctx):
=======
                description=f"⭐ Favorites: {game_universe.favorited_count}\n🧍 Players: {game_universe.playing}\n👨‍👨‍👦 Visits: {game_universe.visits}\n🛠 Creator: {game.builder}\n\n{nextcord.utils.escape_markdown(game.description)}\n\n[Link To {game.name}]({game.url})"
            )
            embed_stats.timestamp = datetime.now()
            
            embed_stats.set_image(url=f"https://www.roblox.com/asset-thumbnail/image?assetId={game.id}&width=768&height=432&format=png")
            
            
            await ctx.reply(embed=embed_stats)
        else:
            embed=nextcord.Embed(
                title="Server Info Error",
                colour= nextcord.Colour.red(),
                description=f'Server Info Game has not been setup!'
            )
                
            embed.timestamp = datetime.now()    
                
            await ctx.reply(embed=embed)
            
            
    @stats.command()
    async def return_group(self, ctx):
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["server_collection"]
            
        member_channel = None
        bot_channel = None
        game_channel = None
        game_id = None
        group_channel = None
        group_id = None
        game_favorite_channel = None
        game_favorite_id = None
            
        for x in collection.find({"_id": ctx.guild.id}):
            member_channel = x["member_channel"]
            bot_channel = x["bot_channel"]
            game_channel = x["game_channel"]
            game_id = x["game_id"]
            group_channel = x["group_channel"]
            group_id = x["group_id"]
            game_favorite_channel = x["game_favorite_channel"]
            game_favorite_id = x["game_favorite_id"]
            
        if group_channel != None:
            group = await roblox_client.get_group(group_id)
            embed_stats = nextcord.Embed(
                title=group.name,
                color=nextcord.Colour.blurple(),
                description=f"👨‍👨‍👦 Members: {group.member_count}\n🛠 Creator: {group.owner.name}\n\n{nextcord.utils.escape_markdown(group.description)}"
            )
            embed_stats.timestamp = datetime.now()
            
            
            
            await ctx.reply(embed=embed_stats)
        else:
            embed=nextcord.Embed(
                title="Server Info Error",
                colour= nextcord.Colour.red(),
                description=f'Server Info Group has not been setup!'
            )
                
            embed.timestamp = datetime.now()    
                
            await ctx.reply(embed=embed)

    @stats.command()
    async def return_favorite(self, ctx):
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["server_collection"]
            
        member_channel = None
        bot_channel = None
        game_channel = None
        game_id = None
        group_channel = None
        group_id = None
        game_favorite_channel = None
        game_favorite_id = None
            
        for x in collection.find({"_id": ctx.guild.id}):
            member_channel = x["member_channel"]
            bot_channel = x["bot_channel"]
            game_channel = x["game_channel"]
            game_id = x["game_id"]
            group_channel = x["group_channel"]
            group_id = x["group_id"]
            game_favorite_channel = x["game_favorite_channel"]
            game_favorite_id = x["game_favorite_id"]
            
        if game_favorite_channel != None:
<<<<<<< HEAD
            embed_loading=nextcord.Embed(
                title="",
                colour= nextcord.Colour.blurple(),
                description=f'🔎 Retrieving Game Data...'
            )

            message_temp = await ctx.reply(embed=embed_loading)
=======
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
            game = await roblox_client.get_place(game_favorite_id)
            game_universe = await roblox_client.get_universe(game.universe.id)
            embed_stats = nextcord.Embed(
                title=game.name,
                color=nextcord.Colour.blurple(),
<<<<<<< HEAD
                description=f"⭐ Favorites: {game_universe.favorited_count}\n🧍 Players: {game_universe.playing}\n👨‍👨‍👦 Visits: {game_universe.visits}\n🛠 Creator: {game.builder}\n\n{nextcord.utils.escape_markdown(game.description)}"
            )
            embed_stats.timestamp = datetime.now()
            
            link = Button(label=f"Link to {game.name}", url=game.url, style=nextcord.ButtonStyle.blurple)
            view=View()
            view.add_item(link)

            embed_stats.set_image(url=f"https://www.roblox.com/asset-thumbnail/image?assetId={game.id}&width=768&height=432&format=png")
            
            await message_temp.delete()
            await ctx.reply(embed=embed_stats,view=view)
        else:
            embed=nextcord.Embed(
                title="❌ Server Info Error",
=======
                description=f"⭐ Favorites: {game_universe.favorited_count}\n🧍 Players: {game_universe.playing}\n👨‍👨‍👦 Visits: {game_universe.visits}\n🛠 Creator: {game.builder}\n\n{nextcord.utils.escape_markdown(game.description)}\n\n[Link To {game.name}]({game.url})"
            )
            embed_stats.timestamp = datetime.now()
            
            embed_stats.set_image(url=f"https://www.roblox.com/asset-thumbnail/image?assetId={game.id}&width=768&height=432&format=png")
            
            
            await ctx.reply(embed=embed_stats)
        else:
            embed=nextcord.Embed(
                title="Server Info Error",
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
                colour= nextcord.Colour.red(),
                description=f'Server Info Favorites has not been setup!'
            )
                
            embed.timestamp = datetime.now()    
                
            await ctx.reply(embed=embed)
    
    
    
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
            game_favorite_channel = None
            
            for x in collection.find({"_id": guild.id}):
                member_channel = x["member_channel"]
                bot_channel = x["bot_channel"]
                game_channel = x["game_channel"]
                game_id = x["game_id"]
                group_channel = x["group_channel"]
                group_id = x["group_id"]
                game_favorite_channel = x["game_favorite_channel"]
                game_favorite_id = x["game_favorite_id"]
            
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
            
            if game_favorite_channel != None:
                channel_game_favorite = self.client.get_channel(game_favorite_channel)
            else:
                channel_game_favorite = None
            
            
            
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
                place = await roblox_client.get_place(game_id)
                
                universe = await roblox_client.get_universe(place.universe.id)
                
                text_split = channel_game.name.split(": ")

                if int(universe.playing) != int(text_split[1]):
                    await channel_game.edit(name=f"Players: {universe.playing}")
            
            if channel_group != None:

                group = await roblox_client.get_group(group_id)
                
                text_split_group = channel_group.name.split(": ")
                
                if group.get_members != int(text_split_group[1]):
                    await channel_group.edit(name=f"Group: {group.member_count}")
                    
            if channel_game_favorite != None:
                place = await roblox_client.get_place(game_favorite_id)
                
                universe = await roblox_client.get_universe(place.universe.id)
                
                text_split_favorite = channel_game_favorite.name.split(": ")
                
                if int(universe.favorited_count) != int(text_split_favorite[1]):
                    await channel_game_favorite.edit(name=f"Favorites: {universe.favorited_count}")
                    
            
                
            
                
    

    
        
        
def setup(client):
    client.add_cog(server_info(client))
        