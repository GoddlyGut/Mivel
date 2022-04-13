import nextcord
from nextcord import Color, Embed, Member
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from datetime import datetime
import roblox
roblox_client = roblox.Client()
import pymongo
from pymongo import MongoClient
from nextcord.ui import Button, View

class roblox_features(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="roblox-user-search", description="Use this command to search for roblox players!")
    async def roblox_user_search(self, interaction: Interaction, username=str):
        try:
            user = await roblox_client.get_user_by_username(username, expand=True)
        except:
            error_embed = Embed(
                title="❌ Error",
                color=nextcord.Colour.red(),
                description="User not found!"
            )
            
            error_embed.timestamp = datetime.now()
            
            await interaction.response.send_message(embed=error_embed)
            return

        
        # status = await user.get_status()

        embed = Embed(title=f"Info for {user.name}")
        embed.add_field(
            name="Username",
            value="`" + user.name + "`"
        )
        embed.add_field(
            name="Display Name",
            value="`" + user.display_name + "`"
        )
        embed.add_field(
            name="User ID",
            value="`" + str(user.id) + "`"
        )
        
        embed.add_field(
            name="Date Created",
            value="`"+user.created.strftime("%m/%d/%Y, %H:%M:%S")+"`"
        )
        embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={user.id}&width=420&height=420&format=png")

        embed.add_field(
            name="Description",
            value="```" +
            (nextcord.utils.escape_markdown(
                user.description or "No description")) + "```",
            inline=False
        )

        embed.color = nextcord.Color.blurple()

        embed.timestamp = datetime.now()

        await interaction.response.send_message(embed=embed)

        
    @nextcord.slash_command(name="roblox-user-info", description="This command prints your roblox user information")
    async def roblox_user_info(self, interaction:Interaction):
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        in_verification_collection = db["in_verification"]
        user_userid_collection = db["user_userid"]
        
        roblox_id = None

        for x in user_userid_collection.find({"_id": interaction.user.id}):
            roblox_id = x["roblox_user_id"]
        
        if roblox_id is None:
            await interaction.response.send_message(f"{interaction.user.mention}, You need to verify yourself before using this command!")
        else:
            user = await roblox_client.get_user(roblox_id)

            embed = Embed(title=f"Info for {user.name}")
            embed.add_field(
                name="Username",
                value="`" + user.name + "`"
            )
            embed.add_field(
                name="Display Name",
                value="`" + user.display_name + "`"
            )
            embed.add_field(
                name="User ID",
                value="`" + str(user.id) + "`"
            )
            
            embed.add_field(
                name="Date Created",
                value="`"+user.created.strftime("%m/%d/%Y, %H:%M:%S")+"`"
            )

            embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={user.id}&width=420&height=420&format=png")
            
            embed.add_field(
                name="Description",
                value="```" +
                (nextcord.utils.escape_markdown(
                    user.description or "No description")) + "```",
                inline=False
            )
            embed.color = nextcord.Color.blurple()

            embed.timestamp = datetime.now()

            await interaction.response.send_message(embed=embed)
            
            
    @nextcord.slash_command(name="other-roblox-user-info", description="This command prints a users roblox user information")
    async def roblox_other_info(self, interaction:Interaction, member:Member=SlashOption(required=True)):
        
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        in_verification_collection = db["in_verification"]
        user_userid_collection = db["user_userid"]
        
        roblox_id = None

        for x in user_userid_collection.find({"_id": member.id}):
            roblox_id = x["roblox_user_id"]
        
        
        if roblox_id is None:
            await interaction.response.send_message(f"{interaction.user.mention}, {member.name} has not verified themselves!")
        else:
            user = await roblox_client.get_user(roblox_id)

            embed = Embed(title=f"Info for {user.name}")
            embed.add_field(
                name="Username",
                value="`" + user.name + "`"
            )
            embed.add_field(
                name="Display Name",
                value="`" + user.display_name + "`"
            )
            embed.add_field(
                name="User ID",
                value="`" + str(user.id) + "`"
            )
            
            embed.add_field(
                name="Date Created",
                value="`"+user.created.strftime("%m/%d/%Y, %H:%M:%S")+"`"
            )
            embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={user.id}&width=420&height=420&format=png")

            embed.add_field(
                name="Description",
                value="```" +
                (nextcord.utils.escape_markdown(
                    user.description or "No description")) + "```",
                inline=False
            )
            
            embed.color = nextcord.Color.blurple()
            

            

            embed.timestamp = datetime.now()

            await interaction.response.send_message(embed=embed)

    @commands.group(invoke_without_command=True)
    async def verify(self, ctx):
        embed = nextcord.Embed(
            title="📦 Available Setup Commands:",
            colour=nextcord.Colour.blurple(),
            description="```m!verify setup <@role>```**Allows you to setup the verification system role**\n```m!verify disable```**Allows you to disable the verification system**\n```m!verify enable```**Allows you to enable the verification system**",

        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

    @verify.command()
    async def setup(self, ctx, role: nextcord.Role):
        if ctx.author.guild_permissions.administrator:
            
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["verification_collection"]
            
            verify_info = {"_id":ctx.guild.id, "role":role.id, "enabled":True}
                
 
            try:
                collection.insert_one(verify_info)
            except:
                collection.update({"_id":ctx.guild.id},{"$set":{"role":role.id}})
            

            embed = Embed(
                title="✅ Verification Setup",
                color=nextcord.Colour.green(),
                description=f"The verified role has been set to {role.mention}"
            )

            embed.timestamp = datetime.now()

            await ctx.reply(embed=embed)

        else:
            embed_error_perms = nextcord.Embed(
                title="❌ Error",
                colour=nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )

            embed_error_perms.timestamp = datetime.now()

            await ctx.reply(embed=embed_error_perms)


    @verify.command()
    async def disable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["verification_collection"]
            
            role = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                role = x["role"]
                enabled = x["enabled"]
            
            if role != None:
                embed = Embed(
                    title="✅ Verification Setup",
                    color=nextcord.Colour.green(),
                    description=f"The verification system has been disabled!"
                )
                
                if role is None:
                    embed_error=nextcord.Embed(
                        title="❌ Error",
                        colour= nextcord.Colour.red(),
                        description=f'Please finish setting up the verification system!'
                    )
                    
                    embed_error.timestamp = datetime.now()
                    
                    await ctx.reply(embed=embed_error)
                    
                else:
                    collection.update_one({"_id":ctx.guild.id},{"$set":{"enabled":False}})

                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
            else:
                embed_error_setup = nextcord.Embed(
                    title="❌ Verification Error",
                    colour=nextcord.Colour.red(),
                    description="The verification system has not been setup!"
                )

                embed_error_setup.timestamp = datetime.now()

                await ctx.reply(embed=embed_error_setup)
                
        else:
            embed_error_perms = nextcord.Embed(
                title="❌ Error",
                colour=nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )

            embed_error_perms.timestamp = datetime.now()

            await ctx.reply(embed=embed_error_perms)

    @verify.command()
    async def enable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["verification_collection"]
            
            role = None
            
            for x in collection.find({"_id": ctx.guild.id}):
                role = x["role"]
                enabled = x["enabled"]
            
            if role != None:
                embed = Embed(
                    title="✅ Verification Setup",
                    color=nextcord.Colour.green(),
                    description=f"The verification system has been enabled!"
                )
                
                if role is None:
                    embed_error=nextcord.Embed(
                        title="❌ Error",
                        colour= nextcord.Colour.red(),
                        description=f'Please finish setting up the verification system!'
                    )
                    
                    embed_error.timestamp = datetime.now()
                    
                    await ctx.reply(embed=embed_error)
                    
                else:
                    collection.update_one({"_id":ctx.guild.id},{"$set":{"enabled":True}})

                embed.timestamp = datetime.now()
                
                await ctx.reply(embed=embed)
        else:
            embed_error_perms = nextcord.Embed(
                title="❌ Error",
                colour=nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )

            embed_error_perms.timestamp = datetime.now()

            await ctx.reply(embed=embed_error_perms)

    @nextcord.slash_command(name="verify", description="Use this command to link your roblox account with your discord account!")
    async def verify_command(self, interaction: Interaction, username: str = SlashOption(description="Your roblox username", required=True)):
        
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        in_verification_collection = db["in_verification"]
        verification_collection = db["verification_collection"]
        user_userid_collection = db["user_userid"]
        

        in_verification = None
        enabled = None
        role = None

        for x in verification_collection.find({"_id": interaction.guild.id}):
            role = x["role"]
            enabled = x["enabled"]

        for x in in_verification_collection.find({"_id": interaction.user.id}):
            in_verification = x["in_verification"]
            

            

        if role != None:
            if enabled == True:
                if in_verification == False or in_verification is None:


                    in_verify_info = {"_id":interaction.user.id, "in_verification":True}
                    
                    try:
                        in_verification_collection.insert_one(in_verify_info)
                    except:
                        in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":True}})
                    




                        in_verify_info = {"_id":interaction.user.id, "in_verification":False}
                
                        try:
                            in_verification_collection.insert_one(in_verify_info)
                        except:
                            in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":False}})
                        
                        
                        

                        
                        try:
                            user = await roblox_client.get_user_by_username(username, expand=True)
                        except:
                            embed_fail = Embed(
                                title="❌ Verification Error",
                                color=nextcord.Color.red(),
                                description=f"You did not type a correct username. Please re-run the verification process!"
                            )

                            embed_fail.timestamp = datetime.now()
                            await interaction.response(embed=embed_fail)
                            
                            return
                            
                        
                        found = False
                        same_username = False
                        
                        for x in user_userid_collection.find():
                            discord_id = x["_id"]
                            user_id = x["roblox_user_id"]
                            if int(user_id) == user.id:
                                if int(discord_id) == interaction.user.id:
                                    same_username = True
                                else:
                                    found = True
                        
                        if found == False and same_username == False:
                            embed = nextcord.Embed(
                                title=f"User Info For @{user.name}",
                                color=nextcord.Color.green()
                            )
                            
                            embed.add_field(
                                name="Username",
                                value="```" + user.name + "```"
                            )
                            embed.add_field(
                                name="Display Name",
                                value="```" + user.display_name + "```"
                            )
                            embed.add_field(
                                name="User ID",
                                value="```" + str(user.id) + "```"
                            )
                            
                            embed.add_field(
                                name="Date Created",
                                value="```"+user.created.strftime("%m/%d/%Y, %H:%M:%S")+"```"
                            )
                            embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={user.id}&width=420&height=420&format=png")

                            embed.add_field(
                                name="Description",
                                value="```" +
                                (nextcord.utils.escape_markdown(
                                    user.description or "No description")) + "```",
                                inline=False
                            )

                            embed.color = nextcord.Color.blurple()

                            embed.timestamp = datetime.now()
                            
                            view = View()
                            yes_button = Button(label="Yes", style=nextcord.ButtonStyle.green)
                            no_button = Button(label="No", style=nextcord.ButtonStyle.red)
                            view.add_item(yes_button)
                            view.add_item(no_button)
                            
                            channel = interaction.channel
                            
                            await interaction.send(embed=embed, view=view, ephemeral=False)
                            
                            async def yes_button_callback(inter): 
                                
                                
                                embed_success = Embed(
                                    title="",
                                    description=f"✅ {interaction.user.mention}, You are now verified under @{user.name}",
                                    color=nextcord.Color.green()
                                )
                                await channel.send(embed=embed_success)
                                        
                                in_verify_info = {"_id":interaction.user.id, "in_verification":False}
                    
                                try:
                                    in_verification_collection.insert_one(in_verify_info)
                                except:
                                    in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":False}})


                                roblox_info = {"_id":interaction.user.id, "roblox_user_id": user.id}
                                
                                try:
                                    user_userid_collection.insert_one(roblox_info)
                                except:
                                    user_userid_collection.update({"_id":interaction.user.id},{"$set":{"roblox_user_id": user.id}})
                                
                                await interaction.user.edit(nick=user.name)
                                
                                role_val = nextcord.utils.get(interaction.guild.roles, id=role)
                                await interaction.user.add_roles(role_val)
                                
                            async def no_button_callback(inter): 
                                
                                
                                embed_error = Embed(
                                    title="",
                                    description=f"❌ {interaction.user.mention}, Restart the verification process!",
                                    color=nextcord.Color.red()
                                )
                                await channel.send(embed=embed_error)
                                        
                                in_verify_info = {"_id":interaction.user.id, "in_verification":False}
                    
                                try:
                                    in_verification_collection.insert_one(in_verify_info)
                                except:
                                    in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":False}})

                                
                            yes_button.callback = yes_button_callback
                            no_button.callback = no_button_callback
                            
                            return
                            
                                   
                        else:
                            if same_username == True:
                                embed_error_same = Embed(
                                    title="",
                                    description=f"❌ You are already verified under @{user.name}!",
                                    color=nextcord.Color.red()
                                )
                                
                                await interaction.response.send_message(embed=embed_error_same)
                                
                            elif found == True:
                                embed_error = Embed(
                                    title="",
                                    description=f"❌ Someone already verified under @{user.name}! Please try a different username!",
                                    color=nextcord.Color.red()
                                )
                                
                                await interaction.response.send_message(embed=embed_error)

                                               
                            

                else:
                    embed_error_progress = nextcord.Embed(
                        title="❌ Verification Error",
                        colour=nextcord.Colour.red(),
                        description="You already are in the verification process!"
                    )

                    embed_error_progress.timestamp = datetime.now()

                    await interaction.response.send_message(embed=embed_error_progress)


            else:
                embed_error_disable = nextcord.Embed(
                    title="❌ Verification Error",
                    colour=nextcord.Colour.red(),
                    description="The verification system has been disabled!"
                )

                embed_error_disable.timestamp = datetime.now()
                await interaction.response.send_message(embed=embed_error_disable)
        else:
            embed_error_setup = nextcord.Embed(
                title="❌ Verification Error",
                colour=nextcord.Colour.red(),
                description="The verification system has not been setup!"
            )

            embed_error_setup.timestamp = datetime.now()

            await interaction.response.send_message(embed=embed_error_setup)


def setup(client):
    client.add_cog(roblox_features(client))
