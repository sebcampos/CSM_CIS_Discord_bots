import time
import BotManager
from HappyBot import HappyBot

DEBUG = True

# adding a bot
happy_id = BotManager.add_bot(
    HappyBot,  # class to be initialized
    "HappyBot",  # directory containing the bot
    HappyBot.client_id  # The client ID provided by discord
)

# retrieve instance from BotManager via id
happy = BotManager.get_bot(happy_id)


# loop to wait until all bots are int `active` state
BotManager.logger.info("Initalizing Bots ...")
while not BotManager.all_bots_active():
    continue

if DEBUG:
    BotManager.logger.info("Debug Console Active: enter `exit()` to quit")
    time.sleep(1)

# main loop
while True:
    if DEBUG:
        try:
            exec(input(">>> "))
        except Exception as e:
            BotManager.logger.warning(str(e)+"\nenter `exit()` to quit")
            continue
    elif not DEBUG:
        if input("hit enter to quit"):
            break


