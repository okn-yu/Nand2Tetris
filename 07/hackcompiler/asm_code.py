class AsmCode:
    asmLines = []

    # push処理
    # 1. 対象セグメントから値を取得する //セグメント依存
    # 2. スタックの先頭に値を設定する　//共通処理
    # 3. increment SP　//共通処理

    @classmethod
    def push_constant(cls, value):
        AsmCode.set_stack(value)
        AsmCode.inc_sp()

    @classmethod
    def push_from_base_addr(cls, sgm, index):
        AsmCode.set_areg_from_reg('%s' % AsmCode.sgm_2_reg(sgm))  # @Register, A=M
        AsmCode.inc_areg(index)  # Loop: A=A+1
        AsmCode.set_dreg_from_sgm()  # d=M
        AsmCode.set_areg_from_reg('SP')  # @SP
        AsmCode.set_sgm_from_dreg()  # M=D
        AsmCode.inc_sp()  # Mem[SP] = Mem[SP] + 1

    @classmethod
    def push(cls, sgm, index):
        AsmCode.set_areg('%s' % AsmCode.sgm_2_reg(sgm))  # @Register
        AsmCode.inc_areg(index)  # Loop: A=A+1
        AsmCode.set_dreg_from_sgm()  # d=M
        AsmCode.set_areg_from_reg('SP')  # @SP
        AsmCode.set_sgm_from_dreg()  # M=D
        AsmCode.inc_sp()  # Mem[SP] = Mem[SP] + 1

    # pop処理
    # 1. decrement SP //共通処理
    # 2. スタックの先頭の値を取得する　//Dレジスタに値を設定する
    # 3. 対象セグメントに値を設定する //Aレジスタに値を設定する

    @classmethod
    def pop_from_base_addr(cls, sgm, index):
        AsmCode.dec_sp()  # Mem[SP] = Mem[SP] =1
        AsmCode.set_areg_from_sgm()  # A=M
        AsmCode.set_dreg_from_sgm()  # D=M
        AsmCode.set_areg_from_reg('%s' % AsmCode.sgm_2_reg(sgm))  # @Register, A=M
        AsmCode.inc_areg(index)  # Loop: A=A+1
        AsmCode.set_sgm_from_dreg()  # M=D

    @classmethod
    def pop(cls, sgm, index):
        AsmCode.dec_sp()  # A=Mem[SP]
        AsmCode.set_areg_from_sgm()  # A=M
        AsmCode.set_dreg_from_sgm()  # D=M
        AsmCode.set_areg('%s' % AsmCode.sgm_2_reg(sgm))  # @Register
        AsmCode.inc_areg(index)  # Loop: A=A+1
        AsmCode.set_sgm_from_dreg()  # M=D

    ### Handle SP. ###

    @classmethod
    def dec_sp(cls):
        AsmCode.append_lines('@SP', 'M=M-1')

    @classmethod
    def inc_sp(cls):
        AsmCode.append_lines('@SP', 'M=M+1')

    @classmethod
    def st_2_dreg(cls):
        AsmCode.append_lines('@SP', 'A=M', 'D=M')

    @classmethod
    def st_2_areg(cls):
        AsmCode.append_lines('@SP', 'A=M')

    ### Handle A/D reg. ###

    @classmethod
    def set_dreg(cls, value):
        AsmCode.append_lines('@%s' % value, 'D=A')

    @classmethod
    def set_dreg_from_sgm(cls):
        AsmCode.append_lines('D=M')

    @classmethod
    def set_sgm_from_dreg(cls):
        AsmCode.append_lines('M=D')

    @classmethod
    def set_areg(cls, value):
        AsmCode.append_lines('@%s' % value)

    @classmethod
    def set_areg_from_sgm(cls):
        AsmCode.append_lines('A=M')

    @classmethod
    def set_areg_from_reg(cls, value):
        AsmCode.set_areg(value)
        AsmCode.set_areg_from_sgm()

    @classmethod
    def inc_areg(cls, index):
        for i in range(int(index)):
            AsmCode.append_lines('A=A+1')

    ### Handle Virtual Regsiters. ###

    @classmethod
    def _init_vsgm(cls):
        # for UT.
        AsmCode.set_vreg(value='256', reg='SP')
        AsmCode.set_vreg(value='300', reg='LCL')
        AsmCode.set_vreg(value='400', reg='ARG')
        # AsmCode.set_vreg(value='3000', reg='THIS')
        # AsmCode.set_vreg(value='3010', reg='THAT')

    @classmethod
    def set_vreg(cls, value, reg):
        AsmCode.set_dreg(value)
        AsmCode.set_areg(reg)
        AsmCode.set_sgm_from_dreg()

    ### Handle Stack sgm. ###

    @classmethod
    def set_stack(cls, value):
        AsmCode.set_dreg(value)
        AsmCode.set_areg('SP')
        AsmCode.set_areg_from_sgm()
        AsmCode.set_sgm_from_dreg()

    ### Other methods. ###

    @classmethod
    def set_bool(cls, bool):
        AsmCode.set_areg('SP')
        AsmCode.set_areg_from_sgm()

        if bool == 'TRUE':
            AsmCode.append_lines('M=-1')
        elif bool == 'FALSE':
            AsmCode.append_lines('M=0')

    @classmethod
    def sgm_2_reg(cls, sgm):
        if sgm == 'local':
            return 'LCL'
        elif sgm == 'argument':
            return 'ARG'
        elif sgm == 'this':
            return 'THIS'
        elif sgm == 'that':
            return 'THAT'
        elif sgm == 'temp':
            return 'R5'
        elif sgm == 'pointer':
            return 'THIS'
        # static segment begins from 16.
        elif sgm == 'static':
            return '16'
        else:
            return None

    @classmethod
    def append_lines(cls, *strings):
        for string in strings:
            AsmCode.asmLines.append(string)
