OS_FILES = ['Array', 'Keyboard', 'Math', 'Memory', 'Output', 'Screen', 'String', 'Sys']

API_ARG = {
    'Array.new': '1',
    'Keyboard.readInt': '1',
    'Main.double' : '1',
    'Main.fill': '2',
    'Main.convert' : '1',
    'Main.nextMask' : '1',
    'Main.fillMemory' : '3',
    'Math.multiply' : '2',
    'Math.divide' : '2',
    'Memory.peek' : '1',
    'Memory.poke' : '2',
    'Output.printInt': '1',
    'Output.println' : '0',
    'Output.printString': '1',
    'String.new': '1',
    'String.appendChar' : '2',
}

ARITHMETIC_OP_2_CMD = {
    '+' : 'add',
    '-' : 'sub',
    '<' : 'lt',
    '>' : 'gt',
    '=' : 'eq',
    '&' : 'and'
}

VOID_SUBROUTINES = [
    'Output.printInt',
    'Output.printString'
]