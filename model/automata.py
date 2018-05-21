import json
import string
import re

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
        current_states = {self.initial_state}
        temporary_states = set()
        for symbol in sentence:
            for state in current_states:
                [temporary_states.add(k) for k in self.transitions[state, symbol]]
            current_states.clear()
            [current_states.add(v) for v in temporary_states]
            temporary_states.clear()

        return ((current_states & self.final_states) != set())

    def enumerate(self, n):
        if n < 0:
            raise ValueError('Must be a natural number')

        if n == 0 and self.initial_state in self.final_states:
            return '&'

        keys = {k for k, v in self.transitions.items() if v & self.final_states != set()}
        maybe_accepted_strings = {(key[0], key[1]) for key in keys}
        for i in range(n-1):
            old_strings = maybe_accepted_strings.copy()
            maybe_accepted_strings = set()
            for string in old_strings:
                new_states = {k for k, v in self.transitions.items() if string[0] in v}
                for new_state in new_states:
                    maybe_accepted_strings.add((new_state[0], new_state[1]+string[1]))

        accepted_strings = {s[1] for s in maybe_accepted_strings if s[0] == self.initial_state}
        return accepted_strings

    def determinize(self):
        statesToDeterminize = list()

        newTransitions = dict()
        newStates = set()
        newFinalStates = set()
        newInitialState = '{' + self.initial_state + '}'
        newStates.add(newInitialState)
        if self.initial_state in self.final_states:
            newFinalStates.add(newInitialState)
        
        statesToDeterminize.append(newInitialState)
        self.initial_state = newInitialState

        for state in statesToDeterminize:
            isFinalState = False
            state = state[:-1]
            state = state.replace('{', '')
            state = state.replace(' ', '')
            for symbol in self.symbols:
                newState = '{'
                determinization = set()

                for st in state.split(','):
                    try:
                        for t in self.transitions[st, symbol]:
                            determinization.add(t)
                    except KeyError:
                        continue

                for d in determinization:
                    if d in self.final_states:
                        isFinalState = True

                    newState += d + ','

                if newState != '{':
                    newState = newState[:-1] + '}'
                    newStates.add(newState)
                    if isFinalState:
                        newFinalStates.add(newState)
                    newTransitions['{' + state + '}', symbol] = {newState}

                    if newState not in statesToDeterminize:
                        statesToDeterminize.append(newState)

        for s in self.symbols:
            for state in newStates:
                try:
                    test = newTransitions[state, s]
                except KeyError:
                    newTransitions[state, s] = set()

        self.states = newStates
        self.final_states = newFinalStates
        self.transitions = newTransitions

    def minimize(self):
        pass

    def union(self, other):
        pass

    def reverse(self):
        pass
    
    def closure(self):
        pass

    def concatenation(self, other):
        pass

    def complement(self):
        self.determinize()
        self.rename_states()
        self.complete()
        self.final_states = self.states - self.final_states

    def complete(self):
        #funnction to put the error state
        for k, v in self.transitions.items():
            if v == set():
                self.states.add('qErro')
                self.transitions[k] = {'qErro'}

        if 'qErro' in self.states:
            for s in self.symbols:
                self.transitions['qErro', s] = {'qErro'}

    def intersection(self, other):
        pass

    def difference(self, other):
        pass

    def convert_to_grammar(self):
        from .grammar import Grammar
        grammar = Grammar()
        map_state_letter = dict()
        suffix = ''
        for i, state in enumerate(self.states):
            if i != 0 and i % 26 == 0:
                suffix += '\''
            map_state_letter[state] = string.ascii_uppercase[i]+suffix

        initial_productions = set()
        for s in self.symbols:
            aux_states = self.transitions[self.initial_state, s]
            if aux_states != set():
                for aux_state in aux_states:
                    if aux_state in self.final_states:
                        initial_productions.add(s)
                    initial_productions.add(s+map_state_letter[aux_state])

        if self.initial_state in self.final_states:
            new_initial_productions = initial_productions.copy()
            new_initial_productions.add('&')
            grammar.add(map_state_letter[self.initial_state]+'\'', new_initial_productions)
        grammar.add(map_state_letter[self.initial_state], initial_productions)

        for state in self.states - {self.initial_state}:
            productions = set()
            for s in self.symbols:
                aux_states = self.transitions[state, s]
            if aux_states != set():
                for aux_state in aux_states:
                    if aux_state in self.final_states:
                        productions.add(s)
                    productions.add(s+map_state_letter[aux_state])
            grammar.add(map_state_letter[state], productions)

        for k, v in grammar.productions.items():
            if v == set():
                for i, j in grammar.productions.items():
                    discard = [discard_s for discard_s in j if re.search(k, discard_s)]
                    for s in discard:
                        j.discard(s)
        
        return grammar

    def rename_states(self):
        i = int(1)
        statesMap = dict()
        newStates = set()
        newFinalStates = set()
        newTransitions = dict()
        newInitialState = 'q0'
        statesMap[self.initial_state] = newInitialState
        if self.initial_state in self.final_states:
            newFinalStates.add(newInitialState)
        self.initial_state = newInitialState
        newStates.add(newInitialState)

        for state in self.states:
            state = state.replace('{', '')
            state = state.replace('}', '')
            if state != 'q0':
                newState = 'q' + str(i)
                statesMap['{' + state + '}'] = newState
                newStates.add(newState)
                i += 1

        for state in self.states:
            if state in self.final_states:
                newFinalStates.add(statesMap[state])
            for symbol in self.symbols:
                try:
                    for t in self.transitions[state, symbol]:
                        newTransitions[statesMap[state], symbol] = {statesMap[t]}
                except KeyError:
                    continue

        for s in self.symbols:
            for state in newStates:
                try:
                    test = newTransitions[state, s]
                except KeyError:
                    newTransitions[state, s] = set()

        self.transitions = newTransitions
        self.states = newStates
        self.final_states = newFinalStates

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
            self.transitions = {(k[0], k[1]):set(k[2]) for k in data.get('transitions')}

        else:
            raise ValueError('Not a valid file!')

    def copy(self):
        new_automata = Automata()
        new_automata.symbols = self.symbols.copy()
        new_automata.states = self.states.copy()
        new_automata.final_states = self.final_states.copy()
        new_automata.transitions = self.transitions.copy()
        new_automata.initial_state = self.initial_state
        return new_automata

    def __str__(self):
        symbols = 'symbol: ' + str(self.symbols) + '\n'
        states = 'states: ' + str(self.states) + '\n'
        initial = 'initial: ' + str(self.initial_state) + '\n'
        final = 'final: ' + str(self.final_states) + '\n'
        transitions = 'transitions: ' + str(self.transitions) + '\n'
        return symbols + states + initial + final + transitions
