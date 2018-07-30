import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class SymbolTable:

    def __init__(self, filePath):

        print('SymbolTable...%s' % filePath)

        self.classTable = {}                                        # classTable['name'] = ('kind', 'type', index)
        self.classIndex = 0
        self.subroutineTable = {}                                   # classTable['name'] = ('kind', 'type', index)
        self.subroutineIndex = 0
        self.symbolTable = [self.classTable, self.subroutineTable]  # symbolTable = [classTable, symbolTable]

        self._xmlFilePath = filePath
        self._read_txmlFile()
        self.define()


    def _read_txmlFile(self):
        # print(self._xmlFilePath)
        tree = ET.parse(self._xmlFilePath)
        self._root = tree.getroot()

    def define(self):
        for e in self._root.iter('identifier'):
            if e.attrib:
                name = e.text
                kind = e.attrib['kind']
                type = e.attrib['type']

                if kind == 'var':
                    self.subroutineTable[name] = (kind, type, self.subroutineIndex)
                    self.subroutineIndex += 1

                if kind == 'field':
                    self.classTable[name] = (kind, type, self.classIndex)
                    self.classIndex += 1

        print(self.symbolTable)

    def var_count(self, kind):
        pass
        # return Integer

    def kind_of(self, name):
        pass
        # return static, field, arg, var, none

    def type_of(self, name):
        pass
        # return int, char, boolean, className

    def index_of(self, name):
        pass
        # return Integer

