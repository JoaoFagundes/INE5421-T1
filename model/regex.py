import json

class Regex():

    def __init__(self, regex_string=None):
        self.string = regex_string

    def save(self, path):
        data = {}
        data['object'] = 'regex'
        data['regex_string'] = self.string

        with open(path, 'w') as regex_file:
            json.dump(data, regex_file, indent=4)

    def load(self, path):
        with open(path, 'r') as regex_file:
            data = json.load(regex_file)

        if data.get('object') == 'regex':
            self.string = data.get('regex_string')
        else:
            raise ValueError('Not a valid file!')

