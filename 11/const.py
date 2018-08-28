OS_FILES = ['Array', 'Keyboard', 'Math', 'Memory', 'Output', 'Screen', 'String', 'Sys']

API_ARG = {
    'Array.new': '1',
    'Keyboard.readInt': '1',
    'Main.double' : '2',
    'Math.multiply' : '2',
    'Math.divide' : '2',
    'Output.printInt': '1',
    'Output.println' : '1',
    'Output.printString': '1',
    'String.new': '1',
    'String.appendChar' : '2',
}

ARITHMETIC_OP_2_CMD = {
    '+' : 'add',
    '-' : 'sub',
    '<' : 'lt',
    '>' : 'gt',
}

VOID_SUBROUTINES = [
    'Output.printInt',
    'Output.printString'
]