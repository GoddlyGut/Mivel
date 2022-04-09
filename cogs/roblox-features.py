import asyncio
import nextcord
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from datetime import datetime
import roblox
roblox_client = roblox.Client()
import pymongo
from pymongo import MongoClient


class roblox_features(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="roblox-user-search", description="Use this command to search for roblox players!")
    async def roblox_user_search(self, interaction: Interaction, username=str):
        try:
            user = await roblox_client.get_user_by_username(username, expand=True)
        except:
            error_embed = Embed(
                title="Error",
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
            description="`m!verify setup <@role>`-**Allows you to setup the verification system role**\n`m!verify disable`-**Allows you to disable the verification system**\n`m!verify enable`-**Allows you to enable the verification system**",

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
                    return
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
                    return
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
    async def verify_command(self, interaction: Interaction):
        
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
            

        def check(m):
            return interaction.user == m.author

        if role != None:
            if enabled == True:
                if in_verification == False or in_verification is None:


                    in_verify_info = {"_id":interaction.user.id, "in_verification":True}
                    
                    try:
                        in_verification_collection.insert_one(in_verify_info)
                    except:
                        in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":True}})
                    

                    channel = await interaction.user.create_dm()

                    await interaction.response.send_message(f"{interaction.user.mention}, please check your dms!")


                    embed_setup = Embed(
                        title="Verification Process",
                        color=nextcord.Colour.blurple(),
                        description=f"This message will guide you on how to get verified in {interaction.guild.name}",
                    )
                    
                    embed_setup.add_field(
                        name="Step 1", value="Please go to `roblox.com` and paste your username in this dm. You have 1 minute to complete this step.", inline=False)
                    embed_setup.add_field(
                        name="Step 2", value="Once finished with the above step, paste this value into your roblox profile description `verificationbotpasteconfirmaccount`. **Be sure to change this once you are completed with the verification process!**", inline=False)
                    embed_setup.add_field(
                        name="Step 3", value=f"Once finished with the above step, type `confirm` and you will be granted the verified role in {interaction.guild.name}", inline=False)
                    embed_setup.timestamp = datetime.now()
                    await channel.send(embed=embed_setup)

                    while True:
                        try:
                            msg = await self.client.wait_for('message', timeout=60.0, check=check)
                        except asyncio.TimeoutError:
                            embed_error_time = nextcord.Embed(
                                title="❌ Verification Error",
                                colour=nextcord.Colour.red(),
                                description=f"Your time has ran out! Please re-run the `/verify` command in {interaction.guild.name}!"
                            )

                            embed_error_time.timestamp = datetime.now()

                            await channel.send(embed=embed_error_time)

                            in_verify_info = {"_id":interaction.user.id, "in_verification":False}
                    
                            try:
                                in_verification_collection.insert_one(in_verify_info)
                            except:
                                in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":False}})
                            
                            break

                        if isinstance(msg.channel, nextcord.channel.DMChannel):
                            if msg and msg.author != "Mivel":
                                try:
                                    print(str(msg.content))
                                    username = await roblox_client.get_user_by_username(str(msg.content), expand=True)
                                except:
                                    embed_fail = Embed(
                                        title="❌ Verification Error",
                                        color=nextcord.Color.red(),
                                        description=f"You did not type a correct username. Please re-run the verification process in {interaction.guild.name}. If you think this is an error, you can join our support server here: [Support Server](https://discord.gg/HvPTFMfPRy)"
                                    )

                                    embed_fail.timestamp = datetime.now()
                                    await msg.reply(embed=embed_fail)
                                    break
                                    
                                    
                                    
                                in_verify_info = {"_id":interaction.user.id, "in_verification":False}
                    
                                try:
                                    in_verification_collection.insert_one(in_verify_info)
                                except:
                                    in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":False}})


                                embed_success_one = Embed(
                                    title="✅ Step 1 Completed",
                                    color=nextcord.Color.green(),
                                    description="You completed step 1 successfully! For the next step, paste `verificationbotpasteconfirmaccount` into your roblox profile description and type `confirm` here. You have 2 minutes to complete this step. To cancel, simply type `cancel`."
                                )

                                embed_success_one.timestamp = datetime.now()
                                
                                await msg.reply(embed=embed_success_one)
                                try:
                                    msg_confirm = await self.client.wait_for('message', timeout=120.0, check=check)
                                except asyncio.TimeoutError:
                                    embed_error_time = nextcord.Embed(
                                        title="❌ Verification Error",
                                        colour=nextcord.Colour.red(),
                                        description=f"Your time has ran out! Please re-run the `/verify` command in {interaction.guild.name}!"
                                    )

                                    embed_error_time.timestamp = datetime.now()

                                    await channel.send(embed=embed_error_time)

                                    in_verify_info = {"_id":interaction.user.id, "in_verification":False}
                    
                                    try:
                                        in_verification_collection.insert_one(in_verify_info)
                                    except:
                                        in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":False}})

                                    break

                                if isinstance(msg_confirm.channel, nextcord.channel.DMChannel):
                                    if msg_confirm.content.lower() == "confirm":
                                        updated_username = await roblox_client.get_user_by_username(str(username.name), expand=True)

                                        if updated_username.description == "verificationbotpasteconfirmaccount":
                                            embed_success_two = Embed(
                                                title="✅ Verification Completed",
                                                color=nextcord.Color.green(),
                                                description=f"You have completed the verification process! The roblox account you linked is `@{username.name}`. You now have the verified role in {interaction.guild.name}"
                                            )

                                            embed_success_two.timestamp = datetime.now()

                                            await msg_confirm.reply(embed=embed_success_two)


                                            
                                            embed_updated = Embed(title=f"Info for {username.name}")
                                            embed_updated.add_field(
                                                name="Username",
                                                value="`" + username.name + "`"
                                            )
                                            embed_updated.add_field(
                                                name="Display Name",
                                                value="`" + username.display_name + "`"
                                            )
                                            embed_updated.add_field(
                                                name="User ID",
                                                value="`" + str(username.id) + "`"
                                            )
                                            
                                            embed_updated.add_field(
                                                name="Date Created",
                                                value="`"+username.created.strftime("%m/%d/%Y, %H:%M:%S")+"`"
                                            )
                                            embed_updated.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={username.id}&width=420&height=420&format=png")

                                            embed_updated.add_field(
                                                name="Description",
                                                value="```" +
                                                (nextcord.utils.escape_markdown(
                                                    username.description or "No description")) + "```",
                                                inline=False
                                            )

                                            embed_updated.color = nextcord.Color.green()

                                            embed_updated.timestamp = datetime.now()

                                            await msg_confirm.channel.send(embed=embed_updated)

  
                                            in_verify_info = {"_id":interaction.user.id, "in_verification":False}
                                    
                                            try:
                                                in_verification_collection.insert_one(in_verify_info)
                                            except:
                                                in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":False}})
                                            
                                            
                                            roblox_info = {"_id":interaction.user.id, "roblox_user_id": updated_username.id}
                                            
                                            try:
                                                user_userid_collection.insert_one(roblox_info)
                                            except:
                                                user_userid_collection.update({"_id":interaction.user.id},{"$set":{"roblox_user_id": updated_username.id}})
                                            print(role)
                                            
                                            role_val = nextcord.utils.get(interaction.guild.roles, id=role)
                                            await interaction.user.add_roles(role_val)

                                            break
                                        else:


                                            embed_fail_two = Embed(
                                                title="❌ Verification Error",
                                                color=nextcord.Color.red(),
                                                description=f"You did not type the correct text into your roblox profile description. Be sure to type `verificationbotpasteconfirmaccount`. Please re-run the verification process in {interaction.guild.name}. If you think this is an error, you can join our support server here: [Support Server](https://discord.gg/HvPTFMfPRy)"
                                            )
                                            embed_fail_two.timestamp = datetime.now()

                                            await msg_confirm.reply(embed=embed_fail_two)

                                            in_verify_info = {"_id":interaction.user.id, "in_verification":False}
                                    
                                            try:
                                                in_verification_collection.insert_one(in_verify_info)
                                            except:
                                                in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":False}})
                                            break
                                    else:
                                        embed_quit = Embed(
                                            title="❌ Verification Quit",
                                            color=nextcord.Color.red(),
                                            description=f"You have successfully quit the verification process"
                                        )
                                        embed_quit.timestamp = datetime.now()

                                        await msg_confirm.reply(embed=embed_quit)

                                        in_verify_info = {"_id":interaction.user.id, "in_verification":False}
                                    
                                        try:
                                            in_verification_collection.insert_one(in_verify_info)
                                        except:
                                            in_verification_collection.update({"_id":interaction.user.id},{"$set":{"in_verification":False}})

                                        break

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
