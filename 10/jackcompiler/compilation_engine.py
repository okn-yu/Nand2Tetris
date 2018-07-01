import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from jackcompiler import jack_tokenizer as jt


class compilationEngine:

    def __init__(self, tXMLTokensList):
        self._read_txmlFile()
        self._rootElement = ET.Element('class')
        self._compile_class()
        self._write_xml()

    def _read_txmlFile(self):
        tree = ET.parse('ArrayTest/MainT.xml')
        self._root = tree.getroot()
        self._index = 0

    def _current_element(self):
        tag = self._root[self._index].tag
        text = self._root[self._index].text.strip()
        return tag, text

    def _next_element(self):
        tag = self._root[self._index + 1].tag
        text = self._root[self._index + 1].text.strip()
        return tag, text

    def _add_xml(self, element):
        tag, text = self._current_element()

        sub = ET.SubElement(element, tag)
        sub.text = ' ' + text + ' '
        self._index += 1

    # def _add_empty_xml(self, element):
    #     tag, text = self._current_element()
    #
    #     sub = ET.SubElement(element, '')
    #     sub.text = ''
    #     # self._index += 1

    def _compile_class(self):

        while True:
            tag, text = self._current_element()
            if text in ['static', 'field']:
                self._compileClassVarDec(self._rootElement)
            elif text in ['constructor', 'function', 'method']:
                self._compileSubroutine(self._rootElement)
            elif text == '}':
                self._add_xml(self._rootElement)
                break
            else:
                self._add_xml(self._rootElement)

    def _compileClassVarDec(self, element):
        pass

    def _compileSubroutine(self, element):
        srDecElement = ET.SubElement(element, 'subroutineDec')
        while True:
            tag, text = self._current_element()
            if text == '(':
                self._add_xml(srDecElement)
                self._compileParameterList(srDecElement)
            elif text == '{':
                self._compileSubroutineBody(srDecElement)
                break
            else:
                self._add_xml(srDecElement)

    def _compileParameterList(self, element):
        paramListElement = ET.SubElement(element, 'parameterList')

    def _compileSubroutineBody(self, element):
        srBodyElement = ET.SubElement(element, 'subroutineBody')
        while True:
            print('body')
            tag, text = self._current_element()
            if text == '{':
                self._add_xml(srBodyElement)
            elif text == 'var':
                self._compileVarDec(srBodyElement)
            # elif text == '}':
            #
            else:
                self._compileStatements(srBodyElement)  # statements
                self._add_xml(srBodyElement)  # '}'
                break

    def _compileVarDec(self, element):
        varDecElement = ET.SubElement(element, 'varDec')
        while True:
            tag, text = self._current_element()
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
            tag, text = self._current_element()
            if text == 'let':
                print('let')
                self._compileLet(varDecElement)
            elif text == 'if':
                print('if')
                self._compileIf(varDecElement)
            elif text == 'while':
                print('while')
                self._compileWhile(varDecElement)
            elif text == 'do':
                print('do')
                self._compileDo(varDecElement)
            elif text == 'return':
                print('return')
                self._compileReturn(varDecElement)
            else:
                print('statements break')
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
            self._add_xml(doElement)  # token: className or varName
            self._add_xml(doElement)  # token: '.'
            self._add_xml(doElement)  # token: subroutineName
            self._add_xml(doElement)  # token: '('
            self._compileExpressionList(doElement)  # token: expressionList
            self._add_xml(doElement)  # token: ')'
            self._add_xml(doElement)  # token: ';'

    def _compileLet(self, element):
        letElement = ET.SubElement(element, 'letStatement')
        while True:
            tag, text = self._current_element()
            if text == 'let':  # token: 'let'
                self._add_xml(letElement)
            elif tag == 'identifier':  # token: 'var'
                self._add_xml(letElement)
            elif text == '[':  # tokens: '[' expression ']'
                self._add_xml(letElement)
                self._compileExpression(letElement)
                self._add_xml(letElement)
            elif text == '=':  # tokens: '=' expression ';'
                self._add_xml(letElement)
                self._compileExpression(letElement)
                self._add_xml(letElement)
                break

    def _compileWhile(self, element):
        print('while')
        whileElement = ET.SubElement(element, 'whileStatement')
        self._add_xml(whileElement)  # token: 'while'
        self._add_xml(whileElement)  # token: '('
        self._compileExpression(whileElement)  # token: expression
        self._add_xml(whileElement)  # token: ')'
        self._add_xml(whileElement)  # token: '{'
        self._compileStatements(whileElement)  # token: statements
        self._add_xml(whileElement)  # token: '}'

    def _compileReturn(self, element):
        print('return')
        returnElement = ET.SubElement(element, 'returnStatement')
        self._add_xml(returnElement)

    def _compileIf(self, element):
        ifElement = ET.SubElement(element, 'ifStatement')
        self._add_xml(ifElement)

    def _compileExpression(self, element):
        expElement = ET.SubElement(element, 'expression')
        tag, text = self._current_element()
        self._compileTerm(expElement)  # token: expression
        print(self._index)
        print(tag, text)
        while True:
            tag, text = self._current_element()
            print(self._index, tag, text)
            if text in ['+', '-', '*', '/', '&amp', '|', '<', '>', '=']:
                print('op')
                self._add_xml(expElement)  # token: op
                self._compileTerm(expElement)  # token: term
            else:
                print('expression break')
                break

    def _compileTerm(self, element):
        termElement = ET.SubElement(element, 'term')
        tag, text = self._current_element()
        if tag == 'integerConstant':  # token: integerConstant
            self._add_xml(termElement)
        elif tag == 'stringConstant':  # token: stringConstant
            self._add_xml(termElement)
        elif text in ['+', '-', '*', '/']:  # token: KeywordConstant
            self._add_xml(termElement)
        elif tag == 'identifier':  # token: varname
            tag, text = self._next_element()
            if text == '[':
                self._add_xml(termElement)  # token: varName
                self._add_xml(termElement)  # token: '['
                self._compileExpression(termElement)  # token: expression
                self._add_xml(termElement)  # token: ']'
            elif text == '(':
                self._add_xml(termElement)  # token: subroutineName
                self._add_xml(termElement)  # token: '('
                self._compileExpressionList(termElement)  # token: expressionList
                self._add_xml(termElement)  # token: ')'
            elif text == '.':
                self._add_xml(termElement)  # token: className or varName
                self._add_xml(termElement)  # token: '.'
                self._add_xml(termElement)  # token: subroutineName
                self._add_xml(termElement)  # token: '('
                self._compileExpressionList(termElement)  # token: expressionList
                self._add_xml(termElement)  # token: ')'
            else:
                self._add_xml(termElement)

    def _compileExpressionList(self, element):
        expListElement = ET.SubElement(element, 'expressionList')
        while True:
            tag, text = self._current_element()
            if text == ',':
                self._add_xml(expListElement)  # token: ','
                self._compileExpression(expListElement)  # token: expression
            else:
                self._compileExpression(expListElement)  # token: expression
                break

    def _edit_xml_string(self):

        pretty_string = minidom.parseString(self._xmlString).toprettyxml(indent='  ')
        self._xmlString = pretty_string.strip('<?xml version="1.0" ?>').strip()

        for line in self._xmlString.split('\n'):
            if '/>' in line:
                shortTag = line
                tagName = line.strip()[1:-2]
                indent = line.split('<')[0]
                startTag = indent + '<' + tagName + '>' + '\n'
                endTag = indent + '</' + tagName + '>'
                self._xmlString = self._xmlString.replace(line, startTag + endTag)

        return self._xmlString

    def _write_xml(self):
        self._xmlString = ET.tostring(self._rootElement, "utf-8", short_empty_elements=False)

        self._edit_xml_string()

        with open('test.xml', 'w') as f:
            f.write(self._xmlString)

        # tree = ET.ElementTree(self._rootElement)
        # tree.write('test.xml', xml_declaration=None, default_namespace=None, method="xml", short_empty_elements=False)
