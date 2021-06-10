"""Class Controller"""
# coding: utf-8
from view.menu import Menu
from model.player import Player
from model.date import Date
from model.tournament import Tournament
from model.round import Round
import re


class Controller:
    """ Class Controller"""
    __TOURNAMENT = ""

    def start(self):
        """ Orchestrator"""
        choice = self.menu_principal()
        while choice != 0:
            if choice == 1:
                choice = self.player_management()
            elif choice == 2:
                choice = self.tournament_management()
            elif choice == 6:
                choice = self.create_player()
            elif choice == 7:
                choice = Controller.input_update_rank_player()
            elif choice == 8:
                choice = self.new_tournament()
            elif choice == 9:
                choice = self.load_tournament()
            elif choice == 13:
                tournaments = Tournament.get_tournaments()
                Menu().resume_tournament(tournaments)
                choice = 2
            elif choice == 14:
                choice = self.play_tournament()
            elif choice == 11:
                choice = Controller.display_player_by_last_name()
            elif choice == 12:
                choice = Controller.display_player_by_ranking()
            else:
                self.start()

    @staticmethod
    def display_player_by_last_name():
        """
            Display player by last name
            return 1 ( choice display menu player)

        Returns:
            1 (int)
        """
        Player.load_players()
        Menu().display_player(Player.get_players_by_name())
        return 1

    @staticmethod
    def display_player_by_ranking():
        """
            Display player by ranking
            return 1 ( choice display menu player)

        Returns:
            1 (int)
        """
        Player.load_players()
        Menu().display_player(Player.get_players_by_ranking())
        return 1

    @staticmethod
    def check_input_by_regex(message, regex):
        """
            check input by type and by regex
            if ok return input else ask again

        Returns:
            input (str)
        """
        while True:
            try:
                input_str = str(input(message)).capitalize()
            except ValueError:
                # input incorrect retry
                continue
            if not re.fullmatch(regex, input_str):
                # Value input incorrect
                continue
            else:
                return input_str

    @staticmethod
    def menu_principal():
        """
            Clean console
            Display principal menu
            check input if ok return input

        Returns:
         - input (int)
        """
        Menu().clean()
        Menu().display_menu("menu_principal")
        choice = Controller.choice_int('Enter your choice: ', "^[0-2]")
        if choice == 0:
            exit()
        else:
            return choice

    @staticmethod
    def player_management():
        """
            Display menu player_management
            check input if ok return input

        Returns:
         - input (int)
        """
        Menu().display_menu('player_management')
        return Controller.choice_int('Enter your choice: ', "6|7|11|12|99")

    @staticmethod
    def tournament_management():
        """
            Display menu tournament_management
            check input if ok return input

        Returns:
         - input (int)
        """

        Menu().display_menu('tournament_management')
        return Controller.choice_int('Enter your choice: ', "8|9|13|99")

    @staticmethod
    def create_player():
        """
            Display menu_create_player
            check input data for new player
            create and save player
            display  menu_create_player
            check input if ok return input

        Returns:
         - input (int)

        """
        Menu().display_menu('create_player')
        data_player = {
            'last_name': Controller.check_input_by_regex("Indicate the Last Name of the player: ", "[A-Za-z]+"),
            'first_name': Controller.check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+"),
            'date_birth': Date().check_date('Indicate the Date birth of the player in format dd/mm/yyyy : ', '/'),
            'gender': Controller.check_input_by_regex('Indicate Gender of the player M/F: ', "^[M|F]"),
            'ranking': Controller.check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")
        }
        Player.save_player(Player(**data_player))
        Menu().display_menu('menu_create_player')
        return Controller.choice_int('Enter your choice: ', "6|1")

    def new_tournament(self):
        """
            Display new_tournament
            check input data for new tournament
            create new tournament
            create first round
            display  tournament
            if user valid tournament
                save tournament
                start round
                display round
                check input if ok return input
            else return 2 ( menu tournament_management)

        Returns:
         - input (int)

        """
        Menu().display_menu('new_tournament')
        data_tournament = {
            'name': self.check_input_by_regex("Indicate the Name of the tournament: ", "[A-Za-z0-9_. ]+"),
            'location': self.check_input_by_regex("Indicate the Location of the tournament: ", "[A-Za-z0-9_. ]+"),
            'start_date': Date().check_date("Indicate the Start date of the tournament 'dd/mm/yyyy': ", '/'),
            'end_date': Date().check_date("Indicate the End date of the tournament 'dd/mm/yyyy': ", '/'),
            'nbr_of_turn': self.check_input_by_regex(
                "Indicate the number of rounds (default is 4) of the tournament: ", "^[0-4]"),
            'time_control': self.check_input_by_regex(
                'Indicate the type of game of the tournament Bullet, Blitz or Rapid: ', "^[Bullet|Blitz|Rapid]+"),
            'description': self.check_input_by_regex("Indicate the Description of the tournament: ",
                                                     "[A-Za-z0-9_. ]+"),
            'players': self.input_players_for_tournament(),
            'rounds': [],
            'status': 'In progress'
        }

        self.__TOURNAMENT = Tournament(**data_tournament)
        self.__TOURNAMENT.first_round()
        self.display_tournament(self.__TOURNAMENT)
        Menu().display_menu('confirm_tournament')
        if 'N' == Controller.check_input_by_regex('Validate this Tournament ? (Y)/(N): ', "^[Y/N]"):
            return 2
        self.__TOURNAMENT.save_tournament(self.__TOURNAMENT)
        Menu().start_round(len(self.__TOURNAMENT.rounds))
        return Controller.choice_int('Enter your choice: ', "2|14|99")

    def load_tournament(self):
        """
            Load tournament witch input name
            if input tournament exist
                display tournament
                if tournament Finished  => return 2 (display menu tournament_management)
                if tournament In progress =>  load tournament and return 14 ( start the current tour )
            else:
                display resume all tournaments and return 9 (load_tournament)

        Returns:
            - int
        """
        tournaments = Tournament.get_tournaments()
        tournament_name = Controller.check_input_by_regex("Indicate the Name of the Tournament : ", "[A-Za-z0-9.]+")
        tournament = Tournament().find_tournament_by_name(tournament_name)
        if tournament:
            self.display_tournament(tournament)
            if tournament.status == "In progress":
                self.__TOURNAMENT = tournament
                return 14
            return 2
        else:
            Menu().resume_tournament(tournaments)
            return 9

    @classmethod
    def display_tournament(cls, tournament):
        """
            Display Tournament

        Returns:
            - None
        """
        players = Player().get_players_db()
        index_players_total_point = Round.index_players_total_points(tournament.rounds)
        Menu().display_tournament(tournament, players, index_players_total_point)

    @staticmethod
    def valid_round(tournament):
        """
            If user valid round
                save round
                return true
            else
                return false

        Returns
          - bool
        """
        if not tournament.rounds[-1].end_date:
            if 'Y' == Controller.check_input_by_regex('Validate this round ? (Y)/(N): ', "^[Y/N]"):
                tournament.stop_round()
                Tournament.update_round_tournament(tournament)
                return True
            else:
                return False
        else:
            return True

    def play_tournament(self):
        """
            display  tournament
            if round in progress is not valid by user
               return  2  ( menu tournament_management )

            while nbr_round < nbr_of_turn
                if  nbr_round < nbr_of_turn
                    new round
                    display round
                    if user select 14 (  Enter the results of the matches of the Round )
                        continue loop
                    else
                        return choice user to menu
                else
                    stop tournament
                    save tournament
                    display tournament
                    return 2  ( menu tournament_management)

        Returns:
           - int
        """
        while True:
            Controller().display_tournament(self.__TOURNAMENT)
            if not self.input_winner_of_round(self.__TOURNAMENT):
                return 2
            if len(self.__TOURNAMENT.rounds) < int(self.__TOURNAMENT.nbr_of_turn):
                Menu().display_menu('new_round')
                self.__TOURNAMENT.new_round()
                self.display_tournament(self.__TOURNAMENT)
                Menu().start_round(len(self.__TOURNAMENT.rounds))
                choice_ = Controller.choice_int('Enter your choice: ', "2|14|99")
                if choice_ != 14:
                    return choice_
                continue
            else:
                self.__TOURNAMENT.stop()
                Tournament.update_round_tournament(self.__TOURNAMENT)
                self.display_tournament(self.__TOURNAMENT)
                return 2

    def input_winner_of_round(self, new_tournament):
        """
            if the round points are less than 4
                distribute the points in the different matches
                display tournament
                if round isn't valid exit

        Returns:
          - None
        """
        points = Tournament.somme_result(new_tournament.rounds[-1].pairs)
        while points < 4:
            result = Controller.check_input_by_regex(
                "Indicate the Name of the winners or the number of null matches (ex 4) :  ", "[A-Za-z1-4]+"
            )
            points = int(new_tournament.update_round(result))
            self.display_tournament(new_tournament)
        return Controller.valid_round(new_tournament)

    @staticmethod
    def input_update_rank_player():
        """
            Display menu edit player
            Load Players
            search name input player
            if exist :
                display player
                set rank player
                display player
                return 1 ( menu player)
            else:
                display player not found
                display all players
                return 7 (edit player)

        Returns:
            - number (int ) : return 1 ( menu player) or return 7 (edit player)
        """
        Menu().display_menu('edit_player')
        Player.load_players()
        last_name = Controller.check_input_by_regex("Indicate the First Name of the player: ", "[A-Za-z]+")
        player = Player.find_player_by_last_name(last_name)
        if player:
            Menu().display_player(player)
            Menu().display_menu('new_rank')
            new_rank = Controller.check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")
            Player.update_rank_player_by_last_name(last_name, new_rank)
            Menu().display_menu('edit_player')
            player = Player.find_player_by_last_name(last_name)
            Menu().display_player(player)
            return 1
        else:
            Menu().display_menu('no_found_player')
            Player.load_players()
            Menu.display_player(Player.get_players_by_name())
            return 7

    @staticmethod
    def input_players_for_tournament():
        """
            Check player
            if the number players of tournaments is less than 8
                if name player input found display player
                    if the player is validate by user , the player is added to the players
                if Player not found return list of player

        Returns:
            return (list)  index players
        """
        Player.load_players()
        nbr = 0
        index_player = list()
        while nbr < 8:
            name_player = Controller.check_input_by_regex(
                "Indicate the Last Name of player {} of the tournament: ".format(nbr + 1), "[A-Za-z]+")
            index = Player().find_index_player_by_last_name(name_player)
            if index:
                Menu().display_player(Player().find_player_by_last_name(name_player))
                Menu().display_menu('confirm_player')
                if index in index_player:
                    Menu().display_menu('player_already_selected')
                    continue
                if 'Y' == Controller.check_input_by_regex(
                        'Validate the new player for this game ? (Y)/(N): ',
                        "^[Y/N]"):
                    nbr += 1
                    index_player.append(index)
            else:
                Menu().display_menu('no_found_player')
                Menu().display_player(Player().get_players_by_name())
        return index_player

    @staticmethod
    def choice_int(message, regex):
        """
            Check input is valid by regex
            if ok return input else ask again

        Returns:
            input (int)
        """
        while True:
            try:
                result = int(input(message))
            except ValueError:
                continue
            if not re.fullmatch(regex, str(result)):
                continue
            else:
                return result


if __name__ == "__main__":
    pass
