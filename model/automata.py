import json
from typing import Set, Dict

class Automata():

    def __init__(self):
        self.symbols = None
        self.initial_state = None
        self.final_states = set()
        self.transitions = dict()

    def add_transition(self, begin_state, symbol, end_state):
        self.transitions[begin_state, symbol] = end_state
