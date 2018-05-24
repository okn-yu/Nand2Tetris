from hackcompiler.asm_code import AsmCode as asm
from hackcompiler import comp_stack as cs

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
    asm.set_label(fName)
    asm.init_locals(nLocals)


def _return():
    # FLAME=*LCL
    asm.set_areg('LCL')  # @LCL
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg('FRAME')  # @FRAME
    asm.set_sgm_from_dreg()  # M=D

    # RET=*(FRAME-5)
    # TODO: This shoud be implemented next!

    # *ARG=pop()
    asm.dec_sp()  # Mem[SP] = Mem[SP] - 1
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

    asm.set_return_segment('THAT', 1)  # THAT=*(FRAME-1)
    asm.set_return_segment('THIS', 2)  # THIS=*(FRAME-2)
    asm.set_return_segment('ARG', 3)  # ARG=*(FRAME-3)
    asm.set_return_segment('LCL', 4)  # LCL=*(FRAME-4)

    # goto RET
    asm.set_return()  # TODO: This shold be implemented next!

def _call(fName, nArgs):
    cs._push('LCL', 0)
    cs._push('ARG', 0)
    cs._push('THIS', 0)
    cs._push('THAT', 0)

    asm.set_goto(fName)
