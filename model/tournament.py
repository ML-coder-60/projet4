"""Class Round"""
# coding: utf-8

from model.db import Db
from model.round import Round
from model.player import Player
import datetime


class Tournament:
    """Class tournament"""

    __TOURNAMENTS = []

    def __init__(self, **tournament):
        """Initialisation"""
        for attr_name, attr_value in tournament.items():
            setattr(self, attr_name, attr_value)

    @classmethod
    def load_tournaments(cls):
        """ Load tournaments and turn them into an instances list tournaments

        Returns:
        - none
        """
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
        """ Returns all instances tournaments

        Returns:
        - List instances tournaments
        """
        Tournament.load_tournaments()
        return cls.__TOURNAMENTS

    @staticmethod
    def save_tournaments(tournaments):
        """ Save all tournaments in database

        Returns:
        - none
        """
        data_save = list()
        for tournament in tournaments:
            tournament_save = tournament.__dict__.copy()
            rounds = tournament_save['rounds'].copy()
            tournament_save['rounds'] = [turn.__dict__ for turn in rounds]
            data_save.append(tournament_save)
        Db().save_data(data_save, 'tournament')

    @classmethod
    def save_tournament(cls, ins_tournament):
        """ Save Tournament in database
            if present update
               absent  add

        Attrs:
        - tournament (instance)

        Returns:
        - none
        """
        cls.load_tournaments()
        for tournament in cls.__TOURNAMENTS:
            if tournament.name == ins_tournament.name:
                Tournament.save_tournaments(cls.__TOURNAMENTS)
                return None
        cls.__TOURNAMENTS.append(ins_tournament)
        Tournament.save_tournaments(cls.__TOURNAMENTS)

    def stop_round(self):
        """ Set param end_date of turn

        Returns:
        - none
        """
        for turn in self.rounds:
            if not turn.end_date:
                turn.end_date = self.time_now()

    def update_round(self, result):
        """ update the unfinished round ( turn.end_date == False )
            if "result" is a match number
                then the match is zero 0.5 points for both players
            if result is the name of a player
                then 1 point for this player winning the game and 0 for the other player

        Attrs:
        - result (str) : number of match or last_name players

        Returns:
        - return the number of points to distribute for the round
        """
        for turn in self.rounds:
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
    def update_pair(pairs, index_player):
        """ Add 1 point winner

        Attrs:
        - index_player (int) : index of player winner
        - pairs (tuple of list) : match

        Returns:
        - return pairs update
        """
        for pair in pairs:
            if pair[0][0] == index_player:
                if (pair[0][1] + pair[1][1]) < 1:
                    pair[0][1] += 1
                    return pairs
            if pair[1][0] == index_player:
                if (pair[0][1] + pair[1][1]) < 1:
                    pair[1][1] += 1
                    return pairs
        return pairs

    @staticmethod
    def somme_result(turn):
        """ addition the points given during this round

        Returns:
        - return points off round (float)
        """
        somme = float()
        for pair in turn:
            for match in pair:
                somme += float(match[1])
        return somme

    @classmethod
    def update_round_tournament(cls, ins_tournament):
        """ Update round tournament select tournament with name

        Attrs:
        - ins_tournament (instance) : instance tournament

        Returns:
        - return list instances tournaments
        """
        for tournament in cls.__TOURNAMENTS:
            if tournament.name == ins_tournament.name:
                tournament.rounds = ins_tournament.rounds
        Tournament.save_tournaments(cls.__TOURNAMENTS)
        return cls.__TOURNAMENTS

    @staticmethod
    def get_pairs(index_players):
        """ create the pairs of the tournament rounds

        Attrs:
        - index_players (list) : list index instance players

        Returns:
        - return list tuple
        """
        return [
                    ([index_players[0], 0], [index_players[1], 0]),
                    ([index_players[2], 0], [index_players[3], 0]),
                    ([index_players[4], 0], [index_players[5], 0]),
                    ([index_players[6], 0], [index_players[7], 0])
                ]

    def stop(self):
        """ Set param status tournament => Finished

        Returns:
        - none
        """
        self.status = 'Finished'

    def first_round(self):
        """ Create first Round of tournament


        Returns:
        - none
        """
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
        self.rounds.append(Round('round1', self.time_now(), False, Tournament.get_pairs(index_players_first_round)))

    def new_round(self):
        """ Create pairs of round by ranking and point
            and Add new round to rounds

        Returns:
        - None
        """
        index_player = list()
        index_player_by_point = Round.index_players_total_points(self.rounds)
        sort_index_players_by_points = Round.sort_index_players_by_points(index_player_by_point)
        index_player_by_point_by_rank = Round.index_player_by_point_by_rank(sort_index_players_by_points)
        nbr = 1
        # if the pair does not exist, the first 2 "index players" are removed to add them
        # to the new "index player of the new round" list
        # else we check pair player 1/player 3 index does not exist ...
        while len(index_player_by_point_by_rank) > 0:
            #
            if Round.check_pair(self.rounds, [index_player_by_point_by_rank[0],
                                              index_player_by_point_by_rank[nbr]]):
                index_player.append(index_player_by_point_by_rank.pop(0))
                index_player.append(index_player_by_point_by_rank.pop(nbr-1))
                nbr = 1
                continue
            else:
                nbr += 1
        # Add new round to rounds
        self.rounds.append(Round(
            'round'+str(len(self.rounds) + 1),
            self.time_now(),
            False,
            Tournament.get_pairs(index_player))
        )

    @classmethod
    def find_tournament_by_name(cls, name):
        """  search tournament by name
             if find return instance tournament
             else return False

        Attrs:
        - name (str) : name of tournament

        Returns:
        - return instance tournament or False
        """
        for tournament in cls.__TOURNAMENTS:
            if tournament.name == name:
                return tournament
        return False

    @staticmethod
    def time_now():
        """ returns the current date

        Returns:
          - returns the current date in the format  dd/mm/yyyy hh:mm
        """
        return datetime.datetime.now().strftime("%d/%m/%y %H:%M")
