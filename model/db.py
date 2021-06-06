"""Class TinyDBStore"""
# coding: utf-8
from tinydb import TinyDB
import os


class Db:
    """
    initialise, load , save data
    """
    __DB_FILE = 'db.json'
    __DB_REP = 'data'

    def __init__(self):
        """ initialisation base """
        self._db_directory = os.path.dirname(os.path.dirname(__file__))
        self._db_file = os.path.join(self._db_directory, self.__DB_REP, self.__DB_FILE)
        self._db = TinyDB(self._db_file)

    def save_data(self, data, table):
        """ select table ,clean data end backup data in table

        Attrs:
        - data (list): dictionary list including information 
        - table (str): name of the table where the information is saved  
        
        Returns:
        - none 
        """
        data_table = self._db.table(table)
        data_table.truncate()
        data_table.insert_multiple(data)

    def load_data(self, table):
        """return information in the table

        Attrs:
        - table (str): name of the table where the information is loaded

        Returns:
        - dictionary list including information
        """
        data_table = self._db.table(table)
        return data_table.all()

    def close(self):
        """ close connexion """
        self._db.close()


if __name__ == "__main__":
    test = Db()
    print(test.load_data('player'))
