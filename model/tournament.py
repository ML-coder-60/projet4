"""Class Round"""
# coding: utf-8

from model.db import Db
from model.round import Round
from model.date import Date
from model.player import Player


class Tournament:
    """Class tournament"""

    __TOURNAMENTS = []

    def __init__(self, **tournament):
        for attr_name, attr_value in tournament.items():
            setattr(self, attr_name, attr_value)

    @classmethod
    def load_tournaments(cls):
        """ Load data from table tournaments"""
        data = Db().load_data('tournament')
        tournaments = []
        for tournament in data:
            rounds = []
            for turn in tournament['rounds']:
                rounds.append(Round(**turn))
            tournament['rounds'] = rounds
            tournaments.append(tournament)
        cls.__TOURNAMENTS = [Tournament(**tournament) for tournament in tournaments]

    @classmethod
    def get_tournaments(cls):
        Tournament.load_tournaments()
        return cls.__TOURNAMENTS

    @staticmethod
    def save_tournaments(tournaments):
        """ Save data in table tournament"""
        data_save = list()
        for tournament in tournaments:
            tournament_save = tournament.__dict__.copy()
            rounds = tournament_save['rounds'].copy()
            tournament_save['rounds'] = [turn.__dict__ for turn in rounds]
            data_save.append(tournament_save)
        Db().save_data(data_save, 'tournament')

    @classmethod
    def save_tournament(cls, tournament):
        """ Save Tournament"""
        cls.load_tournaments()
        cls.__TOURNAMENTS.append(tournament)
        Tournament.save_tournaments(cls.__TOURNAMENTS)

    def start_round(self):
        """ start round update start_date of turn """
        for turn in self.rounds:
            if not turn.start_date:
                turn.start_date = Date().time_now()

    def stop_round(self):
        """ stop round update end_date of turn """
        for turn in self.rounds:
            if not turn.end_date:
                turn.end_date = Date().time_now()

    def update_round(self, result):
        """ Update Round match result """
        for turn in self.rounds:
            print(turn.__dict__)
            if turn.start_date and not turn.end_date:
                if result == "1" or result == "2" or result == "3" or result == "4":
                    turn.pairs[int(result)-1][0][1] = 0.5
                    turn.pairs[int(result)-1][1][1] = 0.5
                    return self.somme_result(turn.pairs)
                if isinstance(result, str):
                    index_players = Player().find_index_player_by_last_name(result)
                    if isinstance(index_players, int):
                        turn.pairs = self.update_pair(turn.pairs, index_players)
                    return self.somme_result(turn.pairs)

    @staticmethod
    def update_pair(pairs, index):
        """ Add 1 point winner"""
        for pair in pairs:
            if pair[0][0] == index:
                if (pair[0][1] + pair[1][1]) < 1:
                    pair[0][1] += 1
                    return pairs
            if pair[1][0] == index:
                if (pair[0][1] + pair[1][1]) < 1:
                    pair[1][1] += 1
                    return pairs
        return pairs

    @staticmethod
    def somme_result(turn):
        somme = float()
        for pair in turn:
            for match in pair:
                somme += float(match[1])
        return somme

    @classmethod
    def update_round_tournament(cls, data):
        """ Update tournament with name """
        for tournament in cls.__TOURNAMENTS:
            if tournament.name == data.name:
                tournament.rounds = data.rounds
        Tournament.save_tournaments(cls.__TOURNAMENTS)
        return cls.__TOURNAMENTS

    @staticmethod
    def get_pairs(index_players):
        return [
                    ([index_players[0], 0], [index_players[1], 0]),
                    ([index_players[2], 0], [index_players[3], 0]),
                    ([index_players[4], 0], [index_players[5], 0]),
                    ([index_players[6], 0], [index_players[7], 0])
                ]

    def stop(self):
        self.status = 'Finished'

    def first_round(self):
        """ Create first Round """
        all_players = Player().get_players_db()
        list_players = list()
        index_players_by_rank = list()
        players_tournament = [all_players[i] for i in self.players]
        for player in players_tournament:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: int(t['ranking']), reverse=True)
        for player in list_players:
            index_players_by_rank.append(Player().find_index_player_by_last_name(player['last_name']))
        index_players_first_round = [index_players_by_rank[0], index_players_by_rank[4],
                                     index_players_by_rank[1], index_players_by_rank[5],
                                     index_players_by_rank[2], index_players_by_rank[6],
                                     index_players_by_rank[3], index_players_by_rank[7]
                                     ]
        self.rounds.append(Round('round1', False, False, Tournament.get_pairs(index_players_first_round)))

    def new_round(self):
        """ Create round by ranking and point"""
        index_player = list()
        index_player_by_point = Round.index_players_total_points(self.rounds)
        sort_index_players_by_points = Round.sort_index_players_by_points(index_player_by_point)
        index_player_by_point_by_rank = Round.index_player_by_point_by_rank(sort_index_players_by_points)
        nbr = 1
        while len(index_player_by_point_by_rank) > 0:
            if Round.check_pair(self.rounds, [index_player_by_point_by_rank[0],
                                              index_player_by_point_by_rank[nbr]]):
                index_player.append(index_player_by_point_by_rank.pop(0))
                index_player.append(index_player_by_point_by_rank.pop(nbr-1))
                nbr = 1
                continue
            else:
                nbr += 1
        self.rounds.append(Round(
            'round'+str(len(self.rounds) + 1),
            False,
            False,
            Tournament.get_pairs(index_player))
        )

    @classmethod
    def find_tournament_by_name(cls, name):
        """
             find tournament by name
             if find return tournament  else return False
        """
        for tournament in cls.__TOURNAMENTS:
            if tournament.name == name:
                return tournament
        return False
