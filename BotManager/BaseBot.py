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
        super().__init__(*args, **kwargs)
        self._id = kwargs.get("identifier", None)
        self._directory = kwargs.get("directory", None)
        self._db = kwargs.get("db", True)
        self._initialized_at = datetime.datetime.now()
        self._active = False
        self._logger = None
        if self._db and self._directory:
            self._db = sql.connect(f"{path.join(self.directory, self._directory)}.db")

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, name):
        self._logger = utils.init_logger(name)

    @property
    def db(self):
        return self._db

    @property
    def id(self) -> str or None:
        return self._id

    @id.setter
    def id(self, _) -> None:
        self.logger.warning("Id is Immutable")
        return

    @property
    def directory(self) -> str or None:
        return self._directory

    @directory.setter
    def directory(self, directory: str) -> None:
        self._directory = directory

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, state: bool) -> None:
        if type(state) != bool:
            self.logger.warning("Active state must be set to True or false")
            return
        self._active = state

    @property
    def initialized_at(self) -> datetime.datetime:
        return self._initialized_at

    @initialized_at.setter
    def initialized_at(self, _) -> None:
        self.logger.warning("'Initialized at' is immutable")
        return