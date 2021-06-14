"""Class Menu"""
# coding: utf-8
import os


class Menu:

    MAX_LENGTH = 80
    NAME_LENGTH = 20
    DATE_LENGTH = 12
    GENDER_LENGTH = 8
    ELO_LENGTH = 6
    STATUS_LENGTH = 14
    MENU = {"menu_principal": [
                " Dashboard ".center(MAX_LENGTH, "="),
                "[1]  Player Management",
                "[2]  Tournament Management",
                "[0]  Exit"],
            "player_management": [
                " Player Management ".center(MAX_LENGTH, "="),
                "[6]  Create Player",
                "[7]  Edit Player",
                "[11] Player by Last Name",
                "[12] Player by ranking Elo ",
                "[99] Menu"],
            "tournament_management": [
                " Tournament Management ".center(MAX_LENGTH, "="),
                "[8]  Create Tournament",
                "[9]  Load Tournament",
                "[13] View All Tournaments ",
                "[15] Player sort by ranking Elo for tournament",
                "[16] Player sort by Last Name for tournament",
                "[99] Menu"],
            "create_player": [" Create Player ".center(MAX_LENGTH, "=")],
            "menu_create_player": [
                " Create Player ".center(MAX_LENGTH, "="),
                "[6] Create new Player",
                "[1] Player Management"],
            "edit_player": [" Edit Player ".center(MAX_LENGTH, "=")],
            "new_rank": [" Edit Rank ".center(MAX_LENGTH, "=")],
            "no_found_player": [
                " Player Not Found ".center(MAX_LENGTH, "="),
                " ",
                "List of Players Available"],
            "new_tournament": ["===  New Tournament ==="],
            "confirm_player": ["""=== Validate Player """],
            "player_already_selected": ["Player Already Selected in tournament"],
            "player_for_tournament": ["Enter the 8 players for the new tournament"],
            "new_round": [
                "=".center(MAX_LENGTH, "="),
                "[14] Start new round",
                "[2]  Tournament Management",
                "[99] Menu"],
            "confirm_tournament": ["""=== Validate Tournament """]
            }

    def __init__(self):
        """ Initialisation menu attributes """
        for name_menu, text_menu in self.MENU.items():
            setattr(self, name_menu, text_menu)

    @staticmethod
    def clean():
        """ Clean console

        Returns:
        - none
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self, name_menu):
        """ Display menu

        Attrs:
        - name_menu (str):  name of menu

        Returns:
        - print menu
        """
        s = ""
        for text in getattr(self, str(name_menu)):
            s = s + text + "\n"
        print(s)

    @classmethod
    def display_player(cls, player, title=False):
        """ Display title if not False
            Display Player(s)
            if player is instance display player
            if player list of instances display players
        Attrs:
        - player (list instance):  list instance player
        - title (str) : title

        Returns:
        - print/display info player
        """
        menu = "-".center(cls.MAX_LENGTH, '-') + "\n"
        if title:
            menu += str(title).center(cls.MAX_LENGTH, '-') + "\n\n"
        menu += "Last Name".ljust(cls.NAME_LENGTH) + "First Name".ljust(cls.NAME_LENGTH)
        menu += "Gender".ljust(cls.GENDER_LENGTH) + "Date Birth".ljust(cls.DATE_LENGTH)
        menu += "Elo".ljust(cls.ELO_LENGTH) + "\n"
        if isinstance(player, list):
            s = menu
            for instance_player in player:
                s += instance_player.last_name.ljust(cls.NAME_LENGTH)
                s += instance_player.first_name.ljust(cls.NAME_LENGTH)
                s += instance_player.gender.ljust(cls.GENDER_LENGTH)
                s += instance_player.date_birth.ljust(cls.DATE_LENGTH)
                s += instance_player.ranking.ljust(cls.ELO_LENGTH) + "\n"
            print(s)
        else:
            s = menu
            s += player.last_name.ljust(cls.NAME_LENGTH)
            s += player.first_name.ljust(cls.NAME_LENGTH)
            s += player.gender.ljust(cls.GENDER_LENGTH)
            s += player.date_birth.ljust(cls.DATE_LENGTH)
            s += player.ranking.ljust(cls.ELO_LENGTH) + "\n"
            print(s)

    def display_tournament(self, tournament, players, index_player_and_points):
        """ Display Tournament

        Attrs:
        - tournament (instance):  instance tournament
        - players (instance) : list instances players
        - index_player_and_points  (dictionary):
              { index_player_x: total_points_game, index_player_y: total_points_game ....}

        Returns:
        - print/display info player
        """
        self.clean()
        s = " Tournament Description ".center(self.MAX_LENGTH, '=')+"\n"
        s += "Name : ".ljust(self.NAME_LENGTH)+tournament.name.ljust(self.NAME_LENGTH)
        s += "Location : ".ljust(self.NAME_LENGTH)+tournament.location.ljust(self.NAME_LENGTH)+"\n"
        s += "Start date : ".ljust(self.NAME_LENGTH)+tournament.start_date.ljust(self.NAME_LENGTH)
        s += "End date : ".ljust(self.NAME_LENGTH)+tournament.end_date.ljust(self.NAME_LENGTH)+"\n"
        s += "Nbr of rounds : ".ljust(self.NAME_LENGTH)+str(tournament.nbr_of_turn).ljust(self.NAME_LENGTH)
        s += "Type of game : ".ljust(self.NAME_LENGTH)+tournament.time_control.ljust(self.NAME_LENGTH)+"\n"
        s += "Description : ".ljust(self.NAME_LENGTH)+tournament.description.ljust(self.NAME_LENGTH)+"\n\n"
        s += "=".center(self.MAX_LENGTH, '=')+"\n"
        turns = tournament.rounds
        if len(turns) > 0:
            for turn in turns:
                pairs = turn.pairs
                s += turn.name.center(self.MAX_LENGTH, '=')+"\n"
                s += "Start date : ".ljust(self.NAME_LENGTH)+turn.start_date+"\n"
                if turn.end_date:
                    s += "End date : ".ljust(self.NAME_LENGTH)+turn.end_date+"\n"
                num_match = 1
                for match in pairs:
                    str_match = "Match "+str(num_match)
                    s += str_match.center(self.MAX_LENGTH, '-')+"\n"
                    s += "Player".ljust(self.NAME_LENGTH) + "Elo".ljust(self.ELO_LENGTH)
                    s += "Pts".ljust(self.ELO_LENGTH) + "Total Pts".ljust(self.STATUS_LENGTH) + "\n"
                    s += players[match[0][0]].last_name.ljust(self.NAME_LENGTH)
                    s += players[match[0][0]].ranking.ljust(self.ELO_LENGTH)
                    s += str(match[0][1]).ljust(self.ELO_LENGTH)
                    s += str(index_player_and_points[match[0][0]]).ljust(self.STATUS_LENGTH) + "\n"
                    s += players[match[1][0]].last_name.ljust(self.NAME_LENGTH)
                    s += players[match[1][0]].ranking.ljust(self.ELO_LENGTH)
                    s += str(match[1][1]).ljust(self.ELO_LENGTH)
                    s += str(index_player_and_points[match[1][0]]).ljust(self.STATUS_LENGTH) + "\n"
                    num_match += 1
        print(s)

    @classmethod
    def start_round(cls, nbr_round):
        """ Display start_round

        Attrs:
        - nbr_round (int):  number of round

        Returns:
        - print/display menu start round
        """
        s = "=".center(cls.MAX_LENGTH, '=')+"\n"
        s += "[14] Enter the results of the matches of the Round "+str(nbr_round)+"\n"
        s += "[2]  Tournament Management\n"
        s += "[99] Menu\n"
        print(s)

    @classmethod
    def resume_tournament(cls, tournaments):
        """ Print resume tournament

        Attrs:
        - tournaments (list instance):  instances tournaments

        Returns:
            - print/display resume tournament
        """
        s = " Tournament List ".center(cls.MAX_LENGTH, '=')+"\n"
        s += "  Name".ljust(cls.NAME_LENGTH)
        s += "  Date".ljust(cls.DATE_LENGTH)
        s += "  Status".ljust(cls.STATUS_LENGTH)+"\n"
        for tournament in tournaments:
            s += str(tournament.name).ljust(cls.NAME_LENGTH)
            s += str(tournament.end_date).ljust(cls.DATE_LENGTH)
            s += str(tournament.status).ljust(cls.STATUS_LENGTH)+"\n"
        print(s)


if __name__ == "__main__":
    pass
