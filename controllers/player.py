import re
import datetime


class Player:

    def new_player(self):
        """ create new player """
        player = dict()
        player['Last Name'] = self.check_input_name('Last')
        player['First Name'] = self.check_input_name('First')
        player['Date Birth'] = self.get_date_player()
        player['Gender'] = self.check_input_gender()
        player['Ranking'] = self.check_input_rank()
        return player

    @classmethod
    def check_input_by_regex(cls, message, regex):
        """
            check input by type and by regex
            if ok return data input else ask again
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

    def check_input_name(self, parm):
        """ methode check_input_name """
        return self.check_input_by_regex("Indicate the {} Name of the player: ".format(parm), "[A-Za-z]+")

    def check_input_rank(self):
        """ methode check_input_rank """
        return self.check_input_by_regex("indicate the player's Ranking: ", "[0-9]{4}")

    def check_input_gender(self):
        """ methode check_input_gender """
        return self.check_input_by_regex('Indicate Gender of the player M/F: ', "^[M|F]")

    @classmethod
    def get_date_player(cls):
        """
         check input date if ok return date
         else  ask again date
        """
        while True:
            try:
                day, month, year = input("Indicate the Date birth of the player in format 'dd/mm/yyyy': ").split('/')
                return str(datetime.datetime(int(year), int(month), int(day)).strftime("%d/%m/%Y"))
            except ValueError:
                continue
