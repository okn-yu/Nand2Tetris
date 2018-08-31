class SymbolTable:

    def __init__(self):
        self.symbol_tables = []

    def define(self, scope, kind, type, var_name):

        var_count = self._var_count(scope)

        self.symbol_tables.append(
            {
                'scope_name': scope,
                'kind': kind,
                'type': type,
                'var_name': var_name,
                'count': var_count
            }
        )

    def _var_count(self, scope):

        var_count = 0

        for table in self.symbol_tables:
            if table['scope_name'] == scope:
                var_count += 1

        return var_count

    # name: 'static', 'field', 'arg', 'var'
    def kind_of(self, scope, name):
        for table in self.symbol_tables:
            if table['scope_name'] == scope and table['var_name'] == name:
                return table['kind']

    # type_ex: 'int', 'String', 'boolean' ...
    def type_of(self, scope, name):
        for table in self.symbol_tables:
            if table['scope_name'] == scope and table['var_name'] == name:
                return table['type']

    def index_of(self, scope, name):
        for table in self.symbol_tables:
            if table['scope_name'] == scope and table['var_name'] == name:
                return table['count']

    def count_of(self, scope):

        return len([table for table in self.symbol_tables if table['scope_name'] == scope])


