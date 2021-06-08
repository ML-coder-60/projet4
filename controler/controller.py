"""Class Controller"""
# coding: utf-8
from view.menu import Menu
from model.player import Player
from model.date import Date
from model.tournament import Tournament
from model.round import Round
from controler.util import Util


class Controller:
    """ Class Controller"""

    __ALL_PLAYERS = Player().get_players_db()
    __TOURNAMENT = ""

    def __init__(self):
        self.menu = Menu()
        self.util = Util()
        self.date = Date

    def start(self):
        """ Orchestrator"""
        choice = self.menu_principal()
        while choice != 0:
            if choice == 1:
                #Menu().clean()
                choice = self.player_management()
            elif choice == 2:
                #Menu().clean()
                choice = self.tournament_management()
            elif choice == 6:
                #Menu().clean()
                choice = self.create_player()
            elif choice == 7:
                #Menu().clean()
                choice = self.edit_player()
            elif choice == 8:
                #Menu().clean()
                choice = self.new_tournament()
            elif choice == 9:
                choice = self.load_tournament()
            elif choice == 13:
                tournaments = Tournament.get_tournaments()
                Menu().resume_tournament(tournaments)
                choice = 2
                continue
            elif choice == 14:
                choice = self.start_round()
            elif choice == 11:
                Player.load_players()
                self.menu.display_player(Player.get_players_by_name())
                choice = 1
            elif choice == 12:
                Player.load_players()
                Menu().display_player(Player.get_players_by_ranking())
                choice = 1
            else:
                self.start()

    def menu_principal(self):
        Menu().clean()
        Menu().display_menu("menu_principal")
        choice = self.util.choice_int('Enter your choice: ', "^[0-2]")
        if choice == 0:
            exit()
        else:
            return choice

    def player_management(self):
        Menu().display_menu('player_management')
        return self.util.choice_int('Enter your choice: ', "6|7|11|12|99")

    def tournament_management(self):
        Menu().display_menu('tournament_management')
        return self.util.choice_int('Enter your choice: ', "8|9|13|99")

    def create_player(self):
        Menu().display_menu('create_player')
        data_player = {
            'last_name': self.check_input_by_regex("Indicate the Last Name of the player: ", "[A-Za-z]+"),
            'first_name': self.check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+"),
            'date_birth': self.date.check_date('Indicate the Date birth of the player in format dd/mm/yyyy : ', '/'),
            'gender': self.check_input_by_regex('Indicate Gender of the player M/F: ', "^[M|F]"),
            'ranking': self.check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")
        }
        Player.save_player(Player(**data_player))
        Menu().display_menu('menu_create_player')
        return self.util.choice_int('Enter your choice: ', "6|1")

    def new_tournament(self):
        Menu().display_menu('new_tournament')
        data_tournament = {
            'name': self.check_input_by_regex("Indicate the Name of the tournament: ", "[A-Za-z0-9_. ]+"),
            'location': self.check_input_by_regex("Indicate the Location of the tournament: ", "[A-Za-z0-9_. ]+"),
            'start_date': self.date.check_date("Indicate the Start date of the tournament 'dd/mm/yyyy': ", '/'),
            'end_date': self.date.check_date("Indicate the End date of the tournament 'dd/mm/yyyy': ", '/'),
            'nbr_of_turn': self.check_input_by_regex(
                "Indicate the number of rounds (default is 4) of the tournament: ", "^[0-4]"),
            'time_control': self.check_input_by_regex(
                'Indicate the type of game of the tournament Bullet, Blitz or Rapid: ', "^[Bullet|Blitz|Rapid]+"),
            'description': self.check_input_by_regex("Indicate the Description of the tournament: ", "[A-Za-z0-9_. ]+"),
            'players': self.input_players_for_tournament(),
            'rounds': [],
            'status': 'In progress'
        }
        self.__TOURNAMENT = Tournament(**data_tournament)
        self.__TOURNAMENT.first_round()
        index_players_total_point = Round.index_players_total_points(self.__TOURNAMENT.rounds)
        Menu().display_tournament(self.__TOURNAMENT, self.__ALL_PLAYERS, index_players_total_point)
        Menu().display_menu('confirm_tournament')
        if 'N' == Util().check_input_by_regex('Validate this Tournament ? (Y)/(N): ', "^[Y/N]"):
            return 2
        Tournament.save_tournament(self.__TOURNAMENT)
        Menu().start_round(len(self.__TOURNAMENT.rounds))
        return self.util.choice_int('Enter your choice: ', "2|14|99")

    @classmethod
    def load_tournament(cls):
        tournaments = Tournament.get_tournaments()
        tournament_name = Util().check_input_by_regex("Indicate the Name of the Tournament : ", "[A-Za-z0-9.]+")
        tournament = Tournament().find_tournament_by_name(tournament_name)
        if tournament:
            index_players_total_point = Round.index_players_total_points(tournament.rounds)
            Menu().display_tournament(tournament, cls.__ALL_PLAYERS, index_players_total_point)
            if tournament.status == "In progress":
                cls.__TOURNAMENT = tournament
                return 14
            return 2
        else:
            Menu().resume_tournament(tournaments)
            return 9

    def edit_player(self):
        Menu().display_menu('edit_player')
        return self.input_update_rank_player()

    def start_round(self):
        self.__TOURNAMENT.start_round()
        Tournament.update_round_tournament(self.__TOURNAMENT)
        index_players_total_point = Round.index_players_total_points(self.__TOURNAMENT.rounds)
        Menu().display_tournament(self.__TOURNAMENT, self.__ALL_PLAYERS, index_players_total_point)
        self.input_winner_of_round(self.__TOURNAMENT)
        while True:
            if 'Y' == Util().check_input_by_regex('Validate this round ? (Y)/(N): ', "^[Y/N]"):
                self.__TOURNAMENT.stop_round()
                Tournament.update_round_tournament(self.__TOURNAMENT)
            else:
                return 2
            if len(self.__TOURNAMENT.rounds) < int(self.__TOURNAMENT.nbr_of_turn):
                Menu().display_menu('new_round')
                self.__TOURNAMENT.new_round()
                index_players_total_point = Round.index_players_total_points(self.__TOURNAMENT.rounds)
                Menu().display_tournament(self.__TOURNAMENT, self.__ALL_PLAYERS, index_players_total_point)
                Menu().start_round(len(self.__TOURNAMENT.rounds))
                choice_ = self.util.choice_int('Enter your choice: ', "2|14|99")
                if choice_ == 14:
                    self.__TOURNAMENT.start_round()
                    index_players_total_point = Round.index_players_total_points(self.__TOURNAMENT.rounds)
                    Menu().display_tournament(self.__TOURNAMENT, self.__ALL_PLAYERS, index_players_total_point)
                    self.input_winner_of_round(self.__TOURNAMENT)
                else:
                    return choice_
                continue
            else:
                self.__TOURNAMENT.stop()
                Tournament.update_round_tournament(self.__TOURNAMENT)
                index_players_total_point = Round.index_players_total_points(self.__TOURNAMENT.rounds)
                Menu().display_tournament(self.__TOURNAMENT, self.__ALL_PLAYERS, index_players_total_point)
                return 2

    def check_input_by_regex(self, message, regex):
        # check input with regex
        return self.util.check_input_by_regex(message, regex)

    def input_winner_of_round(self, new_tournament):
        points = Tournament.somme_result(new_tournament.rounds[-1].pairs)
        if points >= 4:
            return None
        while True:
            result = self.util.check_input_by_regex(
                "Indicate the Name of the winners or the number of null matches (ex 4) :  ", "[A-Za-z1-4]+"
            )
            points = int(new_tournament.update_round(result))
            index_players_total_point = Round.index_players_total_points(new_tournament.rounds)
            Menu().display_tournament(new_tournament, self.__ALL_PLAYERS, index_players_total_point)
            if points >= 4:
                break

    def input_update_rank_player(self):
        """
            Find player and index by Name and display player
            if Player not found return list of player
        """
        Player.load_players()
        last_name = Util().check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+")
        player = Player.find_player_by_last_name(last_name)
        if player:
            Menu().display_player(player)
            Menu().display_menu('new_rank')
            new_rank = self.util.check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")
            Player.update_rank_player_by_last_name(last_name, new_rank)
            Menu().display_menu('edit_player')
            player = Player.find_player_by_last_name(last_name)
            Menu().display_player(player)
            return 1
        else:
            Menu().display_menu('no_found_player')
            Player.load_players()
            self.menu.display_player(Player.get_players_by_name())
            return 7

    def input_players_for_tournament(self):
        """
            Check player is exist if ok display player
            if Player not found return list of player
            return list 8 index players
        """
        Player.load_players()
        nbr = 0
        index_player = list()
        while nbr < 8:
            name_player = Util().check_input_by_regex(
                    "Indicate the Last Name of player {} of the tournament: ".format(nbr+1), "[A-Za-z]+")
            index = Player().find_index_player_by_last_name(name_player)
            if index:
                Menu().display_player(Player().find_player_by_last_name(name_player))
                Menu().display_menu('confirm_player')
                if index in index_player:
                    Menu().display_menu('player_already_selected')
                    continue
                if 'Y' == self.util.check_input_by_regex('Validate the new player for this game ? (Y)/(N): ', "^[Y/N]"):
                    nbr += 1
                    index_player.append(index)
            else:
                Menu().display_menu('no_found_player')
                Menu().display_player(Player().get_players_by_name())
        return index_player


if __name__ == "__main__":
    pass
