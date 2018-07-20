class SymbolTable:

    def __init__(self):
        pass

        self.classSTable = {}
        self.subroutineSTable = {}

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

