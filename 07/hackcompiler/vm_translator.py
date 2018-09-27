# Usage:
# python -m hackcompiler.VMTranslator MemoryAccess/BasicTest/BasicTest.vm

import sys

from hackcompiler import parser
from hackcompiler import code_writer

if __name__ == "__main__":
    argvs = sys.argv
    filePath = argvs[1]

    parser = parser.Parser(filePath)
    code_writer.CodeWriter(filePath, parser.parsedVMLines)
