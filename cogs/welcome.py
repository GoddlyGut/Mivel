import nextcord
from nextcord.ext import commands
from datetime import datetime
import pymongo
from pymongo import MongoClient
import roblox
roblox_client = roblox.Client()

class welcome_system(commands.Cog):
    def __init__(self, client):
        self.client = client
         
    
    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        embed=nextcord.Embed(
            title="📦 Available Setup Commands:",
            colour= nextcord.Colour.blurple(),
            description="```m!welcome channel <#channel>```**Sets a welcome channel**\n```m!welcome message <'Message'>```**Sets a welcome message**\n```m!welcome disable```**Disables the welcome system**\n```m!welcome enable```**Enables the welcome system**"
        )      
        await ctx.send(embed=embed)
    
    @welcome.command()
    async def channel(self, ctx, channel:nextcord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["welcome_collection"]
            
            message = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                message = x["message"]
                enabled = x["enabled"]
            
            if message is None:
                message = "Welcome to my server! Hope you enjoy your stay!" #default message if nothing is set
            
            welcome_info = {"_id":ctx.guild.id, "channel":channel.id, "message":message, "enabled": True}
            
            try:
                collection.insert_one(welcome_info)
            except:
                collection.update({"_id":ctx.guild.id},{"$set":{"channel":channel.id}})


                
            embed=nextcord.Embed(
                title="✅ Welcome Info Updated",
                colour= nextcord.Colour.green(),
                description=f"Channel has been set to {channel.mention}!"
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

        
        
    @welcome.command()
    async def message(self,ctx,*, message):
        if ctx.message.author.guild_permissions.manage_messages:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["welcome_collection"]
            
            channel = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                channel = x["channel"]
                enabled = x["enabled"]
            
                
            if channel is None:
                embed_error=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description=f'Please finish setting up the welcome system!'
                )
                
                embed_error.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error)
                return
            else:
                welcome_info = {"_id":ctx.guild.id, "channel":channel, "message":message, "enabled": True}
                
                
                
                try:
                    collection.insert_one(welcome_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"message":message}})


                
            embed=nextcord.Embed(
                title="✅ Welcome Info Updated",
                colour= nextcord.Colour.green(),
                description=f"Message has been set to '{message}'!"
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

        
    @welcome.command()
    async def disable(self,ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["welcome_collection"]
            
            channel = None
            message = None

            #{},{"_id":1, "channel":1, "message":1, "enabled":1}
            for x in collection.find({"_id": ctx.guild.id}):
                channel = x["channel"]
                message = x["message"]
                enabled = x["enabled"]
            
            
            
            if channel is None or message is None:
                embed_error=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description=f'Please finish setting up the welcome system!'
                )
                
                embed_error.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error)
                return
            else:
                collection.update_one({"_id":ctx.guild.id},{"$set":{"enabled":False}})

            
            embed=nextcord.Embed(
                title="✅ Welcome System Updated",
                colour= nextcord.Colour.green(),
                description=f"Welcome system has been disabled!"
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
            
            
            
            
            

    @welcome.command()
    async def enable(self,ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["welcome_collection"]
            
            channel = None
            message = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                channel = x["channel"]
                message = x["message"]
                enabled = x["enabled"]
            
            
            if channel is None or message is None:
                embed_error=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description=f'Please finish setting up the welcome system!'
                )
                
                embed_error.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error)
                return
            else:
                collection.update_one({"_id":ctx.guild.id},{"$set":{"enabled":True}})

            
            embed=nextcord.Embed(
                title="✅ Welcome System Updated",
                colour= nextcord.Colour.green(),
                description=f"Welcome system has been enabled!"
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


    @commands.Cog.listener()
    async def on_member_join(self, member):
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["welcome_collection"]
        user_userid_collection = db["user_userid"]
        verification_collection = db["verification_collection"]
        
        roblox_id = None
        channel = None
        message = None
        enabled = None
        
        verify_enabled = None
        role = None
        
        for x in verification_collection.find({"_id": member.guild.id}):
            role = x["role"]
            verify_enabled = x["enabled"]
        
        for x in user_userid_collection.find({"_id": member.id}):
            roblox_id = x["roblox_user_id"]
         
        for x in collection.find({"_id": member.guild.id}):
            channel = x["channel"]
            message = x["message"]
            enabled = x["enabled"]

        
        if role != None:
            if verify_enabled == True:
                if roblox_id != None:
                    roblox_user = await roblox_client.get_user(int(roblox_id))
                    await member.edit(nick=roblox_user.name)
                    role_val = nextcord.utils.get(member.guild.roles, id=role)
                    await member.add_roles(role_val)
        
        if channel is not None and message is not None and enabled is not None:
            if enabled == True:
                try:
                    channel = self.client.get_channel(int(channel)) #suggestion-channel
                except:
                    return

                welcome_description = message
                    
                embed_joined=nextcord.Embed(
                    title="New User!",
                    colour= nextcord.Colour.blurple(),
                    description=f"Hey {member.mention}, {welcome_description}"
                        
                )
                embed_joined.set_thumbnail(url=member.display_avatar.url)
                embed_joined.timestamp = datetime.now()
                    
                await channel.send(embed=embed_joined)
        
        
            
            
            


            
            
    
    

def setup(client):
    client.add_cog(welcome_system(client))
        