"""Class Controller"""
# coding: utf-8
from views.menu import Menu
from models.tinyDBStore import TinyDBStore
from models.player import Players
from models.round import Round
from models.tournament import Tournament, Tournaments
from controllers.util import Util


#### pour les tests
import random


class Controller:
    """ Class Controller"""
    def start(self):
        """ Orchestrator"""
        Util().clean()
        Menu().display_menu('dashboard')
        choice = Util().choice_int('Enter your choice: ')
        if choice == 0:
            TinyDBStore().close()
            exit()
        while choice != 0:
            if choice == 1:
                Menu().display_menu('playermanagement')
                choice = Util().choice_int('Enter your choice: ')
            elif choice == 2:
                Menu().display_menu('tournamentmanagement')
                choice = Util().choice_int('Enter your choice: ')
            elif choice == 6:
                Menu().display_menu('createplayer')
                Players().add_player(Controller.new_player())
                Menu().display_menu('confircreateplayer')
                choice = Util().choice_int('Enter your choice: ')
            elif choice == 7:
                Menu().display_menu('editplayer')
                last_name_player = Util().check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+")
                choice = Controller.update_rank_player(last_name_player)
            elif choice == 8:
                Util().clean()
                Menu().display_menu('newtournament')
                tournament = Tournament(**Controller.new_tournament(self))
                Menu().display_tournament(tournament)
                Util().clean()
                tournament.create_first_round()
                Tournaments().add_tournament(tournament)
                players = Players().players
                Menu().display_tournament(tournament)
                Menu().display_match(tournament, players)
                Menu().display_menu('Start_first_turn')
                choice = Util().choice_int('Enter your choice: ')
            elif choice == 14:
                tournament.start_round()
                Menu().display_tournament(tournament)
                Menu().display_match(tournament, players)
                while True:
                    result = Util().check_input_by_regex(
                        "Indicate the Name of the winners or the number of null matches (ex 4) :  ",
                        "[A-Za-z0-4]+"
                        )
                    points = int(tournament.update_round(result))
                    #######
                    Tournaments().update_round_tournament(tournament)
                    Menu().display_tournament(tournament)
                    Menu().display_match(tournament, players)
                    if points >= 4:
                        break
                if 'Y' == Util().check_input_by_regex('Validate this round ? (Y)/(N): ', "^[Y/N]"):
                    tournament.stop_round()
                    Tournaments().update_round_tournament(tournament)
                if len(tournament.rounds) < int(tournament.nbr_of_turn):
                    Menu().display_menu('New_round')
                    exit()
                exit()

            elif choice == 11:
                for player in Players().list_player_by_name():
                    Menu().display_player(player)
                choice = 1
            elif choice == 12:
                for player in Players().list_player_by_ranking():
                    Menu().display_player(player)
                choice = 1
            else:
                self.start()

    @staticmethod
    def update_rank_player(name_player):
        """
            Find player and index by Name and display player
            if Player not found return list of player
        """
        player = Players().find_player_by_last_name(name_player)
        if player:
            Menu().display_player(player)
            Menu().display_menu('newrank')
            new_rank = Util().check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")
            Players().update_rank_player_by_last_name(name_player, new_rank)
            Menu().display_menu('editplayer')
            player = Players().find_player_by_last_name(name_player)
            Menu().display_player(player)
            return 1
        else:
            Menu().display_menu('notfoundplayer')
            for player in Players().players:
                Menu().display_player(player)
            return 7

    def select_player_for_tournament(self):
        """
            Find player and index by Name and display player
            if Player not found return list of player
        """

        nbr = 0
        ######### debug
        while nbr < 8:
            nbr += 1
        return [0,1,2,3,4,5,6,7]
        index_ = []
        ##############
        while nbr < 8:
            name_player = Util().check_input_by_regex(
                    "Indicate the Last Name of player {} of the tournament: ".format(nbr+1),
                    "[A-Za-z]+")
            index = Players().find_index_players_by_last_name(name_player)
            if index:
                Menu().display_player(Players().players[index])
                Menu().display_menu('confirm_player')
                if index in index_:
                    Menu().display_menu('player_already_selected')
                    continue
                if 'Y' == Util().check_input_by_regex('Validate the new player for this game ? (Y)/(N): ', "^[Y/N]"):
                    nbr += 1
                    index_.append(index)
            else:
                Util.clean()
                Menu().display_menu('notfoundplayer')
                for player in Players().list_player_by_name():
                    Menu().display_player(player)
        return index_

    @staticmethod
    def new_player():
        """ create new player """
        return {
            "last_name": Util().check_input_by_regex("Indicate the Last Name of the player: ", "[A-Za-z]+"),
            "first_name": Util().check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+"),
            "date_birth": Util().check_date("Indicate the Date birth of the player in format dd/mm/yyyy : ", '/'),
            "gender": Util().check_input_by_regex('Indicate Gender of the player M/F: ', "^[M|F]"),
            "ranking": Util().check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")
        }

    def new_tournament(self):
        """ Create new tournament """
#        return {
#                "name": Util().check_input_by_regex("Indicate the Name of the tournament: ", "[A-Za-z0-9_. ]+"),
#                "location": Util().check_input_by_regex("Indicate the Location of the tournament: ", "[A-Za-z0-9_. ]+"),
#                "start_date": Util().check_date("Indicate the Start date of the tournament 'dd/mm/yyyy': ", '/'),
#                "end_date": Util().check_date("Indicate the End date of the tournament 'dd/mm/yyyy': ", '/'),
#                "nbr_of_turn": Util().choice_int('Indicate the number of rounds (default is 4) of the tournament: '),
#                "time_control": Util().check_input_by_regex(
#                    'Indicate the type of game of the tournament Bullet, Blitz or Rapid: ',
#                    "^[Bullet|Blitz|Rapid]+"),
#                "description": Util().check_input_by_regex("Indicate the Description of the tournament: ",
#                                                           "[A-Za-z0-9_. ]+"),
#                "players": [],
#                "rounds": []
#        }
        return {
                "name": "Test"+str(random.randint(0, 100000)),
                "location": "Paris",
                "start_date": "01/05/2021",
                "end_date": "02/05/2021",
                "nbr_of_turn": "4",
                "time_control": "Blitz",
                "description": "Test Tournois 1",
                "players": Controller.select_player_for_tournament(self),
                "rounds": []
        }
