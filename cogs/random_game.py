import nextcord
from nextcord import Guild, Member, member
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ui import Button, View
import datetime
import random
import roblox
roblox_client = roblox.Client("6E2C0CF7F4F7E2DCB1709C167EF155C4DCF29DCA9D9F2B91D9908D28B091941597004A87F31D06522D8BFAE02550F523549B290EEA74A2BB0FC9DC47B5818FA1625230B9C2D3F5C51DE9353670E1F5C34FE6D30A61E28EA6E4E7207C75D3BBBDA2956AAF252624EB2FAABA55F0986971AD106E8132ACCBB3C233F003B44BD55EEC52AE97843AD825B527BF29EA849115F7EFE9C3AEE89901BBE7CEB312FED484D9F633882C03111A6757E44C887845291CB3EB639ACFFD6CAE46554B76C8901A290C1BB20A11446C283C2145C3A2DC428399E5B4C6FA1E96331F9058B662734CD7254223304A56115A26216B1292216888383DED91236A6EAE291D85B7D6BA1AE020344B645A83D8C52B691FA3E82415794C4C9C198A97BAFFEE4733A6ECFCE8ED17296E455E7FBE10A5144555023E6BBA36708047CAEC2E016B4369CBFC9B54E333C2F4C27202F0F009A2EB51F6FAE5845F12CE1F3FF20AAC885B8BAD8D16AD473E9A3F")



class random_game(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="random-roblox-game", description="Use this command to get a random roblox game!")
    async def random_game(self, interaction:Interaction):
        ids = [
            286090429,
            4872321990,
            8781849572,
            2317712696,
            1383356634,
            2474168535,
            6678877691,
            6456351776,
            4282985734,
            1537690962,
            8540346411,
            7560156054,
            4580204640,
            4448566543,
            8583038000,
            8891045283,
            9123917180,
            6755834029,
            1554960397,
            5104202731,
            2534724415,
            2569453732,
            166986752,
            4911514005,
            4787647409,
            3226555017,
            8737602449,
            5771467270,
            5602055394,
            9099326192,
            8610758168,
            5388509011,
            28586816,
            6172932937,
            4468711919,
            6717367660,
            6243699076,
            189707,
            6961824067,
            2913303231,
            5985232436,
            3025990139,
            5041067762,
            9246669064,
            4042427666,
            6266940721,
            2629642516,
            2927931172,
            69184822,
            4490140733,
            5865858426,
            13822889,
            4743001427,
            5167146804,
            2830250344,
            8108627842,
            6653967414,
            5736409216,
            6897226634,
            8288069630
        ]

        random_place = random.choice(ids)

        embed_loading=nextcord.Embed(
            title="",
            colour= nextcord.Colour.blurple(),
            description=f'🔎 Retrieving Game Data...'
        )

        message_temp = await interaction.channel.send(embed=embed_loading)


        game = await roblox_client.get_place(random_place)
        game_universe = await roblox_client.get_universe(game.universe.id)
        embed_stats = nextcord.Embed(
            title=game.name,
            color=nextcord.Colour.blurple(),
            description=f"⭐ Favorites: {game_universe.favorited_count}\n🧍 Players: {game_universe.playing}\n👨‍👨‍👦 Visits: {game_universe.visits}\n🛠 Creator: {game.builder}\n\n{nextcord.utils.escape_markdown(game.description)}"
        )
        embed_stats.timestamp = datetime.datetime.now()


        link = Button(label=f"Link to {game.name}", url=game.url, style=nextcord.ButtonStyle.blurple)
        view=View()
        view.add_item(link)
        
        embed_stats.set_image(url=f"https://www.roblox.com/asset-thumbnail/image?assetId={game.id}&width=768&height=432&format=png")
        await message_temp.delete()
        
        await interaction.response.send_message(embed=embed_stats, view=view)



def setup(client):
    client.add_cog(random_game(client))