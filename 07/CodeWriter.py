INITIAL_SP_ADDRESS = 256


class CodeWriter:
    def __init__(self, filePath, parsedVMLines):
        self.asmLines = []
        self.SP = INITIAL_SP_ADDRESS

        self._initMemory()

        for parsedVMLine in parsedVMLines:
            self._parse(parsedVMLine)
            # self.asmLines.extend(lines)

        print(self.asmLines)
        self._writeCode(filePath, self.asmLines)

    def _initMemory(self):
        # init SP
        self._writeMemory(str(INITIAL_SP_ADDRESS), 'SP')

    def _parse(self, parsedVMLine):
        command = parsedVMLine.get('command')
        commandType = parsedVMLine.get('commandType')
        arg1 = parsedVMLine.get('arg1')
        arg2 = parsedVMLine.get('arg2')

        if commandType == 'C_PUSH':
            return self._writePushPop(arg1, arg2)

        if commandType == 'C_ARITHMETIC':
            return self._writeArithmetic(command)

    def _writePushPop(self, arg1, arg2):
        if arg1 == 'constant':
            self._writeMemory(arg2, str(self.SP))
            self._incrementSP()

    def _writeArithmetic(self, command):
        if command == 'add':
            self._add()

        if command == 'sub':
            self._sub()

        if command == 'eq':
            self._eq()

        if command == 'lt':
            self._lt()

        if command == 'gt':
            self._gt()

        if command == 'neg':
            self._neg()

        if command == 'not':
            self._not()

        if command == 'and':
            self._and()

        if command == 'or':
            self._or()

    def _incrementSP(self):
        self.asmLines.append('@SP')
        self.asmLines.append('M=M+1')
        self.SP += 1

    def _decrementSP(self):
        self.asmLines.append('@SP')
        self.asmLines.append('M=M-1')
        self.SP -= 1

    def _writeMemory(self, value, address):

        if value == 'TRUE':
            self.asmLines.append('@' + address)
            self.asmLines.append('M=-1')

        elif value == 'FALSE':
            self.asmLines.append('@' + address)
            self.asmLines.append('M=0')

        else:
            self.asmLines.append('@' + value)
            self.asmLines.append('D=A')
            self.asmLines.append('@' + address)
            self.asmLines.append('M=D')

    def _neg(self):
        self._unaryFunc('M=-D')

    def _not(self):
        self._unaryFunc('M=!D')

    def _add(self):
        self._binaryFunc('M=M+D')

    def _sub(self):
        self._binaryFunc('M=M-D')

    def _and(self):
        self._binaryFunc('M=M&D')

    def _or(self):
        self._binaryFunc('M=M|D')

    def _eq(self):
        self._boolFunc('JEQ')

    def _lt(self):
        self._boolFunc('JLT')

    def _gt(self):
        self._boolFunc('JGT')

    def _boolFunc(self, jump):
        self._binaryFunc('D=M-D')
        self._decrementSP()

        currentLineNumber = len(self.asmLines)
        self.asmLines.append('@' + str(currentLineNumber + 6))  # 1Line
        self.asmLines.append('D;' + jump)  # 1Line
        self._writeMemory('FALSE', str(self.SP))  # 2Lines

        currentLineNumber = len(self.asmLines)
        self.asmLines.append('@' + str(currentLineNumber + 4))  # 1Line
        self.asmLines.append('0;JMP')  # 1Line
        self._writeMemory('TRUE', str(self.SP))  # 2Lines

        self._incrementSP()

    def _unaryFunc(self, compute):
        self._decrementSP()
        self._writeDRegister(pointer=str(self.SP))
        self.asmLines.append(compute)

        self._incrementSP()

    def _binaryFunc(self, compute):
        self._decrementSP()
        self._writeDRegister(pointer=str(self.SP))

        self._decrementSP()
        self.asmLines.append('@' + str(self.SP))
        self.asmLines.append(compute)

        self._incrementSP()

    def _writeDRegister(self, value=None, pointer=None):
        if value:
            self.asmLines.append('@' + value)
            self.asmLines.append('D=A')

        if pointer:
            self.asmLines.append('@' + pointer)
            self.asmLines.append('D=M')

    def _writeCode(self, filePath, asmLines):
        outFilePath = filePath.split('.')[0] + '.' + 'asm'

        with open(outFilePath, 'w') as f:
            for line in asmLines:
                if line:
                    f.write(line + '\n')
