from hackcompiler.asm_code import AsmCode as asm
from hackcompiler import comp_stack as cs
from hackcompiler import comp_arithmetic as ca

class CodeWriter:
    def __init__(self, filePath, parsedVMLines):

        # Initialized by script.
        asm._init_vsgm()

        for parsedVMLine in parsedVMLines:
            print(parsedVMLine)
            self._parse(parsedVMLine)

        self._write_file(filePath)

    def _parse(self, parsedVMLine):
        command = parsedVMLine.get('command')
        commandType = parsedVMLine.get('commandType')
        segment = parsedVMLine.get('arg1')
        index = parsedVMLine.get('arg2')

        if commandType == 'C_PUSH' or commandType == 'C_POP':
            cs.write_push_pop(command, segment, index)

        if commandType == 'C_ARITHMETIC':
            ca.comp_arithmetic(command)

    def _write_file(self, filePath):
        outFilePath = filePath.split('.')[0] + '.' + 'asm'
        asmLines = asm.asmLines

        with open(outFilePath, 'w') as f:
            for line in asmLines:
                if line:
                    f.write(line + '\n')