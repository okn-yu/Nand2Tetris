import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


class compilationEngine:

    def __init__(self, txmlFilePath):
        self._txmlFilePath = txmlFilePath
        self._read_txmlFile()
        self._root_xml_element = ET.Element('class')
        self._current_element = self._root_xml_element
        self._compile_class()
        self._write_xml()

    def _read_txmlFile(self):
        tree = ET.parse(self._txmlFilePath)
        self._root_txml_element = tree.getroot()
        self._txml_line_number = 0

    def _txml_line(self):
        tag = self._root_txml_element[self._txml_line_number].tag
        text = self._root_txml_element[self._txml_line_number].text.strip()
        return tag, text

    def _next_element(self):
        tag = self._root_txml_element[self._txml_line_number + 1].tag
        text = self._root_txml_element[self._txml_line_number + 1].text.strip()
        return tag, text

    def _add_xml(self, elm):
        tag, text = self._txml_line()
        sub = ET.SubElement(elm, tag)
        sub.text = ' ' + text + ' '
        self._txml_line_number += 1

    # class tokens:
    # 'class' className '{' classVarDec* subroutineDec* '}'
    def _compile_class(self):

        while True:
            tag, text = self._txml_line()
            if text in ['static', 'field']:
                self._compileClassVarDec(self._root_xml_element)
            elif text in ['constructor', 'function', 'method']:
                self._compileSubroutine(self._root_xml_element)
            elif text == '}':
                self._add_xml(self._root_xml_element)
                break
            else:
                self._add_xml(self._root_xml_element)

    # class tokens:
    # 'class' className '{' classVarDec* subroutineDec* '}'
    def _compileClassVarDec(self, element):
        classVarDecElement = ET.SubElement(element, 'classVarDec')
        while True:
            tag, text = self._txml_line()
            if text == 'static' or text == 'field':
                self._add_xml(classVarDecElement)  # 'static' or 'field'
                self._add_xml(classVarDecElement)  # type
                self._add_xml(classVarDecElement)  # varName
            elif text == ',':
                self._add_xml(classVarDecElement)  # ','
                self._add_xml(classVarDecElement)  # varName
            elif text == ';':
                self._add_xml(classVarDecElement)  # ';'
                break

    def _compileSubroutine(self, element):
        srDecElement = ET.SubElement(element, 'subroutineDec')
        while True:
            tag, text = self._txml_line()
            if text == '(':
                self._add_xml(srDecElement)  # '('
                self._compileParameterList(srDecElement)  # parameterList
            elif text == '{':
                self._compileSubroutineBody(srDecElement)  # subroutineBody
                break
            else:
                self._add_xml(srDecElement)

    def _compileParameterList(self, element):
        paramListElement = ET.SubElement(element, 'parameterList')
        while True:
            tag, text = self._txml_line()
            if text in ['int', 'char', 'boolean'] or type == 'identifier':
                self._add_xml(paramListElement)  # type
                self._add_xml(paramListElement)  # varName
            elif text == ',':
                self._add_xml(paramListElement)  # ','
                self._add_xml(paramListElement)  # type
                self._add_xml(paramListElement)  # varName
            else:
                break

    def _compileSubroutineBody(self, element):
        srBodyElement = ET.SubElement(element, 'subroutineBody')
        while True:
            tag, text = self._txml_line()
            if text == '{':
                self._add_xml(srBodyElement)
            elif text == 'var':
                self._compileVarDec(srBodyElement)
            else:
                self._compileStatements(srBodyElement)  # statements
                self._add_xml(srBodyElement)  # '}'
                break

    def _compileVarDec(self, element):
        varDecElement = ET.SubElement(element, 'varDec')
        while True:
            tag, text = self._txml_line()
            if text == ',':
                self._add_xml(varDecElement)
                self._add_xml(varDecElement)
            elif text == ';':
                self._add_xml(varDecElement)
                break
            else:
                self._add_xml(varDecElement)

    def _compileStatements(self, element):
        varDecElement = ET.SubElement(element, 'statements')
        while True:
            tag, text = self._txml_line()
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

    def _compileDo(self, element):
        doElement = ET.SubElement(element, 'doStatement')
        self._add_xml(doElement)  # 'do'
        nextTag, nextText = self._next_element()
        if nextText == '(':
            self._add_xml(doElement)  # subroutineName
            self._add_xml(doElement)  # '('
            self._compileExpressionList(doElement)  # expressionList
            self._add_xml(doElement)  # ')'
            self._add_xml(doElement)  # ';'
        else:
            self._add_xml(doElement)  # className or varName
            self._add_xml(doElement)  # '.'
            self._add_xml(doElement)  # subroutineName
            self._add_xml(doElement)  # '('
            self._compileExpressionList(doElement)  # token: expressionList
            self._add_xml(doElement)  # ')'
            self._add_xml(doElement)  # ';'

    def _compileLet(self, element):
        letElement = ET.SubElement(element, 'letStatement')
        while True:
            tag, text = self._txml_line()
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

    def _compileWhile(self, element):
        whileElement = ET.SubElement(element, 'whileStatement')
        self._add_xml(whileElement)  # 'while'
        self._add_xml(whileElement)  # '('
        self._compileExpression(whileElement)  # expression
        self._add_xml(whileElement)  # ')'
        self._add_xml(whileElement)  # '{'
        self._compileStatements(whileElement)  # statements
        self._add_xml(whileElement)  # '}'

    def _compileReturn(self, element):
        returnElement = ET.SubElement(element, 'returnStatement')
        while True:
            tag, text = self._txml_line()
            if text == 'return':
                self._add_xml(returnElement)  # 'return'
            elif text == ';':
                self._add_xml(returnElement)  # ';'
                break
            else:
                self._compileExpression(returnElement)  # expression

    def _compileIf(self, element):
        ifElement = ET.SubElement(element, 'ifStatement')
        tag, text = self._txml_line()
        self._add_xml(ifElement)  # 'if'
        self._add_xml(ifElement)  # '('
        self._compileExpression(ifElement)  # expression
        self._add_xml(ifElement)  # ')'
        self._add_xml(ifElement)  # '{'
        self._compileStatements(ifElement)  # statements
        self._add_xml(ifElement)  # '}'
        while True:
            tag, text = self._txml_line()
            if text == 'else':
                self._add_xml(ifElement)  # 'else'
                self._add_xml(ifElement)  # '{'
                self._compileStatements(ifElement)  # statements
                self._add_xml(ifElement)  # '}'
            else:
                break

    def _compileExpression(self, element):
        expElement = ET.SubElement(element, 'expression')
        tag, text = self._txml_line()
        self._compileTerm(expElement)  # term
        while True:
            tag, text = self._txml_line()
            if text in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                self._add_xml(expElement)  # op
                self._compileTerm(expElement)  # term
            else:
                break

    def _compileTerm(self, element):
        termElement = ET.SubElement(element, 'term')
        tag, text = self._txml_line()
        if tag == 'integerConstant':  # integerConstant
            self._add_xml(termElement)
        elif tag == 'stringConstant':  # stringConstant
            self._add_xml(termElement)
        elif text in ['true', 'false', 'null', 'this']:  # KeywordConstant
            self._add_xml(termElement)
        elif text in ['-', '~']:
            self._add_xml(termElement)  # unary OP
            self._compileTerm(termElement)  # term
        elif tag == 'symbol':
            self._add_xml(termElement)  # '('
            self._compileExpression(termElement)  # expression
            self._add_xml(termElement)  # ')'
        elif tag == 'identifier':  # varname
            tag, text = self._next_element()
            if text == '[':
                self._add_xml(termElement)  # varName
                self._add_xml(termElement)  # '['
                self._compileExpression(termElement)  # expression
                self._add_xml(termElement)  # ']'
            elif text == '(':
                self._add_xml(termElement)  # subroutineName
                self._add_xml(termElement)  # '('
                self._compileExpressionList(termElement)  # expressionList
                self._add_xml(termElement)  # ')'
            elif text == '.':
                self._add_xml(termElement)  # className or varName
                self._add_xml(termElement)  # '.'
                self._add_xml(termElement)  # subroutineName
                self._add_xml(termElement)  # '('
                self._compileExpressionList(termElement)  # expressionList
                self._add_xml(termElement)  # ')'
            else:
                self._add_xml(termElement)  # varName

    def _compileExpressionList(self, element):
        expListElement = ET.SubElement(element, 'expressionList')
        while True:
            tag, text = self._txml_line()
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
        self._xmlString = ET.tostring(self._root_xml_element, "utf-8", short_empty_elements=False)
        self._edit_xml_string()

        outDirPath = self._txmlFilePath.split('/')[0]  # ex: ArrayTest/MyMainT.xml -> ArrayTest
        outFileName = self._txmlFilePath.split('/')[1].split('.')[0][0:-1]  # ex: ArrayTest/MyMainT.xml -> MyMain
        outFilePath = outDirPath + '/' + outFileName + '.xml'  # ex: ArrayTest/MyMain2.xml

        with open(outFilePath, 'w') as f:
            f.write(self._xmlString)
