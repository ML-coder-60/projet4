"""Class Tournament"""
# coding: utf-8
from models.round import Round
from models.player import Players
from models.tinyDBStore import TinyDBStore
import time




class Tournament:
    def __init__(self, **tournament):
        for attr_name, attr_value in tournament.items():
            setattr(self, attr_name, attr_value)

    def create_first_round(self):
        """ Create first Round """
        first_round = Round('round1', False, False, self.pair_first_turn())
        self.rounds.append(first_round)

    def add_index_player_to_tournament(self, index):
        """ add Index player to tournaments"""
        self.players.append(index)

    def start_round(self):
        """ start round update start_date of turn """
        for turn in self.rounds:
            if not turn['start_date']:
                dmy = time.localtime(time.time())
                turn['start_date'] = time.strftime("%d/%m/%y %H:%M", dmy)

    def stop_round(self):
        """ stop round update end_date of turn """
        for turn in self.rounds:
            if not turn['end_date']:
                dmy = time.localtime(time.time())
                turn['end_date'] = time.strftime("%d/%m/%y %H:%M", dmy)

    def update_round(self, result):
        """ Update Round match result """
        for turn in self.rounds:
            if turn['start_date'] and not turn['end_date']:
                if result == "1" or result == "2" or result == "3" or result == "4":
                    turn['pairs'][int(result)-1][0][1] = 0.5
                    turn['pairs'][int(result)-1][1][1] = 0.5
                    return self.somme_result(turn['pairs'])
                if isinstance(result, str):
                    index_players = Players().find_index_players_by_last_name(result)
                    turn['pairs'] = self.update_pair(turn['pairs'], index_players)
                    return self.somme_result(turn['pairs'])


    @staticmethod
    def somme_result(turn):
        somme = float()
        for pair in turn:
            for match in pair:
                somme += float(match[1])
        return somme

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


    def pair_first_turn(self):
        """ create the pair for first rounds"""
        list_players = list()
        index_players_by_rank = []
        players_tournament = [Players().players[i] for i in self.players]
        for player in players_tournament:
            list_players.append(player.__dict__)
            list_players = sorted(list_players, key=lambda t: int(t['ranking']), reverse=True)
        for p in list_players:
            index_players_by_rank.append(Players().find_index_players_by_last_name(p['last_name']))
        #return [
        #            ([self.players[index_players_by_rank[0]], 0], [self.players[index_players_by_rank[4]], 0]),
        #            ([self.players[index_players_by_rank[1]], 0], [self.players[index_players_by_rank[5]], 0]),
        #            ([self.players[index_players_by_rank[2]], 0], [self.players[index_players_by_rank[6]], 0]),
        #            ([self.players[index_players_by_rank[3]], 0], [self.players[index_players_by_rank[7]], 0])
        #        ]
        return [
                    ([index_players_by_rank[0], 0], [index_players_by_rank[4], 0]),
                    ([index_players_by_rank[1], 0], [index_players_by_rank[5], 0]),
                    ([index_players_by_rank[2], 0], [index_players_by_rank[6], 0]),
                    ([index_players_by_rank[3], 0], [index_players_by_rank[7], 0])
                ]


class Tournaments:
    def __init__(self):
        self.tournaments = self.__load_tournaments()

    @staticmethod
    def __load_tournaments():
        """ Load data from table tournaments"""
        data = TinyDBStore().load_data('tournament')
        tournaments = list()
        for tournament in data:
            rounds = []
            for turn in tournament['rounds']:
                rounds.append(Round(**turn))
            tournament['rounds'] = rounds
            tournaments.append(Tournament(**tournament))
        return tournaments

    def save_tournament(self):
        """ Save data in table tournament"""
        data_save = list()
        tournaments = self.tournaments
        for tournament in tournaments:
            data = tournament.__dict__
            data_round = list()
            for turn in data['rounds']:
                data_round.append(turn.__dict__)
            data['rounds'] = data_round
            data_save.append(data)
        TinyDBStore().save_tournament(data_save)

    def update_round_tournament(self, data):
        """ Update tournament with name """
        for tournament in self.tournaments:
            if tournament.name == data.name:
                tournament.rounds = [Round(**x) for x in data.rounds]
        self.save_tournament()
        return self.tournaments

    def add_tournament(self, tournament):
        """Add tournament """
        self.tournaments.append(tournament)
        self.save_tournament()
        return self.tournaments
