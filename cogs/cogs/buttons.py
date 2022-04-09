from nextcord.ext import commands
import nextcord
from nextcord import Interaction

class Subscriptions(nextcord.ui.View):
        def __init__(self):
            super().__init__(timeout = None)
            self.value = None
        
        @nextcord.ui.button(label="Subscribe", style=nextcord.ButtonStyle.blurple)
        async def subscribe(self, button: nextcord.ui.button, interaction: Interaction):
            await interaction.response.send_message("Thank you for subscribing", ephemeral=True)
            self.value = True
            #self.stop()    

class button(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
    
    @commands.command()
    async def button(self, ctx):
        view = Subscriptions()
        await ctx.send("You have two options:", view=view)
        await view.wait()   
        
    @commands.command()
    async def test(self, ctx):
        await ctx.send("Test")

def setup(client):
    client.add_cog(button(client))