import inspect
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# TODO: judge expression by method!
# TODO: modify call symtable!

class compilationEngine:

    def __init__(self, txmlFilePath, symbol_table, vm_writer):
        self._txmlFilePath = txmlFilePath
        self._read_txmlFile()
        self._class_xml_element = ET.Element('class')
        self.symbol_table = symbol_table
        self.vm_writer = vm_writer
        self._subroutine_name = ''
        self.label_count = 0

        self.vm_writer.crear_vm_file()
        self._compile_class()
        self._write_xml()

    def _read_txmlFile(self):
        tree = ET.parse(self._txmlFilePath)
        self._root_txml_element = tree.getroot()
        self._current_txml_line_number = 0

    def _current_txml_elm(self):
        return self._root_txml_element[self._current_txml_line_number]

    def _next_txml_elm(self):
        return self._root_txml_element[self._current_txml_line_number + 1]

    def debug(func):

        def _indent(stack, indent=''):
            for i in range(0, len(stack)):
                indent += ' '
            return indent

        def _argument(self):

            args_line = []

            for i in range(self._current_txml_line_number, len(self._root_txml_element)):
                # args_line.append(i)
                args_line.append(self._root_txml_element[i].text.strip())

            if len(args_line) > 20:
                return args_line[0:20]
            else:
                return args_line

        def wrapper(self, *args, **kwargs):
            print(_indent(inspect.stack()) + 'start %s:' % func.__name__)
            print(_indent(inspect.stack()), _argument(self))
            returnValue = func(self, *args, **kwargs)
            print(_indent(inspect.stack()) + 'end %s ' % func.__name__)
            return returnValue

        return wrapper

    def _add_parse_tree_xml(self, elm):
        text = self._current_txml_elm().text.strip()
        tag = self._current_txml_elm().tag
        sub = ET.SubElement(elm, tag)
        sub.text = ' ' + text + ' '
        self._current_txml_line_number += 1

    def _tokens(self):

        indent = ''
        args_line = []

        for i in range(0, len(inspect.stack())):
            indent += ' '

        for i in range(self._current_txml_line_number, len(self._root_txml_element)):
            args_line.append(i)
            args_line.append(self._root_txml_element[i].text.strip())

    # class tokens:
    # 'class' className '{' classVarDec* subroutineDec* '}'
    @debug
    def _compile_class(self):
        self._tokens()

        assert self._current_txml_elm().text.strip() == 'class'
        self._add_parse_tree_xml(self._class_xml_element)

        assert self._current_txml_elm().tag == 'identifier'
        self._className = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(self._class_xml_element)

        assert self._current_txml_elm().text.strip() == '{'
        self._add_parse_tree_xml(self._class_xml_element)

        while True:
            if self._current_txml_elm().text.strip() in ['static', 'field']:
                self._compileClassVarDec(self._class_xml_element)
            else:
                break

        while True:
            if self._current_txml_elm().text.strip() in ['constructor', 'function', 'method']:
                self._compileSubroutine(self._class_xml_element)
            else:
                break

        assert self._current_txml_elm().text.strip() == '}'
        self._add_parse_tree_xml(self._class_xml_element)

    # classVarDec tokens:
    # ('static' | 'field') type varName ( ',' varName)* ';'
    @debug
    def _compileClassVarDec(self, element):
        classVarDecElement = ET.SubElement(element, 'classVarDec')

        # ('static' | 'field') type varName
        kind = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(classVarDecElement)

        type = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(classVarDecElement)

        varName = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(classVarDecElement)

        self.symbol_table.define(varName, kind, type)

        while True:
            # (',' varName) * ';'
            text = self._current_txml_elm().text.strip()
            if  text == ',':
                self._add_parse_tree_xml(classVarDecElement)
                varName =  self._current_txml_elm().text.strip()
                self._add_parse_tree_xml(classVarDecElement)
                self.symbol_table.define(varName, kind, type)
            else:
                break

        assert self._current_txml_elm().text.strip()  == ';'
        self._add_parse_tree_xml(classVarDecElement)

    # subroutine token:
    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subrutineBody
    @debug
    def _compileSubroutine(self, element):

        srDecElement = ET.SubElement(element, 'subroutineDec')

        assert self._current_txml_elm().text.strip() in ['constructor', 'function', 'method']
        self._add_parse_tree_xml(srDecElement)

        assert self._current_txml_elm().tag in ['identifier', 'keyword']
        self._add_parse_tree_xml(srDecElement)

        assert self._current_txml_elm().tag == 'identifier'
        self._subroutine_name = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(srDecElement)

        assert self._current_txml_elm().text.strip() == '('
        self._add_parse_tree_xml(srDecElement)

        self._compileParameterList(srDecElement)

        assert self._current_txml_elm().text.strip() == ')'
        self._add_parse_tree_xml(srDecElement)

        self._compileSubroutineBody(srDecElement)

    # ((type varName) (',' type varName)* )?
    @debug
    def _compileParameterList(self, element):
        paramListElement = ET.SubElement(element, 'parameterList')

        while True:
            # type varName
            if self._current_txml_elm().tag in ['keyword', 'identifier']:

                kind = 'arg'
                type = self._current_txml_elm().text.strip()
                self._add_parse_tree_xml(paramListElement)  # type

                varName = self._current_txml_elm().text.strip()
                self._add_parse_tree_xml(paramListElement)  # varName

                self.symbol_table.define(varName, kind, type)

            # ',' type varName
            elif self._current_txml_elm().text.strip() == ',':
                kind = 'arg'

                self._add_parse_tree_xml(paramListElement)  # ','
                type = self._current_txml_elm().text.strip()

                self._add_parse_tree_xml(paramListElement)  # type
                varName = self._current_txml_elm().text.strip()

                self._add_parse_tree_xml(paramListElement)  # varName

                self.symbol_table.define(varName, kind, type)

            else:
                break

    # subroutineBody tokens:
    # '{' varDec* statements* '}'
    @debug
    def _compileSubroutineBody(self, element):
        srBodyElement = ET.SubElement(element, 'subroutineBody')

        assert self._current_txml_elm().text.strip() == '{'
        self._add_parse_tree_xml(srBodyElement)

        self._local_var_count = 0

        while True:
            # varDec
            if self._current_txml_elm().text.strip() == 'var':
                self._compileVarDec(srBodyElement)
            else:
                break

        self.vm_writer.write_function(self._subroutine_name, self.symbol_table.var_count('var'))

        while True:
            # statements
            if self._current_txml_elm().text.strip() in ['let', 'if', 'while', 'do', 'return']:
                self._compileStatements(srBodyElement)
            else:
                break

        assert self._current_txml_elm().text.strip() == '}'
        self._add_parse_tree_xml(srBodyElement)

    # varDec tokens:
    # 'var' type varName ( ',' varName )* ':'
    @debug
    def _compileVarDec(self, element):
        varDecElement = ET.SubElement(element, 'varDec')

        assert self._current_txml_elm().text.strip() == 'var'
        self._add_parse_tree_xml(varDecElement)

        assert self._current_txml_elm().tag in ['keyword', 'identifier']
        type = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(varDecElement)

        assert self._current_txml_elm().tag == 'identifier'
        varName = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(varDecElement)

        self.symbol_table.define(varName, 'var', type)

        while True:
            if self._current_txml_elm().text.strip() == ',':
                self._add_parse_tree_xml(varDecElement)
                varName = self._current_txml_elm().text.strip()
                self._add_parse_tree_xml(varDecElement)
                self.symbol_table.define(varName, 'var', type)
            else:
                break

        assert self._current_txml_elm().text.strip() == ';'
        self._add_parse_tree_xml(varDecElement)

    # statements tokens:
    # statement*
    @debug
    def _compileStatements(self, element):
        self._tokens()

        statementsElement = ET.SubElement(element, 'statements')
        while True:
            text = self._current_txml_elm().text.strip()
            if text == 'let':
                self._compileLet(statementsElement)
            elif text == 'if':
                self._compileIf(statementsElement)
            elif text == 'while':
                self._compileWhile(statementsElement)
            elif text == 'do':
                self._compileDo(statementsElement)
            elif text == 'return':
                self._compileReturn(statementsElement)
            else:
                break

    # doStatement tokens:
    # 'do' subroutineCall ';'
    @debug
    def _compileDo(self, element):
        doElement = ET.SubElement(element, 'doStatement')
        # 'do'
        self._add_parse_tree_xml(doElement)
        # subroutineCall
        self._compileSubroutineCall(doElement)
        # ';'
        self._add_parse_tree_xml(doElement)

    # subroutineCall tokens:
    # subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
    @debug
    def _compileSubroutineCall(self, element):
        # subroutineName
        if self._next_txml_elm().text.strip() == '(':
            self._subroutine_name = self._current_txml_elm().text.strip()
            self._add_parse_tree_xml(element)
        # className or varName '.' subroutineName
        elif self._next_txml_elm().text.strip() == '.':
            self._subroutine_name = self._current_txml_elm().text.strip()
            self._add_parse_tree_xml(element)
            self._add_parse_tree_xml(element)
            self._subroutine_name += '.' + self._current_txml_elm().text.strip()
            self._add_parse_tree_xml(element)
        else:
            raise SyntaxError

        # '(' expressionList ')' ';'
        assert self._current_txml_elm().text.strip() == '('
        self._add_parse_tree_xml(element)

        self._compileExpressionList(element)

        assert self._current_txml_elm().text.strip() == ')'
        self._add_parse_tree_xml(element)

        self.vm_writer.write_call(self._subroutine_name)

    # letStatement tokens:
    # 'let' varName ('[' expression ']')? '=' expression ';'
    @debug
    def _compileLet(self, element):
        self._tokens()
        letElement = ET.SubElement(element, 'letStatement')

        let_statement_with_array = False

        assert self._current_txml_elm().text.strip() == 'let'
        self._add_parse_tree_xml(letElement)

        assert self._current_txml_elm().tag == 'identifier'
        varName = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(letElement)

        if self._current_txml_elm().text.strip() == '[':
            let_statement_with_array = True
            self.vm_writer.write_push(self._var_seg(varName), self._var_index(varName))
            self._add_parse_tree_xml(letElement)
            self._compileExpression(letElement)
            self._add_parse_tree_xml(letElement)
            self.vm_writer.write_arithmetic('+')
            # self.vm_writer.write_pop('pointer', 1)
            self.vm_writer.write_pop('temp', 0)


        assert self._current_txml_elm().text.strip() == '='
        self._add_parse_tree_xml(letElement)

        self._compileExpression(letElement)

        assert self._current_txml_elm().text.strip() == ';'
        self._add_parse_tree_xml(letElement)

        # substitution
        if let_statement_with_array:
            self.vm_writer.write_push('temp', 0)
            self.vm_writer.write_pop('pointer', 1)
            self.vm_writer.write_pop('that', 0)
        else:
            self.vm_writer.write_pop(self._var_seg(varName), self._var_index(varName))

    # while statement tokens:
    # 'while' '(' expression ')' '{' statements '}'
    @debug
    def _compileWhile(self, element):
        whileElement = ET.SubElement(element, 'whileStatement')

        assert self._current_txml_elm().text.strip() == 'while'
        self._add_parse_tree_xml(whileElement)

        self.vm_writer.write_label('WHILE_EXP', self.label_count)

        assert self._current_txml_elm().text.strip() == '('
        self._add_parse_tree_xml(whileElement)

        self._compileExpression(whileElement)

        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if('WHILE_END', self.label_count)

        assert self._current_txml_elm().text.strip() == ')'
        self._add_parse_tree_xml(whileElement)

        assert self._current_txml_elm().text.strip() == '{'
        self._add_parse_tree_xml(whileElement)

        self._compileStatements(whileElement)

        self.vm_writer.write_goto('WHILE_EXP', self.label_count)
        self.vm_writer.write_label('WHILE_END', self.label_count)

        assert self._current_txml_elm().text.strip() == '}'
        self._add_parse_tree_xml(whileElement)

        self.label_count += 1

    # return statement tokens:
    # 'return' expression? ';'
    @debug
    def _compileReturn(self, element):
        returnElement = ET.SubElement(element, 'returnStatement')
        # 'return'
        self._add_parse_tree_xml(returnElement)

        text = self._current_txml_elm().text.strip()
        tag =  self._current_txml_elm().tag
        # 'expression?
        if tag == 'integerConstant' or tag == 'stringConstant' \
            or text in ['true', 'false', 'null', 'this'] \
            or text in ['+', '-', '*', '/'] \
            or tag == 'identifier' \
            or text in ['-', '~'] \
            or text in ['(']:
            self._compileExpression(returnElement)
        else:
            # if void, return 0.
            self.vm_writer.write_push('constant', 0)
        # ';'
        self._add_parse_tree_xml(returnElement)
        self.vm_writer.write_return()

    # if statement tokens:
    # 'if' '(' expression ')' '{ statements '}' ( 'else' '{' statements '}' )?
    @debug
    def _compileIf(self, element):
        ifElement = ET.SubElement(element, 'ifStatement')
        self._add_parse_tree_xml(ifElement)  # 'if'
        self._add_parse_tree_xml(ifElement)  # '('
        self._compileExpression(ifElement)  # expression
        self._add_parse_tree_xml(ifElement)  # ')'
        self._add_parse_tree_xml(ifElement)  # '{'
        self._compileStatements(ifElement)  # statements
        self._add_parse_tree_xml(ifElement)  # '}'

        if self._current_txml_elm().text.strip() == 'else':
            self._add_parse_tree_xml(ifElement)  # 'else'
            self._add_parse_tree_xml(ifElement)  # '{'
            self._compileStatements(ifElement)  # statements
            self._add_parse_tree_xml(ifElement)  # '}'

    # expression tokens:
    # term (op term)*
    @debug
    def _compileExpression(self, element):
        expElement = ET.SubElement(element, 'expression')
        # term
        self._compileTerm(expElement)
        # (op term)*
        while True:
            op = self._current_txml_elm().text.strip()
            if op in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                self._add_parse_tree_xml(expElement)
                self._compileTerm(expElement)
                self.vm_writer.write_arithmetic(op)
            else:
                break

    # term tokens:
    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall |\
    #  '(' expression ')' | unaryOp term
    @debug
    def _compileTerm(self, element):
        termElement = ET.SubElement(element, 'term')
        text = self._current_txml_elm().text.strip()
        tag = self._current_txml_elm().tag
        # integerConstant
        if tag == 'integerConstant':
            self._add_parse_tree_xml(termElement)
            self.vm_writer.write_push('constant', int(text))
        # stringConstant
        elif tag == 'stringConstant':
            self._add_parse_tree_xml(termElement)
            self._compileString(text)
        # KeywordConst
        elif text in ['true', 'false', 'null', 'this']:
            self._add_parse_tree_xml(termElement)
            if text in ['null', 'false']:
                self.vm_writer.write_push('constant', 0)
            if text == 'true':
                self.vm_writer.write_push('constant', 1)
                self.vm_writer.write_arithmetic('neg')
        # unaryOp term
        elif text in ['-', '~']:
            self._add_parse_tree_xml(termElement)
            self._compileTerm(termElement)
            # '(' expression ')'
        elif tag == 'symbol':
            self._add_parse_tree_xml(termElement)
            self._compileExpression(termElement)
            self._add_parse_tree_xml(termElement)
        elif tag == 'identifier':
            next_text = self._next_txml_elm().text.strip()
            # varName '[' expression ']'
            if next_text == '[':
                varName = text
                self._add_parse_tree_xml(termElement)
                self.vm_writer.write_push(self._var_seg(varName), self._var_index(varName))
                self._add_parse_tree_xml(termElement)
                self._compileExpression(termElement)
                self.vm_writer.write_arithmetic('+')
                self._add_parse_tree_xml(termElement)
                self.vm_writer.write_pop('pointer', 1)
                self.vm_writer.write_push('that', 0)

            # subroutineCall
            elif next_text in ['(', '.']:
                self._compileSubroutineCall(termElement)
            # varName
            else:
                self._add_parse_tree_xml(termElement)
                self.vm_writer.write_push(self._var_seg(text), self._var_index(text))

    def _compileString(self, string):

        string = string + ' '

        self.vm_writer.write_push('constant', len(string))
        self.vm_writer.write_call('String.new')

        for char in string:
            self.vm_writer.write_push('constant', ord(char))
            self.vm_writer.write_call('String.appendChar')

    # expressionList tokens:
    # (expression (',' expression )* )?
    @debug
    def _compileExpressionList(self, element):
        expListElement = ET.SubElement(element, 'expressionList')
        while True:
            text = self._current_txml_elm().text.strip()
            tag = self._current_txml_elm().tag
            if text == ',':
                self._add_parse_tree_xml(expListElement)
                self._compileExpression(expListElement)
            # expression
            elif tag == 'integerConstant' or tag == 'stringConstant' \
                    or text in ['true', 'false', 'null', 'this'] \
                    or text in ['+', '-', '*', '/'] \
                    or tag == 'identifier' \
                    or text in ['-', '~'] \
                    or text in ['(']:
                self._compileExpression(expListElement)
            else:
                break

    def _var_seg(self, var):
        kind =  self.symbol_table.kind_of(var)

        if kind == 'var':
            return 'local'
        elif kind == 'arg':
            return 'argument'
        elif kind == 'field':
            return  ''
        else:
            raise SyntaxError

    def _var_index(self, var):
        return self.symbol_table.index_of(var)

    def _edit_xml_string(self):
        pretty_string = minidom.parseString(self._xmlString).toprettyxml(indent='  ')
        self._xmlString = pretty_string.strip('<?xml version="1.0" ?>').strip()

        for line in self._xmlString.split('\n'):
            if '/>' in line:
                tagName = line.strip()[1:-2]
                indent = line.split('<')[0]
                startTag = indent + '<' + tagName + '>' + '\n'
                endTag = indent + '</' + tagName + '>'
                self._xmlString = self._xmlString.replace(line, startTag + endTag)

    def _write_xml(self):
        self._xmlString = ET.tostring(self._class_xml_element, "utf-8", short_empty_elements=False)
        self._edit_xml_string()

        outDirPath = self._txmlFilePath.split('/')[0]  # ex: ArrayTest/MyMainT.xml -> ArrayTest
        outFileName = self._txmlFilePath.split('/')[1].split('.')[0][0:-1]  # ex: ArrayTest/MyMainT.xml -> MyMain
        outFilePath = outDirPath + '/' + outFileName + '.xml'  # ex: ArrayTest/MyMain.xml

        with open(outFilePath, 'w') as f:
            f.write(self._xmlString)

