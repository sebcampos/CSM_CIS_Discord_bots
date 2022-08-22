import time
import BotManager
from HappyBot import HappyBot

DEBUG = True

happy_id = BotManager.add_bot(HappyBot, "HappyBot", HappyBot.client_id)

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
    if input("hit enter to quit"):
        break


