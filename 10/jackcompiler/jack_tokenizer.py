import os


class jack_tokenizer:
    def __init__(self, filePath):

        self._currentLine = None
        self._currentToken = None
        self._tolenList = []
        self._tokenize(filePath)

        # for lines in self.linesList:
        #     if (lines[0:2] == '//') or (lines == '\r\n') or (lines == '\n'):
        #         pass
        #     else:
        #         # line: command //comment
        #         command = (lines.split('//')[0])
        #         self._commandsList.append(command.split())
        #
        # while True:
        #     if self._has_more_tokens():
        #         self._advance()
        #         self._parser()
        #     else:
        #         break

    def _tokenize(self, filePath):

        effectiveLines = self._read_file(filePath)
        tokenLists = self._read_lines(effectiveLines)

    def _read_file(self, filePath):

        effectiveLines = []

        with open(filePath, mode='r') as file:
            rawLines = file.readlines()

        for line in rawLines:
            if (line[0:2] == '//') or (line == '\r\n') or (line == '\n') or (line == '\t\n'):
                pass
            elif '//' in line:
                code = (line.split('//')[0]) # line: code // comment
                effectiveLines.append(code)
            elif line[-1:] == '\n':
                code = line[:-1]
                effectiveLines.append(code)

        return effectiveLines

    def _read_lines(self, effectiveLines):

        print(effectiveLines)
        for line in effectiveLines:
            print(line)


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

    def _has_more_tokens(self):
        if len(self._commandsList) > 0:
            return True
        else:
            return False

    def _advance(self):
        self._currentCommand = self._commandsList.pop(0)
