import os


class jack_tokenizer:
    def __init__(self, filePath):

        self._currentLine = None
        self._currentToken = None
        self._tokensList = []
        self._XMLTokensList = ['<tokens>\n']
        self._tokenize(filePath)

        while True:
            if self._has_more_tokens():
                self._advance()
                self._tokenType()
            else:
                break

        self._writeXML(filePath)

    def _tokenize(self, filePath):

        rawLines = self._read_jack_file(filePath)
        effectiveLines = self._read_jack_line(rawLines)
        self._divide_2_tokens(effectiveLines)

    def _read_jack_file(self, filePath):

        with open(filePath, mode='r') as file:
            return file.readlines()

    def _read_jack_line(self, rawLines):

        effectiveLines = []

        for line in rawLines:

            if (line[0:2] == '//') or (line == '\r\n') or (line == '\n') or (line == '\t\n') or (line[0:2] == '/*'):
                continue

            if '//' in line:
                line = (line.split('//')[0])  # line: code // comment

            line = line.strip()

            effectiveLines.append(line)

        return effectiveLines

    def _divide_2_tokens(self, effectiveLines):

        for line in effectiveLines:

            # divide by dot.
            if '.' in line:
                line = line.split('.')[0] + ' . ' + line.split('.')[1]

            if ',' in line:
                line = line.split(',')[0] + ' , ' + line.split(',')[1]

            if '(' in line:
                line = line.split('(')[0] + ' ( ' + line.split('(')[1]

            if ')' in line:
                line = line.split(')')[0] + ' ) ' + line.split(')')[1]

            if '[' in line:
                line = line.split('[')[0] + ' [ ' + line.split('[')[1]

            if ']' in line:
                line = line.split(']')[0] + ' ] ' + line.split(']')[1]

            if ';' in line:
                line = line.split(';')[0] + ' ;'

            if '<' in line:
                line = line.replace('<', '&lt;')

            if '>' in line:
                line = line.replace('<', '&gt;')

            if '"' in line:
                splitedLine = (line.split('"'))
                self._tokensList.extend(splitedLine[0].split())
                self._tokensList.append(splitedLine[1])
                self._tokensList.extend(splitedLine[2].split())

            else:
                self._tokensList.extend(line.split())

        print(self._tokensList)

    def _has_more_tokens(self):
        if len(self._tokensList) > 0:
            return True
        else:
            return False

    def _advance(self):
        self._currentToken = self._tokensList.pop(0)

    def _tokenType(self):

        keywordList = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                       'void',
                       'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

        symbolList = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '&lt;', '&gt;', '=', '~']

        if self._currentToken in keywordList:
            tokenType = 'keyword'

        elif self._currentToken in symbolList:
            tokenType = 'symbol'

        elif not self._currentToken[0].isdigit() and not ' ' in self._currentToken:
            tokenType = 'identifier'

        elif self._currentToken.isdigit() and int(self._currentToken) in range(0, 32767):
            tokenType = 'integerConstant'

        elif not '\n' in self._currentToken and not '"' in self._currentToken:
            tokenType = 'stringConstant'

        else:
            print('invalid token!')

        tXMLLine = '<' + tokenType + '> ' + self._currentToken + ' </' + tokenType + '>' + '\n'

        self._XMLTokensList.append(tXMLLine)
        return

    def _writeXML(self, filePath):

        # outFilePath ex: ArrayTest/Main.jack
        outDirPath = filePath.split('/')[0]
        outFileName = filePath.split('/')[1].split('.')[0]
        outFilePath = outDirPath + '/' + 'My' + outFileName + 'T.xml'

        self._XMLTokensList.append('</tokens>')

        with open(outFilePath, 'w') as f:
            for line in self._XMLTokensList:
                if line:
                    print(line)
                    f.write(line)
