"""Class Menu"""
# coding: utf-8


class Menu:
    MENU = {"dashboard": [
            "===      Dashboard       ===",
            "[1]  Player Management",
            "[2]  Tournament Management",
            "[3]  Restore Last State",
            "[4]  Save State",
            "[0]  Exit"],
            "playermanagement": [
            "===  Player Management   ===",
            "[6]  Create Player",
            "[7]  Edit Player",
            "[11] Player by Last Name",
            "[12] Player ranking ",
            "[99] Menu"],
            "tournamentmanagement": [
            "=== Tournament Management ===",
            "[8]  Create Tournament",
            "[9]  Load Tournament",
            "[13] View Tournament",
            "[99] Menu"],
            "createplayer": [
            "=== Create Player ==="],
            "confircreateplayer": [
            "=== Create Player ===",
            "[10] Save new Player And Return Menu ",
            "[6] Create new Player",
            "[1] Player Management"],
            "editplayer": ["=== Edit Player ==="""],
            "newrank": ["""=== Edit Rank ==="""],
            "notfoundplayer": [
            "=== Player Not Found ===",
            " ",
            "List of Players Available"],
            "newtournament": ["===  New Tournament ==="],
            "confirm_player": ["""=== Validate Player """],
            "player_already_selected": ["Player Already Selected in tournament"],
            "player_for_tournament": ["Enter the 8 players for the new tournament"]
            }

    def __init__(self):
        for name_menu, text_menu in self.MENU.items():
            setattr(self, name_menu, text_menu)

    def display_menu(self, name_menu):
        """ Display menu """
        s = ""
        for text in getattr(self, name_menu):
            s = s + text + "\n"
        print(s)

    @staticmethod
    def display_player(player):
        """ Display Player  """
        s = "Last Name  : "+player.Last_Name+"\n"
        s += "First Name : "+player.First_Name+"\n"
        s += "Date Birth : "+player.Date_Birth+"\n"
        s += "Gender     : "+player.Gender+"\n"
        s += "Ranking    : "+player.Ranking+"\n"
        print(s)

    @staticmethod
    def display_tournament(tournament):
        """ Display Tournament """
        s = "========\t\tTournament Description\t\t========\n"
        s += "Name : "+tournament.Name
        s += "\t\t\t\tLocation : "+tournament.Location+"\n"
        s += "Start date : "+tournament.Start_date
        s += "\t\t\tEnd date : "+tournament.End_date+"\n"
        s += "Nbr of rounds : "+str(tournament.Nbr_of_turn)
        s += "\t\t\tType of game : "+tournament.Time_control+"\n"
        s += "Description : "+tournament.Description+"\n"
        s += "=========================================================="
        print(s)

    @staticmethod
    def display_last_first_name(player):
        s = "Last Name  : "+player.Last_Name+"\t\tFirst Name : "+player.First_Name
        print(s)
