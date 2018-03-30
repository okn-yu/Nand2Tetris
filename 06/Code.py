class Code:

    def __init__(self):
        pass

    def dest(cls, destMnemonic):

        if destMnemonic == 'null':
            return '000'

        if destMnemonic == 'M':
            return '001'

        if destMnemonic == 'D':
            return '010'

        if destMnemonic == 'MD':
            return '011'

        if destMnemonic == 'A':
            return '100'

        if destMnemonic == 'AM':
            return '101'

        if destMnemonic == 'AD':
            return '110'

        if destMnemonic == 'AMD':
            return '111'

    @classmethod
    def comp(cls, compMnemonic):

        if compMnemonic == '0':
            return '0101010'

        if compMnemonic == '1':
            return '0111111'

        if compMnemonic == '-1':
            return '0111010'

        if compMnemonic == 'D':
            return '0001100'

        if compMnemonic == 'A':
            return '0110000'

        if compMnemonic == '!D':
            return '0001101'

        if compMnemonic == '!A':
            return '0110000'

        if compMnemonic == '-D':
            return '0001111'

        if compMnemonic == '-A':
            return '0110011'

        if compMnemonic == 'D+1':
            return '0011111'

        if compMnemonic == 'A+1':
            return '0110111'

        if compMnemonic == 'D-1':
            return '0001110'

        if compMnemonic == 'A-1':
            return '0110010'

        if compMnemonic == 'D+A':
            return '0000010'

        if compMnemonic == 'D-A':
            return '0010011'

        if compMnemonic == 'A-D':
            return '0000111'

        if compMnemonic == 'D&A':
            return '0000000'

        if compMnemonic == 'D|A':
            return '0010101'

        if compMnemonic == 'M':
            return '1110000'

        if compMnemonic == '!M':
            return '1110001'

        if compMnemonic == '-M':
            return '1110011'

        if compMnemonic == 'M+1':
            return '1110111'

        if compMnemonic == 'M-1':
            return '1110010'

        if compMnemonic == 'D+M':
            return '1000010'

        if compMnemonic == 'D-M':
            return '1010011'

        if compMnemonic == 'M-D':
            return '1000111'

        if compMnemonic == 'D&M':
            return '1000000'

        if compMnemonic == 'D|M':
            return '1010101'

    @classmethod
    def jump(cls, jumpMnemonic):

        if jumpMnemonic == 'null':
            return '000'

        if jumpMnemonic == 'JGT':
            return '001'

        if jumpMnemonic == 'JEQ':
            return '010'

        if jumpMnemonic == 'JGE':
            return '011'

        if jumpMnemonic == 'JLT':
            return '100'

        if jumpMnemonic == 'JNE':
            return '101'

        if jumpMnemonic == 'JLE':
            return '110'

        if jumpMnemonic == 'JMP':
            return '111'
