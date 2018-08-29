import os

from jackcompiler import const

class VMWriter():

    def __init__(self, jackFile_path):
        # ex Seven/Main.vm -> Seven/Main
        self._stripped_file_path = jackFile_path.split('.')[0]
        # ex Seven/Main -> Main
        self._stripped_file_name = self._stripped_file_path.split('/')[-1]

    def write_arithmetic(self, op):
        if op in ['+', '-', '<', '>']:
            op = const.ARITHMETIC_OP_2_CMD[op]
            self._write_vm_file(op)

        if op == '*':
            self.write_call('Math.multiply')

    def write_call(self, function_name):
        arg = const.API_ARG[function_name]
        line = 'call' + ' ' + function_name + ' ' + arg
        self._write_vm_file(line)

        if function_name in const.VOID_SUBROUTINES:
            self._write_vm_file('pop temp 0')

    def write_function(self, subroutine_name, local_var_count):
        line = 'function' + ' ' + self._stripped_file_name + '.' + subroutine_name + ' ' + str(local_var_count)
        self._write_vm_file(line)

    def write_push(self, var, index=None):

        if type(var) is int:
            line = 'push' + ' ' + 'constant' +  ' ' + str(var)
        elif type(var) is str:
            line = 'push' + ' ' + var + ' ' + str(index)
        else:
            raise SyntaxError

        self._write_vm_file(line)

    def write_return(self):
        self._write_vm_file('return')

    def crear_vm_file(self):
        vm_file = self._stripped_file_path + '.vm'
        os.remove(vm_file)

    def _write_vm_file(self, line):
        vm_file = self._stripped_file_path + '.vm'
        with open(vm_file, 'a') as f:
            f.write(str(line) + '\n')
