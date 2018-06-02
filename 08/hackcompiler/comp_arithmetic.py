from hackcompiler.asm_code import AsmCode as asm
from hackcompiler import comp_stack as cs


def write_arithmetic(command):
    if command == 'neg':
        return _unary('M=-D')

    if command == 'not':
        return _unary('M=!D')

    if command == 'add':
        return _binary('M=M+D')

    if command == 'sub':
        return _binary('M=M-D')

    if command == 'and':
        return _binary('M=M&D')

    if command == 'or':
        return _binary('M=M|D')

    if command == 'eq':
        return _comp('JEQ')

    if command == 'lt':
        return _comp('JLT')

    if command == 'gt':
        return _comp('JGT')


def _comp(jump): # TODO use Label!
    # jmp Example: 'JEQ', 'JGT', 'JLT'
    cs.dec_sp()
    cs.st_2_dreg()
    cs.dec_sp()
    cs.st_2_areg()
    asm.append_lines('D=M-D')
    #asm.set_areg(str(len(asm.asmLines) + 7))  # 1Line  # 7 = 1 + 3 + 1 + 1 + 1
    asm.set_areg(str(_count_unlabeld_line() + 7))
    asm.append_lines('D;' + jump)  # 1Line
    _set_bool('FALSE')  # 3Lines
    #asm.set_areg(str(len(asm.asmLines) + 5))  # 1Line # 5 = 1 + 3 + 1
    asm.set_areg(str(_count_unlabeld_line() + 5))
    asm.append_lines('0;JMP')  # 1Line
    _set_bool('TRUE')  # 3Lines
    cs.inc_sp()
    return

def _count_unlabeld_line():

    count = 0

    for line in asm.asmLines:
        if line[0] == '(' and line[-1] == ')':
            pass
        else:
            count += 1

    return count

def _unary(compute):
    # compute Example: 'M=-D', 'M=!D''
    cs.dec_sp()
    cs.st_2_dreg()
    asm.append_lines(compute)
    cs.inc_sp()
    return


def _binary(compute):
    # compute Example: 'M=M+D', 'M=M-D', 'M=M&D', 'M=M|D'
    cs.dec_sp()
    cs.st_2_dreg()
    cs.dec_sp()
    cs.st_2_areg()
    asm.append_lines(compute)
    cs.inc_sp()
    return


def _set_bool(bool):
    asm.set_areg('SP')
    asm.set_areg_from_sgm()

    if bool == 'TRUE':
        asm.append_lines('M=-1')
    elif bool == 'FALSE':
        asm.append_lines('M=0')