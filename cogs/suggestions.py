from nextcord.ext import commands
import nextcord
from nextcord import Interaction
from datetime import datetime
import pymongo
from pymongo import MongoClient

class suggestions(commands.Cog):
    def __init__(self, client):
        self.client = client
    
   
    

    @nextcord.slash_command(name="suggest",description="Use this command to send a suggestion!")
    async def suggest(self, interaction: Interaction, suggestion = nextcord.SlashOption(description="Please fill out a suggestion here!", required=True)):
        
        
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["suggestion_collection"]
            
        channel = None

        #{},{"_id":1, "channel":1, "message":1, "enabled":1}
        for x in collection.find({"_id": interaction.guild.id}):
            channel = x["channel"]
            enabled = x["enabled"]
        
        if channel is None:
            embed_error=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description=f'Please finish setting up the suggestion system!'
            )
                
            embed_error.timestamp = datetime.now()
                
            await interaction.response.send_message(embed=embed_error, ephemeral=True)
        else:
            if enabled == False:
                embed_not_enabled=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description="Suggestion system has been disabled!"
                )   
                    
                embed_not_enabled.timestamp = datetime.now()
        
                await interaction.response.send_message(embed=embed_not_enabled, ephemeral=True)
            else: 
                channel_val = self.client.get_channel(int(channel)) #suggestion-channel
                embed=nextcord.Embed(
                    title="Suggestion",
                    colour= nextcord.Colour.blurple()
                 )
                        
                embed.set_footer(text="Type /suggest to send a suggestion!")
                embed.add_field(name="User", value=interaction.user.mention,inline=False)
                embed.add_field(name="Suggestion Text", value=suggestion, inline=False)
                    
                    
                    
                msg = await channel_val.send(embed=embed)
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")
                    
                    
                embed_success=nextcord.Embed(
                    title="✅ Suggestion Sent",
                    colour= nextcord.Colour.green(),
                    description=f"Suggestion submitted to {channel_val.mention}"
                )
                            
                embed_success.timestamp = datetime.now()
                        
                await interaction.response.send_message(embed=embed_success, ephemeral=True)
    
    
    @commands.group(invoke_without_command=True)
    async def suggestion(self, ctx):
        embed=nextcord.Embed(
            title="📦 Available Setup Commands:",
            colour= nextcord.Colour.blurple(),
            description="```m!suggestion channel <#channel>```**Sets a suggestion channel**\n```m!suggestion disable```**Disables suggestions system**\n```m!suggestion enable```**Enables suggestions system**"
        )      
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    @suggestion.command()
    async def channel(self, ctx, channel:nextcord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:

            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["suggestion_collection"]
            
            
            for x in collection.find({"_id": ctx.guild.id}):
                enabled = x["enabled"]
            
            
            welcome_info = {"_id":ctx.guild.id, "channel":channel.id, "enabled": True}
            
            try:
                collection.insert_one(welcome_info)
            except:
                collection.update({"_id":ctx.guild.id},{"$set":{"channel":channel.id}})
            
            
            embed=nextcord.Embed(
                title="✅ Suggest Info Updated",
                colour= nextcord.Colour.green(),
                description=f"Channel has been set to {channel.mention}"
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
    
        
        
        
    @suggestion.command()
    async def disable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["suggestion_collection"]
                
            channel = None

            #{},{"_id":1, "channel":1, "message":1, "enabled":1}
            for x in collection.find({"_id": ctx.guild.id}):
                channel = x["channel"]
                enabled = x["enabled"]
            
            
            if channel is None:
                embed_error=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description=f'Please finish setting up the suggestion system!'
                )
                
                embed_error.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error)
                return
            else:
                collection.update_one({"_id":ctx.guild.id},{"$set":{"enabled":False}})
            

            embed=nextcord.Embed(
                title="✅ Suggest Settings Updated",
                colour= nextcord.Colour.green(),
                description=f'Suggest system has been disabled!'
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
        
    @suggestion.command()
    async def enable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["suggestion_collection"]
                
            channel = None

            #{},{"_id":1, "channel":1, "message":1, "enabled":1}
            for x in collection.find({"_id": ctx.guild.id}):
                channel = x["channel"]
                enabled = x["enabled"]
            
            
            if channel is None:
                embed_error=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description=f'Please finish setting up the suggestion system!'
                )
                
                embed_error.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error)
                return
            else:
                collection.update_one({"_id":ctx.guild.id},{"$set":{"enabled":True}})
            

            embed=nextcord.Embed(
                title="✅ Suggest Settings Updated",
                colour= nextcord.Colour.green(),
                description=f'Suggest system has been enabled!'
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
    



def setup(client):
    client.add_cog(suggestions(client))