import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class compilationEngine:

    def __init__(self, txmlFilePath, symbol_table, vm_writer):
        self._txmlFilePath = txmlFilePath
        self._read_txmlFile()
        self._class_xml_element = ET.Element('class')
        self.symbol_table = symbol_table
        self.vm_writer = vm_writer
        self._compile_class()
        self._write_xml()

    def _read_txmlFile(self):
        tree = ET.parse(self._txmlFilePath)
        self._root_txml_element = tree.getroot()
        self._current_txml_line_number = 0

    def _current_txml_line(self):
        tag = self._root_txml_element[self._current_txml_line_number].tag
        text = self._root_txml_element[self._current_txml_line_number].text.strip()
        return tag, text

    def _next_txml_elm(self):
        tag = self._root_txml_element[self._current_txml_line_number + 1].tag
        text = self._root_txml_element[self._current_txml_line_number + 1].text.strip()
        return tag, text

    def _add_xml(self, elm):
        tag, text = self._current_txml_line()
        sub = ET.SubElement(elm, tag)
        sub.text = ' ' + text + ' '
        self._current_txml_line_number += 1

    # class tokens:
    # 'class' className '{' classVarDec* subroutineDec* '}'
    def _compile_class(self):

        tag, text = self._current_txml_line()
        assert text == 'class'
        self._add_xml(self._class_xml_element)

        tag, text = self._current_txml_line()
        assert tag == 'identifier'
        self._className = text
        self._add_xml(self._class_xml_element)

        tag, text = self._current_txml_line()
        assert text == '{'
        self._add_xml(self._class_xml_element)


        while True:
            tag, text = self._current_txml_line()
            if text in ['static', 'field']:
                self._compileClassVarDec(self._class_xml_element)
            elif text in ['constructor', 'function', 'method']:
                self._compileSubroutine(self._class_xml_element)
            else:
                break

        tag, text = self._current_txml_line()
        assert text == '}'
        self._add_xml(self._class_xml_element)

    # classVarDec tokens:
    # ('static' | 'field') type varName ( ',' varName)* ';'
    def _compileClassVarDec(self, element):
        classVarDecElement = ET.SubElement(element, 'classVarDec')

        tag, text = self._current_txml_line()
        assert text == 'static' or text == 'field'
        # ('static' | 'field') type varName
        kind = text
        self._add_xml(classVarDecElement)
        tag, text = self._current_txml_line()
        type = text
        self._add_xml(classVarDecElement)
        tag, text = self._current_txml_line()
        varName = text
        self._add_xml(classVarDecElement)
        
        self.symbol_table.define(kind, type, varName)

        while True:
            # (',' varName) * ';'
            tag, text = self._current_txml_line()
            if text == ',':
                self._add_xml(classVarDecElement)
                self._add_xml(classVarDecElement)
            elif text == ';':
                self._add_xml(classVarDecElement)
                break

    # subroutine token:
    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subrutineBody
    def _compileSubroutine(self, element):

        self._subroutine_name = ''
        self._local_var_count = 0

        srDecElement = ET.SubElement(element, 'subroutineDec')

        tag, text = self._current_txml_line()
        assert text in ['constructor', 'function', 'method']
        self._add_xml(srDecElement)

        tag, text = self._current_txml_line()
        assert tag == 'identifier' or tag == 'keyword'
        self._add_xml(srDecElement)

        tag, text = self._current_txml_line()
        assert tag == 'identifier'
        self._subroutine_name = text
        self._add_xml(srDecElement)
        self.vm_writer.write_function(self._subroutine_name, self._local_var_count)

        tag, text = self._current_txml_line()
        assert text == '('
        self._add_xml(srDecElement)

        self._compileParameterList(srDecElement)

        tag, text = self._current_txml_line()
        assert text == ')'
        self._add_xml(srDecElement)

        self._compileSubroutineBody(srDecElement)

    # ((type varName) (',' type varName)* )?
    def _compileParameterList(self, element):
        paramListElement = ET.SubElement(element, 'parameterList')

        while True:
            tag, text = self._current_txml_line()
            if text in ['int', 'char', 'boolean'] or type == 'identifier':
                self._add_xml(paramListElement)  # type
                self._add_xml(paramListElement)  # varName
                self._local_var_count += 1
            elif text == ',':
                self._add_xml(paramListElement)  # ','
                self._add_xml(paramListElement)  # type
                self._add_xml(paramListElement)  # varName
                self._local_var_count += 1
            else:
                break

    # subroutineBody tokens:
    # '{' varDec* statements* '}'
    def _compileSubroutineBody(self, element):
        srBodyElement = ET.SubElement(element, 'subroutineBody')
        while True:
            tag, text = self._current_txml_line()
            if text == '{':
                self._add_xml(srBodyElement)
            elif text == 'var':
                self._compileVarDec(srBodyElement)
            else:
                self._compileStatements(srBodyElement)  # statements
                self._add_xml(srBodyElement)  # '}'
                break

    # varDec tokens:
    # 'var' type typeName '(' ',' varName ')'* ':'
    def _compileVarDec(self, element):
        varDecElement = ET.SubElement(element, 'varDec')
        while True:
            tag, text = self._current_txml_line()
            if text == ',':
                self._add_xml(varDecElement)
                self._add_xml(varDecElement)
            elif text == ';':
                self._add_xml(varDecElement)
                break
            else:
                self._add_xml(varDecElement)

    # statements tokens:
    # statement*
    def _compileStatements(self, element):
        varDecElement = ET.SubElement(element, 'statements')
        while True:
            tag, text = self._current_txml_line()
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
        self._add_xml(doElement)
        # subroutineCall
        self._compileSubroutineCall(doElement)
        # ';'
        self._add_xml(doElement)

    # subroutineCall tokens:
    # subroutineName '(' expressionList ')' ';' | (className | varName) '.' subroutineName '(' expressionList ')'
    def _compileSubroutineCall(self, element):
        tag, text = self._next_txml_elm()
        # subroutineCall
        if text == '(':
            # subroutineName
            tag, text = self._current_txml_line()
            self._subroutine_name = text
            self._add_xml(element)
        else:
            # className or varName '.' subroutineName
            tag, text = self._current_txml_line()
            self._subroutine_name = text
            self._add_xml(element)  # className or varName
            self._add_xml(element)  # '.'
            tag, text = self._current_txml_line()
            self._subroutine_name += '.' + text
            self._add_xml(element)  # subroutineName

        # '(' expressionList ')' ';'
        self._add_xml(element)  # '('
        self._compileExpressionList(element)  # token: expressionList
        self._add_xml(element)  # ')'

        self.vm_writer.write_call(self._subroutine_name)

    # letStatement tokens:
    # 'let' varName ('[' expression ']')? '=' expression ';'
    def _compileLet(self, element):
        letElement = ET.SubElement(element, 'letStatement')
        while True:
            tag, text = self._current_txml_line()
            if text == 'let':  # 'let'
                self._add_xml(letElement)
            elif tag == 'identifier':  # 'var'
                self._add_xml(letElement)
            elif text == '[':  # '[' expression ']'
                self._add_xml(letElement)
                self._compileExpression(letElement)
                self._add_xml(letElement)
            elif text == '=':  # '=' expression ';'
                self._add_xml(letElement)
                self._compileExpression(letElement)
                self._add_xml(letElement)
                break

    # while statement tokens:
    # 'while' '(' expression ')' '{' statements '}'
    def _compileWhile(self, element):
        whileElement = ET.SubElement(element, 'whileStatement')
        self._add_xml(whileElement)  # 'while'
        self._add_xml(whileElement)  # '('
        self._compileExpression(whileElement)  # expression
        self._add_xml(whileElement)  # ')'
        self._add_xml(whileElement)  # '{'
        self._compileStatements(whileElement)  # statements
        self._add_xml(whileElement)  # '}'

    # return statement tokens:
    # 'return' expression? ';'
    def _compileReturn(self, element):
        returnElement = ET.SubElement(element, 'returnStatement')
        # 'return'
        self._add_xml(returnElement)
        # 'expression?
        tag, text = self._current_txml_line()
        if tag == 'expression':
            self._compileExpression(returnElement)
        else:
            # if void, return 0.
            self.vm_writer.write_push(0)
        # ';'
        self._add_xml(returnElement)
        self.vm_writer.write_return()

    # if statement tokens:
    # 'if' '(' expression ')' '{ statements '}' ( 'else' '{' statements '}' )?
    def _compileIf(self, element):
        ifElement = ET.SubElement(element, 'ifStatement')
        tag, text = self._current_txml_line()
        self._add_xml(ifElement)  # 'if'
        self._add_xml(ifElement)  # '('
        self._compileExpression(ifElement)  # expression
        self._add_xml(ifElement)  # ')'
        self._add_xml(ifElement)  # '{'
        self._compileStatements(ifElement)  # statements
        self._add_xml(ifElement)  # '}'
        while True:
            tag, text = self._current_txml_line()
            if text == 'else':
                self._add_xml(ifElement)  # 'else'
                self._add_xml(ifElement)  # '{'
                self._compileStatements(ifElement)  # statements
                self._add_xml(ifElement)  # '}'
            else:
                break

    # expression tokens:
    # term (op term)*
    def _compileExpression(self, element):
        expElement = ET.SubElement(element, 'expression')
        # term
        tag, text = self._current_txml_line()
        self._compileTerm(expElement)
        while True:
            tag, text = self._current_txml_line()
            if text in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                # op
                self._add_xml(expElement)
                # term
                self._compileTerm(expElement)
                self.vm_writer.write_arithmetic(text)
            else:
                break

    # term tokens:
    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall |\
    #  '(' expression ')' | unaryOp term
    def _compileTerm(self, element):
        termElement = ET.SubElement(element, 'term')
        tag, text = self._current_txml_line()
        # integerConstant
        if tag == 'integerConstant':  
            self._add_xml(termElement)
            self.vm_writer.write_push(int(text))
        # stringConstant
        elif tag == 'stringConstant':  
            self._add_xml(termElement)
            self._compileString(text)
        # KeywordConst
        elif text in ['true', 'false', 'null', 'this']:  
            self._add_xml(termElement)
        # unaryOp term
        elif text in ['-', '~']:
            self._add_xml(termElement) 
            self._compileTerm(termElement)  
        # '(' expression ')'
        elif tag ==  'symbol':
            self._add_xml(termElement)
            self._compileExpression(termElement)
            self._add_xml(termElement)
        elif tag == 'identifier':
            tag, text = self._next_txml_elm()
            # varName '[' expression ']'
            if text == '[':
                self._add_xml(termElement)
                self._add_xml(termElement)
                self._compileExpression(termElement)
                self._add_xml(termElement)
            # subroutineCall
            elif text == '(' or text == '.':
                self._compileSubroutineCall(termElement)
            # varName
            else:
                self._add_xml(termElement)

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
            tag, text = self._current_txml_line()
            if text == ',':
                self._add_xml(expListElement)  # ','
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

