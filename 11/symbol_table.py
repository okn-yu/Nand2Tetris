import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class SymbolTable:

    def __init__(self, filePath):

        print('SymbolTable...%s' % filePath)
        self._xmlFilePath = filePath

        self._read_txmlFile()
        self._find_variables()

        # self.classSTable = {}
        # self.subroutineSTable = {}

    def _read_txmlFile(self):
        # print(self._xmlFilePath)
        tree = ET.parse(self._xmlFilePath)
        self._root = tree.getroot()

    def _find_variables(self):
        for e in self._root.iter('identifier'):
            if e.attrib:
                print(e.tag, e.text)

        # print(self._root.findall('identifier'))

    def define(self, name, type, kind):
        pass

        # symbolTable[name] = (type, kind, index)
        # ex. var int length;  -> symbolTable{'a': ('int', 'var', 0)}

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

