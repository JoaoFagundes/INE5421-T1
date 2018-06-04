# Joao Victor Fagundes
# Salomao Rodrigues Jacinto
# INE5421 - Trabalho Prático I Junho 2018

import json
from collections import OrderedDict

class Grammar():

    def __init__(self):
        self.productions = OrderedDict()

    def initial_symbol(self):
        for k in self.productions.keys():
            return k

    def add(self, key, set_values):
        self.productions[key] = set_values

    def remove(self, key):
        self.productions.pop(key)
    
    def edit_key(self, old_key, new_key, set_values):
        self.productions = OrderedDict([(new_key, v) 
                        if k == old_key else (k,v) for k, v in self.productions.items()])
        self.add(new_key, set_values)

    def convert_to_automata(self):
        from .automata import Automata
        automata = Automata()
        map_letter_state = dict()
        i = int(0)
        map_letter_state[self.initial_symbol()] = 'q'+str(i)
        automata.initial_state = 'q'+str(i)
        for k in self.productions.keys()-{self.initial_symbol()}:
            i += 1
            map_letter_state[k] = 'q'+str(i)
            automata.states.add('q'+str(i))

        final_state = 'q'+str(i+1)
        automata.add_final_state(final_state)
        automata.states.add(final_state)

        initial_productions = self.productions[self.initial_symbol()]
        if '&' in initial_productions:
            automata.add_final_state(map_letter_state[self.initial_symbol()])

        for k, values in self.productions.items():
            end_states = dict()
            for v in values:
                try:
                    lower_symbol = v[0]
                    upper_symbol = v[1]
                    if lower_symbol not in end_states.keys():
                        end_states[lower_symbol] = {map_letter_state[upper_symbol]}
                    else:
                        aux = end_states[lower_symbol]
                        aux.add(map_letter_state[upper_symbol])
                        end_states[lower_symbol] = aux

                except IndexError:
                    lower_symbol = v[0]
                    if lower_symbol not in end_states.keys():
                        end_states[lower_symbol] = {final_state}
                    else:
                        aux = end_states[lower_symbol]
                        aux.add(final_state)
                        end_states[lower_symbol] = aux

            for i, j in end_states.items():
                automata.add_symbol(i)
                automata.add_transition(map_letter_state[k], i, j)

        for s in automata.symbols:
            automata.transitions[final_state, s] = set()

        return automata

    def save(self, path):
        data = {}
        data['object'] = 'grammar'
        data_dict = OrderedDict()
        for k, v in self.productions.items():
            data_dict[k] = sorted(v)
        data['productions'] = data_dict

        with open(path, 'w') as grammar_file:
            json.dump(data, grammar_file, indent=4)

    def load(self, path):
        with open(path, 'r') as grammar_file:
            data = json.load(grammar_file, object_pairs_hook=OrderedDict)

        if data.get('object') == 'grammar':
            for k, v in data.get('productions').items():
                self.productions[k] = set(v)

        else:
            raise ValueError('Not a valid file!')
