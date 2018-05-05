from Parser import Parser
from CodeWriter import CodeWriter
import sys

if __name__ == "__main__":
    argvs = sys.argv
    # filePath example: StackArithmetic/SimpleAdd/SimpleAdd.vm
    filePath = argvs[1]

    parser = Parser(filePath)
    CodeWriter(filePath, parser.parsedVMLines)
