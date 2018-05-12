# Usage:
# python -m hackcompiler.VMTranslator MemoryAccess/BasicTest/BasicTest.vm or
# PYTHONPATH=. python hackcompiler/vmtranslator.py MemoryAccess/BasicTest/BasicTest.vm

import sys

from hackcompiler import parser
from hackcompiler import codewriter

if __name__ == "__main__":
    argvs = sys.argv
    # filePath example: StackArithmetic/SimpleAdd/SimpleAdd.vm
    filePath = argvs[1]

    parser = parser.Parser(filePath)
    codewriter.CodeWriter(filePath, parser.parsedVMLines)
