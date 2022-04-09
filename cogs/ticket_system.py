from nextcord.ext import commands
import nextcord
from nextcord import Interaction
from nextcord import Interaction
from nextcord.utils import get
from datetime import datetime
import pymongo
from pymongo import MongoClient

   

class ticket_system(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
    @commands.group(invoke_without_command=True)
    async def ticket(self, ctx):
        embed=nextcord.Embed(
            title="📦 Available Setup Commands:",
            colour= nextcord.Colour.blurple(),
<<<<<<< HEAD
            description="```m!ticket role <@role>```**Sets a role that can view tickets**\n```m!ticket message <'message'>```**Sets a ticket message**\n```m!ticket disable```**Disables the ticket system**\n```m!ticket enable```**Enables the ticket system**" 
=======
            description="`m!ticket role <@role>`-**Sets a role that can view tickets**\n`m!ticket message <'message'>`-**Sets a ticket message**\n`m!ticket disable`-**Disables the ticket system**\n`m!ticket enable`-**Enables the ticket system**" 
>>>>>>> a3b827067ed31a7fa14adf500ce1e60781a1e9dd
        )

        await ctx.send(embed=embed)
    
    @ticket.command()
    async def role(self, ctx,*, support_role:nextcord.Role):
        if ctx.author.guild_permissions.administrator:
            
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["ticket_collection"]
            
            message = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                message = x["message"]
                enabled = x["enabled"]
                
                
            if message is None:
                message = "Thanks for creating a ticket! The support team will be with you shortly!" #default message if nothing is set
            
            ticket_info = {"_id":ctx.guild.id, "role":support_role.id, "message":message, "enabled": True}
            
            try:
                collection.insert_one(ticket_info)
            except:
                collection.update({"_id":ctx.guild.id},{"$set":{"role":support_role.id}})
            
            embed=nextcord.Embed(
                title="✅ Ticket Info Updated",
                colour= nextcord.Colour.green(),
                description=f"Ticket support role has been set to {support_role.mention}"
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
    

        
        
    @ticket.command()
    async def disable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["ticket_collection"]
            
            role = None
            message = None

            #{},{"_id":1, "channel":1, "message":1, "enabled":1}
            for x in collection.find({"_id": ctx.guild.id}):
                role = x["role"]
                message = x["message"]
                enabled = x["enabled"]
            
            
            
            if role is None and message is None:
                embed_error=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description=f'Please finish setting up the ticket system!'
                )
                
                embed_error.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error)
                return
            else:
                collection.update_one({"_id":ctx.guild.id},{"$set":{"enabled":False}})
                
            embed=nextcord.Embed(
                title="✅ Ticket System Updated",
                colour= nextcord.Colour.green(),
                description=f"Ticket system has been disabled!"
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
        
    @ticket.command()
    async def enable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["ticket_collection"]
            
            role = None
            message = None

            #{},{"_id":1, "channel":1, "message":1, "enabled":1}
            for x in collection.find({"_id": ctx.guild.id}):
                role = x["role"]
                message = x["message"]
                enabled = x["enabled"]
            
            
            
            if role is None and message is None:
                embed_error=nextcord.Embed(
                    title="❌ Error",
                    colour= nextcord.Colour.red(),
                    description=f'Please finish setting up the ticket system!'
                )
                
                embed_error.timestamp = datetime.now()
                
                await ctx.reply(embed=embed_error)
                return
            else:
                collection.update_one({"_id":ctx.guild.id},{"$set":{"enabled":True}})
                
            embed=nextcord.Embed(
                title="✅ Ticket System Updated",
                colour= nextcord.Colour.green(),
                description=f"Ticket system has been disabled!"
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

    @ticket.command()
    async def message(self, ctx, *,ticket_message: str):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["ticket_collection"]
            
            role = None
            
            
            for x in collection.find({"_id": ctx.guild.id}):
                role = x["role"]
                enabled = x["enabled"]
                
                
            
            ticket_info = {"_id":ctx.guild.id, "role":role, "message":ticket_message, "enabled": True}
            
            try:
                collection.insert_one(ticket_info)
            except:
                collection.update({"_id":ctx.guild.id},{"$set":{"message":ticket_message}})
            
            embed=nextcord.Embed(
                title="✅ Ticket Info Updated",
                colour= nextcord.Colour.green(),
                description=f"Ticket message has been set to '{ticket_message}'"
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
    
    
        
    
    @nextcord.slash_command(name="ticket", description="Use this command to create a ticket")
    async def ticket_create(self, interaction: Interaction):
        
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["ticket_collection"]
            
        role = None
        message = None

        #{},{"_id":1, "channel":1, "message":1, "enabled":1}
        for x in collection.find({"_id": interaction.guild.id}):
            role = x["role"]
            message = x["message"]
            enabled = x["enabled"]
        
        if role is None and message is None:
            embed_error=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="Please setup the ticket bot before use!"
            )
                        
            embed_error.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=embed_error, ephemeral=True)
        else:
            if enabled == False:
                embed_not_enabled=nextcord.Embed(
                    title="✅ Ticket System Updated",
                    colour= nextcord.Colour.red(),
                    description="Ticket system has been disabled!"
                )   
                    
                embed_not_enabled.timestamp = datetime.now()
        
                await interaction.response.send_message(embed=embed_not_enabled, ephemeral=True)
            else:
                support_role = role
                ticket_message = message
                if get(interaction.guild.categories, name="Support-Category"):
                    SupportCategory = get(interaction.guild.categories, name="Support-Category")
                    if support_role != None:
                        admin_role = get(interaction.guild.roles, id=int(support_role))
                        overwrites={
                            interaction.user: nextcord.PermissionOverwrite(view_channel=True),
                            interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                            admin_role: nextcord.PermissionOverwrite(view_channel=True),
                        }
                    else:
                        overwrites={
                            interaction.user: nextcord.PermissionOverwrite(view_channel=True),
                            interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                        }
                        
                    
                    channel = await interaction.guild.create_text_channel(f"support~{interaction.user.name}", category=SupportCategory, overwrites=overwrites)
                    
                    
                else:
                    if support_role != None:
                        admin_role = get(interaction.guild.roles, id=int(support_role))
                        overwrites={
                            interaction.user: nextcord.PermissionOverwrite(view_channel=True),
                            interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                            admin_role: nextcord.PermissionOverwrite(view_channel=True),
                        }

                    else:
                        overwrites={
                            interaction.user: nextcord.PermissionOverwrite(view_channel=True),
                            interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                        }

                    
                    newCategory = await interaction.guild.create_category("Support-Category")
                    
                    
                    
                    channel = await interaction.guild.create_text_channel(f"support~{interaction.user.name}", category=newCategory, overwrites=overwrites)
                
                embed = nextcord.Embed(
                    title="Ticket",
                    colour= nextcord.Colour.blurple()
                )
                        
                embed.timestamp=datetime.now()
                embed.add_field(name="User", value=interaction.user.mention)
                if ticket_message is None:
                    ticket_message = "Hello! Please wait for support member to meet with you."
                embed.add_field(name="Support", value=ticket_message, inline=False)
                msg = await channel.send(embed=embed)
                await msg.add_reaction("🗑️")
                await interaction.response.send_message(f"Created message in {channel.mention}", ephemeral=True)
                
                
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.emoji.name == "🗑️":
            channel = self.client.get_channel(payload.channel_id)
            if channel.category.name == "Support-Category":
                message = await channel.fetch_message(payload.message_id)
                reaction = get(message.reactions, emoji = payload.emoji.name)
                if reaction and reaction.count > 1:
                    await channel.delete()
        





def setup(client):
    client.add_cog(ticket_system(client))