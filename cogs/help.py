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
        embed.add_field(name="Ticket Setup Commands", value="`m!ticket_settings role <@role>`\n`m!ticket_settings message <'message'>`\n`m!ticket_settings enable`\n`m!ticket_settings disable`\n",inline=False)
        embed.add_field(name="Suggest Setup Commands", value="`m!suggest_settings channel <#channel>`\n`m!suggest_settings enable`\n`m!suggest_settings disable`\n",inline=False)
        embed.add_field(name="Welcome Setup Commands", value="`m!welcome_settings channel <#channel>`\n`m!welcome_settings enable`\n`m!welcome_settings disable`\n",inline=False)
        embed.add_field(name="Server Stats Setup Commands", value="`m!server_info setup_members`\n`m!server_info disable_members`\n`m!server_info setup_bots`\n`m!server_info disable_bots`\n`m!server_info setup_game <PlaceId>`\n`m!server_info disable_game`\n`m!server_info setup_group <GroupId>`\n`m!server_info disable_group`\n`m!server_info setup_favorites <PlaceId>`\n`m!server_info disable_favorites`",inline=False)
        embed.add_field(name="Verify Setup Commands", value="`m!verify_process setup <@role>`\n`m!verify_process disable`\n`m!verify_process enable`",inline=False)

        embed.set_footer(text="Programmed by GoddlyGut#0001")
        embed.set_author(name="Mivel",icon_url=self.client.user.display_avatar.url)
        embed.color = nextcord.Color.blurple()

        await interaction.response.send_message(embed=embed)
        
        
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
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
            embed.add_field(name="Ticket Setup Commands", value="`m!ticket_settings role <@role>`\n`m!ticket_settings message <'message'>`\n`m!ticket_settings enable`\n`m!ticket_settings disable`\n",inline=False)
            embed.add_field(name="Suggest Setup Commands", value="`m!suggest_settings channel <#channel>`\n`m!suggest_settings enable`\n`m!suggest_settings disable`\n",inline=False)
            embed.add_field(name="Welcome Setup Commands", value="`m!welcome_settings channel <#channel>`\n`m!welcome_settings enable`\n`m!welcome_settings disable`\n",inline=False)
            embed.add_field(name="Server Stats Setup Commands", value="`m!server_info setup_members`\n`m!server_info disable_members`\n`m!server_info setup_bots`\n`m!server_info disable_bots`\n`m!server_info setup_game <PlaceId>`\n`m!server_info disable_game`\n`m!server_info setup_group <GroupId>`\n`m!server_info disable_group`\n`m!server_info setup_favorites <PlaceId>`\n`m!server_info disable_favorites`",inline=False)
            embed.add_field(name="Verify Setup Commands", value="`m!verify_process setup <@role>`\n`m!verify_process disable`\n`m!verify_process enable`",inline=False)

            embed.set_footer(text="Programmed by GoddlyGut#0001")
            embed.set_author(name="Mivel",icon_url=self.client.user.display_avatar.url)
            embed.color = nextcord.Color.blurple()
            await general.send(embed=embed)
def setup(client):
    client.add_cog(help(client))