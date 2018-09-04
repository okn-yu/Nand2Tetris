import os
import inspect

from jackcompiler import const

class VMWriter():

    def __init__(self, jackFile_path):
        # ex Seven/Main.vm -> Seven/Main
        self._stripped_file_path = jackFile_path.split('.')[0]
        # ex Seven/Main -> Main
        self._stripped_file_name = self._stripped_file_path.split('/')[-1]

        self._line_number = 1

        self._label_count = 0
        self._label_index = 0

    def write_arithmetic(self, op):
        if op in ['+', '-', '<', '>', '=', '&']:
            op = const.ARITHMETIC_OP_2_CMD[op]
            self._write_vm_file(op)
        elif op == '*':
            self.write_call('Math.multiply')
        elif op == '/':
            self.write_call('Math.divide')
        else:
            self._write_vm_file(op)

    def write_call(self, function_name, arg_count):
        # arg = const.API_ARG[function_name]
        line = 'call' + ' ' + function_name + ' ' + str(arg_count)
        self._write_vm_file(line)

        if function_name in const.VOID_SUBROUTINES:
            self._write_vm_file('pop temp 0')

    def write_function(self, subroutine_name, local_var_count):
        line = 'function' + ' ' + self._stripped_file_name + '.' + subroutine_name + ' ' + str(local_var_count)

        self._write_vm_file(line)

    def write_goto(self, label):
        label_index = self._ref_index()
        line = 'goto' + ' ' + label + str(label_index)

        self._write_vm_file(line)

    def write_if(self, label):
        if label == 'IF_TRUE':
            label_index = self._add_index()
        else:
            label_index = self._ref_index()

        line = 'if-goto' + ' ' + label + str(label_index)
        self._write_vm_file(line)

    def write_label(self, label):
        if label == 'WHILE_EXP':
            label_index = self._add_index()
        elif label == 'WHILE_END':
            label_index = self._ref_index()
            self._dec_index()
        elif label == 'IF_END':
            label_index = self._ref_index()
            self._dec_index()
        else:
            label_index = self._ref_index()

        line = 'label' + ' ' + label + str(label_index)
        self._write_vm_file(line)

    def _add_index(self):
        self._label_count += 1
        self._label_index = self._label_count
        return self._label_index

    def _dec_index(self):
        self._label_index -= 1

    def _ref_index(self):
        return self._label_index

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

        def _indent(stack, indent=''):
            for i in range(0, len(stack)):
                indent += ' '
            return indent

        print(_indent(inspect.stack()), '[OUTPUT_CODE line:%s %s]' %(self._line_number, line))
        self._line_number += 1

        vm_file = self._stripped_file_path + '.vm'
        with open(vm_file, 'a') as f:
            f.write(str(line) + '\n')
