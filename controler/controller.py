"""Class Controller"""
# coding: utf-8
from view.menu import Menu
from model.player import Player
from model.date import Date
from model.tournament import Tournament
from model.round import Round
from controler.util import Util

## debug
import random


class Controller:
    """ Class Controller"""

    __ALL_PLAYERS = Player().get_players_db()

    def __init__(self):
        self.menu = Menu()
        self.util = Util()
        self.date = Date

    def start(self):
        """ Orchestrator"""
        Menu().display_menu("99")
        choice = self.util.choice_int('Enter your choice: ', "^[0-4]")
        if choice == 0:
            exit()
        while choice != 0:
            if choice == 1:
                self.menu.display_menu(choice)
                choice = self.util.choice_int('Enter your choice: ', "6|7|11|12|99")
            elif choice == 2:
                self.menu.display_menu(choice)
                choice = Util().choice_int('Enter your choice: ', "8|9|13|99")
            elif choice == 6:
                Menu().display_menu(choice)
                data_player = {'last_name': self.input_last_name(),
                               'first_name': self.input_first_name(),
                               'date_birth': self.input_date_birth(),
                               'gender': self.input_gender(),
                               'ranking': self.input_ranking()
                               }
                Player.save_player(Player(**data_player))
                Menu().display_menu('menu_create_player')
                choice = self.util.choice_int('Enter your choice: ', "6|1")
            elif choice == 7:
                Menu().display_menu(choice)
                choice = self.input_update_rank_player(choice)
            elif choice == 8:
                Menu().display_menu(choice)
#                data_tournament = {'name': self.input_name_tournament(),
#                                   'location': self.input_location_tournament(),
#                                   'start_date': self.input_start_date_tournament(),
#                                   'end_date': self.input_end_date_tournament(),
#                                   'nbr_of_turn': self.input_nrb_of_turn_tournament(),
#                                   'time_control': self.input_time_control_tournament(),
#                                   'description': self.input_description_tournament(),
#                                   'players': self.input_select_player_for_tournament()
#                                    'rounds': [],
#                                    'status': 'In progress'
#                                   }
                data_tournament = {'name': "test"+str(random.randint(0, 1000)),
                                   'location': "Paris",
                                   'start_date': "02/03/2020",
                                   'end_date': "03/04/2020",
                                   'nbr_of_turn': "4",
                                   'time_control': "Blitz",
                                   'description': "sdfgdsqffgdsfgsdsfgd",
                                   'players': self.input_players_for_tournament(),
                                   'rounds': [],
                                   'status': 'In progress'}
                new_tournament = Tournament(**data_tournament)
                new_tournament.first_round()
                index_players_total_point = Round.index_players_total_points(new_tournament.rounds)
                Menu().display_tournament(new_tournament, self.__ALL_PLAYERS, index_players_total_point)
                Menu().display_menu('confirm_tournament')
                if 'N' == Util().check_input_by_regex('Validate this Tournament ? (Y)/(N): ', "^[Y/N]"):
                    choice = 2
                    continue
                Tournament.save_tournament(new_tournament)
                Menu().start_round(len(new_tournament.rounds))
                choice = self.util.choice_int('Enter your choice: ', "2|14|99")
