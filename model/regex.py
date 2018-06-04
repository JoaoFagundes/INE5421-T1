# Joao Victor Fagundes
# Salomao Rodrigues Jacinto
# INE5421 - Trabalho Prático I Junho 2018

import json
import re

TERMINAL_SYMBOLS = '[a-z0-9]'
OPERATORS = {'|', '?', '*', '.'}

class Node():

    def __init__(self, symbol, left_str, right_str):
        self.symbol = symbol
        self.left = left_str
        self.right = right_str

    def up(self, visited=None):
        if visited is None:
            visited = set()

        if self.symbol == '.':
            return self.right.down(visited)
        elif self.symbol == '*':
            return self.left.down(visited) | self.right.up(visited)
        elif self.symbol == '?':
            return self.right.up(visited)
        elif self.symbol == '|':
            node = self.right
            while node.symbol == '.' or node.symbol == '|':
                node = node.right
            return node.right.up(visited)
        return {self}

    def down(self, visited=None):
        if visited is None:
            visited = set()

        if self in visited:
            return {self} if self.symbol not in OPERATORS else set()

        visited |= {self}
        if self.symbol == '|':
            return self.left.down(visited) | self.right.down(visited)
        elif self.symbol == '?':
            return self.left.down(visited) | self.right.up(visited)
        elif self.symbol == '*':
            return self.left.down(visited) | self.right.up(visited)
        elif self.symbol == '.':
            return self.left.down(visited)

        return {self}

    def thread(self):
        inorder = list()
        node = self
        while inorder or node:
            if node:
                inorder.append(node)
                node = node.left
            else:
                node = inorder.pop()
                if node.right is None:
                    node.right = inorder[-1] if inorder else Node('$', None, None)
                    node = None
                else:
                    node = node.right

    def print_tree_by_level(self):
        level = [self]
        level_symbols = [i.symbol for i in level]
        print('Level: '+str(level_symbols))
        while len(level) > 0:
            new_level = list()
            for i in level:
                if i is None:
                    new_level.append(None)
                    new_level.append(None)
                else:
                    new_level.append(i.left)
                    new_level.append(i.right)

            level = new_level.copy()
            level_symbols.clear()
            count = 0
            for i in level:
                if i is None:
                    count += 1
                    level_symbols.append('$')
                else:
                    level_symbols.append(i.symbol)

            if len(level) == count:
                return

            print('Level: '+str(level_symbols))

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

        <factor> ::= <base> ({ '*' } | { '?' })

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
            <factor> ::= <base> ({ '*' } | { '?' })
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
        from .automata import Automata
        automata = Automata()
        tree = RegexParser(self.string).parse()
        tree.thread() 

        i_states = 0
        next_states = set()

        automata.initial_state = 'q'+str(i_states)
        automata.states.add(automata.initial_state)

        composition = frozenset(tree.down())  
        state_composition = dict()

        next_states.add(automata.initial_state)
        state_composition[automata.initial_state] = composition

        while next_states:
            current_state = next_states.pop()
            composition_symbol_nodes = dict()
            for c in state_composition[current_state]:
                if c.symbol not in composition_symbol_nodes.keys():
                    composition_symbol_nodes[c.symbol] = {c}
                else:
                    nodes = composition_symbol_nodes[c.symbol]
                    nodes.add(c)
                    composition_symbol_nodes[c.symbol] = nodes

            for k_symbol in composition_symbol_nodes.keys():
                if k_symbol == '$':
                    automata.final_states.add(current_state)
                else:
                    automata.symbols.add(k_symbol)
                    new_composition = set()
                    for c in composition_symbol_nodes[k_symbol]:
                        new_composition |= c.right.up()

                    frozen_composition = frozenset(new_composition)
                    already_in = False
                    for k_state, v in state_composition.items():                     
                        if v == frozen_composition:
                            automata.transitions[(current_state, k_symbol)] = {k_state}
                            already_in = True

                    if not already_in:
                        i_states += 1
                        new_state = 'q'+str(i_states)
                        automata.states.add(new_state)
                        next_states.add(new_state)
                        automata.transitions[(current_state, k_symbol)] = {new_state}
                        state_composition[new_state] = frozen_composition

        for s in automata.symbols:
            for state in automata.states:
                try:
                    test = automata.transitions[state, s]
                except KeyError:
                    automata.transitions[state, s] = set()

        return automata
        

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
