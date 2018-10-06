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

    def write_arithmetic(self, op):
        if op in ['+', '-', '<', '>', '=', '&', '|']:
            op = const.ARITHMETIC_OP_2_CMD[op]
            self._write_vm_file(op)
        elif op == '*':
            self.write_call('Math.multiply', 2)
        elif op == '/':
            self.write_call('Math.divide', 2)
        else:
            self._write_vm_file(op)

    def write_call(self, function_name, arg_count):
        # arg = const.API_ARG[function_name]
        line = 'call' + ' ' + function_name + ' ' + str(arg_count)
        self._write_vm_file(line)

    def write_function(self, subroutine_name, local_var_count):
        line = 'function' + ' ' + self._stripped_file_name + '.' + subroutine_name + ' ' + str(local_var_count)
        self._write_vm_file(line)
        self._init_label()

    def _init_label(self):
        self._if_label_count = 0
        self._while_label_count = 0
        self._if_label_stack = []
        self._while_label_stack = []

    def write_goto(self, label):
        label_type = label.split('_')[0]
        if label_type == 'WHILE':
            label_index = self._while_label_stack[-1]
        elif label_type == 'IF':
            label_index = self._if_label_stack[-1]
        else:
            raise SyntaxError

        line = 'goto' + ' ' + label + str(label_index)
        self._write_vm_file(line)

    def write_if(self, label):
        if label == 'WHILE_EXP':
            label_index = self._while_label_stack[-1]
        elif label == 'WHILE_END':
            label_index = self._while_label_stack[-1]
        elif label == 'IF_TRUE':
            label_index = self._add_if_label_stack()
        elif label == 'IF_FALSE':
            label_index = self._if_label_stack[-1]
        elif label == 'IF_END':
            label_index = self._if_label_stack[-1]
        else:
            raise SyntaxError

        line = 'if-goto' + ' ' + label + str(label_index)
        self._write_vm_file(line)

    def write_label(self, label):
        if label == 'WHILE_EXP':
            label_index = self._add_while_label_stack()
        elif label == 'WHILE_END':
            label_index = self._while_label_stack.pop()
        elif label == 'IF_TRUE':
            label_index = self._if_label_stack[-1]
        elif label == 'IF_FALSE':
            label_index = self._if_label_stack[-1]
        elif label == 'IF_END':
            label_index = self._if_label_stack.pop()
        else:
            raise SyntaxError

        line = 'label' + ' ' + label + str(label_index)
        self._write_vm_file(line)

    def _add_while_label_stack(self):
        index = self._while_label_count
        self._while_label_count += 1
        self._while_label_stack.append(index)
        return index

    def _add_if_label_stack(self):
        index = self._if_label_count
        self._if_label_count += 1
        self._if_label_stack.append(index)
        return index

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
