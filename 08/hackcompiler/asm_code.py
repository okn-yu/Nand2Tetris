class AsmCode:
    asmLines = []

    ### Handle A/D reg. ###

    @classmethod
    def set_dreg(cls, value):
        AsmCode.append_lines('@%s' % value, 'D=A')

    @classmethod
    def set_dreg_from_sgm(cls):
        AsmCode.append_lines('D=M')

    @classmethod
    def set_dreg_from_areg(cls):
        AsmCode.append_lines('D=A')

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
            AsmCode.set_areg(reg)   # @REG
            AsmCode.set_areg_from_sgm() # A=M
        else:
            AsmCode.set_areg(reg)   # A=M

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

    ### Other methods. ###

    @classmethod
    def _init_vsgm(cls):
        pass
        # AsmCode.set_vreg(value='261', reg='SP')
        # AsmCode.set_vreg(value='300', reg='LCL')
        # AsmCode.set_vreg(value='400', reg='ARG')

    @classmethod
    def set_vreg(cls, value, reg):
        AsmCode.set_dreg(value)
        AsmCode.set_areg(reg)
        AsmCode.set_sgm_from_dreg()

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
