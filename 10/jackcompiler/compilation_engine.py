import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from jackcompiler import jack_tokenizer as jt


class compilationEngine:

    def __init__(self, tXMLTokensList):
        self._read_txmlFile()
        # self._xmlTokensList = tXMLTokensList[1:-1]

        self._rootElement = ET.Element('class')

        # self._terminalDict = {}
        # self._nonTerminalDict = {}
        # self._tokensList = []
        # self._compiledList = []

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

    def _compile_term(self, element):
        tag, text = self._current_element()

        sub = ET.SubElement(element, tag)
        sub.text = text
        self._index += 1

    def _compile_class(self):

        self._compile_term(self._rootElement)
        self._compile_term(self._rootElement)
        self._compile_term(self._rootElement)

        while True:
            tag, text = self._current_element()
            if text in ['static', 'field']:
                self._compileClassVarDec()
            else:
                break

        while True:
            tag, text = self._current_element()
            if text in ['constructor', 'function', 'method']:
                self._compileSubroutine()
            else:
                break

        self._compile_term(self._rootElement)

        #
        # tag, text = self._current_element()
        # if text == 'static' or 'field':
        #     self._compileClassVarDec()
        #
        # tag, text = self._current_element()
        # if text == 'constructor' or 'function' or 'method':
        #     self._compileSubroutine()

        # self._compile_term()

    def _compileClassVarDec(self):
        pass

    def _compileSubroutine(self):
        subElement = ET.SubElement(self._rootElement, 'subroutineDec')

        self._compile_term(subElement)
        self._compile_term(subElement)
        self._compile_term(subElement)
        self._compile_term(subElement)

        self._compileParameterList(subElement)

        tag, text = self._current_element()
        sub = ET.SubElement(subElement, tag)
        sub.text = text

    def _compileParameterList(self, element):
        subElement = ET.SubElement(element, 'parameterList')
        #subsubElement = ET.SubElement(subElement, 'parameterList')

    def _compileVarDec(self):
        tag, text = self._current_element()

        if text == 'static' or 'field':
            pass
        else:
            pass

    def _compileStatements(self):
        pass

    def _compileDo(self):
        pass

    def _compileLet(self):
        pass

    def _compileWhile(self):
        pass

    def _compileReturn(self):
        pass

    def _compileIf(self):
        pass

    def _compileExpression(self):
        pass

    def _compileTerm(self):
        pass

    def _compileExpressionList(self):
        pass

    def _write_xml(self):
        string = ET.tostring(self._rootElement, 'utf-8')
        pretty_string = minidom.parseString(string).toprettyxml(indent='  ')
        xmlString = pretty_string.strip('<?xml version="1.0" ?>').strip()

        with open('test.xml', 'w') as f:
            f.write(xmlString)
