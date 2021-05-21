"""Class Menu"""
# coding: utf-8
import os


class Menu:
    MENU = {"99": [
                "===      Dashboard       ===",
                "[1]  Player Management",
                "[2]  Tournament Management",
                "[3]  Restore Last State",
                "[4]  Save State",
                "[0]  Exit"],
            "1": [
                "===  Player Management   ===",
                "[6]  Create Player",
                "[7]  Edit Player",
                "[11] Player by Last Name",
                "[12] Player ranking ",
                "[99] Menu"],
            "2": [
                "=== Tournament Management ===",
                "[8]  Create Tournament",
                "[9]  Load Tournament",
                "[13] View Tournament",
                "[99] Menu"],
            "6": [
                "=== Create Player ==="],
            "menu_create_player": [
                "=== Create Player ===",
                "[6] Create new Player",
                "[1] Player Management"],
            "7": ["=== Edit Player ==="""],
            "new_rank": ["""=== Edit Rank ==="""],
            "no_found_player": [
                "=== Player Not Found ===",
                " ",
                "List of Players Available"],
            "8": ["===  New Tournament ==="],
            "confirm_player": ["""=== Validate Player """],
            "player_already_selected": ["Player Already Selected in tournament"],
            "player_for_tournament": ["Enter the 8 players for the new tournament"],
            "Start_first_turn": [
                "=========================================================",
                "[14] Start round 1",
                "[2]  Tournament Management",
                "[99] Menu"],
            "New_round": [
                "=========================================================",
                "[14] Start new round",
                "[2]  Tournament Management",
                "[99] Menu"],
            }

    def __init__(self):
        for name_menu, text_menu in self.MENU.items():
            setattr(self, name_menu, text_menu)

    @staticmethod
    def clean():
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self, name_menu):
        """ Display menu """
        if name_menu == 99:
            self.clean()
        s = ""
        for text in getattr(self, str(name_menu)):
            s = s + text + "\n"
        print(s)

    @staticmethod
    def display_player(player):
        """ Display Player  """
        s = "Last Name  : "+player.last_name+"\t\tFirst Name : "+player.first_name+" ("+player.gender+")\n"
        s += "Date Birth : "+player.date_birth+"\t\tRanking  Elo : "+player.ranking+"\n"
        print(s)

    @staticmethod
    def display_tournament(tournament, players):
        """ Display Tournament """
        s = "========\tTournament Description\t========\n"
        s += "Name : \t\t\t"+tournament.name+"\n"
        s += "Location : \t\t\t"+tournament.location+"\n"
        s += "Start date : \t\t\t"+tournament.start_date+"\n"
        s += "End date : \t\t\t"+tournament.end_date+"\n"
        s += "Nbr of rounds : \t\t"+str(tournament.nbr_of_turn)+"\n"
        s += "Type of game : \t\t\t"+tournament.time_control+"\n"
        s += "Description : \t\t\t"+tournament.description+"\n"
        s += "=========================================================\n"
        turns = tournament.rounds
        if len(turns) > 0:
            for turn in turns:
                pairs = turn.pairs
                s += "=================\t"+turn.name+"\t\t=================\n\n"
                num_match = 1
                for match in pairs:
                    amatch = list(match)
                    s += "Match "+str(num_match)+":   Player : " + players[amatch[0][0]].last_name
                    s += "\t\tElo(" + players[amatch[0][0]].ranking
                    s += ")  point : " + str(amatch[0][1]) + "\n"
                    s += "           Player : " + players[amatch[1][0]].last_name
                    s += "\t\tElo(" + players[amatch[1][0]].ranking
                    s += ")  point : " + str(amatch[1][1]) + "\n"
                    num_match += 1
        print(s)
