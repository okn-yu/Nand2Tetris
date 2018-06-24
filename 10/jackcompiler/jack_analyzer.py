import os, sys

from jackcompiler import compilation_engine as ce
from jackcompiler import jack_tokenizer as jt
from jackcompiler import path_parser as pp

if __name__ == "__main__":

    argvs = sys.argv
    # path example: ArrayTest
    path = argvs[1]
    pathParser = pp.PathParser(path)

    for jackFile in pathParser.jackFilesList:
        tokenizer = jt.jackTokenizer(jackFile)
        ce.compilationEngine(tokenizer.XMLTokensList)