import json

class Automata():

    def __init__(self):
        self.symbols = set()
        self.states = set()
        self.initial_state = None
        self.final_states = set()
        self.transitions = dict()

    def add_transition(self, begin_state, symbol, end_states):
        if end_states == {}:
            self.transitions[begin_state, symbol] = set()
        if end_states <= self.states:
            self.transitions[begin_state, symbol] = end_states
        else:
            states = ','.join(end_states - self.states)
            raise ValueError('States {} do not exist!'.format(states))

    def remove_transition(self, begin_state, symbol):
        pass

    def add_state(self, state):
        if self.initial_state is None:
            self.initial_state = state

        self.states.add(state)

    def remove_state(self, state):
        if state != self.initial_state:
            self.states.discard(state)
            self.final_states.discard(state)

            for symbol in self.symbols:
                if (state, symbol) in self.transitions:
                    del self.transitions[state, symbol]

            empty = set()
            for begin_state, end_state in self.transitions.items():
                end_state.discard(state)
                if end_state == {}:
                    empty.add(begin_state)

            for empty_transition in empty:
                del self.transitions[empty_transition]

        else:
            raise ValueError('Cannot remove initial state')

    def add_symbol(self, symbol):
        self.symbols.add(symbol)

    def remove_symbol(self, symbol):
        self.symbols.discard(symbol)
        for state in self.states:
            if (state, symbol) in self.transitions:
                del self.transitions[state, symbol]

    def add_final_state(self, state):
        self.final_states.add(state)

    def save(self, path):
        pass

    def load(self, path):
        pass
