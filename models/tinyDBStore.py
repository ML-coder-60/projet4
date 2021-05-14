"""Class TinyDBStore"""
# coding: utf-8
from tinydb import TinyDB
import os


class TinyDBStore:
    """
    initialise, load , save
    """
    DB_FILE = 'db.json'
    DB_REP = 'data'

    def __init__(self):
        """ initialisation base """
        self._db_directory = os.path.dirname(os.path.dirname(__file__))
        self._db_file = os.path.join(self._db_directory, self.DB_REP, self.DB_FILE)
        self._db = TinyDB(self._db_file)

    def __save_data(self, data, table):
        """
            select table ,clean data end backup data in table
        """
        data_table = self._db.table(table)
        data_table.truncate()
        data_table.insert_multiple(data)

    def load_data(self, table):
        """return data table"""
        data_table = self._db.table(table)
        result = data_table.all()
        return result

    def save_player(self, data):
        """ Save data in table player"""
        self.__save_data(data, 'player')

    def save_tournament(self, data):
        """ Save data in table tournament"""
        self.__save_data(data, 'tournament')

    def close(self):
        self._db.close()
