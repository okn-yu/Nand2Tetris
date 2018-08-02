import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

OS_FILES = ['Array', 'Keyboard', 'Math', 'Memory', 'Output', 'Screen', 'String', 'Sys']


class VMWriter:

    def __init__(self, xmlFilePath):

        print('VMWriter:' + xmlFilePath)

        self._xmlFilePath = xmlFilePath
        self._fileName = ''

        self._get_fileName()

        self._read_txmlFile()
        self._compile_class()
        # self._write_file()

    def _read_txmlFile(self):

        tree = ET.parse(self._xmlFilePath)
        self._root = tree.getroot()

    def _get_fileName(self):

        if '/' in self._xmlFilePath:
            self._fileName = self._xmlFilePath.split('/')[-1]
        else:
            self._fileName = self._xmlFilePath

    # class tokens:
    # 'class' className '{' classVarDec* subroutineDec* '}'
    def _compile_class(self):

        iter_tree = self._root.iter()
        classElm = next(iter_tree)
        assert classElm.tag == 'class'

        print('start compile_class')

        for child_tree in classElm:
            if child_tree.tag == 'identifier':
                self.className = child_tree.text.strip()
            if child_tree.tag == 'classVarDec':
                ClassVarDec(child_tree)
            if child_tree.tag == 'subroutineDec':
                Subroutine(child_tree, self.className)

        print('end compile_class')


class ClassVarDec:

    def __init__(self, tree):
        pass

    # classVarDec tokens.
    # ( 'static' | 'field' ) type varName ( ',' varName )* ';'
    def _compile_class_var_dec(self):
        pass


