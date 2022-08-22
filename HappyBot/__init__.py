from random import choice

import pandas as pd
from discord import Embed, Color
from art import art

from BotManager.BaseBot import BaseBot
from credentials import CLIENT_ID


class HappyBot(BaseBot):
    client_id = CLIENT_ID
    GIR_URL = "https://static.wikia.nocookie.net/zimwiki/images/d/d2/Girdog.png/revision/latest?cb=20210819050259"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.puns = self.fetch_from_database("select * from puns").puns_from_scrape.tolist()

    async def on_ready(self):
        self.logger = str(self.user)
        self.logger.info(f"{self.user} is connected")
        self.active = True

    async def on_message(self, message):
        if message.content.startswith("::punny"):
            embed = await self.basic_embed(title="Punny", description=self.random_pun())
            await message.channel.send(embed=embed)
        if message.content.startswith("::project"):
            embed = await self.basic_embed(title="Project", description=self.random_pun())
            await message.channel.send()
        if message.content.startswith("::test"):
            embed = await self.basic_embed(False)
            await message.channel.send(embed=embed)

    async def basic_embed(self, title, description, thumbnail=GIR_URL):
        embed = Embed(
            title=title,
            description=description,
            colour=Color.random()
        )
        embed.set_thumbnail(url=thumbnail)
        #embed.set_image(url="https://static.wikia.nocookie.net/zimwiki/images/d/d2/Girdog.png/revision/latest?cb=20210819050259")
        #embed.add_field(name="NAME", value="wut", inline=False)
        return embed

    def fetch_from_database(self, sql) -> pd.DataFrame:
        return pd.read_sql(sql, self.db)

    def add_to_database(self, table, data):
        pd.DataFrame(data).to_sql(table, con=self.db, if_exists="append")

    def random_pun(self):
        return "*" + choice(self.puns) + "*\n\t" + art("random")
