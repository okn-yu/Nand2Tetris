from hackcompiler.asm_code import AsmCode as asm


def write_push_pop(command, sgm, index):
    if command == 'push':
        _push_command(sgm, index)
    elif command == 'pop':
        _pop_command(sgm, index)
    else:
        # Raise Exception.
        pass


# push処理
# 1. 対象セグメントから値を取得する
# 2. スタックの先頭に値を設定する
# 3. increment SP

def _push_command(sgm, index):
    if sgm == 'constant':
        _push_constant(index)
        return
    else:
        _push(sgm, index)
        return


def _push_constant(index):
    set_stack(index)


def _push(sgm, index):
    asm.set_areg_from_reg('%s' % asm.sgm_2_reg(sgm))  # @REGISTER, A=M
    asm.inc_areg(index)  # Loop: A=A+1
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg_from_reg('SP')  # @SP, A=M
    asm.set_sgm_from_dreg()  # M=D
    inc_sp()  # Mem[SP] = Mem[SP] + 1


# pop処理
# 1. decrement SP
# 2. スタックの先頭の値を取得する
# 3. 対象セグメントに値を設定する


def _pop_command(sgm, index):
    if sgm in ['local', 'argument', 'this', 'that']:
        _pop_2_pointed_mem(sgm, index)
    else:
        _pop_2_mem(sgm, index)


def _pop_2_pointed_mem(sgm, index):
    dec_sp()  # Mem[SP] = Mem[SP] - 1
    asm.set_areg_from_sgm()  # A=M
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg('%s' % asm.sgm_2_reg(sgm))  # @reg
    asm.set_areg_from_sgm()  # A=M
    asm.inc_areg(index)  # Loop: A=A+1
    asm.set_sgm_from_dreg()  # M=D


def _pop_2_mem(sgm, index):
    dec_sp()  # Mem[SP] = Mem[SP] - 1
    asm.set_areg_from_sgm()  # A=M
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg('%s' % asm.sgm_2_reg(sgm))  # @reg
    asm.inc_areg(index)  # Loop: A=A+1
    asm.set_sgm_from_dreg()  # M=D


def set_stack(value):
    asm.set_dreg(value)
    asm.set_areg('SP')
    asm.set_areg_from_sgm()  # A=M
    asm.set_sgm_from_dreg()  # M=D
    inc_sp()


def dec_sp():
    asm.append_lines('@SP', 'M=M-1')


def inc_sp():
    asm.append_lines('@SP', 'M=M+1')


def st_2_dreg():
    asm.append_lines('@SP', 'A=M', 'D=M')


def st_2_areg():
    asm.append_lines('@SP', 'A=M')
