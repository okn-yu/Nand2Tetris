class Parser:
    def __init__(self, fileName):
        self._commandsList = []
        self._currentCommand = ''
        self._currentType = ''
        self.parsedAsmLines = []
        self._lineNum = 0

        with open(fileName, mode='r') as file:
            linesList = file.readlines()

        for line in linesList:
            if line[0:2] == '//' or line == '\r\n':
                pass
            else:
                # line: command //comment
                command = (line.split('//')[0])
                self._commandsList.extend(command.split())

        while True:
            if self._hasMoreCommands():
                self._advance()
                self._parser()
            else:
                break

    def _parser(self):
        self.parsedAsmLines.append(
            {
                'currentCommand': self._currentCommand,
                'commandType': self._commandType(),
                'symbol': self._symbol(),
                'dest': self._dest(),
                'comp': self._comp(),
                'jump': self._jump(),
                'lineNum': self._lineNumber()
            }
        )

    def _hasMoreCommands(self):
        if len(self._commandsList) > 0:
            return True
        else:
            return False

    def _advance(self):
        self._currentCommand = self._commandsList.pop(0)

    def _commandType(self):
        if self._currentCommand[0:1] == '@':
            return 'A_COMMAND'
        elif self._currentCommand[0] == '(' and self._currentCommand[-1] == ')':
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def _symbol(self):
        if self._commandType() == 'A_COMMAND':
            return self._currentCommand[1:]

        if self._commandType() == 'L_COMMAND':
            return self._currentCommand[1:-1]

    def _dest(self):
        if '=' in self._currentCommand:
            return self._currentCommand.split('=')[0]
        else:
            return None

    def _comp(self):
        if '=' in self._currentCommand:
            return self._currentCommand.split('=')[1]
        elif ';' in self._currentCommand:
            return self._currentCommand.split(';')[0]
        else:
            return self._currentCommand

    def _jump(self):
        if ';' in self._currentCommand:
            return self._currentCommand.split(';')[1]
        else:
            return None

    def _lineNumber(self):
        if self._commandType() != 'L_COMMAND':
            self._lineNum += 1
        return self._lineNum
