import logging

from discord import Client
from os import path
from . import utils
import sqlite3 as sql
import datetime


class BaseBot(Client):
    """
    This class creates a Base Bot using the discord.py library
    """

    def __init__(self, *args, **kwargs):
        """
        The BaseBot inhearts from the discord.Client Class
        and then call the Client Class init method. After
        it adds some attributes and functions to the Bot
        :param args: all positional args
        :param kwargs: all keyword args
        """
        super().__init__(*args, **kwargs)
        self._id = kwargs.get("identifier", None)
        self._directory = kwargs.get("directory", None)
        self._db = kwargs.get("db", True)
        self._initialized_at = datetime.datetime.now()
        self._active = False
        self._logger = None
        if self._db and self._directory:
            self._db = sql.connect(f"{path.join(self.directory, self._directory)}.db",
                                   check_same_thread=False)  # hmm...

    @property
    def logger(self) -> logging.Logger or None:
        """
        Returns the bots logger instance
        :return: Logger Class
        """
        return self._logger

    @logger.setter
    def logger(self, name):
        """
        Inits a logger for the Bot giving it the bots name
        :param name: name of bot defined by discord
        :return: void
        """
        self._logger = utils.init_logger(name)

    @property
    def db(self) -> sql.Connection:
        """
        Returns the bots sqlite3 conn or connection object
        :return: sql Connection Class
        """
        return self._db

    @property
    def id(self) -> str or None:
        """
        the uuid assigned when class is created
        if created by the BotManager module
        :return: string or None
        """
        return self._id

    @id.setter
    def id(self, _) -> None:
        """
        keeps id from being changed
        :return:
        """
        self.logger.warning("Id is Immutable")
        return

    @property
    def directory(self) -> str or None:
        """
        The directory containing the bot
        :return: str
        """
        return self._directory

    @directory.setter
    def directory(self, directory: str) -> None:
        """
        allows the directory to be redefined
        :param directory: new directory
        :return: void
        """
        self._directory = directory

    @property
    def active(self) -> bool:
        """
        the active state of the bot
        :return: boolean
        """
        return self._active

    @active.setter
    def active(self, state: bool) -> None:
        """
        allows to change the active state of the
        bot to either True or False
        :param state: boolean
        :return: void
        """
        if type(state) != bool:
            self.logger.warning("Active state must be set to True or false")
            return
        self._active = state

    @property
    def initialized_at(self) -> datetime.datetime:
        """
        Timestamp the bot was created
        :return: datetime object
        """
        return self._initialized_at

    @initialized_at.setter
    def initialized_at(self, _) -> None:
        """
        disallows `initialized_at` from being modified
        :return: void
        """
        self.logger.warning("'Initialized at' is immutable")
        return
