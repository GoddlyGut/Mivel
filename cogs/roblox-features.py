import asyncio
from roblox.thumbnails import Thumbnail, AvatarThumbnailType
import sqlite3
import nextcord
from nextcord import Embed, Guild, Member, member
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord import Interaction, SlashOption, ChannelType
from datetime import datetime, timedelta
import roblox
from roblox.thumbnails import AvatarThumbnailType
roblox_client = roblox.Client()



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
        db_roblox_userid = sqlite3.connect('roblox_userid.sqlite')
        cursor_roblox_userid = db_roblox_userid.cursor()
        cursor_roblox_userid.execute(f"SELECT roblox_user_id FROM main WHERE user_id = {interaction.user.id}")
        result_roblox_userid = cursor_roblox_userid.fetchone()
        
        if result_roblox_userid is None:
            await interaction.response.send_message(f"{interaction.user.mention}, You need to verify yourself before using this command!")
        else:
            user = await roblox_client.get_user(int(result_roblox_userid[0]))

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
        db_roblox_userid = sqlite3.connect('roblox_userid.sqlite')
        cursor_roblox_userid = db_roblox_userid.cursor()
        cursor_roblox_userid.execute(f"SELECT roblox_user_id FROM main WHERE user_id = {member.id}")
        result_roblox_userid = cursor_roblox_userid.fetchone()
        
        if result_roblox_userid is None:
            await interaction.response.send_message(f"{interaction.user.mention}, This member has not verified themselves!")
        else:
            user = await roblox_client.get_user(int(result_roblox_userid[0]))

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
    async def verify_proccess(self, ctx):
        embed = nextcord.Embed(
            title="Server Info",
            colour=nextcord.Colour.blurple(),
            description="Available Setup Commands: \n`m!verify_proccess setup`\n`m!verify_proccess disable`\n`m!verify_proccess enable`",

        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

    @verify_proccess.command()
    async def setup(self, ctx, role: nextcord.Role):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('verify.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT role FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()

            cursor_role = db.cursor()
            cursor_role.execute(
                f"SELECT role FROM main WHERE guild_id = {ctx.guild.id}")
            result_role = cursor_role.fetchone()

            embed = Embed(
                title="Verification Setup",
                color=nextcord.Colour.green(),
                description=f"The verified role has been set to {role.mention}"
            )

            embed.timestamp = datetime.now()

            if result is None:
                sql = ("INSERT INTO main(guild_id, role) VALUES(?,?)")
                val = (ctx.guild.id, role.id)
                await ctx.reply(embed=embed)
            elif result is not None:
                sql = ("UPDATE main SET role = ? WHERE guild_id = ?")
                val = (role.id, ctx.guild.id)
                await ctx.reply(embed=embed)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

        else:
            embed_error_perms = nextcord.Embed(
                title="Error",
                colour=nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )

            embed_error_perms.timestamp = datetime.now()

            await ctx.reply(embed=embed_error_perms)

    @setup.error
    async def setup_error(self, ctx, error):
        embed = nextcord.Embed(
            title="Error",
            colour=nextcord.Colour.red(),
            description=error
        )

        embed.timestamp = datetime.now()
        await ctx.reply(embed=embed)

    @verify_proccess.command()
    async def disable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('verify.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT Enabled FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()

            cursor_role = db.cursor()
            cursor_role.execute(f"SELECT role FROM main WHERE guild_id = {ctx.guild.id}")
            result_role = cursor_role.fetchone()

            if result_role != None:
                embed = Embed(
                    title="Verification Setup",
                    color=nextcord.Colour.green(),
                    description=f"The verification system has been disabled!"
                )

                embed.timestamp = datetime.now()

                if result is None:
                    sql = ("INSERT INTO main(guild_id, Enabled) VALUES(?,?)")
                    val = (ctx.guild.id, "False")
                    await ctx.reply(embed=embed)
                elif result is not None:
                    sql = ("UPDATE main SET Enabled = ? WHERE guild_id = ?")
                    val = ("False", ctx.guild.id)
                    await ctx.reply(embed=embed)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
            else:
                embed_error_setup = nextcord.Embed(
                    title="Verification Error",
                    colour=nextcord.Colour.red(),
                    description="The verification system has not been setup!"
                )

                embed_error_setup.timestamp = datetime.now()

                await ctx.reply(embed=embed_error_setup)
        else:
            embed_error_perms = nextcord.Embed(
                title="Error",
                colour=nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )

            embed_error_perms.timestamp = datetime.now()

            await ctx.reply(embed=embed_error_perms)

    @verify_proccess.command()
    async def enable(self, ctx):
        if ctx.author.guild_permissions.administrator:
            db = sqlite3.connect('verify.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT Enabled FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()

            cursor_role = db.cursor()
            cursor_role.execute(f"SELECT role FROM main WHERE guild_id = {ctx.guild.id}")
            result_role = cursor_role.fetchone()

            if result_role != None:

                embed = Embed(
                    title="Verification Setup",
                    color=nextcord.Colour.green(),
                    description=f"The verification system has been enabled!"
                )

                embed.timestamp = datetime.now()

                if result is None:
                    sql = ("INSERT INTO main(guild_id, Enabled) VALUES(?,?)")
                    val = (ctx.guild.id, "True")
                    await ctx.reply(embed=embed)
                elif result is not None:
                    sql = ("UPDATE main SET Enabled = ? WHERE guild_id = ?")
                    val = ("True", ctx.guild.id)
                    await ctx.reply(embed=embed)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
            else:
                embed_error_setup = nextcord.Embed(
                    title="Verification Error",
                    colour=nextcord.Colour.red(),
                    description="The verification system has not been setup!"
                )

                embed_error_setup.timestamp = datetime.now()

                await ctx.reply(embed=embed_error_setup)
        else:
            embed_error_perms = nextcord.Embed(
                title="Error",
                colour=nextcord.Colour.red(),
                description="You do not have the required permissions!"
            )

            embed_error_perms.timestamp = datetime.now()

            await ctx.reply(embed=embed_error_perms)

    @nextcord.slash_command(name="verify", description="Use this command to link your roblox account with your discord account!")
    async def verify(self, interaction: Interaction):
        db = sqlite3.connect('verify.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT Enabled FROM main WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()

        cursor_role = db.cursor()
        cursor_role.execute(f"SELECT role FROM main WHERE guild_id = {interaction.guild.id}")
        result_role = cursor_role.fetchone()

        db_verification = sqlite3.connect('in_verification.sqlite')
        cursor_verification = db_verification.cursor()
        cursor_verification.execute(f"SELECT in_verification FROM main WHERE user_id = {interaction.user.id}")
        result_verification = cursor_verification.fetchone()

        db_roblox_userid = sqlite3.connect('roblox_userid.sqlite')
        cursor_roblox_userid = db_roblox_userid.cursor()
        cursor_roblox_userid.execute(f"SELECT roblox_user_id FROM main WHERE user_id = {interaction.user.id}")
        result_roblox_userid = cursor_roblox_userid.fetchone()

        def check(m):
<<<<<<< HEAD
            return interaction.user == m.author
=======
            return interaction.user == m.au
>>>>>>> aa5f0954c2dd112317c80d97175a8ffea795b161

        if result_role != None:
            if result[0] is None or result[0] == "True":
                role = nextcord.utils.get(
                    interaction.guild.roles, id=int(result_role[0]))
                
                if result_verification is None or result_verification[0] == "False" or result_verification[0] is None:

                    if result_verification is None:
                        sql = ("INSERT INTO main(user_id, in_verification) VALUES(?,?)")
                        val = (interaction.user.id, "True")
                    elif result_verification is not None:
                        sql = ("UPDATE main SET in_verification = ? WHERE user_id = ?")
                        val = ("True", interaction.user.id)

                    cursor_verification.execute(sql, val)
                    db_verification.commit()

                    channel = await interaction.user.create_dm()

                    await interaction.response.send_message(f"{interaction.user.mention}, please check your dms!")


                    embed_setup = Embed(
                        title="Verification Process",
                        color=nextcord.Colour.blurple(),
                        description=f"This message will guide you on how to get verified in {interaction.guild.name}",
                    )
                    # embed_setup.author(name="Mivel",icon_url=self.client.user.display_avatar.url)
                    embed_setup.add_field(
                        name="Step 1", value="Please go to `roblox.com` and paste your username in this dm. You have 1 minute to complete this step.", inline=False)
                    embed_setup.add_field(
                        name="Step 2", value="Once finished with the above step, paste this value into your roblox profile description `mivelverificationtext`. **Be sure to change this once you are completed with the verification process!**", inline=False)
                    embed_setup.add_field(
                        name="Step 3", value=f"Once finished with the above step, type `confirm` and you will be granted the verified role in {interaction.guild.name}", inline=False)
                    embed_setup.timestamp = datetime.now()
                    await channel.send(embed=embed_setup)

                    while True:
                        try:
                            msg = await self.client.wait_for('message', timeout=60.0, check=check)
                        except asyncio.TimeoutError:
                            embed_error_time = nextcord.Embed(
                                title="Verification Error",
                                colour=nextcord.Colour.red(),
                                description=f"Your time has ran out! Please re-run the `/verify` command in {interaction.guild.name}!"
                            )

                            embed_error_time.timestamp = datetime.now()

                            await channel.send(embed=embed_error_time)

                            if result_verification[0] is None:
                                sql_false = ("INSERT INTO main(user_id, in_verification) VALUES(?,?)")
                                val_false = (interaction.user.id, "False")
                            elif result_verification[0] is not None:
                                sql_false = ("UPDATE main SET in_verification = ? WHERE user_id = ?")
                                val_false = ("False", interaction.user.id)

                                cursor_verification.execute(sql_false, val_false)
                                db_verification.commit()
                                cursor_verification.close()
                                db_verification.close()

                                break

                        if isinstance(msg.channel, nextcord.channel.DMChannel):
                            if msg and msg.author != "Mivel":
                                try:
                                    username = await roblox_client.get_user_by_username(str(msg.content), expand=True)
                                except:
                                    embed_fail = Embed(
                                        title="Verification Error",
                                        color=nextcord.Color.red(),
                                        description=f"You did not type a correct username. Please re-run the verification process in {interaction.guild.name}."
                                    )

                                    embed_fail.timestamp = datetime.now()

                                    await msg.reply(embed=embed_fail)

                                    cursor_verification_updated = db_verification.cursor()
                                    cursor_verification_updated.execute(f"SELECT in_verification FROM main WHERE user_id = {interaction.user.id}")
                                    result_verification_updated = cursor_verification_updated.fetchone()

                                    if result_verification_updated is None:
                                        sql_false = ("INSERT INTO main(user_id, in_verification) VALUES(?,?)")
                                        val_false = (interaction.user.id, "False")
                                    elif result_verification_updated is not None:
                                        sql_false = ("UPDATE main SET in_verification = ? WHERE user_id = ?")
                                        val_false = ("False", interaction.user.id)

                                    cursor_verification.execute(sql_false, val_false)
                                    db_verification.commit()
                                    cursor_verification.close()
                                    db_verification.close()

                                    break

                                embed_success_one = Embed(
                                    title="Step 1 Completed",
                                    color=nextcord.Color.green(),
                                    description="You completed step 1 successfully! For the next step, paste `mivelverificationtext` into your roblox profile description and type `confirm` here. You have 2 minutes to complete this step. To cancel, simply type `cancel`."
                                )

                                embed_success_one.timestamp = datetime.now()

                                await msg.reply(embed=embed_success_one)
                                try:
                                    msg_confirm = await self.client.wait_for('message', timeout=120.0, check=check)
                                except asyncio.TimeoutError:
                                    embed_error_time = nextcord.Embed(
                                        title="Verification Error",
                                        colour=nextcord.Colour.red(),
                                        description=f"Your time has ran out! Please re-run the `/verify` command in {interaction.guild.name}!"
                                    )

                                    embed_error_time.timestamp = datetime.now()

                                    await channel.send(embed=embed_error_time)

                                    if result_verification is None:
                                        sql_false = ("INSERT INTO main(user_id, in_verification) VALUES(?,?)")
                                        val_false = (
                                            interaction.user.id, "False")
                                    elif result_verification is not None:
                                        sql_false = ("UPDATE main SET in_verification = ? WHERE user_id = ?")
                                        val_false = ("False", interaction.user.id)

                                    cursor_verification.execute(sql_false, val_false)
                                    db_verification.commit()
                                    cursor_verification.close()
                                    db_verification.close()

                                    break

                                if isinstance(msg_confirm.channel, nextcord.channel.DMChannel):
                                    if msg_confirm.content.lower() == "confirm":
                                        updated_username = await roblox_client.get_user_by_username(str(username.name), expand=True)

                                        if updated_username.description == "mivelverificationtext":
                                            embed_success_two = Embed(
                                                title="Verification Completed",
                                                color=nextcord.Color.green(),
                                                description=f"You have completed the verification process! The roblox account you linked is `@{username.name}`. You now have the verified role in {interaction.guild.name}"
                                            )

                                            embed_success_two.timestamp = datetime.now()

                                            await msg_confirm.reply(embed=embed_success_two)

  

                                            cursor_verification_updated = db_verification.cursor()
                                            cursor_verification_updated.execute(f"SELECT in_verification FROM main WHERE user_id = {interaction.user.id}")
                                            result_verification_updated = cursor_verification_updated.fetchone()

                                            if result_verification_updated is None:
                                                sql_false = ("INSERT INTO main(user_id, in_verification) VALUES(?,?)")
                                                val_false = (interaction.user.id, "False")
                                            elif result_verification_updated is not None:
                                                sql_false = ("UPDATE main SET in_verification = ? WHERE user_id = ?")
                                                val_false = ("False", interaction.user.id)

                                            cursor_verification.execute(sql_false, val_false)
                                            db_verification.commit()
                                            cursor_verification.close()
                                            db_verification.close()
                                            
                                            

                                            
                                            if result_roblox_userid is None:
                                                sql_roblox = ("INSERT INTO main(user_id, roblox_user_id) VALUES(?,?)")
                                                val_roblox = (interaction.user.id, updated_username.id)
                                            elif result_roblox_userid is not None:
                                                sql_roblox = ("UPDATE main SET roblox_user_id = ? WHERE user_id = ?")
                                                val_roblox = (updated_username.id, interaction.user.id)
                                            
                                            cursor_roblox_userid.execute(sql_roblox, val_roblox)
                                            db_roblox_userid.commit()
                                            cursor_roblox_userid.close()
                                            db_roblox_userid.close()
                                            
                                            role = nextcord.utils.get(interaction.guild.roles, id=int(result_role[0]))
                                            await interaction.user.add_roles(role)

                                            break
                                        else:
                                            cursor_verification_updated = db_verification.cursor()
                                            cursor_verification_updated.execute(f"SELECT in_verification FROM main WHERE user_id = {interaction.user.id}")
                                            result_verification_updated = cursor_verification_updated.fetchone()

                                            embed_fail_two = Embed(
                                                title="Verification Error",
                                                color=nextcord.Color.red(),
                                                description=f"You did not type the correct text into your roblox profile description. Be sure to type `mivelverificationtext`. Please re-run the verification process in {interaction.guild.name}."
                                            )
                                            embed_fail_two.timestamp = datetime.now()

                                            await msg_confirm.reply(embed=embed_fail_two)

                                            if result_verification_updated is None:
                                                sql_false = ("INSERT INTO main(user_id, in_verification) VALUES(?,?)")
                                                val_false = (interaction.user.id, "False")
                                            elif result_verification_updated is not None:
                                                sql_false = ("UPDATE main SET in_verification = ? WHERE user_id = ?")
                                                val_false = ("False", interaction.user.id)

                                            cursor_verification.execute(sql_false, val_false)
                                            db_verification.commit()
                                            cursor_verification.close()
                                            db_verification.close()
                                            break
                                    else:
                                        embed_quit = Embed(
                                            title="Verification Quit",
                                            color=nextcord.Color.red(),
                                            description=f"You have successfully quit the verification process"
                                        )
                                        embed_quit.timestamp = datetime.now()

                                        await msg_confirm.reply(embed=embed_quit)

                                        cursor_verification_updated = db_verification.cursor()
                                        cursor_verification_updated.execute(f"SELECT in_verification FROM main WHERE user_id = {interaction.user.id}")
                                        result_verification_updated = cursor_verification_updated.fetchone()

                                        if result_verification_updated is None:
                                            sql_false = ("INSERT INTO main(user_id, in_verification) VALUES(?,?)")
                                            val_false = (interaction.user.id, "False")
                                        elif result_verification_updated is not None:
                                            sql_false = ("UPDATE main SET in_verification = ? WHERE user_id = ?")
                                            val_false = ("False", interaction.user.id)
                                        cursor_verification.execute(sql_false, val_false)
                                        db_verification.commit()
                                        cursor_verification.close()
                                        db_verification.close()

                                        break

                else:
                    embed_error_progress = nextcord.Embed(
                        title="Verification Error",
                        colour=nextcord.Colour.red(),
                        description="You already are in the verification process!"
                    )

                    embed_error_progress.timestamp = datetime.now()

                    await interaction.response.send_message(embed=embed_error_progress)

            else:
                embed_error_disable = nextcord.Embed(
                    title="Verification Error",
                    colour=nextcord.Colour.red(),
                    description="The verification system has been disabled!"
                )

                embed_error_disable.timestamp = datetime.now()
                await interaction.response.send_message(embed=embed_error_disable)
        else:
            embed_error_setup = nextcord.Embed(
                title="Verification Error",
                colour=nextcord.Colour.red(),
                description="The verification system has not been setup!"
            )

            embed_error_setup.timestamp = datetime.now()

            await interaction.response.send_message(embed=embed_error_setup)


def setup(client):
    client.add_cog(roblox_features(client))
