import os, sys

import compilation_engine as ce
import jack_tokenizer as jt
import path_parser as pp
import symbol_table as st
import vm_writer as vw

# Usage: python -m jack_compiler Average

if __name__ == "__main__":

    argvs = sys.argv
    # path example: Averae
    path = argvs[1]
    pathParser = pp.PathParser(path)

    for jackFile in pathParser.jackFilesList:
        tokenizer = jt.jackTokenizer(jackFile)                       # input:xxx.jack File. output:xxxT.xml File.
        compEngine = ce.compilationEngine(tokenizer.outFilePath)     # input:xxxT.xml File. output:xxx.xml File.
        symTable = st.SymbolTable(compEngine.outFilePath)            # input:xxx.xml File. output:xxx.VM File
        vw.VMWriter(compEngine.outFilePath)

    # jackTokenizer()       # input:xxx.jack File. output:xxxT.xml File.
    # compilationEngine()   # input:xxxT.xml File. output:xxx.xml File.
    # symbolTable()         # input:xxx.xml File. output:xxx.symbolTable.
    # vmWriter()            # input:xxx.xml File & symbolTable. output xxx.vm File.

    # for jackFile in pathParser.jackFilesList:
    #     tokenizer = jt.jackTokenizer(jackFile)
    #     ce.compilationEngine(tokenizer.outFilePath)