import datetime
import pprint
import threading
from discord import Intents
from discord.errors import LoginFailure
from .BaseBot import BaseBot
from .utils import init_logger
import uuid

# keeps track of the bots
bots = {}

# the logger for the BotManager module
logger = init_logger("BOTMANAGER")


def add_bot(bot: object, directory: str, client_id: str) -> str or bool:
    """
    This method creates an id using uuid, and inits a the Bot handed to it with
    the directory and client id. A separate daemon thread is created for this bot
    :param bot: A Bot inheriting from the BaseBot Class
    :param directory: the directory or module containing the bot
    :param client_id: the discord client id for the bot
    :return: uuid as a string if successful boolean false if not
    """

    # Calls the bot's init method with the given args
    identifier = str(uuid.uuid4())
    intents = Intents.default()
    intents.message_content = True
    new_bot = bot(intents=intents, identifier=identifier, directory=directory)

    # Creates a new thread with the bots run method as the target (run method inhereted from the Client Class)
    # TODO change threading to asyncio if possible
    try:
        new_thread = threading.Thread(target=new_bot.run, args=(client_id,), kwargs={"log_handler": None})
        new_thread.daemon = True
        new_thread.start()
    except LoginFailure:
        new_bot.logger.warning("invalid login credentials, bot not added")
        return False

    # every bot will be saved to the `bots` dictionary
    # with the following info
    bots[new_bot.id] = \
        {
            "directory": new_bot.directory,
            "bot": new_bot,
            "thread": new_thread,
            "timestamp": datetime.datetime.now()
        }
    # return the bot's id
    return new_bot.id


def get_bot(identifier: str) -> object:
    """
    Retrieve the bot instance by id
    :param identifier: bots uuid
    :return: Bot
    """
    if bots.get(identifier):
        return bots.get(identifier).get("bot")
    return False


def all_bots_active() -> bool:
    """
    This method validates the status of all bots
    returning True if all bot's active attributes
    are set to True
    :return: boolean
    """
    return all([get_bot(bot_id).active for bot_id in bots])


def remove_bot(identifier: str) -> bool:
    """
    This method deletes a bot instance
    returning true if the bot was deleted
    :param identifier: uuid for bot
    :return: bool
    """
    if bots.get(identifier, False):
        del bots[identifier]["bot"]
        del bots[identifier]["thread"]
        del bots[identifier]
        return True
    print(f"No bot with id {identifier} found")
    return False


def display_bots() -> None:
    """
    prints the bots dictionary to the console
    :return: void
    """
    pprint.pprint(bots)
