import os

commandDict = {
    'add': 'C_ARITHMETIC',
    'sub': 'C_ARITHMETIC',
    'neg': 'C_ARITHMETIC',
    'eq': 'C_ARITHMETIC',
    'gt': 'C_ARITHMETIC',
    'lt': 'C_ARITHMETIC',
    'and': 'C_ARITHMETIC',
    'or': 'C_ARITHMETIC',
    'not': 'C_ARITHMETIC',
    'push': 'C_PUSH',
    'pop': 'C_POP',
    'label': 'C_LABEL',
    'goto': 'C_GOTO',
    'if-goto': 'C_IF',
    'function': 'C_FUNCTION',
    'call': 'C_CALL',
    'return': 'C_RETURN'
}


class Parser:
    def __init__(self, filePath):
        self._commandsList = []
        self._currentCommand = ''
        self.parsedVMLines = []
        self.linesList = []
        self._parse_file_path(filePath)

        for lines in self.linesList:
            if (lines[0:2] == '//') or (lines == '\r\n') or (lines == '\n'):
                pass
            else:
                # line: command //comment
                command = (lines.split('//')[0])
                self._commandsList.append(command.split())

        while True:
            if self._has_more_commands():
                self._advance()
                self._parser()
            else:
                break

    def _parser(self):
        parsedVMDict = {
            'fileName': None,
            'command': None,
            'commandType': None,
            'arg1': None,
            'arg2': None
        }

        for index, commandElement in enumerate(self._currentCommand):
            if index == 0:
                parsedVMDict['fileName'] = commandElement
            if index == 1:
                parsedVMDict['command'] = commandElement
                parsedVMDict['commandType'] = commandDict[commandElement]
            if index == 2:
                parsedVMDict['arg1'] = commandElement
            if index == 3:
                parsedVMDict['arg2'] = commandElement

        self.parsedVMLines.append(parsedVMDict)

    def _has_more_commands(self):
        if len(self._commandsList) > 0:
            return True
        else:
            return False

    def _advance(self):
        self._currentCommand = self._commandsList.pop(0)

    def _parse_file_path(self, filePath):
        if os.path.isfile(filePath):
            self._open_file(filePath)
        elif os.path.isdir(filePath):
            self._open_dir(filePath)
        else:
            print('invalid FilePath.')

    def _open_file(self, filePath):
        if filePath[-2:] != 'vm':
            return

        with open(filePath, mode='r') as file:
            rawLines = file.readlines()

            fileName = self._get_fileName(filePath)
            fileLines = self._add_fileName(fileName, rawLines)

            sysLine = fileName + ' ' +  'function Sys.init 0\n'

            # Call Sys.init shold be in Mem[0].
            if sysLine in fileLines:
                self.linesList = fileLines + self.linesList
            else:
                self.linesList.extend(fileLines)

            print(self.linesList)

    def _open_dir(self, filePath):
        filesList = os.listdir(filePath)

        for file in filesList:
            self._parse_file_path(filePath + file)

    def _add_fileName(self, fileName, lines):

        for index, line in enumerate(lines):
            lines[index] = fileName + ' ' + line

        return lines

    def _get_fileName(self, filePath):
        fileName = filePath.split('/')[-1]
        return fileName
