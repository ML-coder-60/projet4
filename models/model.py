"""Class Model"""
# coding: utf-8
from models.player import Player
from models.tinyDBStore import TinyDBStore


class Model:
    def __init__(self):
        self.dao = TinyDBStore()
        self.players = self.list_players()

    def list_players(self):
        data_players = self.dao.load_data('player')
        return [Player(**player) for player in data_players]

    def list_player_by_name(self):
        """ List Player by Name"""
        data_players = self.dao.load_data('player')
        player_by_name = sorted(data_players, key=lambda t: t['Last_Name'])
        return [Player(**player) for player in player_by_name]

    def list_player_by_ranking(self):
        """ List player by rank"""
        data_players = self.dao.load_data('player')
        player_by_rank = sorted(data_players, key=lambda t: int(t['Ranking']), reverse=True)
        return [Player(**player) for player in player_by_rank]

    def add_player(self, player):
        self.players.append(player)

    def save_player(self):
        data_save = list()
        for player in self.players:
            data_player = {
                'First_Name': player.First_Name,
                'Last_Name': player.Last_Name,
                'Date_Birth': player.Date_Birth,
                'Gender': player.Gender,
                'Ranking': player.Ranking
            }
            data_save.append(data_player)
        self.dao.save_data(data_save, 'player')
        return 1

    def find_player_by_last_name(self, name_player):
        """
            find player by Last name
            if find return player and number index of player
            else return False for player an index
        """
        print(name_player)
        for player in self.players:
            if player.Last_Name == name_player:
                return player
        return False

    def update_rank_player_by_last_name(self, last_name, rank):
        """ Update rank for player with last_name """
        for player in self.players:
            if player.Last_Name == last_name:
                player.Ranking = rank
        self.save_player()

