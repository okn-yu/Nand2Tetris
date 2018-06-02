from hackcompiler.asm_code import AsmCode as asm
from hackcompiler import comp_stack as cs

def write_label(label, funcName):
    _set_label(label, funcName)
    return


def write_goto(label, funcName):
    _set_goto(label, funcName)
    return


def write_if_goto(label):
    _set_if_goto(label)
    return


def _set_goto(label, funcName):
    if funcName:
        asm.set_areg(funcName + '$' + label)
    else:
        asm.set_areg(label)
    asm.append_lines('0;JMP')


def _set_label(label, funcName):
    if funcName:
        asm.append_lines('(' + funcName + '$' + label + ')')
    else:
        asm.append_lines('(' + label + ')')

def _set_if_goto(label):
    cs.dec_sp()  # SP--
    cs.st_2_dreg()  # A=M, D=A
    asm.set_areg(label)  # A=Label
    asm.append_lines('D;JNE')  # If D != 0; then goto label.
