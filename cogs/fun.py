import requests
import json
from typing import Optional
from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    def get_iquote(self):
        response = requests.get("https://zenquotes.io/api//random")
        quote_json = json.loads(response.text)
        quote = "\"" + quote_json[0]['q'] + "\" -" + quote_json[0]['a']
        return (quote_json)
    def get_nasa(self):
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key=KljLJ0j9I3khrq8LbWjYsHncz680WFJabuRLkhIv")
        response_json = json.loads(response.text)
        return response_json
    def get_covid19_details(self):
        response = requests.get("https://api.covid19api.com/summary")
        response_json = json.loads(response.text)
        return response_json
    def get_meme(self):
        response = requests.get("https://meme-api.herokuapp.com/gimme")
        response_json = json.loads(response.text)
        return response_json
        
    @command(name = "inspire", aliases = ["iquote"], help="sends a random inspirational quote")
    async def send_iquote(self, ctx):
        embed = Embed(title = "Inspirational Quote",
                     colour = ctx.author.colour,
                     timestamp = datetime.utcnow())
        iquote = self.get_iquote()
        embed.add_field(name="Quote", value=iquote[0]['q'], inline=False)
        embed.add_field(name="Author", value=iquote[0]['a'] , inline=False)
        await ctx.send(embed=embed)

    @command(name = "astropic", aliases = ["astropicotd","nasapic","nasapicotd"], help = "sends astronomy pic of the day from NASA")
    async def send_nasa_pic_otd(self, ctx):
        embed = Embed(title = "NASA",
                     description = "Picture of the day",
                     colour = ctx.author.colour,
                     timestamp = datetime.utcnow())
        embed.set_thumbnail(url="https://user-images.githubusercontent.com/63065397/156291255-4af80382-836c-4801-8b4f-47da33ea36c5.png")
        embed.set_footer(text="updated daily at 05:00:00 UTC [00:00:00 ET]")
        nasa_api = self.get_nasa()
        embed.set_image(url=nasa_api["url"])
        embed.add_field(name="Date", value=nasa_api["date"], inline=False)
        embed.add_field(name="Image Title", value=nasa_api["title"] , inline=False)
        await ctx.send(embed=embed)

    @command(name="covid19", help = "sends COVID-19 stats of the given country (global stats if country == null)")
    async def covid19_data(self, ctx, country: Optional[str]):
        found = False
        stats = self.get_covid19_details()
        if country:
            for k in stats["Countries"]:
                if (k["CountryCode"] == country) or (k["Country"] == country):
                    embed = Embed(
                        title = k["Country"],
                        description = "COVID-19 Statistics",
                        colour = 0xff0000,
                        timestamp = datetime.utcnow()
                    )
                    flag_url="https://flagcdn.com/w640/" + str(k["CountryCode"]).lower() + ".jpg"
                    embed.set_thumbnail(url=flag_url)
                    fields = [
                        ("New Confirmed Cases", k["NewConfirmed"], True),
                        ("Total Confirmed Cases", k["TotalConfirmed"], True),
                        ("Country Code", k["CountryCode"], True),
                        ("New Deaths", k["NewDeaths"], True),
                        ("Total Deaths", k["TotalDeaths"], True),
                        ("Report Time (UTC)", "Date: " + k["Date"][0:10] + " & Time: " + k["Date"][11:19], True),
                        ("New Recovered", k["NewRecovered"], True),
                        ("Total Recovered", k["TotalRecovered"], True)
                    ]
                    for n,v,i in fields:
                        embed.add_field(name=n,value=v,inline=i)
                    await ctx.send(embed=embed)
                    found = True
        else:
            k = stats["Global"]
            embed = Embed(
                title = "Global",
                description = "COVID-19 Statistics",
                colour = 0xff0000,
                timestamp = datetime.utcnow()
            )
            embed.set_thumbnail(url="https://user-images.githubusercontent.com/63065397/156144079-6f90504d-ad48-4f2e-bec5-bae31cebd858.png")
            fields = [
                ("New Confirmed Cases", k["NewConfirmed"], True),
                ("Total Confirmed Cases", k["TotalConfirmed"], True),
                ("New Deaths", k["NewDeaths"], True),
                ("Total Deaths", k["TotalDeaths"], True),
                ("New Recovered", k["NewRecovered"], True),
                ("Total Recovered", k["TotalRecovered"], True)
            ]
            for n,v,i in fields:
                embed.add_field(name=n,value=v,inline=i)
            await ctx.send(embed=embed)
            found = True
        if not found:
            embed = Embed(
                title = "Error",
                description = "Country Not Found",
                colour = 0xff0000
            )
            embed.add_field(name="Given Country Name", value=country, inline=True)
            await ctx.send(embed=embed)

    @command(name = "meme", aliases = ["hehe"], help = "sends a random meme")
    async def send_meme(self, ctx):
        embed = Embed(title = "MEME",
                     colour = 0xffee00,
                     timestamp = datetime.utcnow())
        meme = self.get_meme()
        embed.add_field(name="Post Link", value=meme["postLink"], inline=True)
        embed.add_field(name="Author", value=meme["author"] , inline=True)
        embed.add_field(name="Header", value=meme["title"] , inline=False)
        embed.set_image(url=meme["url"])
        embed.set_thumbnail(url="https://user-images.githubusercontent.com/63065397/156142184-0675cfee-2863-41d7-bef8-87f600a713b0.png")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))