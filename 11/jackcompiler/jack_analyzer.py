import os, sys

from jackcompiler import compilation_engine as ce
from jackcompiler import jack_tokenizer as jt
from jackcompiler import path_parser as pp
from jackcompiler import symbol_table as st
from jackcompiler import vm_writer as vw


# Usage:
# cd ~/PycharmProject/Nand2Tetris/10
# python -m jackcompiler.jack_analyzer Avarage

if __name__ == "__main__":

    argvs = sys.argv
    path = argvs[1]
    pathParser = pp.PathParser(path)

    for jackFile in pathParser.jackFilesList:
        tokenizer = jt.jackTokenizer(jackFile)
        symbol_table = st.SymbolTable()
        vm_writer = vw.VMWriter(jackFile)
        ce.compilationEngine(tokenizer.outFilePath, symbol_table, vm_writer)