"""Class TinyDBStore"""
# coding: utf-8
import datetime


class Date:
    """ Class date"""

    @classmethod
    def check_date(cls, message, param):
        """
            check input date if ok return date  else  ask again date
        """
        while True:
            try:
                day, month, year = input(message).split(param)
                return str(datetime.datetime(int(year), int(month), int(day)).strftime("%d/%m/%Y"))
            except ValueError:
                continue

    @staticmethod
    def time_now():
        """ return date """
        return datetime.datetime.now().strftime("%d/%m/%y %H:%M")
