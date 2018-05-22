import json
import re
from collections import deque

TERMINAL_SYMBOLS = '[a-z0-9]'

class Node():

    def __init__(self, symbol, left_str, right_str):
        self.symbol = symbol
        self.left = left_str
        self.right = right_str

    def print_tree_by_level(self, root):
        buf = deque()
        output = []
        if not root:
            print('$')
        else:
            buf.append(root)
            count, nextCount = 1, 0
            while count:
                node = buf.popleft()
                if node:
                    output.append(node.symbol)
                    count -= 1
                    for n in (node.left, node.right):
                        if n:
                            buf.append(n)
                            nextCount += 1
                        else:
                            buf.append(None)
                else:
                    output.append('$')
                if not count:
                    print(output)
                    output = []
                    count, nextCount = nextCount, 0
            # print the remaining all empty leaf node part
            output.extend(['$']*len(buf))
            print(output)

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
                    | '(' <regex> ')'
        A base is a character, 
        or a parenthesized regular expression.        
    """

    def __init__(self, regex_string):
        self.regex_string = regex_string

    def parse(self):
        print(self.regex_string)
        tree = self.regex()
        if len(self.regex_string) != 0:
            raise ValueError('Not a valid regex!')

        return tree

    def peek(self):
        if self.more():
            return self.regex_string[0]
        
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
        """
            <regex>  ::= <term>'|'<regex>
                        | <term>
        """
        term = self.term()
        if self.more() and self.peek() == '|':
            self.eat('|')
            regex = self.regex()
            return Node('|', term, regex)
        
        return term

    def term(self):
        """
            <term>   ::= { <factor> }
            ou
            <term>   ::= <factor> <term> | <factor>
        """
        factor = self.factor()
        if self.more() and self.peek() != ')' and self.peek() != '|':
            term = self.term()
            factor = Node('.', factor, term)

        return factor 

    def factor(self):
        """
            <factor> ::= <base> { '*' }
        """
        base = self.base()
        while self.more() and (self.peek() == '*' or self.peek() == '?'):
            base = Node(self.next_char(), base, None)

        return base

    def base(self):
        """
            <base>   ::= <char>
                        | '(' <regex> ')'
        """
        char = self.peek()
        if char == '(':
            self.eat('(')
            regex = self.regex()
            self.eat(')')
            return regex
        elif re.fullmatch(TERMINAL_SYMBOLS, char) is not None:
            return Node(self.next_char(), None, None)
        else:
            raise ValueError('Not a valid regex!')

class Regex():

    def __init__(self, regex_string=None):
        self.string = regex_string

    def convert_to_automata(self):
        tree = RegexParser(self.string).parse()
        tree.print_tree_by_level(tree)

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
