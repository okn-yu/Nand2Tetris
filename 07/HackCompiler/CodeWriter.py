class CodeWriter:
    def __init__(self, filePath, parsedVMLines):
        self._asmLines = []

        # initialized by script.
        self._initVirtualSegment()

        for parsedVMLine in parsedVMLines:
            print(parsedVMLine)
            self._parse(parsedVMLine)

        print(self._asmLines)
        self._writeCode(filePath, self._asmLines)

    def _initVirtualSegment(self):
        # for UT.
        self._writeVirtualSegment(value=str(256), addr='SP')
        self._writeVirtualSegment(value=str(300), addr='LCL')
        self._writeVirtualSegment(value=str(400), addr='ARG')
        self._writeVirtualSegment(value=str(3000), addr='THIS')
        self._writeVirtualSegment(value=str(3010), addr='THAT')

    def _parse(self, parsedVMLine):
        command = parsedVMLine.get('command')
        commandType = parsedVMLine.get('commandType')
        segment = parsedVMLine.get('arg1')
        index = parsedVMLine.get('arg2')

        if commandType == 'C_PUSH' or commandType == 'C_POP':
            return self._writePushPop(command, segment, index)

        if commandType == 'C_ARITHMETIC':
            return self._compArithmetic(command)

    def _writePushPop(self, command, segment, index):
        if command == 'push':
            self._push(segment, index)

        elif command == 'pop':
            self._pop(segment, index)

    def _push(self, segment, index):
        if segment == 'constant':
            self._writeVirtualSegment(index, pointer='SP')
            self._incrementSP()
            return

        register = self._conv2Register(segment)

        if segment == 'temp':
            self._asmCode('@%s' % 'R5')
        else:
            self._asmCode('@%s' % register, 'A=M')

        for i in range(int(index)):
            self._asmCode('A=A+1')

        self._asmCode('D=M')
        self._asmCode('@SP', 'A=M', 'M=D') # TODO: should use finction!
        self._incrementSP()

    def _pop(self, segment, index):
        register = self._conv2Register(segment)
        self._decrementSP()

        self._asmCode('@SP', 'A=M', 'D=M') # TODO: should use function!

        if segment == 'temp': # R5 value is not Pointer.
            self._asmCode('@%s' % 'R5')
        else:
            self._asmCode('@%s' % register, 'A=M')

        for i in range(int(index)):
            self._asmCode('A=A+1')

        self._asmCode('M=D')

    def _conv2Register(self, segment):

        if segment == 'local':
            return 'LCL'
        elif segment == 'argument':
            return 'ARG'
        elif segment == 'this':
            return 'THIS'
        elif segment == 'that':
            return 'THAT'
        elif segment == 'temp':
            return 'R5'
        else:
            raise RuntimeError('Undefined segment.')

    def _compArithmetic(self, command):

        if command == 'add':
            self._compBinary('M=M+D')

        if command == 'sub':
            self._compBinary('M=M-D')

        if command == 'eq':
            self._isBoolean('JEQ')

        if command == 'lt':
            self._isBoolean('JLT')

        if command == 'gt':
            self._isBoolean('JGT')

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

    def _isBoolean(self, jump):
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