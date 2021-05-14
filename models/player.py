""" Class Player"""
# coding: utf-8
from models.tinyDBStore import TinyDBStore


class Player:
    def __init__(self, **player):
        for attr_name, attr_value in player.items():
            setattr(self, attr_name, attr_value)


class Players:
    def __init__(self):
        self.players = self.__load_players()

    @staticmethod
    def __load_players():
        """ Load data from table player"""
        data = TinyDBStore().load_data('player')
        return [Player(**player) for player in data]

    def list_player_by_ranking(self):
        """ return les instances des players by rank"""
        list_players = list()
        for player in self.players:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: int(t['ranking']), reverse=True)
        return [Player(**player) for player in list_players]

    def add_player(self, data_player):
        """Add player """
        self.players.append(Player(**data_player))
        self.save_player()
        return self.players

    def save_player(self):
        """ Save data in table player"""
        data_save = list()
        for player in self.players:
            data_player = player.__dict__
            data_save.append(data_player)
        TinyDBStore().save_player(data_save)

    def list_player_by_name(self):
        """ List Player by Name"""
        list_players = list()
        for player in self.players:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: str(t['last_name']))
        return [Player(**player) for player in list_players]

    def update_rank_player_by_last_name(self, last_name, rank):
        """ Update rank for player with last_name """
        for player in self.players:
            if player.last_name == last_name:
                player.ranking = rank
        self.save_player()
        return self.players

    def find_player_by_last_name(self, name_player):
        """
            find player by Last name
            if find return player and number index of player
            else return False for player an index
        """
        for player in self.players:
            if player.last_name == name_player:
                return player
        return False

    def find_index_players_by_last_name(self, last_name):
        """ find index from list players """
        for index, value in enumerate(self.players):
            if value.last_name == last_name:
                return index
        return False
