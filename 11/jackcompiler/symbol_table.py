class SymbolTable:

    def __init__(self):
        self._class_symbol_table = []
        self._subroutine_symbol_table = []

    def start_subroutine(self):
        self._subroutine_symbol_table = []

    def define(self, var_name, kind, type):
        if kind in ['static', 'field']:
            symbol_table = self._class_symbol_table
        elif kind in ['arg', 'var']:
            symbol_table = self._subroutine_symbol_table
        else:
            raise SyntaxError

        symbol_table.append(
            {
                'name': var_name,
                'kind': kind,
                'type': type,
                'index': self.var_count(kind)
            }
        )

    def var_count(self, kind):
        if kind in ['static', 'field']:
            symbol_table = self._class_symbol_table
        elif kind in ['arg', 'var']:
            symbol_table = self._subroutine_symbol_table
        else:
            raise SyntaxError

        return len([column for column in symbol_table if column['kind'] == kind])

    # name: 'static', 'field', 'arg', 'var'
    def kind_of(self, name):
        return self.resolve_var(name)['kind']

    # type_ex: 'int', 'String', 'boolean' ...
    def type_of(self, name):
        return self.resolve_var(name)['type']

    def index_of(self, var_name):
        return self.resolve_var(var_name)['index']

    def resolve_var(self, var_name):
        for column in self._subroutine_symbol_table:
            if column['name'] == var_name:
                return column

        for column in self._class_symbol_table:
            if column['name'] == var_name:
                return column
        
        return None
