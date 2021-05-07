""" Class Player"""
# coding: utf-8


class Player:
    def __init__(self, **player):
        for attr_name, attr_value in player.items():
            setattr(self, attr_name, attr_value)
