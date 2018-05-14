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
        if state in self.final_states:
            self.final_states.discard(state)
        else:
            self.final_states.add(state)

    def membership(self, sentence):
        current_states = set()
        current_states.add(self.initial_state)
        temporary_states = set()
        for symbol in sentence:
            for state in current_states:
                [temporary_states.add(k) for k in self.transitions[state, symbol]]
            current_states.clear()
            [current_states.add(v) for v in temporary_states]
            temporary_states.clear()

        return ((current_states & self.final_states) != set())

    def determinize(self):
        statesToDeterminize = list()

        newTransitions = dict()
        newStates = set()
        newFinalStates = set()
        newInitialState = "{" + self.initial_state + "}"
        newStates.add(newInitialState)
        statesToDeterminize.append(newInitialState)
        self.initial_state = newInitialState

        for state in statesToDeterminize:
            isFinalState = False
            state = state[:-1]
            state = state.replace('{', '')
            state = state.replace(' ', '')
            for symbol in self.symbols:
                newState = "{"
                determinization = set()

                for st in state.split(','):
                    for t in self.transitions[st, symbol]:
                        determinization.add(t)
                
                for d in determinization:
                    if d in self.final_states:
                        isFinalState = True

                    newState += d + ","

                newState = newState[:-1] + '}'
                newStates.add(newState)
                if isFinalState:
                    newFinalStates.add(newState)
                newTransitions[state, symbol] = newState
                
                if newState not in statesToDeterminize:
                    statesToDeterminize.append(newState)

        self.states = newStates
        self.final_states = newFinalStates
        self.transitions = newTransitions

        

    def save(self, path):
        data = {}
        data['object'] = 'automata'
        data['symbols'] = sorted(self.symbols)
        data['states'] = sorted(self.states)
        data['initial_state'] = self.initial_state
        data['final_states'] = sorted(self.final_states)
        data['transitions'] = [(k[0], k[1], sorted(v)) for k, v in self.transitions.items()]

        with open(path, 'w') as automata_file:
            json.dump(data, automata_file, indent=4)

    def load(self, path):
        with open(path, 'r') as automata_file:
            data = json.load(automata_file)

        if data.get('object') == 'automata':
            self.symbols = set(data.get('symbols'))
            self.states = set(data.get('states'))
            self.initial_state = data.get('initial_state')
            self.final_states = set(data.get('final_states'))
            self.transitions = {(k[0], k[1]):k[2] for k in data.get('transitions')}

        else:
            raise ValueError('Not a valid file!')

    def __str__(self):
        symbols = 'symbol: ' + str(self.symbols) + '\n'
        states = 'states: ' + str(self.states) + '\n'
        initial = 'initial: ' + str(self.initial_state) + '\n'
        final = 'final: ' + str(self.final_states) + '\n'
        transitions = 'transitions: ' + str(self.transitions) + '\n'
        return symbols + states + initial + final + transitions
