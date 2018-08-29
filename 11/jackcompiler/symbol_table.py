class SymbolTable:

    def __init__(self):

        self.classTable = {}                                        # classTable['name'] = ('kind', 'type', index)
        self.classIndex = 0
        self.subroutineTable = {}                                   # classTable['name'] = ('kind', 'type', index)
        self.subroutineIndex = 0
        self.symbolTable = []

    def define(self, kind, type, var):

        pass

        # if scopeName in self.symbolTable:
        #     scopeName = {}
        #     scopeName[name] = (kind, type)
        #     self.symbolTable.append(scopeName)
        # else:
        # for e in self._root.iter('identifier'):
        #     if e.attrib:
        #         name = e.text.strip()
        #         scope = e.attrib['scope']
        #         kind = e.attrib['kind']
        #         type = e.attrib['type']
        #
        #         num = 0
        #
        #         for table in self.symbolTable:
        #             if table[0] == scope:
        #                 num += 1
        #
        #         self.symbolTable.append((scope, name, kind, type, num))
        #
        # print('symbolTable: %s' %  self.symbolTable)

    def var_count(self, kind):
        pass
        # return Integer

    def kind_of(self, scope, name):
        return self._search_symbol(scope, name)[2]
        # return static, field, argument, var, none

    def type_of(self, scope, name):
        return self._search_symbol(scope, name)[3]
        # return int, char, boolean, className

    def index_of(self, scope, name):
        return self._search_symbol(scope, name)[4]
        # return Integer

    def _search_symbol(self, scope, symbol):

        tables = [tup for tup in self.symbolTable if tup[0] == scope]

        for table in tables:
            if symbol == table[1]:
                return table

