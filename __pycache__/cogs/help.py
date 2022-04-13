from nextcord import Embed, Member
from nextcord.ui import Button, View
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
            description="This is a list of available setup commands provided by Mivel! Run these commands to get a list of setup options! **Other commands are slash-commands!** If you need support, you can join our support server!",
        )
        embed.add_field(name="⚙️ Default Prefix", value="```m!```",inline=False)
        embed.add_field(name="📜 Ticket System", value="```m!ticket help```")
        embed.add_field(name="✏️ Suggest System", value="```m!suggestion help```")
        embed.add_field(name="👋 Welcome System", value="```m!welcome help```")
        embed.add_field(name="📈 Server System", value="```m!stats help```")
        embed.add_field(name="✅ Verify System", value="```m!verify help```")
        embed.add_field(name="📣 Promote System", value="```m!promote help```")
        embed.set_footer(text="Programmed by GoddlyGut#0001")
        embed.set_author(name="Mivel",icon_url=self.client.user.display_avatar.url)
        embed.color = nextcord.Color.blurple()

        link = Button(label="Link to Support Server", url="https://discord.gg/HvPTFMfPRy", style=nextcord.ButtonStyle.blurple)
        view=View()
        view.add_item(link)

        await interaction.response.send_message(embed=embed, view=view)
        
        
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        channel = await guild.owner.create_dm()
        embed_joined = Embed(
            title="Mivel",
            color=nextcord.Colour.green(),
            description="Hey there! Thanks for adding Mivel to your server! All the server setup commands can be accessed by typing `/help` in your server channel. If you have any questions, you can join our discord here: [Support Server](https://discord.gg/HvPTFMfPRy)"
        )
        
        embed_joined.timestamp = datetime.now()
        await channel.send(embed=embed_joined)
        
        
        general = find(lambda x: x.name == 'general',  guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            embed = nextcord.Embed(
                title="Commands",
                description="This is a list of available setup commands provided by Mivel! Run these commands to get a list of setup options! **Other commands are slash-commands!** If you need support, you can join our support server!",
            )
            embed.add_field(name="⚙️ Default Prefix", value="```m!```",inline=False)
            embed.add_field(name="📜 Ticket System", value="```m!ticket help```")
            embed.add_field(name="✏️ Suggest System", value="```m!suggestion help```")
            embed.add_field(name="👋 Welcome System", value="```m!welcome help```")
            embed.add_field(name="📈 Server System", value="```m!stats help```")
            embed.add_field(name="✅ Verify System", value="```m!verify help```")
            embed.add_field(name="📣 Promote System", value="```m!promote help```")
            embed.set_footer(text="Programmed by GoddlyGut#0001")
            embed.set_author(name="Mivel",icon_url=self.client.user.display_avatar.url)
            embed.color = nextcord.Color.blurple()

            link = Button(label="Link to Support Server", url="https://discord.gg/HvPTFMfPRy", style=nextcord.ButtonStyle.blurple)
            view=View()
            view.add_item(link)

            await general.send(embed=embed, view=view)
def setup(client):
    client.add_cog(help(client))