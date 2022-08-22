from random import choice

import pandas as pd
from discord import Embed, Color, Emoji  # TODO figure out this emoji bs
from art import art
from . import tools

from BotManager.BaseBot import BaseBot
from credentials import CLIENT_ID


class HappyBot(BaseBot):
    """
    A basic bot made from the BaseBot
    """
    client_id = CLIENT_ID
    GIR_URL = "https://static.wikia.nocookie.net/zimwiki/images/d/d2/Girdog.png/revision/latest?cb=20210819050259"
    GITHUB_LOGO = "https://github.githubassets.com/images/modules/logos_page/Octocat.png"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.add_to_database("puns", {"puns_from_scrape":tools.scrape_puns()})
        self.puns = self.fetch_from_database("select * from puns").puns_from_scrape.tolist()

    async def on_ready(self):
        self.logger = str(self.user)
        self.logger.info(f"{self.user} is connected")
        self.active = True

    async def on_member_join(self, member):
        embed = self.basic_embed(f"Welcome {member.name}  🎉 🎉 🎉", tools.welcome_message_content)
        await member.send(embed=embed)

    async def on_message(self, message):
        if message.content.startswith("::punny"):
            embed = await self.basic_embed(title="Punny", description=self.random_pun())
            await message.channel.send(embed=embed)
        if message.content.startswith("::project"):
            embed = await self.basic_embed(title="Project", description=tools.project_message, thumbnail=self.GITHUB_LOGO)
            await message.channel.send(embed=embed)
        if message.content.startswith("::email"):
            add_to_db = tools.add_email_to_db(message.author.name, message.content, self)
            if add_to_db:
                embed = await self.basic_embed("Success!", f"{message.author.name} successfully registered")
                await message.channel.send(embed=embed)
            else:
                embed = await self.error(message)
                await message.channel.send(embed=embed)

    async def error(self, message):
        embed = await self.basic_embed("Crap",
                                       f"Sorry {message.author.name}\nsomething when wrong message me so we can fix it...")
        return embed

    @staticmethod
    async def basic_embed(title, description, thumbnail=GIR_URL):
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

    def get_emails(self):
        return pd.read_sql("select * from emails", self.db)