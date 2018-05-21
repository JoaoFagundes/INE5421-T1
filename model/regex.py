import json

class RegexParser():
    """
        Regex Parser at the link below
        http://matt.might.net/articles/parsing-regex-with-recursive-descent/

        GLC describing the regex structure:

        <regex>  ::= <term>'|'<regex>
                    | <term>

        A regular expression is a term 
        or a regular expression is a term, a '|' and another regular expression.

        <term>   ::= { <factor> }

        A term is a possibly empty sequence of factors.

        <factor> ::= <base> { '*' }

        A factor is a base followed by a possibly empty sequence of '*'.
             
        <base>   ::= <char>
                    | '\' <char>
                    | '(' <regex> ')'
        A base is a character, 
        or an escaped character, 
        or a parenthesized regular expression.        
    """

    def __init__(self, regex_string):
        self.regex_string = regex_string

    def parse(self):
        pass

    def peek(self):
        if self.more():
            return self.regex_string[0]
        else:
            return ''

    def eat(self, char):
        if self.peek() == char:
            self.regex_string = self.regex_string[1::]
        else:
            raise ValueError('Expected: '+str(char)+ 
                             'got: '+str(self.peek()))

    def next_char(self):
        char = self.peek()
        self.eat(char)
        return char

    def more(self):
        if len(self.regex_string) == 0:
            return False

        return True

    def regex(self):
        pass

    def term(self):
        pass

    def factor(self):
        pass

    def base(self):
        pass

class Regex():

    def __init__(self, regex_string=None):
        self.string = regex_string

    def convert_to_automata(self):
        pass

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
