from hackcompiler.asm_code import AsmCode as asm


def write_push_pop(command, sgm, index):
    if command == 'push':
        _push(sgm, index)

    elif command == 'pop':
        _pop(sgm, index)


def _push(sgm, index):
    if sgm == 'constant':
        asm.push_constant(index)
        return
    else:
        asm.push(sgm, index)
        return


def _pop(sgm, index):
    asm.pop(sgm, index)
    return
