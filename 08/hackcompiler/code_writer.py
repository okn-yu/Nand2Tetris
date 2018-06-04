import os

from hackcompiler.asm_code import AsmCode as asm
from hackcompiler import comp_stack as cs
from hackcompiler import comp_arithmetic as ca
from hackcompiler import prog_flow as pf
from hackcompiler import sub_call as sc


class CodeWriter:
    def __init__(self, filePath, parsedVMLines):

        asm._init_vsgm()

        for parsedVMLine in parsedVMLines:
            # print(parsedVMLine)
            self._parse(parsedVMLine)

        self._write_file(filePath)

    def _parse(self, parsedVMLine):
        command = parsedVMLine.get('command')
        commandType = parsedVMLine.get('commandType')
        arg1 = parsedVMLine.get('arg1')
        arg2 = parsedVMLine.get('arg2')
        fileName = parsedVMLine.get('fileName')

        if commandType == 'C_PUSH' or commandType == 'C_POP':
            cs.write_push_pop(command, arg1, arg2, fileName)
            return

        if commandType == 'C_ARITHMETIC':
            ca.write_arithmetic(command)
            return

        if commandType == 'C_LABEL':
            if not 'funcName' in locals():
                self.funcName = None

            pf.write_label(arg1, self.funcName)
            return

        if commandType == 'C_GOTO':
            if not 'funcName' in locals():
                self.funcName = None

            pf.write_goto(arg1, self.funcName)
            return

        if commandType == 'C_IF':
            pf.write_if_goto(arg1)
            return

        if commandType == 'C_FUNCTION':
            sc.write_function(arg1, arg2)
            self.funcName = arg1
            return

        if commandType == 'C_CALL':
            sc.write_call(arg1, arg2)
            return

        if commandType == 'C_RETURN':
            sc.write_return()
            return

    # filePath example.
    # File: FunctionCalls/SimpleFunction/SimpleFunction.vm
    # Dir: FunctionCalls/SimpleFunction/
    def _write_file(self, filePath):

        if os.path.isfile(filePath):
            outFilePath = filePath.split('.')[0] + '.' + 'asm'
        elif os.path.isdir(filePath):
            outFilePath = filePath + filePath.split('/')[-2] + '.' + 'asm'

        asmLines = asm.asmLines

        with open(outFilePath, 'w') as f:
            for line in asmLines:
                if line:
                    print(line)
                    f.write(line + '\n')
