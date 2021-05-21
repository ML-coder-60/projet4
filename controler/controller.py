"""Class Controller"""
# coding: utf-8
from view.menu import Menu
from model.player import Player
from model.date import Date
from model.tournament import Tournament
from controler.util import Util


class Controller:
    """ Class Controller"""
    def __init__(self):
        self.menu = Menu()
        self.player = Player()
        self.util = Util()
        self.date = Date
        self.tournament = Tournament

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
                new_player = Player(**data_player)
                new_player.save_players()
                self.player.save_player(new_player)
                Menu().display_menu('menu_create_player')
                choice = self.util.choice_int('Enter your choice: ', "6|1")
            elif choice == 7:
                Menu().display_menu(choice)
                choice = self.input_update_rank_player(choice)
            elif choice == 8:
                Menu().display_menu(choice)
                players = Player().list_players()
#                data_tournament = {'name': self.input_name_tournament(),
#                                   'location': self.input_location_tournament(),
#                                   'start_date': self.input_start_date_tournament(),
#                                   'end_date': self.input_end_date_tournament(),
#                                   'nbr_of_turn': self.input_nrb_of_turn_tournament(),
#                                   'time_control': self.input_time_control_tournament(),
#                                   'description': self.input_description_tournament(),
#                                   'players': self.input_select_player_for_tournament()
#                                   }
                data_tournament = {'name': "test",
                                   'location': "Paris",
                                   'start_date': "02/03/2020",
                                   'end_date': "03/04/2020",
                                   'nbr_of_turn': "4",
                                   'time_control': "Blitz",
                                   'description': "sdfgdsqffgdsfgsdsfgd",
                                   'players': self.input_players_for_tournament()
                                   }

                new_tournament = Tournament(**data_tournament)
                Menu().display_tournament(new_tournament, players)
                new_tournament.create_first_round()
                Menu().display_tournament(new_tournament, players)
                Menu().display_menu('Start_first_turn')
                choice = self.util.choice_int('Enter your choice: ', "2|14|99")
            elif choice == 14:
                new_tournament.start_round()
                Menu().display_tournament(new_tournament, players)
                while True:
                    result = self.util.check_input_by_regex(
                        "Indicate the Name of the winners or the number of null matches (ex 4) :  ",
                        "[A-Za-z1-4]+"
                        )
                    points = int(new_tournament.update_round(result))
                    Tournament().update_round(points)
                    Menu().display_tournament(new_tournament, players)
                    if points >= 4:
                        break
                if 'Y' == Util().check_input_by_regex('Validate this round ? (Y)/(N): ', "^[Y/N]"):
                    new_tournament.stop_round()
                    Tournament().update_round_tournament(new_tournament)
                if len(new_tournament.rounds) < int(new_tournament.nbr_of_turn):
                    Menu().display_menu('New_round')
                    new_tournament.new_round()
                    players = Player().list_players()
                    Menu().display_tournament(new_tournament, players)
                    Menu().display_menu('Start_first_turn')
                    choice = Util().choice_int('Enter your choice: ')
                    exit()
                exit()

            elif choice == 11:
                self.player.load_players()
                for player in self.player.players_by_name():
                    self.menu.display_player(player)
                choice = 1
            elif choice == 12:
                self.player.load_players()
                for player in self.player.players_by_ranking():
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

    def input_update_rank_player(self, choice):
        """
            Find player and index by Name and display player
            if Player not found return list of player
        """
        self.player.load_players()
        last_name = Util().check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+")
        player = self.player.find_player_by_last_name(last_name)
        if player:
            Menu().display_player(player)
            Menu().display_menu('new_rank')
            new_rank = self.util.check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")
            self.player.update_rank_player_by_last_name(last_name, new_rank)
            Menu().display_menu(choice)
            player = self.player.find_player_by_last_name(last_name)
            Menu().display_player(player)
            return 1
        else:
            Menu().display_menu('no_found_player')
            self.player.load_players()
            for player in self.player.players_by_name():
                self.menu.display_player(player)
            return 7


    def input_players_for_tournament(self):
        """
            Check player is exist if ok display player
            if Player not found return list of player
            return list 8 index players
        """
        self.player.load_players()
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
                for player in self.player.players_by_name():
                    Menu().display_player(player)
        return index_player