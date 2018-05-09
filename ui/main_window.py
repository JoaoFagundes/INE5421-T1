import re
from model.grammar import Grammar
from model.regex import Regex
from model.automata import Automata
from ui.main_window_ui import Ui_MainWindow
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QInputDialog, QFileDialog)

SYMBOL_INPUT='(([a-z0-9],)?)*[a-z0-9]'
STATE_INPUT='(([q][0-9]*,)?)*q[0-9]*'
INITIAL_GRAMMAR='[A-Z][\']*->[a-z0-9&]([A-Z][\']*)?(\|[a-z0-9&]([A-Z][\']*)?)*'
GRAMMAR_INPUT='[A-Z][\']*->[a-z0-9]([A-Z][\']*)?(\|[a-z0-9]([A-Z][\']*)?)*'

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Information)

        self._regex = Regex()
        self._automata = Automata()
        self._grammar = Grammar()
        self._item_data = ''

        #Regex
        self.importRegexButton.clicked.connect(self.import_regex)
        self.exportRegexButton.clicked.connect(self.export_regex)
        self.convertRegexButton.clicked.connect(self.convert_regex)

        #Automata
        self.importAutomataButton.clicked.connect(self.import_automata)
        self.exportAutomataButton.clicked.connect(self.export_automata)
        self.convertAutomataButton.clicked.connect(self.convert_automata)
        self.addStateButton.clicked.connect(self.add_state)
        self.removeStateButton.clicked.connect(self.remove_state)
        self.addSymbolButton.clicked.connect(self.add_symbol)
        self.removeSymbolButton.clicked.connect(self.remove_symbol)
        self.toggleFinalStateButton.clicked.connect(self.toggle_final_state)
        self.enumerateButton.clicked.connect(self.enumerate)
        self.checkStringButton.clicked.connect(self.check_string)
        self.transitionTable.cellChanged.connect(self.update_automata)

        #Grammar
        self.importGrammarButton.clicked.connect(self.import_grammar)
        self.exportGrammarButton.clicked.connect(self.export_grammar)
        self.convertGrammarButton.clicked.connect(self.convert_grammar)
        self.addProdButton.clicked.connect(self.add_production)
        self.removeProdButton.clicked.connect(self.remove_production)
        self.productionList.itemClicked.connect(self.grammar_item_clicked)
        self.productionList.itemChanged.connect(self.update_grammar)

        #Operations
        self.actionIntersection.triggered.connect(self.intersection_action)
        self.actionDifference.triggered.connect(self.difference_action)
        self.actionReverse.triggered.connect(self.reverse_action)
        self.actionDeterminize.triggered.connect(self.determinize_action)
        self.actionMinimize.triggered.connect(self.minimize_action)
        self.actionUnion.triggered.connect(self.union_action)
        self.actionConcatenation.triggered.connect(self.concatenation_action)
        self.actionClosure.triggered.connect(self.closure_action)

    def import_regex(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            try:
                self._regex.load(path)
                self.regexInput.setText(self._regex.string)
            except ValueError as error:
                QMessageBox.critical(self, 'Error', error.args[0])

    def export_regex(self):
        regex_string = self.regexInput.text()
        self._regex = Regex(regex_string)
        path, _ = QFileDialog.getSaveFileName(self)
        if path:
            self._regex.save(path)

    def convert_regex(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def import_automata(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def export_automata(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def convert_automata(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def add_state(self):
        text, ok = QInputDialog.getText(
            self, 'Add State', 'You can input a single state qN or a list of '+
                               'states. e.g(q0, q1, ...)')
        if ok:
            text = text.strip().replace(" ", "")
            while re.fullmatch(STATE_INPUT, text) is None:
                text, ok = QInputDialog.getText(self, 'Add State', 
                    'The state has to be a \'q\' followed by a number')
                if ok:
                    text = text.strip().replace(" ", "")

            self.message.setText('Your input was: '+text)
            self.message.show()

    def remove_state(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def add_symbol(self):
        text, ok = QInputDialog.getText(
            self, 'Add Symbol', 'You can input a single symbol or a list of '+
                                'symbols. e.g(a, b, c, ...)')
        
        if ok:
            text = text.strip().replace(" ", "")
            while re.fullmatch(SYMBOL_INPUT, text) is None:
                text, ok = QInputDialog.getText(self, 'Add Symbol', 
                    'Only lower case letters and numbers are accepted as symbols!')
                if ok:
                    text = text.strip().replace(" ", "")

            self.message.setText(text)
            self.message.show()
                

    def remove_symbol(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def toggle_final_state(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def enumerate(self):
        n, ok = QInputDialog.getInt(
            self, 'Enumerate', 'Which size of sentence')
        if ok:
            self.message.setText('Enumerate sentences with size: '+str(n))
            self.message.show()

    def check_string(self):
        accepted = False

        if accepted:
            self.message.setText('The string is accepted by the automaton!')
            self.message.show()
        else:
            self.message.setText('The string is NOT accepted by the automaton!')
            self.message.show()

    def update_automata(self):
        pass

    def import_grammar(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            try:
                self._grammar.load(path)
                for k, v in self._grammar.productions.items():
                    text = k + '->'
                    for p in v:
                        text += p + '|'
                    self.productionList.addItem(text[:-1])

            except ValueError as error:
                QMessageBox.critical(self, 'Error', error.args[0])

    def export_grammar(self):
        path, _ = QFileDialog.getSaveFileName(self)
        if path:
            self._grammar.save(path)

    def convert_grammar(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def add_production(self):
        keys = self._grammar.productions.keys()
        if self.productionList.count() == 0:
            text, ok = QInputDialog.getText(
                self, 'Add Initial Production', 'Input a production '+
                      'e.g(A -> aA | bB)')
        
            if ok:
                text = text.strip().replace(" ", "")
                while re.fullmatch(INITIAL_GRAMMAR, text) is None:
                    text, ok = QInputDialog.getText(self, 'Add Initial Production', 
                        'Production not regular!')
                    if ok:
                        text = text.strip().replace(" ", "")

                self.productionList.addItem(text)
                key, set_values = text.split('->')    
                self._grammar.add(key, set(set_values.split('|')))

        else:
            text, ok = QInputDialog.getText(
                self, 'Add Production', 'Input a production '+
                      'e.g(A -> aA | bB)')
        
            if ok:
                text = text.strip().replace(" ", "")
                while re.fullmatch(GRAMMAR_INPUT, text) is None:
                    text, ok = QInputDialog.getText(self, 'Add Production', 
                        'Production not regular!')
                    if ok:
                        text = text.strip().replace(" ", "")

                key, set_values = text.split('->')
                if key not in keys:
                    self.productionList.addItem(text)
                    self._grammar.add(key, set(set_values.split('|')))
                else:
                    self.message.setText('This non terminal symbol already exists!')
                    self.message.show()

    def remove_production(self):
        for item in self.productionList.selectedItems():
            key = item.text().split('->')[0]
            self._grammar.remove(key)
            self.productionList.takeItem(self.productionList.row(item))

    def grammar_item_clicked(self, item):
        self.productionList.itemChanged.disconnect(self.update_grammar)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self._item_data=item.text()
        self.productionList.itemChanged.connect(self.update_grammar)

    def update_grammar(self, item):
        self.productionList.itemChanged.disconnect(self.update_grammar)
        keys = self._grammar.productions.keys()
        print(self.productionList.indexFromItem(item).row())
        if self.productionList.indexFromItem(item).row() == 0:
            if re.fullmatch(INITIAL_GRAMMAR, item.text()) is None:
                item.setText(self._item_data)
                self.message.setText('Production not Regular!')
                self.message.show()
            else:
                key, set_values = item.text().split('->')
                old_key = self._item_data.split('->')[0]
                if key not in keys or key == old_key :
                    self._grammar.edit_key(old_key, key, set(set_values.split('|')))
                else:
                    item.setText(self._item_data)
                    self.message.setText('This non terminal symbol already exists!')
                    self.message.show()

        else:
            if re.fullmatch(GRAMMAR_INPUT, item.text()) is None:
                item.setText(self._item_data)
                self.message.setText('Production not Regular!')
                self.message.show()
            else:
                key, set_values = item.text().split('->')
                old_key = self._item_data.split('->')[0]
                if key not in keys or key == old_key :
                    self._grammar.edit_key(old_key, key, set(set_values.split('|')))
                else:
                    item.setText(self._item_data)
                    self.message.setText('This non terminal symbol already exists!')
                    self.message.show()
                
        self.productionList.itemChanged.connect(self.update_grammar)

    def intersection_action(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def difference_action(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def reverse_action(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def determinize_action(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def minimize_action(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def union_action(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def concatenation_action(self):
        self.message.setText('Not implemented yet!')
        self.message.show()

    def closure_action(self):
        self.message.setText('Not implemented yet!')
        self.message.show()
