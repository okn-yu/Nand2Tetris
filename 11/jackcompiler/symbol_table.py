class SymbolTable:

    def __init__(self):
        self._class_symbol_table = []
        self._subroutine_symbol_table = []

    # あるサブルーチン内部では別サブルーチンのローカル変数を参照することはない。
    # そのためシンボルテーブルはクラス用と現在処理しているサブルーチン内部の2種類のみで良い。

    def start_subroutine(self):
        self._subroutine_symbol_table = []

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

    def varCount(self, scope):
        return len(
            [table for table in self.symbol_tables if (table['scope_name'] == scope and (table['kind'] != 'field'))])
