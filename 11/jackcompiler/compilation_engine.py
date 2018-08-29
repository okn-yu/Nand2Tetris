import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class compilationEngine:

    def __init__(self, txmlFilePath, symbol_table, vm_writer):
        self._txmlFilePath = txmlFilePath
        self._read_txmlFile()
        self._class_xml_element = ET.Element('class')
        self.symbol_table = symbol_table
        self.vm_writer = vm_writer
        self._subroutine_name = ''
        self._subroutine_scope = ''
        self._local_var_count = 0

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

    def _add_parse_tree_xml(self, elm):
        text = self._current_txml_elm().text.strip()
        tag = self._current_txml_elm().tag
        sub = ET.SubElement(elm, tag)
        sub.text = ' ' + text + ' '
        self._current_txml_line_number += 1

    # class tokens:
    # 'class' className '{' classVarDec* subroutineDec* '}'
    def _compile_class(self):

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
            elif self._current_txml_elm().text.strip() in ['constructor', 'function', 'method']:
                self._compileSubroutine(self._class_xml_element)
            else:
                break

        assert self._current_txml_elm().text.strip() == '}'
        self._add_parse_tree_xml(self._class_xml_element)

    # classVarDec tokens:
    # ('static' | 'field') type varName ( ',' varName)* ';'
    def _compileClassVarDec(self, element):
        classVarDecElement = ET.SubElement(element, 'classVarDec')

        # ('static' | 'field') type varName
        kind = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(classVarDecElement)
        type = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(classVarDecElement)
        varName = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(classVarDecElement)
        
        self.symbol_table.define(self._subroutine_scope, kind, type, varName)

        while True:
            # (',' varName) * ';'
            tag, text = self._current_txml_elm()
            if self._current_txml_elm().text.strip() == ',':
                self._add_parse_tree_xml(classVarDecElement)
                self._add_parse_tree_xml(classVarDecElement)
            else:
                self._add_parse_tree_xml(classVarDecElement)
                break

    # subroutine token:
    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subrutineBody
    def _compileSubroutine(self, element):

        srDecElement = ET.SubElement(element, 'subroutineDec')

        assert self._current_txml_elm().text.strip() in ['constructor', 'function', 'method']
        self._add_parse_tree_xml(srDecElement)

        assert self._current_txml_elm().tag in ['identifier', 'keyword']
        self._add_parse_tree_xml(srDecElement)

        assert self._current_txml_elm().tag == 'identifier'
        self._subroutine_name = self._current_txml_elm().text.strip()
        self._subroutine_scope = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(srDecElement)
        self.vm_writer.write_function(self._subroutine_name, self._local_var_count)

        assert self._current_txml_elm().text.strip() == '('
        self._add_parse_tree_xml(srDecElement)

        self._compileParameterList(srDecElement)

        assert self._current_txml_elm().text.strip() == ')'
        self._add_parse_tree_xml(srDecElement)

        self._compileSubroutineBody(srDecElement)

    # ((type varName) (',' type varName)* )?
    def _compileParameterList(self, element):
        paramListElement = ET.SubElement(element, 'parameterList')

        while True:
            # type varName
            if self._current_txml_elm().tag in ['keyword', 'identifier']:
                self._add_parse_tree_xml(paramListElement)  # type
                self._add_parse_tree_xml(paramListElement)  # varName
                self._local_var_count += 1
            # ',' type varName
            elif self._current_txml_elm().text.strip() == ',':
                self._add_parse_tree_xml(paramListElement)  # ','
                self._add_parse_tree_xml(paramListElement)  # type
                self._add_parse_tree_xml(paramListElement)  # varName
                self._local_var_count += 1
            else:
                break

    # subroutineBody tokens:
    # '{' varDec* statements* '}'
    def _compileSubroutineBody(self, element):
        srBodyElement = ET.SubElement(element, 'subroutineBody')

        assert self._current_txml_elm().text.strip() == '{'
        self._add_parse_tree_xml(srBodyElement)

        while True:
            if self._current_txml_elm().text.strip() == 'var':
                self._compileVarDec(srBodyElement)
            elif self._current_txml_elm().text.strip() in ['let', 'if', 'while', 'do', 'return']:
                self._compileStatements(srBodyElement)  # statements
            else:
                break

        assert self._current_txml_elm().text.strip() == '}'
        self._add_parse_tree_xml(srBodyElement)

    # varDec tokens:
    # 'var' type varName ( ',' varName )* ':'
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

        self.symbol_table.define(self._subroutine_name, 'var', type, varName)

        while True:
            if self._current_txml_elm().text.strip() == ',':
                self._add_parse_tree_xml(varDecElement)
                varName = self._current_txml_elm().text.strip()
                self._add_parse_tree_xml(varDecElement)
                self.symbol_table.define(self._subroutine_name, 'var', type, varName)
            else:
                break

        assert self._current_txml_elm().text.strip() == ';'
        self._add_parse_tree_xml(varDecElement)

    # statements tokens:
    # statement*
    def _compileStatements(self, element):
        varDecElement = ET.SubElement(element, 'statements')
        while True:
            text = self._current_txml_elm().text.strip()
            if text == 'let':
                self._compileLet(varDecElement)
            elif text == 'if':
                self._compileIf(varDecElement)
            elif text == 'while':
                self._compileWhile(varDecElement)
            elif text == 'do':
                self._compileDo(varDecElement)
            elif text == 'return':
                self._compileReturn(varDecElement)
            else:
                break

    # doStatement tokens:
    # 'do' subroutineCall ';'
    def _compileDo(self, element):
        doElement = ET.SubElement(element, 'doStatement')
        # 'do'
        self._add_parse_tree_xml(doElement)
        # subroutineCall
        self._compileSubroutineCall(doElement)
        # ';'
        self._add_parse_tree_xml(doElement)

    # subroutineCall tokens:
    # subroutineName '(' expressionList ')' ';' | (className | varName) '.' subroutineName '(' expressionList ')'
    def _compileSubroutineCall(self, element):
        # subroutineName
        if  self._next_txml_elm().text.strip() == '(':
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
        self._add_parse_tree_xml(element)
        self._compileExpressionList(element)
        self._add_parse_tree_xml(element)

        self.vm_writer.write_call(self._subroutine_name)

    # letStatement tokens:
    # 'let' varName ('[' expression ']')? '=' expression ';'
    def _compileLet(self, element):
        letElement = ET.SubElement(element, 'letStatement')

        assert self._current_txml_elm().text.strip() == 'let'
        self._add_parse_tree_xml(letElement)

        assert self._current_txml_elm().tag == 'identifier'
        varName = self._current_txml_elm().text.strip()
        self._add_parse_tree_xml(letElement)

        if self._current_txml_elm().text.strip() == '[':
            self._add_parse_tree_xml(letElement)
            self._compileExpression(letElement)
            self._add_parse_tree_xml(letElement)

        assert self._current_txml_elm().text.strip() == '='
        self._add_parse_tree_xml(letElement)
        self._compileExpression(letElement)

        assert self._current_txml_elm().text.strip() == ';'
        self._add_parse_tree_xml(letElement)

        self._compile_let_var(varName)

    def _compile_let_var(self, varName):

        type = self.symbol_table.type_of(self._subroutine_scope, varName)
        if type == 'Array':
            seg = 'that'
        else:
            seg = 'local'

        count = self.symbol_table.index_of(self._subroutine_scope, varName)
        self.vm_writer.write_pop(seg, count)


    # while statement tokens:
    # 'while' '(' expression ')' '{' statements '}'
    def _compileWhile(self, element):
        whileElement = ET.SubElement(element, 'whileStatement')
        self._add_parse_tree_xml(whileElement)  # 'while'
        self._add_parse_tree_xml(whileElement)  # '('
        self._compileExpression(whileElement)  # expression
        self._add_parse_tree_xml(whileElement)  # ')'
        self._add_parse_tree_xml(whileElement)  # '{'
        self._compileStatements(whileElement)  # statements
        self._add_parse_tree_xml(whileElement)  # '}'

    # return statement tokens:
    # 'return' expression? ';'
    def _compileReturn(self, element):
        returnElement = ET.SubElement(element, 'returnStatement')
        # 'return'
        self._add_parse_tree_xml(returnElement)
        # 'expression?
        if self._current_txml_elm().tag == 'expression':
            self._compileExpression(returnElement)
        else:
            # if void, return 0.
            self.vm_writer.write_push(0)
        # ';'
        self._add_parse_tree_xml(returnElement)
        self.vm_writer.write_return()

    # if statement tokens:
    # 'if' '(' expression ')' '{ statements '}' ( 'else' '{' statements '}' )?
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
    def _compileExpression(self, element):
        expElement = ET.SubElement(element, 'expression')
        # term
        self._compileTerm(expElement)
        # (op term)*
        while True:
            op = self._current_txml_elm().text.strip()
            if  op in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                self._add_parse_tree_xml(expElement)
                self._compileTerm(expElement)
                self.vm_writer.write_arithmetic(op)
            else:
                break

    # term tokens:
    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall |\
    #  '(' expression ')' | unaryOp term
    def _compileTerm(self, element):
        termElement = ET.SubElement(element, 'term')
        text = self._current_txml_elm().text.strip()
        tag = self._current_txml_elm().tag
        # integerConstant
        if tag == 'integerConstant':  
            self._add_parse_tree_xml(termElement)
            self.vm_writer.write_push(int(text))
        # stringConstant
        elif tag == 'stringConstant':  
            self._add_parse_tree_xml(termElement)
            self._compileString(text)
        # KeywordConst
        elif text in ['true', 'false', 'null', 'this']:  
            self._add_parse_tree_xml(termElement)
        # unaryOp term
        elif text in ['-', '~']:
            self._add_parse_tree_xml(termElement) 
            self._compileTerm(termElement)  
        # '(' expression ')'
        elif tag ==  'symbol':
            self._add_parse_tree_xml(termElement)
            self._compileExpression(termElement)
            self._add_parse_tree_xml(termElement)
        elif tag == 'identifier':
            text = self._next_txml_elm().text.strip()
            # varName '[' expression ']'
            if text == '[':
                self._add_parse_tree_xml(termElement)
                self._add_parse_tree_xml(termElement)
                self._compileExpression(termElement)
                self._add_parse_tree_xml(termElement)
            # subroutineCall
            elif text == '(' or text == '.':
                self._compileSubroutineCall(termElement)
            # varName
            else:
                self._add_parse_tree_xml(termElement)

    def _compileString(self, string):

        string = string + ' '

        self.vm_writer.write_push(len(string))
        self.vm_writer.write_call('String.new')

        for char in string:
            self.vm_writer.write_push(ord(char))
            self.vm_writer.write_call('String.appendChar')


    # expressionList tokens:
    # (expression (',' expression)* )?
    def _compileExpressionList(self, element):
        expListElement = ET.SubElement(element, 'expressionList')
        while True:
            text = self._current_txml_elm().text.strip()
            tag = self._current_txml_elm().tag
            if text == ',':
                self._add_parse_tree_xml(expListElement)  # ','
                self._compileExpression(expListElement)  # expression
            elif tag == 'integerConstant' or tag == 'stringConstant' \
                    or text in ['true', 'false', 'null', 'this'] \
                    or text in ['+', '-', '*', '/'] \
                    or tag == 'identifier' \
                    or text in ['-', '~'] \
                    or text in ['(']:
                self._compileExpression(expListElement)  # expression
            else:
                break

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

