class SymbolTable:
    def __init__(self, parsedAsmLines):
        self.symbolDict = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SCREEN': 16384,
            'KBD': 24576}
        self.symbolList = []
        self.lineNumber = 0
        self._parse(parsedAsmLines)
        self._createSymbolTable()

    def _parse(self, parsedAsmLines):
        for parsedAsmDict in parsedAsmLines:
            symbol = parsedAsmDict.get('symbol')
            commandType = parsedAsmDict.get('commandType')
            self._preSymbolTable(symbol, commandType)
            self._updateLineNumber(commandType)

    def _addEntry(self, symbol, address):
        self.symbolDict[symbol] = address

    def _preSymbolTable(self, symbol, commandType):
        if not symbol or (symbol in self.symbolDict) or symbol.isdigit():
            return

        if commandType == 'L_COMMAND':
            self.symbolDict[symbol] = self.lineNumber

            if symbol in self.symbolList:
                self.symbolList.remove(symbol)
                
            return

        if commandType == 'A_COMMAND' and (symbol not in self.symbolList):
            self.symbolList.append(symbol)

    def _updateLineNumber(self, commandType):
        if not commandType == 'L_COMMAND':
            self.lineNumber += 1

    def _createSymbolTable(self):
        variableAddress = 16

        for symbol in self.symbolList:
            self._addEntry(symbol, variableAddress)
            variableAddress += 1
