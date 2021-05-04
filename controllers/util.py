import re
import datetime


class Util:

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

    @classmethod
    def check_date(cls, message, param):
        """
         check input date if ok return date
         else  ask again date
        """
        while True:
            try:
                day, month, year = input(message).split(param)
                return str(datetime.datetime(int(year), int(month), int(day)).strftime("%d/%m/%Y"))
            except ValueError:
                continue

    @classmethod
    def choice_int(cls, message):
        """ Check response is valid"""
        while True:
            try:
                return int(input(message))
            except ValueError:
                continue
