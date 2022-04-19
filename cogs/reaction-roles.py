import nextcord
from nextcord import Color, Embed, Emoji, Member
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from datetime import datetime
import pymongo
from pymongo import MongoClient
from nextcord.ui import Button, View
from nextcord.utils import get
import asyncio
import emoji

class reaction_role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def reaction(self, ctx):
        embed = nextcord.Embed(
            title="📦 Available Setup Commands:",
            colour=nextcord.Colour.blurple(),
            description="```m!reaction setup <@role>```**Allows you to setup the reaction role system**",
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        
    @reaction.command()
    async def setup(self, ctx, role:nextcord.Role):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["reaction_roles"]
                    

            embed_add_reaction = Embed(
                title="",
                description="Add your reaction to this response!",
                color=nextcord.Color.blurple()
            )
            
            embed_add_reaction.set_footer(text="This prompt expires in 2 minutes!")
            
            msg = await ctx.reply(embed=embed_add_reaction)
            
            def check(reaction, user):
                return user == ctx.author

            def check_msg(m):
                if ctx.channel == m.channel:
                    return ctx.author == m.author
            
            while True:
                try:
                    reaction = await self.client.wait_for("reaction_add", timeout=120.0, check=check)
                except asyncio.TimeoutError:
                    embed_error_time = nextcord.Embed(
                        title="",
                        colour=nextcord.Colour.red(),
                        description=f"❌ Your time has ran out!"
                    )

                    

                    await ctx.send(embed=embed_error_time)

                    break

                    
                
                emoji_str = emoji.demojize(str(reaction[0]))
                
                
                if emoji.emoji_count(str(reaction[0])) > 0:
                    pass
                    
                else:

                    embed_error = nextcord.Embed(
                        title="",
                        colour=nextcord.Colour.red(),
                        description=f"❌ You did not use a valid emoji! Please make sure it is a default emoji!"
                    )


                    await ctx.send(embed=embed_error)
                    
                    

                    break
 
                embed_next_step = Embed(
                    title="",
                    description="Please type in the `Message Id` the reaction role will attach to",
                    color=nextcord.Colour.blurple()
                )
                
                embed_next_step.set_footer(text="This prompt expires in 5 minutes!")
                    
                await ctx.send(embed=embed_next_step)
                
                try:
                    msg = await self.client.wait_for('message', timeout=300.0, check=check_msg)
                except asyncio.TimeoutError:
                    embed_error_time = nextcord.Embed(
                        title="",
                        colour=nextcord.Colour.red(),
                        description=f"❌ Your time has ran out!"
                    )


                    await ctx.send(embed=embed_error_time)

                    break
                Found = False
                
                for channel in ctx.guild.text_channels:
                    try:
                        msg_specific = await channel.fetch_message(int(msg.content))
                    except:
                        embed_error_invalid = nextcord.Embed(
                            title="",
                            colour=nextcord.Colour.red(),
                            description=f"❌ You did not provide a valid message id!"
                        )
                        await ctx.send(embed=embed_error_invalid)
                        break
                    if msg_specific != None:
                        Found = True
                        break
                
                if Found == False:
                    break
                
                msg_to_react = msg_specific

                try:
                    await msg_to_react.add_reaction(str(reaction[0]))
                except:
                    embed_error_invalid = nextcord.Embed(
                        title="",
                        colour=nextcord.Colour.red(),
                        description=f"❌ You did not provide a valid message id!"
                    )
                    await ctx.send(embed=embed_error_invalid)

                    break

                embed_success = Embed(
                    title="",
                    description=f"✅ Reaction role for {role.mention} has been set to {reaction[0]}! Reaction attached to message: `{msg_to_react.id}`!",
                    color=nextcord.Color.blurple()
                )
                
                await ctx.send(embed=embed_success)
                
                embed_role = Embed(
                    title="",
                    description=msg.content,
                    color=nextcord.Colour.blurple()
                )
                    
                
                emoji_info = {"_id":ctx.guild.id, f"{emoji_str}":f"{role.id}/{int(msg.content)}"}
                try:
                    collection.insert_one(emoji_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{f"{emoji_str}":f"{role.id}/{int(msg.content)}"}})
                
                break
                
                
            

        else:
            embed_error_perms = nextcord.Embed(
                title="",
                colour=nextcord.Colour.red(),
                description="❌ You do not have the required permissions!"
            )


            await ctx.reply(embed=embed_error_perms)
            
            
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["reaction_roles"]
        
        emoji_val = None
        
        try:
            for x in collection.find({"_id": payload.guild_id}):
                emoji_val = x[emoji.demojize(str(payload.emoji.name))]
        except:
            return
      
        if emoji_val != None:
            text_split = emoji_val.split("/")
            role_id = int(text_split[0])
            message_id = int(text_split[1])
            
            
            if payload.message_id == message_id:
                if payload.user_id != self.client.user.id:
                    guild = await self.client.fetch_guild(payload.guild_id)
                    
                    role_val = nextcord.utils.get(guild.roles, id=role_id)
                    
                    
                    try:
                        await payload.member.add_roles(role_val)
                    except:
                        return
                    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["reaction_roles"]
        
        emoji_val = None
        
        try:
            for x in collection.find({"_id": payload.guild_id}):
                emoji_val = x[emoji.demojize(str(payload.emoji.name))]
        except:
            return
      
        if emoji_val != None:
            text_split = emoji_val.split("/")
            role_id = int(text_split[0])
            message_id = int(text_split[1])
            

            if payload.message_id == message_id:
                if payload.user_id != self.client.user.id:
                    guild = await self.client.fetch_guild(payload.guild_id)
                    role_val = nextcord.utils.get(guild.roles, id=role_id)


                    
                    member = await guild.fetch_member(int(payload.user_id))

                    try:
                        await member.remove_roles(role_val)
                    except:
                        return
                    


            
            

        
        
def setup(client):
    client.add_cog(reaction_role(client))