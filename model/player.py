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

    @classmethod
    def load_players(cls):
        """ Load players from the database """
        cls.__PLAYERS = [Player(**player_attributes) for player_attributes in Db().load_data('player')]

    @classmethod
    def get_players_by_ranking(cls, players=None):
        """ return instances players by rank"""
        if players is None:
            players = []
        if players is None:
            players = list()
        list_players = list()
        if len(players) == 0:
            players = cls.__PLAYERS
        for player in players:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: int(t['ranking']), reverse=True)
        result = [Player(**player) for player in list_players]
        return result

    @classmethod
    def get_players_by_name(cls):
        """ List Player by Name"""
        list_players = list()
        for player in cls.__PLAYERS:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: str(t['last_name']))
        result = [Player(**player) for player in list_players]
        return result

    @classmethod
    def get_players_index(cls):
        """ Return index of Players """
        index_players = list()
        for player in cls.__PLAYERS:
            index_players.append(cls.find_index_player_by_last_name(player.last_name))
        return index_players

    @classmethod
    def find_player_by_last_name(cls, last_name):
        """
            find player by Last name
            if find return player and number index of player
            else return False for player an index
        """
        for player in cls.__PLAYERS:
            if player.last_name == last_name:
                return player
        return False

    def get_players(self):
        """ return all player """
        return self.__PLAYERS

    @staticmethod
    def get_players_db():
        """  return all player """
        return [Player(**player_attributes) for player_attributes in Db().load_data('player')]

    def find_index_player_by_last_name(self, last_name):
        """ find index from list players """
        self.load_players()
        for index, value in enumerate(self.__PLAYERS):
            if value.last_name == last_name:
                return index
        return False

    @classmethod
    def save_player(cls, player):
        """ Save player"""
        cls.load_players()
        cls.__PLAYERS.append(player)
        Player.save_players(cls.__PLAYERS)

    def add_player(self, player):
        """ Add Player to __PLAYERS"""
        self.__PLAYERS.append(player)

    @staticmethod
    def save_players(players):
        """ Save Players in database """
        data_save = list()
        for player in players:
            data_player = player.__dict__
            data_save.append(data_player)
        Db().save_data(data_save, 'player')

    @classmethod
    def update_rank_player_by_last_name(cls, last_name, rank):
        """ Update rank for player with last_name """
        for player in cls.__PLAYERS:
            if player.last_name == last_name:
                player.ranking = rank
        Player.save_players(cls.__PLAYERS)


if __name__ == "__main__":
    pass
