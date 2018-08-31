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
        elif op == '*':
            self.write_call('Math.multiply')
        elif op == '/':
            self.write_call('Math.divide')
        else:
            self._write_vm_file(op)

    def write_call(self, function_name):
        arg = const.API_ARG[function_name]
        line = 'call' + ' ' + function_name + ' ' + arg
        self._write_vm_file(line)

        if function_name in const.VOID_SUBROUTINES:
            self._write_vm_file('pop temp 0')

    def write_function(self, subroutine_name, local_var_count):
        line = 'function' + ' ' + self._stripped_file_name + '.' + subroutine_name + ' ' + str(local_var_count)
        self._write_vm_file(line)

    def write_goto(self, label, count):
        line = 'goto' + ' ' + label + str(count)
        self._write_vm_file(line)

    def write_if(self, label, count):
        line = 'if-goto' + ' ' + label + str(count)
        self._write_vm_file(line)

    def write_label(self, label, count):
        line = 'label' + ' ' + label + str(count)
        self._write_vm_file(line)

    def write_push(self, seg, index):

        line = 'push' + ' ' + seg + ' ' + str(index)
        self._write_vm_file(line)

    def write_pop(self, seg, index):

        line = 'pop' + ' ' + seg + ' ' + str(index)
        self._write_vm_file(line)

    def write_return(self):
        self._write_vm_file('return')

    def crear_vm_file(self):
        vm_file = self._stripped_file_path + '.vm'
        if os.path.isfile(vm_file):
            os.remove(vm_file)

    def _write_vm_file(self, line):
        vm_file = self._stripped_file_path + '.vm'
        with open(vm_file, 'a') as f:
            f.write(str(line) + '\n')
