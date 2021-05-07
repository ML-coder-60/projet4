"""Class Tournament"""
# coding: utf-8


class Tournament:
    def __init__(self, **tournament):
        for attr_name, attr_value in tournament.items():
            setattr(self, attr_name, attr_value)
