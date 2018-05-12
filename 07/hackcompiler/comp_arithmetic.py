from hackcompiler.asm_code import AsmCode as asm


def comp_arithmetic(command):
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


def _comp(jump):
    # jmp Example: 'JEQ', 'JGT', 'JLT'
    asm.dec_sp()
    asm.st_2_dreg()
    asm.dec_sp()
    asm.st_2_areg()
    asm.append_lines('D=M-D')
    asm.set_areg(str(len(asm.asmLines) + 7))  # 1Line  # 7 = 1 + 3 + 1 + 1 + 1
    asm.append_lines('D;' + jump)  # 1Line
    asm.set_bool('FALSE')  # 3Lines
    asm.set_areg(str(len(asm.asmLines) + 5))  # 1Line # 5 = 1 + 3 + 1
    asm.append_lines('0;JMP')  # 1Line
    asm.set_bool('TRUE')  # 3Lines
    asm.inc_sp()


def _unary(compute):
    # compute Example: 'M=-D', 'M=!D''
    asm.dec_sp()
    asm.st_2_dreg()
    asm.append_lines(compute)
    asm.inc_sp()


def _binary(compute):
    # compute Example: 'M=M+D', 'M=M-D', 'M=M&D', 'M=M|D'
    asm.dec_sp()
    asm.st_2_dreg()
    asm.dec_sp()
    asm.st_2_areg()
    asm.append_lines(compute)
    asm.inc_sp()
