"""Class Round"""
# coding: utf-8


class Round:
    """ Class Round """

    __ROUNDS = []

    def __init__(self, name, start_date, end_date, index_players):
        """Initialisation"""
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.pairs = [
                    ([index_players[0], 0], [index_players[4], 0]),
                    ([index_players[1], 0], [index_players[5], 0]),
                    ([index_players[2], 0], [index_players[6], 0]),
                    ([index_players[3], 0], [index_players[7], 0])
                ]
