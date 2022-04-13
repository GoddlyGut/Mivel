from nextcord import Embed, Member
from nextcord.ui import Button, View
from nextcord.ext import commands
import nextcord
from nextcord import GuildSticker, Interaction
from nextcord.ext.commands import MissingPermissions, has_permissions
from datetime import datetime
from nextcord.utils import find
import pymongo
from pymongo import MongoClient
import asyncio

class promotion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def promote(self, ctx):
        embed = nextcord.Embed(
            title="📦 Available Setup Commands:",
            colour=nextcord.Colour.blurple(),
            description="```m!promote setup <#channel>```**Allows you to setup the promotion channel**\n```m!promote disable```**Allows you to disable the promotion system**\n```m!promote enable```**Allows you to enabled the promotion system**\n",

        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

    @promote.command()
    async def setup(self, ctx, channel:nextcord.TextChannel):
        if ctx.author.guild_permissions.administrator:

            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["promotion_collection"]

            channel_data = None
            enabled = None

            for x in collection.find({"_id": ctx.guild.id}):
                channel_data = x["channel"]
                enabled = x["enabled"]

            promotion_info = {"_id":ctx.guild.id, "channel":channel.id, "enabled": True}

            try:
                collection.insert_one(promotion_info)
            except:
                collection.update({"_id":ctx.guild.id},{"$set":{"channel":channel.id}})

            embed=nextcord.Embed(
                title="",
                colour= nextcord.Colour.green(),
                description=f"✅ Promotion channel has been set to {channel.mention}!"
            )
                    
            
            await ctx.reply(embed=embed)

            
                
        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)

            return


    @promote.command()
    async def disable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["promotion_collection"]

            channel_data = None
            enabled = None

            for x in collection.find({"_id": ctx.guild.id}):
                channel_data = x["channel"]
                enabled = x["enabled"]

            if channel_data is None:
                embed_error_disable=nextcord.Embed(
                    title="",
                    colour= nextcord.Colour.red(),
                    description="❌ Please setup the promotion bot before disabling it!"
                )
                    
            
                await ctx.reply(embed=embed_error_disable)
            else:
                promotion_info = {"_id":ctx.guild.id, "channel":channel_data, "enabled": False}

                try:
                    collection.insert_one(promotion_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"enabled":False}})

                embed=nextcord.Embed(
                    title="",
                    colour= nextcord.Colour.green(),
                    description=f"✅ Promotion channel has been disabled!"
                )
                        
                
                await ctx.reply(embed=embed)


        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)

            return 


    @promote.command()
    async def enable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            cluster = MongoClient(mongo_url)
            db = cluster["database"]
            collection = db["promotion_collection"]

            channel_data = None
            enabled = None

            for x in collection.find({"_id": ctx.guild.id}):
                channel_data = x["channel"]
                enabled = x["enabled"]

            if channel_data is None:
                embed_error_enabled=nextcord.Embed(
                    title="",
                    colour= nextcord.Colour.red(),
                    description="❌ Please setup the promotion bot before enabling it!"
                )
                    
            
                await ctx.reply(embed=embed_error_enabled)
            else:
                promotion_info = {"_id":ctx.guild.id, "channel":channel_data, "enabled": True}

                try:
                    collection.insert_one(promotion_info)
                except:
                    collection.update({"_id":ctx.guild.id},{"$set":{"enabled":True}})

                embed=nextcord.Embed(
                    title="",
                    colour= nextcord.Colour.green(),
                    description=f"✅ Promotion channel has been enabled!"
                )
                        
                
                await ctx.reply(embed=embed)


        else:
            embed_error_perms=nextcord.Embed(
                title="❌ Error",
                colour= nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )
                    
            embed_error_perms.timestamp = datetime.now()
            
            await ctx.reply(embed=embed_error_perms)

            return 

    @nextcord.slash_command(name="promote", description="Use this command to promote something you made!")
    async def promote_command(self, interaction:Interaction):
        mongo_url = "mongodb+srv://GoddlyGut:Chess123@cluster0.ardmx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["database"]
        collection = db["promotion_collection"]

        channel_data = None
        enabled = None

        for x in collection.find({"_id": interaction.guild.id}):
            channel_data = x["channel"]
            enabled = x["enabled"]

        if channel_data != None:
            if enabled == True:
                channel = await interaction.user.create_dm()

                embed_check_dm = nextcord.Embed(
                    title="",
                    description=f"{interaction.user.mention}, please check your dms!",
                    colour=nextcord.Colour.blurple()
                )
                
            
                await interaction.response.send_message(embed=embed_check_dm)

                embed_setup = Embed(
                    title="",
                    color=nextcord.Colour.blurple(),
                    description=f"Please specify the **item** you will be promoting(Ex: Group, Game, Server) If you want to cancel, simply type `.cancel`",
                )

                await channel.send(embed=embed_setup)

                def check(m):
                    return interaction.user == m.author

                while True:
                    try:
                        msg = await self.client.wait_for('message', timeout=120.0, check=check)
                    except asyncio.TimeoutError:
                        embed_error_time = nextcord.Embed(
                            title="❌ Promotion Error",
                            colour=nextcord.Colour.red(),
                            description=f"Your time has ran out! Please re-run the `/promote` command in {interaction.guild.name}!"
                        )

                        embed_error_time.timestamp = datetime.now()

                        await channel.send(embed=embed_error_time)

                        break

                    if isinstance(msg.channel, nextcord.channel.DMChannel):
                        if msg.content != ".cancel":
                            promotion_type = msg.content

                            embed_success_one = Embed(
                                title="",
                                color=nextcord.Color.blurple(),
                                description="Please specify a **name** for the item you will be posting. If you want to cancel, simply type `.cancel`"
                            )
                                
                            await msg.reply(embed=embed_success_one)
                            try:
                                msg_name = await self.client.wait_for('message', timeout=300.0, check=check)
                            except asyncio.TimeoutError:
                                embed_error_time = nextcord.Embed(
                                    title="❌ Promotion Error",
                                    colour=nextcord.Colour.red(),
                                    description=f"Your time has ran out! Please re-run the `/promote` command in {interaction.guild.name}!"
                                )

                                embed_error_time.timestamp = datetime.now()

                                await channel.send(embed=embed_error_time)

                                break

                            if isinstance(msg.channel, nextcord.channel.DMChannel):
                                if msg_name.content != ".cancel":
                                    item_name = msg_name.content

                                    embed_success_two = Embed(
                                        title="",
                                        color=nextcord.Color.blurple(),
                                        description="Please specify a **description** for the item you will be posting. If you want to cancel, simply type `.cancel`"
                                    )
                                        
                                    await msg.reply(embed=embed_success_two)
                                    try:
                                        msg_description = await self.client.wait_for('message', timeout=300.0, check=check)
                                    except asyncio.TimeoutError:
                                        embed_error_time = nextcord.Embed(
                                            title="❌ Promotion Error",
                                            colour=nextcord.Colour.red(),
                                            description=f"Your time has ran out! Please re-run the `/promote` command in {interaction.guild.name}!"
                                        )

                                        embed_error_time.timestamp = datetime.now()

                                        await channel.send(embed=embed_error_time)

                                        break

                                    if isinstance(msg_description.channel, nextcord.channel.DMChannel):
                                        if msg_description.content != ".cancel":
                                            promotion_description = msg_description.content
                                            embed_success_two = Embed(
                                                title="",
                                                color=nextcord.Color.blurple(),
                                                description="Please specify a **link** for the item you will be posting. If you want to cancel, simply type `.cancel`"
                                            )
                                                
                                            await msg.reply(embed=embed_success_two)

                                            try:
                                                msg_link = await self.client.wait_for('message', timeout=300.0, check=check)
                                            except asyncio.TimeoutError:
                                                embed_error_time = nextcord.Embed(
                                                    title="❌ Promotion Error",
                                                    colour=nextcord.Colour.red(),
                                                    description=f"Your time has ran out! Please re-run the `/promote` command in {interaction.guild.name}!"
                                                )

                                                embed_error_time.timestamp = datetime.now()

                                                await channel.send(embed=embed_error_time)

                                                break
                                            if isinstance(msg_link.channel, nextcord.channel.DMChannel):
                                                if msg_link.content != ".cancel":
                                                    link = msg_link.content

                                                    embed_success_three = Embed(
                                                        title="",
                                                        color=nextcord.Color.blurple(),
                                                        description="Please specify an **image**. If you don't want an image, type `None`. If you want to cancel, simply type `.cancel`"
                                                    )
                                                        
                                                    await msg.reply(embed=embed_success_three)


                                                    try:
                                                        msg_image = await self.client.wait_for('message', timeout=300.0, check=check)
                                                    except asyncio.TimeoutError:
                                                        embed_error_time = nextcord.Embed(
                                                            title="❌ Promotion Error",
                                                            colour=nextcord.Colour.red(),
                                                            description=f"Your time has ran out! Please re-run the `/promote` command in {interaction.guild.name}!"
                                                        )

                                                        embed_error_time.timestamp = datetime.now()

                                                        await channel.send(embed=embed_error_time)

                                                        break
                                                    if isinstance(msg_image.channel, nextcord.channel.DMChannel):
                                                        if msg_image.content != ".cancel":
                                                            
                                                            if msg_image.attachments == []:
                                                                image = None
                                                            else:
                                                                image = msg_image.attachments[0].url

                                                            channel_promote = self.client.get_channel(channel_data)

                                                            color_random = nextcord.Color.random()

                                                            embed_promote = nextcord.Embed(
                                                                title="**📣 Promotion**",
                                                                description=f"{interaction.user} is promoting a **{promotion_type}**!",
                                                                color=color_random
                                                            )

                                                            embed_promote.add_field(name="**Name:**", value=item_name, inline=None)
                                                            embed_promote.add_field(name="**Description:**", value=promotion_description, inline=None)
                                                            embed_promote.add_field(name="**Link:**", value=f"{link}", inline=None)
                                                            embed_promote.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
                                                            if image != None:
                                                                embed_promote.set_image(url=image)
                                                            
                                                            view = View()

                                                            yes_button = Button(label="Yes", style = nextcord.ButtonStyle.green)
                                                            no_button = Button(label="No", style = nextcord.ButtonStyle.red)

                                                            view.add_item(yes_button)
                                                            view.add_item(no_button)
                                                            

                                                            await channel.send("Does this look right?",embed=embed_promote, view=view)

                                                            async def yes_button_callback(interaction):
                                                                view.stop()
                                                                color_random = nextcord.Color.random()

                                                                embed_promote = nextcord.Embed(
                                                                    title="**📣 Promotion**",
                                                                    description=f"{interaction.user} is promoting a **{promotion_type}**!",
                                                                    color=color_random
                                                                )
                                                                embed_promote.add_field(name="**Name:**", value=item_name, inline=None)
                                                                embed_promote.add_field(name="**Description:**", value=promotion_description, inline=None)
                                                                embed_promote.add_field(name="**Link:**", value=f"{link}", inline=None)
                                                                embed_promote.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
                                                                if image != None:
                                                                    embed_promote.set_image(url=image)

                                                                await channel_promote.send(embed=embed_promote)

                                                                embed_success_posted = Embed(
                                                                    title="",
                                                                    description=f"✅ Successfully posted your promotion!"
                                                                )

                                                                await channel.send(embed=embed_success_posted)

                                                            async def no_button_callback(interaction):
                                                                embed_error_repeat=nextcord.Embed(
                                                                    title="",
                                                                    color=nextcord.Colour.red(),
                                                                    description="Hmm. Maybe try running the command again?"
                                                                )

                                                                await channel.send(embed=embed_error_repeat)

                                                            yes_button.callback = yes_button_callback
                                                            no_button.callback = no_button_callback


                                                            break
                                                        else:
                                                            embed_cancel=nextcord.Embed(
                                                                title="",
                                                                color=nextcord.Colour.green(),
                                                                description="✅ Cancelled Prompt"
                                                            )

                                                            await channel.send(embed=embed_cancel)

                                                            break
                                                else:
                                                                                                
                                                    embed_cancel=nextcord.Embed(
                                                        title="",
                                                        color=nextcord.Colour.green(),
                                                        description="✅ Cancelled Prompt"
                                                    )

                                                    await channel.send(embed=embed_cancel)

                                                    break
                                        else:
                                            embed_cancel=nextcord.Embed(
                                                title="",
                                                color=nextcord.Colour.green(),
                                                description="✅ Cancelled Prompt"
                                            )

                                            await channel.send(embed=embed_cancel)

                                            break

                                else:
                                    embed_cancel=nextcord.Embed(
                                        title="",
                                        color=nextcord.Colour.green(),
                                        description="✅ Cancelled Prompt"
                                    )

                                    await channel.send(embed=embed_cancel)

                                    break
                        else:
                            embed_cancel=nextcord.Embed(
                                title="",
                                color=nextcord.Colour.green(),
                                description="✅ Cancelled Prompt"
                            )

                            await channel.send(embed=embed_cancel)

                            break
            else:       

                embed_disabled=nextcord.Embed(
                    title="",
                    colour= nextcord.Colour.red(),
                    description="❌ The promotion bot has been disabled by the owner!"
                )
                    
            
                await interaction.response.send_message(embed=embed_disabled)

        else:
            embed_error=nextcord.Embed(
                title="",
                colour= nextcord.Colour.red(),
                description="❌ Please setup the promotion bot before using it!"
            )
                
        
            await interaction.response.send_message(embed=embed_error)

def setup(client):
    client.add_cog(promotion(client))