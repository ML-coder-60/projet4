"""Class TinyDBStore"""
# coding: utf-8
from models.player import Player
from models.tinyDBStore import TinyDBStore


class Model:
    def __init__(self):
        self.player = Player()
        self.dao = TinyDBStore()
