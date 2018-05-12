from hackcompiler.asm_code import AsmCode as asm


def write_push_pop(command, sgm, index):
    if command == 'push':
        _push(sgm, index)

    elif command == 'pop':
        _pop(sgm, index)


def _push(sgm, index):
    if sgm in ['argument', 'this', 'that', 'local']:
        asm.push_from_base_addr(sgm, index)
        return

    if sgm == 'constant':
        asm.push_constant(index)
        return

    if sgm in ['temp', 'pointer', 'static']:
        asm.push(sgm, index)
        return


def _pop(sgm, index):
    if sgm in ['argument', 'this', 'that', 'local']:
        asm.pop_from_base_addr(sgm, index)
        return

    if sgm in ['temp', 'pointer', 'static']:
        asm.pop(sgm, index)
        return
