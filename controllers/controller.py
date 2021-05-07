"""Class Controller"""
# coding: utf-8
from models.player import Player
from models.tournament import Tournament
from controllers.util import Util


class Controller:
    """ Class Controller"""
    def __init__(self, menu, model):
        self.menu = menu
        self.model = model

    def start(self):
        """ Orchestrator"""
        Util().clean()
        self.menu.display_menu('dashboard')
        choice = Util().choice_int('Enter your choice: ')
        if choice == 0:
            self.model.dao.close()
            exit()
        while choice != 0:
            if choice == 1:
                self.menu.display_menu('playermanagement')
                choice = Util().choice_int('Enter your choice: ')
            elif choice == 2:
                self.menu.display_menu('tournamentmanagement')
                choice = Util().choice_int('Enter your choice: ')
            elif choice == 6:
                self.menu.display_menu('createplayer')
                new_player = Player(**Controller.new_player())
                self.model.add_player(new_player)
                self.menu.display_menu('confircreateplayer')
                choice = Util().choice_int('Enter your choice: ')
            elif choice == 7:
                self.menu.display_menu('editplayer')
                last_name_player = Util().check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+")
                choice = self.update_rank_player(last_name_player)
            elif choice == 8:
                Util().clean()
                self.menu.display_menu('newtournament')
                new_tournament = Tournament(**Controller.new_tournament())
                self.menu.display_tournament(new_tournament)
                self.menu.display_menu('player_for_tournament')
                players_tournament = self.select_player_for_tournament(new_tournament)
                Util.clean()
                self.menu.display_tournament(new_tournament)
                for player in players_tournament:
                    self.menu.display_last_first_name(player)
                choice = Util().choice_int('Enter your choice: ')

            elif choice == 10:
                choice = self.model.save_player()
            elif choice == 11:
                for player in self.model.list_player_by_name():
                    self.menu.display_player(player)
                choice = 1
            elif choice == 12:
                for player in self.model.list_player_by_ranking():
                    self.menu.display_player(player)
                choice = 1
            else:
                self.start()

    def update_rank_player(self, name_player):
        """
            Find player and index by Name and display player
            if Player not found return list of player
        """
        player = self.model.find_player_by_last_name(name_player)
        if player:
            self.menu.display_player(player)
            self.menu.display_menu('newrank')
            new_rank = Util().check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")
            self.model.update_rank_player_by_last_name(name_player, new_rank)
            self.menu.display_menu('editplayer')
            self.menu.display_player(player)
            return 1
        else:
            self.menu.display_menu('notfoundplayer')
            for player in self.model.list_players():
                self.menu.display_player(player)
            return 7

    def select_player_for_tournament(self, tournament):
        """
            Find player and index by Name and display player
            if Player not found return list of player
        """
        players_tournament = []
        name_players = []
        nbr = 0
        while nbr < 3:
            name_player = Util().check_input_by_regex(
                    "Indicate the Last Name of player {} of the tournament: ".format(nbr+1),
                    "[A-Za-z]+")
            player = self.model.find_player_by_last_name(name_player)
            if player:
                self.menu.display_player(player)
                self.menu.display_menu('confirm_player')
                if name_player in name_players:
                    self.menu.display_menu('player_already_selected')
                    continue
                if 'Y' == Util().check_input_by_regex('Validate the new player for this game ? (Y)/(N): ', "^[Y/N]"):
                    nbr += 1
                    name_players.append(name_player)
                    players_tournament.append(player)
            else:
                Util.clean()
                self.menu.display_menu('notfoundplayer')
                for player in self.model.list_player_by_name():
                    self.menu.display_player(player)
                self.menu.display_tournament(tournament)
        return players_tournament

    @staticmethod
    def new_player():
        """ create new player """
        return {
            "Last_Name": Util().check_input_by_regex("Indicate the Last Name of the player: ", "[A-Za-z]+"),
            "First_Name": Util().check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+"),
            "Date_Birth": Util().check_date("Indicate the Date birth of the player in format dd/mm/yyyy : ", '/'),
            "Gender": Util().check_input_by_regex('Indicate Gender of the player M/F: ', "^[M|F]"),
            "Ranking": Util().check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")
        }

    @staticmethod
    def new_tournament():
        """ Create new tournament """
        return {
                "Name": Util().check_input_by_regex("Indicate the Name of the tournament: ", "[A-Za-z0-9_. ]+"),
                "Location": Util().check_input_by_regex("Indicate the Location of the tournament: ", "[A-Za-z0-9_. ]+"),
                "Start_date": Util().check_date("Indicate the Start date of the tournament 'dd/mm/yyyy': ", '/'),
                "End_date": Util().check_date("Indicate the End date of the tournament 'dd/mm/yyyy': ", '/'),
                "Nbr_of_turn": Util().choice_int('Indicate the number of rounds (default is 4) of the tournament: '),
                "Time_control": Util().check_input_by_regex(
                    'Indicate the type of game of the tournament Bullet, Blitz or Rapid: ',
                    "^[Bullet|Blitz|Rapid]+"),
                "Description": Util().check_input_by_regex("Indicate the Description of the tournament: ",
                                                           "[A-Za-z0-9_. ]+")
        }
