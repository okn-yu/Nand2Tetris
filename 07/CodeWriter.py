INITIAL_SP_ADDRESS = 256


class CodeWriter:
    def __init__(self, filePath, parsedVMLines):
        self.asmLines = []
        self.SP = INITIAL_SP_ADDRESS

        self._initMemory()

        for parsedVMDict in parsedVMLines:
            lines = self._parse(parsedVMDict)
            self.asmLines.extend(lines)

        self._writeCode(filePath, self.asmLines)

    def _initMemory(self):
        self._updateSP()

    def _updateSP(self):
        self.asmLines.append('@' + str(self.SP))
        self.asmLines.append('D=A')
        self.asmLines.append('@SP')
        self.asmLines.append('M=D')

    def _parse(self, parsedAsmDict):
        command = parsedAsmDict.get('command')
        commandType = parsedAsmDict.get('commandType')
        arg1 = parsedAsmDict.get('arg1')
        arg2 = parsedAsmDict.get('arg2')

        if commandType == 'C_PUSH':
            return self._writePushPop(arg1, arg2)

        if commandType == 'C_ARITHMETIC':
            return self._writeArithmetic(command)

    def _writePushPop(self, arg1, arg2):
        asmLines = []

        if arg1 == 'constant':
            asmLines.append('@' + arg2)
            asmLines.append('D=A')
            asmLines.append('@' + str(self.SP))
            asmLines.append('M=D')

            self.SP += 1
            self._updateSP()

        if arg1 == 'static':
            asmLines.append('@' + self.className + '.' + arg2)
            asmLines.append('D=' + arg2)
            asmLines.append('M=D')

        return asmLines

    def _writeArithmetic(self, command):
        asmLines = []

        if command == 'add':
            self.SP -= 1
            self._updateSP()
            asmLines.append('@' + str(self.SP))
            asmLines.append('D=M')

            self.SP -= 1
            self._updateSP()
            asmLines.append('@' + str(self.SP))
            asmLines.append('M=D+M')

            self.SP += 1
            self._updateSP()

        return asmLines

    def _writeCode(self, filePath, asmLines):
        outFilePath = filePath.split('.')[0] + '.' + 'hack'

        with open(outFilePath, 'w') as f:
            for line in asmLines:
                if line:
                    f.write(line + '\n')
