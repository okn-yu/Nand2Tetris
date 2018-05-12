from hackcompiler.asm_code import AsmCode as asm


def write_push_pop(command, sgm, index):
    if command == 'push':
        _push(sgm, index)

    elif command == 'pop':
        _pop(sgm, index)


def _push(sgm, index):
    if sgm in ['argument', 'this', 'that', 'local']:
        asm.push(sgm, index)
        return

    if sgm == 'constant':
        asm.push_constant(index)
        return

    if sgm in ['temp', 'pointer']:
        asm.push_temp(sgm, index)
        return


def _pop(sgm, index):
    if sgm in ['argument', 'this', 'that', 'local']:
        asm.pop(sgm, index)
        return

    if sgm in ['temp', 'pointer']:
        asm.pop_temp(sgm, index)
        return
