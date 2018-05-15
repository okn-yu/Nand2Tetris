from hackcompiler.asm_code import AsmCode as asm


def write_label(label):
    asm.set_label(label)
    return


def write_goto(label):
    asm.set_goto(label)
    return


def write_if(label):
    asm.set_if(label)
    return
