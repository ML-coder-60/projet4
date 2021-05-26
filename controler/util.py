"""Class Util"""
# coding: utf-8
import re


class Util:
    """ Methode check """

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
    def choice_int(cls, message, regex):
        """ Check response is valid"""
        while True:
            try:
                result = int(input(message))
            except ValueError:
                continue
            if not re.fullmatch(regex, str(result)):
                continue
            else:
                return result
