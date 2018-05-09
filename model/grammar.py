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
