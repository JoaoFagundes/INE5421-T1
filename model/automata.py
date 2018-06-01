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

    def enumerate_strings(self, n):
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

    def empty_language_automata(self):
        self.initial_state = 'q0'
        self.states = {self.initial_state}
        self.final_states = set()
        self.transitions = dict()
        for s in self.symbols:
            self.transitions[self.initial_state, s] = {self.initial_state}
        

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
            state = state[:-1]
            state = state.replace('{', '')
            state = state.replace(' ', '')
            for symbol in self.symbols:
                isFinalState = False
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

    def union(self, other):
        self.symbols.update(other.symbols)
        self.complete()
        self.rename_states()

        other.symbols.update(self.symbols)
        other.complete()
        other.rename_states(len(self.states))

        newInitialState = 'qInitial'
        self.states.add(newInitialState)

        self.states.update(other.states)
        self.final_states.update(other.final_states)
        self.transitions.update(other.transitions)

        if (self.initial_state in self.final_states or
                other.initial_state in self.final_states):
           self.final_states.add(newInitialState)

        for s in self.symbols:
            automata1_transitions = self.transitions[self.initial_state, s]
            automata2_transitions = other.transitions[other.initial_state, s]
            self.transitions[newInitialState, s] = (automata1_transitions|
                                                    automata2_transitions)

        self.initial_state = newInitialState
        self.determinize()
        self.rename_states()

    def concatenation(self, other):
        
        other.rename_states(len(self.states))
        self.states.update(other.states)
        self.symbols.update(other.symbols)

        transitions_to_concat = {k for k,v in self.transitions.items() if v & self.final_states != set()}
        #Maybe this is necessary, maybe not.
        '''if other.initial_state in other.final_states:
            self.final_states.update(other.final_states)
        else:'''
        
        self.final_states = other.final_states
        self.transitions.update(other.transitions)

        for t in transitions_to_concat:
            self.transitions[t] = {other.initial_state}

    
    def reverse(self):
        pass
    
    def closure(self):
        pass

    def complement(self):
        self.determinize()
        self.rename_states()
        self.complete()
        self.final_states = self.states - self.final_states

    def complete(self):
        #funnction to put the error state
        for s in self.symbols:
            for state in self.states:
                try:
                    test = self.transitions[state, s]
                except KeyError:
                    self.transitions[state, s] = set()

        for k, v in self.transitions.items():
            if v == set():
                self.states.add('qErro')
                self.transitions[k] = {'qErro'}

        if 'qErro' in self.states:
            for s in self.symbols:
                self.transitions['qErro', s] = {'qErro'}

    def intersection(self, other):
        other.complement()
        complement1 = other.copy()
        self.complement()
        complement2 = self.copy()
        self.union(complement1.copy())
        union = self.copy()
        self.complement()
        return(complement1, complement2, union)

    def difference(self, other):
        other.complement()
        complement1 = other.copy()
        self.intersection(complement1.copy())
        return complement1

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

    def rename_states(self, i=None):
        if i == None:
            i = int(0)
        statesMap = dict()
        newStates = set()
        newFinalStates = set()
        newTransitions = dict()
        newInitialState = 'q'+str(i)
        statesMap[self.initial_state] = newInitialState
        newStates.add(newInitialState)

        for state in self.states:
            if state != self.initial_state and state != '{'+self.initial_state+'}':
                i += 1
                newState = 'q' + str(i)
                statesMap[state] = newState
                newStates.add(newState)

        for state in self.states:
            if state in self.final_states:
                newFinalStates.add(statesMap[state])
            for symbol in self.symbols:
                try:
                    newTransitions[statesMap[state], symbol] = {statesMap[t] 
                                            for t in self.transitions[state, symbol]}
                except KeyError:
                    continue

        for s in self.symbols:
            for state in newStates:
                try:
                    test = newTransitions[state, s]
                except KeyError:
                    newTransitions[state, s] = set()

        self.initial_state = newInitialState
        self.transitions = newTransitions
        self.states = newStates
        self.final_states = newFinalStates

    def minimize(self):
        if self.determinization_is_needed():
            self.determinize()
            self.rename_states()
        
        self.discard_unreachable_states()
        self.discard_dead_states()
        if self.initial_state not in self.states:
            self.empty_language_automata()
        else:
            self.complete()
            self.discard_equivalent_states()

        self.remove_error_state()

    def discard_unreachable_states(self):
        reachable_states = list()
        reachable_states.append(self.initial_state)

        for state in reachable_states:
            for symbol in self.symbols:
                try:
                    for st in self.transitions[state, symbol]:
                        if st not in reachable_states:
                            reachable_states.append(st)
                except KeyError:
                    continue

        unreachable_states = {state for state in self.states.copy() if state not in reachable_states}
        self.states = self.states - unreachable_states
    
    def discard_dead_states(self):
        living_states = self.final_states.copy()
        new_living_states = set()

        while (True):
            aux = new_living_states.copy()
            new_living_states = {k[0] for k, v in self.transitions.items() if v & living_states != set()}
            for state in new_living_states:
                living_states.add(state)
        
            if aux == new_living_states:
                break


        for k, v in self.transitions.copy().items():
            if v & living_states == set():
                self.states = self.states - v
                self.transitions.pop(k)

    def discard_equivalent_states(self):
        equivalence_classes = dict()
        i = int(2)
        equivalence_classes['q0'] = self.states - self.final_states
        equivalence_classes['q1'] = self.final_states
        copy = dict()
        
        while True:
            copy = equivalence_classes.copy()
            for k, v in copy.items():
                extras = self.combine_states(k, v, equivalence_classes, copy)
                
                while (len(extras) > 1):
                    state = 'q' + str(i)
                    equivalence_classes[state] = extras
                    i += int(1)
                    extras = self.combine_states(state, extras, equivalence_classes, copy)
                else:
                    if len(extras) == 1:
                        state = 'q' + str(i)
                        equivalence_classes[state] = extras
                        i += int(1)
            
            if (copy == equivalence_classes):
                break

        qErro = {k for k, v in equivalence_classes.copy().items() if v == {'qErro'}}
        
        for k in qErro:
            equivalence_classes['qErro'] = equivalence_classes.pop(k)


        self.create_minimum_automata(equivalence_classes)
    
    def combine_states(self, key, _class, equivalence_classes, copy):
        extras = set()
        q = _class.pop()
        subclass = _class.copy()
        _class.add(q)
        for p in subclass:
            for symbol in self.symbols:
                r1 = self.transitions[q, symbol].copy().pop()
                r2 = self.transitions[p, symbol].copy().pop()
                if not self.in_same_classes(r1, r2, copy):
                    equivalence_classes[key].discard(p)
                    extras.add(p)
        return extras

    def in_same_classes(self, q1, q2, equivalence_classes):
        for eq_class in equivalence_classes.values():
            if (({q1, q2} & eq_class) == {q1, q2}):
                return True
        
        return False

    def create_minimum_automata(self, equivalence_classes):
        new_transitions = dict()
        new_states = set()
        new_final_states = set()

        for k, v in self.transitions.items():
            state_origin = None
            state_destination = None
            for new_state, equivalent_states in equivalence_classes.items():
                if k[0] in equivalent_states:
                    state_origin = new_state
                
                if v & equivalent_states != set():
                    state_destination = new_state
            new_transitions[state_origin, k[1]] = {state_destination}

        for new_state, equivalent_states in equivalence_classes.items():
            new_states.add(new_state)
            if self.initial_state in equivalent_states:
                self.initial_state = new_state
                
            for state in equivalent_states:
                if state in self.final_states:
                    new_final_states.add(new_state)

        self.states = new_states
        self.final_states = new_final_states
        self.transitions = new_transitions
    
    def determinization_is_needed(self):
        for origin, destination in self.transitions.items():
            if len(destination) > 1:
                return True

        return False

    def remove_error_state(self):
        error_state = 'qErro'
        '''Only removes an error state if it's not a final state
           
           This guarantees that an automata that had an error state,
           when complemented this error state becomes a valid state
           and therefore should not be removed.
        '''
        if error_state not in self.final_states:
            if error_state in self.states:
                self.states.discard(error_state)

            for k,v in self.transitions.copy().items():
                if (k[0] == error_state) or (error_state in v):
                    self.transitions.pop(k)
    
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
            self.initial_state = str(data.get('initial_state'))
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
