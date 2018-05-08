import json
from collections import OrderedDict

class Grammar():

    def __init__(self):
        self.productions = OrderedDict()

    def initial_symbol(self):
        for k in self.productions.keys():
            return k 

    def add_prod(self, key, set_values):
        self.productions[key] = set_values

    def save(self):
        pass

    def load(self):
        pass
