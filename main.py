from views.menu import *
from models.model import *
from controllers.controller import *

# charge les Menu et les model
menu = Menu()
model = Model()
control = Controller(menu, model)
# lance le menu
control.start()
