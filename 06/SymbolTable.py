class SymbolTable:

    def __init__(self):
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
        self.variableAddress = 16
        self.variableDict = {}
        self.labelDict = {}
        self.symbolList = []

    def addEntry(self, symbol, address):
        self.symbolDict[symbol] = address

    def addVariableList(self, symbol):
        self.variableList.append(symbol)

    def contains(self, symbol):
        return symbol in self.symbolDict

    def deleteVariableList(self, symbol):
        if symbol in self.variableList:
            self.variableList.remove(symbol)

    def getAddress(self, symbol):
        return self.symbolDict[symbol]

    def getVariableAddress(self):
        return self.variableAddress
