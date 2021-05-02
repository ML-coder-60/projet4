"""Class Controller"""
# coding: utf-8

from controllers.player import Player


class Controller:
    """ Class Controller"""
    def __init__(self, menu, model):
        self.menu = menu
        self.model = model
        self.player = Player()

    def start(self):
        """ Orchestrator"""
        self.menu.display_menu('dashboard')
        choice = self.choice_int()
        if choice == 0:
            self.model.dao.close()
            exit()
        while choice != 0:
            if choice == 1:
                self.menu.display_menu('playermanagement')
                choice = self.choice_int()
            elif choice == 2:
                self.menu.display_menu('tournamentmanagement')
                choice = self.choice_int()
            elif choice == 6:
                self.menu.display_menu('createplayer')
                new_player = self.player.new_player()
                self.model.player.add_player(new_player)
                self.menu.display_menu('confircreateplayer')
                choice = self.choice_int()
            elif choice == 7:
                self.menu.display_menu('editplayer')
                last_name_player = self.player.check_input_name('Last')
                choice = self.update_rank_player(last_name_player)
            elif choice == 10:
                choice = self.model.player.save_player()
            elif choice == 11:
                choice = self.menu.display_player(self.model.player.list_player_by_name())
            elif choice == 12:
                choice = self.menu.display_player(self.model.player.list_player_by_ranking())
            else:
                self.start()

    @classmethod
    def choice_int(cls, request="Enter your choice: "):
        """ Check response is valid"""
        while True:
            try:
                return int(input(request))
            except ValueError:
                continue

    def update_rank_player(self, name_player):
        """
            Find player and index by Name and display player
            if Player not found return list of player
        """
        player, index = self.model.player.find_index_player(name_player)
        if isinstance(player, dict):
            self.menu.display_player([player])
            self.menu.display_menu('newrank')
            new_rank = self.player.check_input_rank()
            self.model.player.update_rank_player_by_index(index, new_rank)
            self.menu.display_menu('editplayer')
            self.menu.display_player([player])
            return 1
        else:
            self.menu.display_menu('notfoundplayer')
            players = self.model.player.players
            self.menu.display_player(players)
            return 7
