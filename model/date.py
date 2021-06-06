"""Class TinyDBStore"""
# coding: utf-8
import datetime


class Date:
    """ Class date"""

    @classmethod
    def check_date(cls, message, param):
        """ check input param if date return date  else ask again date

        Attrs:
        - message (str) : Question that will be asked of the user
        - param (str) : Delimiter to separate days months years

        Returns:
        - returns the date in the format  dd/mm/yyyy
        """
        while True:
            try:
                day, month, year = input(message).split(param)
                return str(datetime.datetime(int(year), int(month), int(day)).strftime("%d/%m/%Y"))
            except ValueError:
                continue

    @staticmethod
    def time_now():
        """ returns the current date

        Returns:
          - returns the current date in the format  dd/mm/yyyy hh:mm
        """
        return datetime.datetime.now().strftime("%d/%m/%y %H:%M")


if __name__ == "__main__":
    pass
