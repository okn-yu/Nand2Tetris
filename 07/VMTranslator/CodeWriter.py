class CodeWriter:
    def __init__(self, filePath, parsedVMLines):
        self._asmLines = []

        # initialized by script.
        #self._initVirtualSegment()

        for parsedVMLine in parsedVMLines:
            print(parsedVMLine)
            self._parse(parsedVMLine)

        print(self._asmLines)
        self._writeCode(filePath, self._asmLines)

    def _initVirtualSegment(self):
        self._writeVirtualSegment(value=str(256), pointer='SP')

    def _parse(self, parsedVMLine):
        command = parsedVMLine.get('command')
        commandType = parsedVMLine.get('commandType')
        arg1 = parsedVMLine.get('arg1')
        arg2 = parsedVMLine.get('arg2')

        if commandType == 'C_PUSH' or commandType == 'C_POP':
            return self._writePushPop(command, arg1, arg2)

        if commandType == 'C_ARITHMETIC':
            return self._compArithmetic(command)

    def _writePushPop(self, command, arg1, arg2):
        if command == 'push':
            self._push(arg1, arg2)

        # elif command == 'pop':
        #    self._pop(arg1, arg2) #TODO: Check Code!!

    def _push(self, arg1, arg2):
        if arg1 == 'constant':
            self._writeVirtualSegment(arg2, pointer='SP')
            self._incrementSP()

    '''
    def _pop(self, arg1, arg2):
        if arg1 == 'local':
            self._asmCode('@%s' % arg2, 'D=A', '@LCL', 'A=M+D')
            self._decrementSP()
            self._writeDRegister(pointer=str(self.SP))
            self._asmCode('M=D')
    '''

    def _compArithmetic(self, command):
        if command == 'add':
            self._compBinary('M=M+D')

        if command == 'sub':
            self._compBinary('M=M-D')

        if command == 'eq':
            self._judgeBoolean('JEQ')

        if command == 'lt':
            self._judgeBoolean('JLT')

        if command == 'gt':
            self._judgeBoolean('JGT')

        if command == 'neg':
            self._compUnary('M=-D')

        if command == 'not':
            self._compUnary('M=!D')

        if command == 'and':
            self._compBinary('M=M&D')

        if command == 'or':
            self._compBinary('M=M|D')

    def _incrementSP(self):
        self._asmCode('@SP', 'M=M+1')

    def _decrementSP(self):
        self._asmCode('@SP', 'M=M-1')

    def _writeBoolean(self, boolValue, pointer):
        if boolValue == 'TRUE':
            value = -1
        elif boolValue == 'FALSE':
            value = 0
        self._asmCode('@%s' % pointer, 'A=M', 'M=%s' % value)

    def _writeVirtualSegment(self, value, addr=None, pointer=None):
        if addr and not pointer:
            self._asmCode('@%s' % value, 'D=A')
            self._asmCode('@%s' % addr, 'M=D')
        if not addr and pointer:
            self._asmCode('@%s' % value, 'D=A')
            self._asmCode('@%s' % pointer, 'A=M', 'M=D')

    def _judgeBoolean(self, jump):
        # jmp Example: 'JEQ', 'JGT', 'JLT'
        self._compBinary('D=M-D')
        self._decrementSP()

        currentLineNumber = len(self._asmLines)
        self._asmCode('@' + str(currentLineNumber + 7))  # 1Line  # 7 = 1 + 3 + 1 + 1 + 1
        self._asmCode('D;' + jump)  # 1Line
        self._writeBoolean('FALSE', 'SP')  # 3Lines

        currentLineNumber = len(self._asmLines)
        self._asmCode('@' + str(currentLineNumber + 5))  # 1Line # 5 = 1 + 3 + 1
        self._asmCode('0;JMP')  # 1Line
        self._writeBoolean('TRUE', 'SP')  # 3Lines

        self._incrementSP()

    def _compUnary(self, compute):
        # compute Example: 'M=-D', 'M=!D''
        self._decrementSP()
        self._asmCode('@SP', 'A=M', 'D=M')
        self._asmCode(compute)
        self._incrementSP()

    def _compBinary(self, compute):
        # compute Example: 'M=M+D', 'M=M-D', 'M=M&D', 'M=M|D'
        self._decrementSP()
        self._asmCode('@SP', 'A=M', 'D=M')
        self._decrementSP()
        self._asmCode('@SP', 'A=M', compute)
        self._incrementSP()

    def _asmCode(self, *strings):
        for string in strings:
            self._asmLines.append(string)

    def _writeCode(self, filePath, asmLines):
        outFilePath = filePath.split('.')[0] + '.' + 'asm'

        with open(outFilePath, 'w') as f:
            for line in asmLines:
                if line:
                    f.write(line + '\n')
