""" Class Player"""
from models.tinyDBStore import TinyDBStore


class Player:
    def __init__(self):
        self.players = TinyDBStore().load_data('player')

    def add_player(self, player):
        """ Add Player """
        self.players.append(player)

    def save_player(self):
        """ Save player  return 1 =>  Player Management """
        TinyDBStore().save_data(self.players, 'player')
        return 1

    def find_index_player(self, name_player):
        """
            find player by Last name
            if find return player and number index of player
            else return False for player an index
        """
        n = 0
        for player in self.players:
            if player['Last Name'] == name_player:
                return player, n
            n += 1
        return False, False

    def update_rank_player_by_index(self, index, rank):
        """ Update rank for player with index """
        self.players[index]['Ranking'] = rank
        return self.players[index]

    def list_player_by_name(self):
        """ List Player by Name"""
        return sorted(self.players, key=lambda t: t['Last Name'])

    def list_player_by_ranking(self):
        """ List player by rank"""
        return sorted(self.players, key=lambda t: int(t['Ranking']), reverse=True)
