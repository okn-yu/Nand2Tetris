class Parser:

    def __init__(self, fileName):

        with open(fileName, mode='r') as file:
            self.linesList = file.readlines()
            self.commandsList = []
            self.currentCommand = ''
            self.currentType = ''

        for line in self.linesList:
            if line[0:2] == '//' or line == '\r\n':
                pass
            else:
                # line: command //comment
                command = (line.split('//')[0])
                self.commandsList.extend(command.split())

    def hasMoreCommands(self):

        if len(self.commandsList) > 0:
            return True
        else:
            return False

    def advance(self):

        self.currentCommand = self.commandsList.pop(0)
        return self.currentCommand

    def commandType(self):

        if self.currentCommand[0:1] == '@':
            self.currentType = 'A_COMMAND'

        elif self.currentCommand[0] == '(' and self.currentCommand[-1] == ')':
            self.currentType = 'L_COMMAND'

        else:
            self.currentType = 'C_COMMAND'

        return self.currentType

    def symbol(self):

        if self.currentType == 'A_COMMAND':
            return self.currentCommand[1:]

        if self.currentType == 'L_COMMAND':
            return self.currentCommand[1:-1]

    def dest(self):

        if '=' in self.currentCommand:
            return self.currentCommand.split('=')[0]
        else:
            return 'null'

    def comp(self):

        if '=' in self.currentCommand:
            return self.currentCommand.split('=')[1]
        elif ';' in self.currentCommand:
            return self.currentCommand.split(';')[0]
        else:
            return self.currentCommand

    def jump(self):

        if ';' in self.currentCommand:
            return self.currentCommand.split(';')[1]
        else:
            return 'null'