class Subroutine:

    def __init__(self, tree, fileName):

        self._vmLines = []
        self._fileName = fileName
        self._subroutineName = ''
        self._localVarCount = 0

        self._compile_subroutine_dec(tree)

        self._write_file()

    # subroutine token:
    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subrutineBody
    def _compile_subroutine_dec(self, tree):

        print('start compile_subroutine_dec')

        iter_tree = tree.iter()
        # print(tree) # <Element 'subroutineDec' at 0x10fd59e58>
        # print(next(iter_tree)) # <Element 'subroutineDec' at 0x10fd59e58>

        subroutineElm = next(iter_tree)
        assert subroutineElm.tag == 'subroutineDec'

        kwElm = next(iter_tree)
        assert kwElm.text.strip() in ['constructor', 'function', 'method']

        kwElm = next(iter_tree)
        assert kwElm.tag == 'keyword'

        subroutineNameElm = next(iter_tree)
        assert subroutineNameElm.tag == 'identifier'

        symElm = next(iter_tree)
        assert symElm.text.strip() == '('

        paramListElm = next(iter_tree)
        assert paramListElm.tag == 'parameterList'

        symElm = next(iter_tree)
        assert symElm.text.strip() == ')'

        subroutineBodyElm = next(iter_tree)
        assert subroutineBodyElm.tag == 'subroutineBody'

        self._subroutineName = subroutineNameElm.text.strip()
        self._compile_parameter_list(paramListElm)
        self._compile_subroutine_body(subroutineBodyElm)

    def _compile_parameter_list(self, tree):
        pass

    # subroutineBody tokens:
    # '{' varDec* statements* '}'
    def _compile_subroutine_body(self, tree):
        print('compile_subroutine_body')

        for child_tree in tree:
            tag, text = child_tree.tag, child_tree.text.strip()

            if tag == 'varDec':
                self._compile_var_dec(child_tree)

            if tag == 'statements':
                self._compile_statements(child_tree)

    # varDec tokens:
    # 'var' type typeName '(' ',' varName ')'* ':'
    def _compile_var_dec(self, tree):
        print('compile_var_dec')

        self._localVarCount += 1

        for child_tree in tree:
            text = child_tree.tag, child_tree.text.strip()
            if text == ',':
                self._localVarCount += 1

    # statements tokens:
    # statement*
    def _compile_statements(self, tree):
        print('compile_statements')

        for child_tree in tree:
            tag, text = child_tree.tag, child_tree.text.strip()
            if tag == 'doStatement':
                self._compile_do_statement(child_tree)

    # doStatement tokens:
    # 'do' subroutineCall ';'
    def _compile_do_statement(self, tree):
        print('compile_do_statement')

        iter_tree = tree.iter()

        doStatementElm = next(iter_tree)
        assert doStatementElm.tag == 'doStatement'

        doElm = next(iter_tree)
        assert doElm.text.strip() == 'do'

        self._compile_subroutine_call(iter_tree)

    # subroutineCall tokens:
    # subroutineName '(' expressionList ')' ';' | (className | varName) '.' subroutineName '(' expressionList ')' ';'
    def _compile_subroutine_call(self, iter_tree):
        print('compile_subroutine_call')

        calleeName = next(iter_tree).text.strip()
        symbol = next(iter_tree).text.strip()

        if symbol == '(':
            self._write_call(calleeName)
        elif symbol == '.':
            calleeName += symbol
            calleeName += next(iter_tree).text.strip()
            self._write_call(calleeName)
            next(iter_tree)

        expressionListElm = next(iter_tree)
        assert expressionListElm.tag == 'expressionList'
        self._compile_expression_list(expressionListElm)

    # expressionList tokens:
    # (expression (',' expression)* )?
    def _compile_expression_list(self, tree):
        print('start compile_expression_list')

        print(tree)

        for child_tree in tree:
            tag, text = child_tree.tag, child_tree.text.strip()

            if tag == 'expression':
                self._compile_expression(child_tree)

        print('end compile_expression_list')

    # expression tokens:
    # term (op term)*
    def _compile_expression(self, tree):
        print('start compile_expression')

        termList = []
        opList = []

        for child_tree in tree:
            if child_tree.tag == 'term':
                termList.append(child_tree)

            elif child_tree.tag == 'symbol':
                opList.append(child_tree)

        print('termList: %s' % termList)
        for term in termList:
            self._compile_term(term)

        print('opList: %s' % opList)
        for op in reversed(opList):
            self._compile_op(op)

        print('end compile_expression')

    def _compile_op(self, tree):
        print('start compile_op')

        operator = tree.text.strip()
        print('operator: %s' % operator)
        assert operator in ['+', '-', '*', '/']

        self._write_arithmetic(operator)

        print('end compile_op')

    # symbol tokens:
    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall |\
    #  '(' expression ')' | unaryOp term
    def _compile_term(self, tree):
        print('start compile_term')
        print('term: %s' % tree)

        # in case of 'term' 'symbol' 'term'
        for child_tree in tree:
            tag, text = child_tree.tag, child_tree.text.strip()
            # print(tag, text)

            if tag == 'integerConstant':
                print('integer: %s' % text)
                self._write_push('constant', text)

            elif tag == 'stringConstant':
                self._write_push('constant', text)

            elif tag == 'expression':
                self._compile_expression(child_tree)

        print('end compile_term')

    def _write_push(self, type, var):

        self._vmLines.append('push' + ' ' + type + ' ' + var)

    def _write_pop(self):
        pass

    def _write_arithmetic(self, operator):

        if operator == '+':
            self._vmLines.append('add')

        elif operator == '*':
            self._vmLines.append('mult')

    def _write_label(self):
        pass

    def _write_goto(self):
        pass

    def _write_if(self):
        pass

    def _write_call(self, calleeName):
        self._vmLines.append('call' + ' ' + calleeName)

    def _write_function(self):
        self._vmLines.insert(0, (
                'function' + ' ' + self._fileName + '.' + self._subroutineName + ' ' + str(self._localVarCount)))

    def _write_return(self):
        self._vmLines.append('return')

    def _write_file(self):

        self._write_function()
        self._write_return()

        with open('test.vm', 'w') as f:
            for line in self._vmLines:
                f.write(line + '\n')
