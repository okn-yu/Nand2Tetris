class AsmCode:
    asmLines = []

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
    def set_areg_from_reg(cls, reg):
        if reg in ['ARG', 'THIS', 'THAT', 'LCL', 'SP']:
            AsmCode.set_areg(reg)
            AsmCode.set_areg_from_sgm()
        else:
            AsmCode.set_areg(reg)

    @classmethod
    def inc_areg(cls, index):
        for i in range(int(index)):
            AsmCode.append_lines('A=A+1')

    @classmethod
    def dec_areg(cls, index):
        for i in range(int(index)):
            AsmCode.append_lines('A=A-1')

    @classmethod
    def dec_dreg(cls, index):
        for i in range(int(index)):
            AsmCode.append_lines('D=D-1')

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

    ### Handle Label. ###

    @classmethod
    def set_goto(cls, label):
        AsmCode.set_areg(label)
        AsmCode.append_lines('0;JMP')

    @classmethod
    def set_label(cls, label):
        AsmCode.append_lines('(' + label + ')')

    @classmethod
    def set_if(cls, label):
        AsmCode.dec_sp()  # SP--
        AsmCode.st_2_dreg()  # A=M, D=A
        AsmCode.set_goto(label)  # A=Label
        AsmCode.append_lines('D;JGT')  # If D=0; then goto label.

    ### Handle Function. ###

    @classmethod
    def init_locals(cls, nLocals):
        for i in nLocals:
            AsmCode.set_stack('0')
            AsmCode.inc_sp()

    @classmethod
    def set_return_segment(cls, seg, index):  # seg=*(FRAME-index)
        AsmCode.set_areg('FRAME')  # @FRAME
        AsmCode.set_areg_from_sgm()  # A=M
        AsmCode.dec_areg(index)  # A=A-index
        AsmCode.set_dreg_from_sgm()  # D=M
        AsmCode.set_areg(seg)  # @seg
        AsmCode.set_sgm_from_dreg()  # M=D

    @classmethod
    def set_return(cls):
        AsmCode.set_areg('FRAME')  # @FRAME
        AsmCode.set_areg_from_sgm()  # A=M
        AsmCode.dec_areg(5)  # A=A-5
        AsmCode.set_areg_from_sgm()  # A=M

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
        # pointer segment begins from RAM[3](=THIS).
        elif sgm == 'pointer':
            return '3'
        # static segment begins from RAM[16].
        elif sgm == 'static':
            return '16'
        else:
            return None

    @classmethod
    def append_lines(cls, *strings):
        for string in strings:
            AsmCode.asmLines.append(string)
