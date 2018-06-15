import os, sys

from jackcompiler import compilation_engine
from jackcompiler import jack_tokenizer
from jackcompiler import path_parser as pp

if __name__ == "__main__":

    argvs = sys.argv
    # path example: ArrayTest
    path = argvs[1]
    pathParser = pp.PathParser(path)

    for jackFile in pathParser.jackFilesList:
        pass
        # tokens = jack_tokenizer(jackFile)
        # compilation_engine(tokens)
