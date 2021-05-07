from views.menu import *
from models.model import Model
from controllers.controller import Controller

# charge les Menu et les model
menu = Menu()
model = Model()
control = Controller(menu, model)
# lance le menu
control.start()
