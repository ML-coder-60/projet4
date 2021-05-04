from controllers.util import Util


class Player:

    def new_player(self):
        """ create new player """
        player = dict()
        player['Last Name'] = self.check_input_name('Last')
        player['First Name'] = self.check_input_name('First')
        player['Date Birth'] = self.check_date_player()
        player['Gender'] = self.check_input_gender()
        player['Ranking'] = self.check_input_rank()
        return player

    @staticmethod
    def check_input_name(parm):
        """ methode check_input_name """
        return Util().check_input_by_regex("Indicate the {} Name of the player: ".format(parm), "[A-Za-z]+")

    @staticmethod
    def check_input_rank():
        """ methode check_input_rank """
        return Util().check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")

    @staticmethod
    def check_input_gender():
        """ methode check_input_gender """
        return Util().check_input_by_regex('Indicate Gender of the player M/F: ', "^[M|F]")

    @staticmethod
    def check_date_player():
        """ methode check_input_date """
        return Util().check_date("Indicate the Date birth of the player in format 'dd/mm/yyyy': ", '/')
