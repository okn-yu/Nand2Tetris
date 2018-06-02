from hackcompiler.asm_code import AsmCode as asm
from hackcompiler import comp_stack as cs
from hackcompiler import prog_flow as pf

fNameTable = {}


def write_function(fName, nLocals):
    _function(fName, nLocals)
    return


def write_return():
    _return()
    return


def write_call(arg1, arg2):
    _call(arg1, arg2)
    return


def _function(fName, nLocals):
    pf.write_label(fName, None)
    _init_locals(nLocals)


def _return():
    # FLAME=*LCL
    asm.set_areg('LCL')  # @LCL
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg('FRAME')  # @FRAME
    asm.set_sgm_from_dreg()  # M=D

    # RET=*(FRAME-5)
    _set_return()

    # *ARG=pop()
    cs.dec_sp()  # Mem[SP] = Mem[SP] - 1
    asm.set_areg_from_sgm()  # A=M
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg('ARG')  # @ARG
    asm.set_areg_from_sgm()  # A=M
    asm.set_sgm_from_dreg()  # M=D

    # SP=ARG+1
    asm.set_areg('ARG')  # @ARG
    asm.set_dreg_from_sgm()  # D=M
    asm.append_lines('D=D+1')  # D=D+1
    asm.set_areg('SP')  # @SP
    asm.set_sgm_from_dreg()  # M=D

    _set_return_segment('THAT', 1)  # THAT=*(FRAME-1)
    _set_return_segment('THIS', 2)  # THIS=*(FRAME-2)
    _set_return_segment('ARG', 3)  # ARG=*(FRAME-3)
    _set_return_segment('LCL', 4)  # LCL=*(FRAME-4)

    # GOTO RET.
    asm.set_areg('RETURN')  # @RETURN
    asm.set_areg_from_sgm()  # A=M
    asm.append_lines('0;JMP')


def _set_return_segment(seg, index):  # seg=*(FRAME-index)
    asm.set_areg('FRAME')  # @FRAME
    asm.set_areg_from_sgm()  # A=M
    asm.dec_areg(index)  # A=A-index
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg(seg)  # @seg
    asm.set_sgm_from_dreg()  # M=D


def _set_return():
    asm.set_areg('FRAME')  # @FRAME
    asm.set_areg_from_sgm()  # A=M
    asm.dec_areg(5)  # A=A-5
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg('RETURN')  # @RETURN
    asm.set_sgm_from_dreg()  # M=D


def _call(fName, nArgs):
    # Push RETURN-ADDRESS.
    # cs.set_stack(fName + '$' + 'retAddr')
    _push_return_addr(fName)

    _save_register('LCL')  # Push LCL.
    _save_register('ARG')  # Push ARG.
    _save_register('THIS')  # Push THIS.
    _save_register('THAT')  # Push  TAHT.

    # ARG=SP-n-5
    asm.set_areg('SP')  # @SP
    asm.set_dreg_from_sgm()  # D=M
    index = int(nArgs) + 5
    asm.dec_dreg(str(index))
    asm.set_areg('ARG')  # @
    asm.set_sgm_from_dreg()  # M=D

    # LCL=SP
    asm.set_areg('SP')  # @SP
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg('LCL')  # @LCL
    asm.set_sgm_from_dreg()  # M=D

    pf.write_goto(fName, None)  # Goto Function.

    # SET Label
    # pf.write_label('retAddr', fName)
    _wrie_return_addr_label(fName)


def _push_return_addr(fName):
    if fName in fNameTable:
        fNameTable[fName] += 1
    else:
        fNameTable[fName] = 1

    num = fNameTable[fName]
    cs.set_stack(fName + '$' + 'retAddr' + '-' + str(num))


def _wrie_return_addr_label(fName):
    num = fNameTable[fName]
    pf.write_label('retAddr' + '-' + str(num) , fName )


def _save_register(reg):
    asm.set_areg(reg)  # @reg
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg_from_reg('SP')  # @SP, A=M
    asm.set_sgm_from_dreg()  # M=D
    cs.inc_sp()  # Mem[SP] = Mem[SP] + 1


def _init_locals(nLocals):
    for i in range(int(nLocals)):
        cs.set_stack('0')
