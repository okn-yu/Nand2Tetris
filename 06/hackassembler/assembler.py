import sys

from hackassembler import code
from hackassembler import parser
from hackassembler import symboltable


if __name__ == "__main__":

    # usage ex: python -m hackassembler.assembler max/Max.asm
    # filePath ex: max/Max.asm
    # outDirName ex: max
    # outFileName ex: MyMax.hack
    # outFilePath ex: max/MyMax.hack

    argvs = sys.argv
    filePath = argvs[1]
    outDirName = filePath.split('/')[0]
    outFileName = 'My' + filePath.split('/')[1].split('.')[0] + '.hack'
    outFilePath= outDirName + '/' + outFileName

    parser = parser.Parser(filePath)
    symbolTable = symboltable.SymbolTable(parser.parsedAsmLines)
    asmCode = code.Code(parser.parsedAsmLines, symbolTable.symbolDict)

    with open(outFilePath, 'w') as f:
        for line in asmCode.binaryList:
            if line:
                f.write(line + '\n')
