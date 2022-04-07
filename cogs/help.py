from cgitb import text
from http import client
from unicodedata import name
from nextcord import Embed, Member
from nextcord.ext import commands
import nextcord
from nextcord import GuildSticker, Interaction
from nextcord.ext.commands import MissingPermissions, has_permissions
from datetime import datetime
from nextcord.utils import find

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    
    @nextcord.slash_command(name="help", description="Use this command to get a list of commands!")
    async def help(self, interaction:Interaction):
        embed = nextcord.Embed(
            title="Commands",
            description="This is a list of available commands provided by Mivel!",
        )
        embed.add_field(name="Default Prefix", value="`m!`")
        embed.add_field(name="General Commands", value="`/help`\n`/meme`\n`/ticket`\n`/suggest`\n`/verify`\n",inline=False)
        embed.add_field(name="Roblox Commands", value="`/roblox-user-search`\n`/roblox-user-info`\n`/other-roblox-user-info`",inline=False)
        embed.add_field(name="Moderation Commands", value="`/ban`\n`/unban`\n`/kick`\n`/timeout`\n`/purge`\n`/purge-member`\n`/lockdown`\n`/unlock`\n",inline=False)
        embed.add_field(name="Ticket Setup Commands", value="`m!ticket role <@role>`\n`m!ticket message <'message'>`\n`m!ticket disable`\n`m!ticket enable`\n",inline=False)
        embed.add_field(name="Suggest Setup Commands", value="`m!suggestion channel <#channel>`\n`m!suggestion disable`\n`m!suggestion enable`\n",inline=False)
        embed.add_field(name="Welcome Setup Commands", value="`m!welcome channel <#channel>`\n`m!welcome message <Message>`\n`m!welcome enable`\n`m!welcome disable`\n",inline=False)
        embed.add_field(name="Server Stats Setup Commands", value="`m!stats setup_members`\n`m!stats disable_members`\n`m!stats setup_bots`\n`m!stats disable_bots`\n`m!stats setup_game <PlaceId>`\n`m!stats disable_game`\n`m!stats setup_group <GroupId>`\n`m!stats disable_group`\n`m!stats setup_favorites <PlaceId>`\n`m!stats disable_favorites`",inline=False)
        embed.add_field(name="Verify Setup Commands", value="`m!verify setup <@role>`\n`m!verify disable`\n`m!verify enable`",inline=False)
        embed.set_footer(text="Programmed by GoddlyGut#0001")
        embed.set_author(name="Mivel",icon_url=self.client.user.display_avatar.url)
        embed.color = nextcord.Color.blurple()

        await interaction.response.send_message(embed=embed)
        
        
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        channel = await guild.owner.create_dm()
        embed_joined = Embed(
            title="Mivel",
            color=nextcord.Colour.green(),
            description="Hey there! Thanks for adding Mivel to your server! All the server commands can be accessed by typing `/help` in your server channel. If you have any questions, you can join our discord here: [Support Server](https://discord.gg/HvPTFMfPRy)"
        )
        
        embed_joined.timestamp = datetime.now()
        await channel.send(embed=embed_joined)
        
        
        general = find(lambda x: x.name == 'general',  guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            embed = nextcord.Embed(
                title="Commands",
                description="This is a list of available commands provided by Mivel!",
            )
            embed.add_field(name="Default Prefix", value="`m!`")
            embed.add_field(name="General Commands", value="`/help`\n`/meme`\n`/ticket`\n`/suggest`\n`/verify`\n",inline=False)
            embed.add_field(name="Roblox Commands", value="`/roblox-user-search`\n`/roblox-user-info`\n`/other-roblox-user-info`",inline=False)
            embed.add_field(name="Moderation Commands", value="`/ban`\n`/unban`\n`/kick`\n`/timeout`\n`/purge`\n`/purge-member`\n`/lockdown`\n`/unlock`\n",inline=False)
            embed.add_field(name="Ticket Setup Commands", value="`m!ticket role <@role>`\n`m!ticket message <'message'>`\n`m!ticket disable`\n`m!ticket enable`\n",inline=False)
            embed.add_field(name="Suggest Setup Commands", value="`m!suggestion channel <#channel>`\n`m!suggestion disable`\n`m!suggestion enable`\n",inline=False)
            embed.add_field(name="Welcome Setup Commands", value="`m!welcome channel <#channel>`\n`m!welcome message <Message>`\n`m!welcome enable`\n`m!welcome disable`\n",inline=False)
            embed.add_field(name="Server Stats Setup Commands", value="`m!stats setup_members`\n`m!stats disable_members`\n`m!stats setup_bots`\n`m!stats disable_bots`\n`m!stats setup_game <PlaceId>`\n`m!stats disable_game`\n`m!stats setup_group <GroupId>`\n`m!stats disable_group`\n`m!stats setup_favorites <PlaceId>`\n`m!stats disable_favorites`",inline=False)
            embed.add_field(name="Verify Setup Commands", value="`m!verify setup <@role>`\n`m!verify disable`\n`m!verify enable`",inline=False)

            embed.set_footer(text="Programmed by GoddlyGut#0001")
            embed.set_author(name="Mivel",icon_url=self.client.user.display_avatar.url)
            embed.color = nextcord.Color.blurple()
            await general.send(embed=embed)
def setup(client):
    client.add_cog(help(client))