# Usage:
# python -m HackCompiler.VMTranslator MemoryAccess/BasicTest/BasicTest.vm or
# PYTHONPATH=. python HackCompiler/VMTranslator.py MemoryAccess/BasicTest/BasicTest.vm

import sys

from HackCompiler import Parser
from HackCompiler import CodeWriter

if __name__ == "__main__":
    argvs = sys.argv
    # filePath example: StackArithmetic/SimpleAdd/SimpleAdd.vm
    filePath = argvs[1]

    parser = Parser.Parser(filePath)
    CodeWriter.CodeWriter(filePath, parser.parsedVMLines)
