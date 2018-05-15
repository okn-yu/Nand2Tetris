from hackcompiler.asm_code import AsmCode as asm
from hackcompiler import comp_stack as cs
from hackcompiler import comp_arithmetic as ca
from hackcompiler import prog_flow as pf
from hackcompiler import sub_call as sc

class CodeWriter:
    def __init__(self, filePath, parsedVMLines):

        # Initialized by script.
        #asm._init_vsgm()

        for parsedVMLine in parsedVMLines:
            #print(parsedVMLine)
            self._parse(parsedVMLine)

        self._write_file(filePath)

    def _parse(self, parsedVMLine):
        command = parsedVMLine.get('command')
        commandType = parsedVMLine.get('commandType')
        arg1 = parsedVMLine.get('arg1')
        arg2 = parsedVMLine.get('arg2')

        if commandType == 'C_PUSH' or commandType == 'C_POP':
            cs.write_push_pop(command, arg1, arg2)
            return

        if commandType == 'C_ARITHMETIC':
            ca.write_arithmetic(command)
            return

        if commandType == 'C_LABEL':
            pf.write_label(arg1)
            return
            
        if commandType == 'C_GOTO':
            pf.write_goto(arg1)
            return
            
        if commandType == 'C_IF':
            pf.write_if(arg1)
            return

        if commandType == 'C_FUNCTION':
            sc.write_function(arg1, arg2)
            return
            
        if commandType == 'C_CALL':
            sc.write_call(arg1, arg2)
            return
            
        if commandType == 'C_RETURN':
            sc.write_return()
            return

    def _write_file(self, filePath):
        outFilePath = filePath.split('.')[0] + '.' + 'asm'
        asmLines = asm.asmLines

        with open(outFilePath, 'w') as f:
            for line in asmLines:
                if line:
                    print(line)
                    f.write(line + '\n')