from Code import Code
from Parser import Parser
from SymbolTable import SymbolTable
import sys

if __name__ == "__main__":

    argvs = sys.argv
    # filePath example: max/Max.asm
    filePath = argvs[1]
    outDirName = filePath.split('/')[0]
    outFileName = 'My' + filePath.split('/')[1].split('.')[0]
    # outFilePath example: max/MyMax.
    outFilePath= outDirName + '/' + outFileName + '.hack'

    parser = Parser(filePath)
    symbolTable = SymbolTable(parser.parsedAsmLines)
    asmCode = Code(parser.parsedAsmLines, symbolTable.symbolDict)

    with open(outFilePath, 'w') as f:
        for line in asmCode.binaryList:
            if line:
                f.write(line + '\n')
