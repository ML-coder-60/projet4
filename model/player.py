""" Class Player"""
# coding: utf-8
from model.db import Db


class Player:
    """ Class player, load, save  """

    __PLAYERS = []

    def __init__(self, **player_attributes):
        """ Initialisation player attributes """
        for attr_name, attr_value in player_attributes.items():
            setattr(self, attr_name, attr_value)

    @classmethod
    def load_players(cls):
        """ load players and turn them into an instances list players

        Returns:
          none
        """
        cls.__PLAYERS = [Player(**player_attributes) for player_attributes in Db().load_data('player')]

    @classmethod
    def get_players_by_ranking(cls, players=None):
        """ return a list  instance of players sorted by rank
            if players is None load players from database

        Attrs:
          Player (list):  list  instance of players

        Returns:
          list instance of players sorted by rank
        """
        list_players = list()
        if players is None:
            players = cls.__PLAYERS
        for player in players:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: int(t['ranking']), reverse=True)
        return [Player(**player) for player in list_players]

    @classmethod
    def get_players_by_name(cls, players=None):
        """ Returns a list  instance of Players by Name
            if players is None load players from database

        Attrs:
          Player (list):  list  instance of players

        Returns:
          list instance of players sorted by name
        """
        list_players = list()
        if players is None:
            players = cls.__PLAYERS
        for player in players:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: str(t['last_name']))
        return [Player(**player) for player in list_players]

    @classmethod
    def get_players_index(cls):
        """ Returns list index of instance players

        Returns:
          list index of instance players sorted by name
        """
        index_players = list()
        for player in cls.__PLAYERS:
            index_players.append(cls.find_index_player_by_last_name(player.last_name))
        return index_players

    @classmethod
    def find_player_by_last_name(cls, last_name):
        """ search player by Last name
            if find return instance player
            else return False

        Attrs:
          last_name (str):  Name of aplayer
        Returns:
          instance of player or False
        """
        for player in cls.__PLAYERS:
            if player.last_name == last_name:
                return player
        return False

    @staticmethod
    def get_players_db():
        """  return all instances player """
        return [Player(**player_attributes) for player_attributes in Db().load_data('player')]

    def find_index_player_by_last_name(self, last_name):
        """ search player by Last name
            if find return index instance player
            else return False

        Attrs:
          last_name (str):  Name of player

        Returns:
          index (int)  instance player or False
        """
        self.load_players()
        for index, value in enumerate(self.__PLAYERS):
            if value.last_name == last_name:
                return index
        return False

    @classmethod
    def save_player(cls, player):
        """ Save player to database

        Returns:
          None
        """
        cls.load_players()
        cls.__PLAYERS.append(player)
        Player.save_players(cls.__PLAYERS)

    def add_player(self, player):
        """ Add instance player to __PLAYERS

        Returns:
          None
        """
        self.__PLAYERS.append(player)

    @staticmethod
    def save_players(players):
        """ Save Players in database

        Returns:
          None
        """
        data_save = list()
        for player in players:
            data_player = player.__dict__
            data_save.append(data_player)
        Db().save_data(data_save, 'player')

    @classmethod
    def update_rank_player_by_last_name(cls, last_name, rank):
        """ search player by Last name
            if find update rank player
            else do nothing
            and save players

        Returns:
          None
        """
        for player in cls.__PLAYERS:
            if player.last_name == last_name:
                player.ranking = rank
        Player.save_players(cls.__PLAYERS)
