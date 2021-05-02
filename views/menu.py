"""Class Menu"""
# coding: utf-8
from views.player import Player


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
            "List of Players Available"]
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

    def display_player(self, data):
        """ Display Player  return 1 =>  Player Management """
        [print(Player(x)) for x in data]
        return 1
