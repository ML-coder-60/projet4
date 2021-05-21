"""Class Round"""
# coding: utf-8

from model.db import Db
from model.player import Player
from model.round import Round
from model.date import Date


class Tournament:
    """Class tournament"""

    __TOURNAMENTS = []

    def __init__(self, **tournament):
        for attr_name, attr_value in tournament.items():
            setattr(self, attr_name, attr_value)
        self.rounds = []

    @staticmethod
    def __load_tournaments():
        """ Load data from table tournaments"""
        data = Db().load_data('tournament')
        tournaments = list()
        for tournament in data:
            rounds = []
            for turn in tournament['rounds']:
                rounds.append(Round(**turn))
            tournament['rounds'] = rounds
            tournaments.append(Tournament(**tournament))
        return tournaments

    def save_tournaments(self):
        """ Save data in table tournament"""
        data_save = list()
        for tournament in self.__TOURNAMENTS:
            data = tournament.__dict__
            data_round = list()
            for turn in data['rounds']:
                data_round.append(turn.__dict__)
            data['rounds'] = data_round
            data_save.append(data)
        Db().save_data(data_save, 'tournament')

    def create_first_round(self):
        """ Create first Round """
        all_players = Player().list_players()
        list_players = list()
        index_players_by_rank = list()
        players_tournament = [all_players[i] for i in self.players]
        for player in players_tournament:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: int(t['ranking']), reverse=True)
        for player in list_players:
            index_players_by_rank.append(Player().find_index_player_by_last_name(player['last_name']))
        self.rounds.append(Round('round1', False, False, index_players_by_rank))

    def save_tournament(self, tournament):
        """ Save player"""
        self.__load_tournaments()
        self.__TOURNAMENTS.append(tournament)
        self.save_tournaments()

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
            if turn.start_date and not turn.end_date:
                if result == "1" or result == "2" or result == "3" or result == "4":
                    turn.pairs[int(result)-1][0][1] = 0.5
                    turn.pairs[int(result)-1][1][1] = 0.5
                    return self.somme_result(turn.pairs)
                if isinstance(result, str):
                    index_players = Player().find_index_player_by_last_name(result)
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

    def update_round_tournament(self, data):
        """ Update tournament with name """
        for tournament in self.__TOURNAMENTS:
            if tournament.name == data.name:
                tournament.rounds = [Round(**x) for x in data.rounds]
        self.save_tournaments()
        return self.__TOURNAMENTS


    def new_round(self):
        """ Create round by ranking and point"""
        index_player_by_point_by_rank = list()
        for point, player in self.get_total_point_by_player(self.rounds):
            if len(player) == 1:
                index_player_by_point_by_rank.append(
                    Player().find_index_player_by_last_name(Player().list_players()[int(player[0])].last_name))
            else:
                players__ = list()
                for i in player:
                    players__.append(Player().list_players()[int(i)])
                players_by_ranking = self.get_players_by_ranking(players__)
                for player__ in players_by_ranking:
                    index_player_by_point_by_rank.append(Player().find_index_player_by_last_name(player__.last_name))
        test = [
                ([index_player_by_point_by_rank[0], 0], [index_player_by_point_by_rank[1], 0]),
                ([index_player_by_point_by_rank[2], 0], [index_player_by_point_by_rank[3], 0]),
                ([index_player_by_point_by_rank[4], 0], [index_player_by_point_by_rank[5], 0]),
                ([index_player_by_point_by_rank[6], 0], [index_player_by_point_by_rank[7], 0])
        ]
        print(test)


    def get_total_point_by_player(self, rounds):
        """ return the players (index) with their total game points  """
        index_players_point = dict()

        for turn in rounds:
            for match in turn.pairs:
                for data_player in match:
                    try:
                        index_players_point[data_player[0]] += float(data_player[1])
                    except KeyError:
                        index_players_point[data_player[0]] = float(data_player[1])
        return self.sort_player_by_scrore(index_players_point)

    def sort_player_by_scrore(self, point_by_player):
        point_index_players = dict()
        for key in point_by_player.keys():
            try:
                point_index_players[str(point_by_player[key])].append(str(key))
            except KeyError:
                point_index_players[str(point_by_player[key])] = [str(key)]
        return sorted(point_index_players.items(), key=lambda t: t[0], reverse=True)

    def get_players_by_ranking(self, players):
        """ Return index player by ranking"""
        list_players = list()
        for player in players:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: int(t['ranking']), reverse=True)

        #return list_players
        return [Player(**x) for x in list_players]