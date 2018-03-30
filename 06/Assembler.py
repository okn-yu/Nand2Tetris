import Code, Parser, SymbolTable, sys

def createDict():

    tableAssembler.commandType()
    symbol = tableAssembler.symbol()

    if symbol in table.symbolDict:
        return

    if symbol in table.labelDict:
        return

    if symbol in table.symbolDict:
        return

    if tableAssembler.currentType == 'L_COMMAND':
        table.labelDict[symbol] = table.lineNumber

        if symbol in table.variableDict:
            del table.variableDict[symbol]

    if tableAssembler.currentType == 'A_COMMAND' and not symbol.isdigit():
        table.variableDict[symbol] = 0

        if symbol in table.labelDict:
            del table.labelDict[symbol]

def createSymbolTable():

    for key in table.variableDict:
        table.addEntry(key, table.variableAddress)
        table.variableAddress += 1

    for key, value in table.labelDict.items():
        table.addEntry(key, value)

def createHackBinary():
    codeAssembler.commandType()

    if codeAssembler.currentType == 'C_COMMAND':
        return '111' + code.comp(codeAssembler.comp()) + code.dest(codeAssembler.dest()) + code.jump(codeAssembler.jump())

    if codeAssembler.currentType == 'A_COMMAND':
        symbol = codeAssembler.symbol()

        if symbol.isdigit():
            address = int(symbol)
        else:
            address = table.getAddress(symbol)

        return '0' + (bin(address))[2:].zfill(15)

if __name__ == "__main__":

    argvs = sys.argv
    fileName = argvs[1]

    tableAssembler = Parser.Parser(fileName)
    table = SymbolTable.SymbolTable()

    while True:
        if tableAssembler.hasMoreCommands():
            tableAssembler.advance()
            #createSymbolTable()
            createDict()
            if not tableAssembler.currentType == 'L_COMMAND':
                table.lineNumber += 1
        else:
            break

    createSymbolTable()

    #for variable in table.variableList:
    #    print(variable +': ' + str(table.symbolDict[variable]))

    #print(table.symbolDict)
    #print(len(table.labelList))

    codeAssembler = Parser.Parser(fileName)
    code = Code.Code()
    binaryList = []


    while True:
        if codeAssembler.hasMoreCommands():
            codeAssembler.advance()
            binaryList.append(createHackBinary())
        else:
            break

    # example
    # fileName: pong/Pong.asm -> outFileName: pong/Mypong.hack
    dirName = fileName.split('/')[0]
    dstFileName = 'My'+fileName.split('/')[1].split('.')[0]
    outFileName = dirName + '/'+ dstFileName + '.hack'
    file = open(outFileName, 'w')

    for line in binaryList:
        if line:
            file.write(line+'\n')
    file.close()
