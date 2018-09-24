class SymbolTable:
    def __init__(self, parsedAsmLines):

        print(parsedAsmLines)
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
        self.lineNumber = 0
        self._variableAddress = 16

        self._parseLCommand([line for line in parsedAsmLines if line.get('commandType') == 'L_COMMAND'])
        self._parseACommand([line for line in parsedAsmLines if line.get('commandType') == 'A_COMMAND'])

    def _parseLCommand(self, lCommands):

        for parsedAsmDict in lCommands:
            symbol = parsedAsmDict.get('symbol')
            lineNum = parsedAsmDict.get('lineNum')
            self.symbolDict[symbol] = lineNum

    def _parseACommand(self, aCommands):

        for parsedAsmDict in aCommands:
            symbol = parsedAsmDict.get('symbol')

            if symbol.isdigit():
                continue
            elif symbol in self.symbolDict:
                continue
            else:
                self._addEntry(symbol, self._variableAddress)
                self._variableAddress += 1

    def _addEntry(self, symbol, address):
        self.symbolDict[symbol] = address
