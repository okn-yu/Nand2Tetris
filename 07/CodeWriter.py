class Code:
    def __init__(self, parsedAsmLines, symbolDict):
        self.binaryList = []

        for parsedAsmDict in parsedAsmLines:
            self._parse(parsedAsmDict, symbolDict)

    def _parse(self, parsedAsmDict, symbolDict):
        symbol = parsedAsmDict.get('symbol')
        commandType = parsedAsmDict.get('commandType')

        if commandType == 'L_COMMAND':
            return

        if commandType == 'C_COMMAND':
            binCode = '111' + self._comp(parsedAsmDict.get('comp')) + self._dest(parsedAsmDict.get('dest')) + self._jump(
                parsedAsmDict.get('jump'))

        if commandType == 'A_COMMAND':
            if symbol.isdigit():
                address = int(symbol)
            else:
                address = symbolDict[symbol]

            binCode = '0' + (bin(address))[2:].zfill(15)

        self.binaryList.append(binCode)