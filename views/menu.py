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

    def display_menu(self, name_menu):
        """ Display menu """
        s = ""
        for text in getattr(self, name_menu):
            s = s + text + "\n"
        print(s)

    @staticmethod
    def display_player(player):
        """ Display Player  """
        s = "Last Name  : "+player.last_name+"\n"
        s += "First Name : "+player.first_name+"\n"
        s += "Date Birth : "+player.date_birth+"\n"
        s += "Gender     : "+player.gender+"\n"
        s += "Ranking    : "+player.ranking+"\n"
        print(s)

    @staticmethod
    def display_tournament(tournament):
        print(tournament)
        """ Display Tournament """
        s = "========\tTournament Description\t========\n"
        s += "Name : \t\t\t"+tournament.name+"\n"
        s += "Location : \t\t\t"+tournament.location+"\n"
        s += "Start date : \t\t\t"+tournament.start_date+"\n"
        s += "End date : \t\t\t"+tournament.end_date+"\n"
        s += "Nbr of rounds : \t\t"+str(tournament.nbr_of_turn)+"\n"
        s += "Type of game : \t\t\t"+tournament.time_control+"\n"
        s += "Description : \t\t\t"+tournament.description+"\n"
        s += "========================================================="
        print(s)

    @staticmethod
    def display_match(tournament, players):
        turns = tournament.rounds
        for turn in turns:
            pair = turn['pairs']
            print(pair)
            s = "=================\t"+turn['name']+"\t\t=================\n\n"
            s += "Match 1:   Player : " + players[pair[0][0][0]].last_name
            s += "\t\t\tpoint : "+str(pair[0][0][1])+"\n"
            s += "           Player : " +  players[pair[0][1][0]].last_name
            s += "\t\t\tpoint : "+str(pair[0][1][1])+"\n"
            s += "Match 2:   Player : " + players[pair[1][0][0]].last_name
            s += "\t\t\tpoint : "+str(pair[1][0][1])+"\n"
            s += "           Player : " + players[pair[1][1][0]].last_name
            s += "\t\t\tpoint : "+str(pair[1][1][1])+"\n"
            s += "Match 3:   Player : " + players[pair[2][0][0]].last_name
            s += "\t\t\tpoint : "+str(pair[2][0][1])+"\n"
            s += "           Player : " + players[pair[2][1][0]].last_name
            s += "\t\t\tpoint : " + str(pair[2][1][1])+"\n"
            s += "Match 4:   Player : " + players[pair[3][0][0]].last_name
            s += "\t\t\tpoint : " + str(pair[3][0][1]) + "\n"
            s += "           Player : " + players[pair[3][1][0]].last_name
            s += "\t\t\tpoint : "+str(pair[3][1][1])+"\n"
            print(s)
