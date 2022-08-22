import datetime
import pprint
import threading
from discord import Intents
from discord.errors import LoginFailure
from .BaseBot import BaseBot
from .utils import init_logger
import uuid

bots = {}
logger = init_logger("BOTMANAGER")

def add_bot(bot: object, directory: str, client_id: str) -> str or bool:
    identifier = str(uuid.uuid4())
    intents = Intents.default()
    intents.message_content = True
    new_bot = bot(intents=intents, identifier=identifier, directory=directory)

    try:
        new_thread = threading.Thread(target=new_bot.run, args=(client_id,), kwargs={"log_handler":None})
        new_thread.daemon = True
        new_thread.start()
    except LoginFailure:
        new_bot.logger.info("[ERROR] invalid login credentials")
        return False

    bots[new_bot.id] = \
        {
            "directory": new_bot.directory,
            "bot": new_bot,
            "thread": new_thread,
            "timestamp": datetime.datetime.now()
        }
    return new_bot.id


def get_bot(identifier: str) -> object:
    if bots.get(identifier):
        return bots.get(identifier).get("bot")
    return False

def all_bots_active():
    return all([get_bot(bot_id).active for bot_id in bots])


def remove_bot(identifier: str) -> bool:
    if bots.get(identifier, False):
        del bots[identifier]
        return True
    print(f"No bot with id {identifier} found")
    return False

def display_bots():
    pprint.pprint(bots)