from hackcompiler.asm_code import AsmCode as asm


def write_push_pop(command, sgm, index):
    if command == 'push':
        _push(sgm, index)

    elif command == 'pop':
        _pop(sgm, index)


# push処理
# 1. 対象セグメントから値を取得する
# 2. スタックの先頭に値を設定する
# 3. increment SP

def _push(sgm, index):
    if sgm == 'constant':
        _push_constant(index)
        return
    else:
        _push(sgm, index)
        return


def _push_constant(index):
    asm.set_stack(index)
    asm.inc_sp()


def _push(sgm, index):
    asm.set_areg_from_reg('%s' % asm.sgm_2_reg(sgm))
    asm.inc_areg(index)  # Loop: A=A+1
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg_from_reg('SP')  # @SP
    asm.set_sgm_from_dreg()  # M=D
    asm.inc_sp()  # Mem[SP] = Mem[SP] + 1


# pop処理
# 1. decrement SP
# 2. スタックの先頭の値を取得する
# 3. 対象セグメントに値を設定する

def _pop(sgm, index):
    asm.dec_sp()  # Mem[SP] = Mem[SP] - 1
    asm.set_areg_from_sgm()  # A=M
    asm.set_dreg_from_sgm()  # D=M
    asm.set_areg_from_reg('%s' % asm.sgm_2_reg(sgm))
    asm.inc_areg(index)  # Loop: A=A+1
    asm.set_sgm_from_dreg()  # M=D
