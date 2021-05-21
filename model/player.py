""" Class Player"""
# coding: utf-8
from model.db import Db


class Player:
    """ Class player, load, """

    __PLAYERS = []

    def __init__(self, **player_attributes):
        """ Initialisation """
        for attr_name, attr_value in player_attributes.items():
            setattr(self, attr_name, attr_value)

    def load_players(self):
        self.__PLAYERS = [Player(**player_attributes) for player_attributes in Db().load_data('player')]

    def players_by_ranking(self):
        """ return instances players by rank"""
        list_players = list()
        for __player in self.__PLAYERS:
            list_players.append(__player.__dict__)
            list_players = sorted(list_players, key=lambda t: int(t['ranking']), reverse=True)
        result = [Player(**__player) for __player in list_players]
        return result

    def players_by_name(self):
        """ List Player by Name"""
        list_players = list()
        for __player in self.__PLAYERS:
            list_players.append(__player.__dict__)
            list_players = sorted(list_players, key=lambda t: str(t['last_name']))
        result = [Player(**__player) for __player in list_players]
        return result

    def index_player(self):
        """ Return index of Players """
        index_players = list()
        for player in self.__PLAYERS:
            index_players.append(self.find_index_player_by_last_name(player.last_name))
        return index_players

    def find_player_by_last_name(self, last_name):
        """
            find player by Last name
            if find return player and number index of player
            else return False for player an index
        """
        self.load_players()
        for __player in self.__PLAYERS:
            if __player.last_name == last_name:
                return __player
        return False

    def list_players(self):
        """
            return all player
        """
        self.load_players()
        return self.__PLAYERS

    def find_index_player_by_last_name(self, last_name):
        """ find index from list players """
        self.load_players()
        for index, value in enumerate(self.__PLAYERS):
            if value.last_name == last_name:
                return index
        return False

    def save_player(self, players):
        """ Save player"""
        self.load_players()
        self.__PLAYERS.append(players)
        self.save_players()

    def save_players(self):
        """ Save data in table player"""
        data_save = list()
        for __player in self.__PLAYERS:
            data_player = __player.__dict__
            data_save.append(data_player)
        Db().save_data(data_save, 'player')

    def update_rank_player_by_last_name(self, last_name, rank):
        """ Update rank for player with last_name """
        for __player in self.__PLAYERS:
            if __player.last_name == last_name:
                __player.ranking = rank
        self.save_players()


if __name__ == "__main__":
    test = Player()
    test.load_players()
    test.create_player('Bob', 'toto', '01/07/2020', 'M', '1500')
    bob = test.find_player_by_last_name('Bob')
    print(bob.__dir__())