#            elif choice == 9:
#                tournaments = Tournament.get_tournaments()
#                for player in Player.get_players_by_ranking():
#                   Menu().display_player(player)
#                choice = 2
            elif choice == 13:
                tournaments = Tournament.get_tournaments()
                Menu().resume_tournament(tournaments)
                choice = 2
                continue
            elif choice == 14:
                new_tournament.start_round()
                Tournament.update_round_tournament(new_tournament)
                index_players_total_point = Round.index_players_total_points(new_tournament.rounds)
                Menu().display_tournament(new_tournament, self.__ALL_PLAYERS, index_players_total_point)
                self.input_winner_of_round(new_tournament)
                while True:
                    if 'Y' == Util().check_input_by_regex('Validate this round ? (Y)/(N): ', "^[Y/N]"):
                        new_tournament.stop_round()
                        Tournament.update_round_tournament(new_tournament)
                    else:
                        choice = 2
                        break
                    if len(new_tournament.rounds) < int(new_tournament.nbr_of_turn):
                        Menu().display_menu('new_round')
                        new_tournament.new_round()
                        index_players_total_point = Round.index_players_total_points(new_tournament.rounds)
                        Menu().display_tournament(new_tournament, self.__ALL_PLAYERS, index_players_total_point)
                        Menu().start_round(len(new_tournament.rounds))
                        choice_ = self.util.choice_int('Enter your choice: ', "2|14|99")
                        if choice_ == 14:
                            new_tournament.start_round()
                            index_players_total_point = Round.index_players_total_points(new_tournament.rounds)
                            Menu().display_tournament(new_tournament, self.__ALL_PLAYERS, index_players_total_point)
                            self.input_winner_of_round(new_tournament)
                        continue
                    else:
                        new_tournament.stop()
                        index_players_total_point = Round.index_players_total_points(new_tournament.rounds)
                        Menu().display_tournament(new_tournament, self.__ALL_PLAYERS, index_players_total_point)
                        choice = 2
                        break
            elif choice == 11:
                Player.load_players()
                for player in Player.get_players_by_name():
                    self.menu.display_player(player)
                choice = 1
            elif choice == 12:
                Player.load_players()
                for player in Player.get_players_by_ranking():
                    Menu().display_player(player)
                choice = 1
            else:
                self.start()

    def input_last_name(self):
        return self.util.check_input_by_regex("Indicate the Last Name of the player: ", "[A-Za-z]+")

    def input_first_name(self):
        return self.util.check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+")

    def input_date_birth(self):
        return self.date.check_date("Indicate the Date birth of the player in format dd/mm/yyyy : ", '/')

    def input_gender(self):
        return self.util.check_input_by_regex('Indicate Gender of the player M/F: ', "^[M|F]")

    def input_ranking(self):
        return self.util.check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")

    def input_name_tournament(self):
        return self.util.check_input_by_regex("Indicate the Name of the tournament: ", "[A-Za-z0-9_. ]+")

    def input_location_tournament(self):
        return self.util.check_input_by_regex("Indicate the Location of the tournament: ", "[A-Za-z0-9_. ]+")

    def input_start_date_tournament(self):
        return self.date.check_date("Indicate the Start date of the tournament 'dd/mm/yyyy': ", '/')

    def input_end_date_tournament(self):
        return self.date.check_date("Indicate the End date of the tournament 'dd/mm/yyyy': ", '/')

    def input_nrb_of_turn_tournament(self):
        return self.util.choice_int('Indicate the number of rounds (default is 4) of the tournament: ', "^[0-4]")

    def input_time_control_tournament(self):
        return self.util.check_input_by_regex('Indicate the type of game of the tournament Bullet, Blitz or Rapid: ',
                                              "^[Bullet|Blitz|Rapid]+")

    def input_description_tournament(self):
        return self.util.check_input_by_regex("Indicate the Description of the tournament: ", "[A-Za-z0-9_. ]+")

    def input_winner_of_round(self, new_tournament):
        while True:
            result = self.util.check_input_by_regex(
                "Indicate the Name of the winners or the number of null matches (ex 4) :  ",
                "[A-Za-z1-4]+"
            )
            points = int(new_tournament.update_round(result))
            index_players_total_point = Round.index_players_total_points(new_tournament.rounds)
            Menu().display_tournament(new_tournament, self.__ALL_PLAYERS, index_players_total_point)
            if points >= 4:
                break

    def input_update_rank_player(self, choice):
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
            Menu().display_menu(choice)
            player = Player.find_player_by_last_name(last_name)
            Menu().display_player(player)
            return 1
        else:
            Menu().display_menu('no_found_player')
            Player.load_players()
            for player in Player.get_players_by_name():
                self.menu.display_player(player)
            return 7

    def input_players_for_tournament(self):
        """
            Check player is exist if ok display player
            if Player not found return list of player
            return list 8 index players
        """
        Player.load_players()
        nbr = 0

        ### debug
        while nbr < 8:
            nbr += 1
        return [0,1,2,3,4,5,6,7]

        index_player = list()
        while nbr < 8:
            name_player = Util().check_input_by_regex(
                    "Indicate the Last Name of player {} of the tournament: ".format(nbr+1),
                    "[A-Za-z]+")
            index = self.player.find_index_player_by_last_name(name_player)
            if index:
                Menu().display_player(self.player.find_player_by_last_name(name_player))
                Menu().display_menu('confirm_player')
                if index in index_player:
                    Menu().display_menu('player_already_selected')
                    continue
                if 'Y' == self.util.check_input_by_regex('Validate the new player for this game ? (Y)/(N): ', "^[Y/N]"):
                    nbr += 1
                    index_player.append(index)
            else:
                Menu().display_menu('no_found_player')
                for player in self.player.get_players_by_name():
                    Menu().display_player(player)
        return index_player