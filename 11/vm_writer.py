import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

import const
import symbol_table as st

# TODO: modify 'elm' -> 'topElm'

class VMWriter:

    def __init__(self, xmlFile):

        print('VMWriter:' + xmlFile)

        self._xmlFile = xmlFile     # ex. Seven/Main.xml
        self._fileName = ''         # ex. Main.xml
        self._filePath = ''         # ex. Seven
        self._className = ''        # ex. main

        self._symbolTable = st.SymbolTable(xmlFile)
        self._vmLines = []
        self._subroutineName = ''
        self._localVarCount = 0

        self._label_count = 0

        self._cutoff_fileName()
        self._cutoff_filePath()
        self._read_txmlFile()

        self._parse_xmlFile()
        self._write_file()

    def _cutoff_fileName(self):

        if '/' in self._xmlFile:
            self._fileName = self._xmlFile.split('/')[-1]
        else:
            self._fileName = self._xmlFile

    def _cutoff_filePath(self):

        if '/' in self._xmlFile:
            self._filePath = self._xmlFile.split('/')[0] + '/'

    def _read_txmlFile(self):

        elm = ET.parse(self._xmlFile)
        self._root = elm.getroot()

    def deco(func):
        def wrapper(*args, **kwargs):
            print('start %s ' % func.__name__)
            func(*args, **kwargs)
            print('end %s ' % func.__name__)

        return wrapper

    def _parse_xmlFile(self):

        assert self._root.tag == 'class'
        self._parse_class_elm()

    # class tokens:
    # 'class' className '{' classVarDec* subroutineDec* '}'
    @deco
    def _parse_class_elm(self):

        classElm = iter(self._root)
        assert next(classElm).text.strip() == 'class'

        classNameElm = next(classElm)
        assert classNameElm.tag == 'identifier'
        self._className = classNameElm.text.strip()

        print('start compile_class')

        for childElm in classElm:
            if childElm.tag == 'classVarDec':
                self._parse_class_var_dec_elm(childElm)
            if childElm.tag == 'subroutineDec':
                self._parse_subroutine_dec_elm(childElm)

        print('end compile_class')

    def _parse_class_var_dec_elm(self, elm):
        pass

    # subroutine token:
    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subrutineBody
    def _parse_subroutine_dec_elm(self, elm):

        print('start compile_subroutine_dec')

        iter_elm = iter(elm)

        kwElm = next(iter_elm)
        assert kwElm.text.strip() in ['constructor', 'function', 'method']

        kwElm = next(iter_elm)
        assert kwElm.tag == 'keyword'

        subroutineNameElm = next(iter_elm)
        assert subroutineNameElm.tag == 'identifier'

        symElm = next(iter_elm)
        assert symElm.text.strip() == '('

        paramListElm = next(iter_elm)
        assert paramListElm.tag == 'parameterList'

        symElm = next(iter_elm)
        assert symElm.text.strip() == ')'

        subroutineBodyElm = next(iter_elm)
        assert subroutineBodyElm.tag == 'subroutineBody'

        self._subroutineName = subroutineNameElm.text.strip()
        self._parse_parameter_list_elm(paramListElm)
        self._parse_subroutine_body_elm(subroutineBodyElm)

    def _parse_parameter_list_elm(self, elm):
        pass

    # subroutineBody tokens:
    # '{' varDec* statements* '}'
    def _parse_subroutine_body_elm(self, elm):
        print('compile_subroutine_body')

        for childElm in elm:
            tag, text = childElm.tag, childElm.text.strip()

            if tag == 'varDec':
                self._parse_var_dec_elm(childElm)

            if tag == 'statements':
                self._parse_statements_elm(childElm)

    # varDec tokens:
    # 'var' type typeName '(' ',' varName ')'* ':'
    def _parse_var_dec_elm(self, elm):
        print('compile_var_dec')

        self._localVarCount += 1

        for childElm in elm:
            text = childElm.text.strip()
            if text == ',':
                self._localVarCount += 1

    # statements tokens:
    # statement*
    def _parse_statements_elm(self, elm):
        print('compile_statements')

        for childElm in elm:
            tag, text = childElm.tag, childElm.text.strip()
            if tag == 'doStatement':
                self._parse_do_statement_elm(childElm)
            if tag == 'letStatement':
                self._parse_let_statement_elm(childElm)
            if tag == 'whileStatement':
                self._parse_while_statement_elm(childElm)

    # doStatement tokens:
    # 'do' subroutineCall ';'
    def _parse_do_statement_elm(self, elm):
        print('compile_do_statement')

        iter_elm = iter(elm)

        doElm = next(iter_elm)
        assert doElm.text.strip() == 'do'

        self._parse_subroutine_call_elm(elm)

    # letStatement tokens:
    # 'let' varName ('[' expression ']')? '=' expression ';'
    def _parse_let_statement_elm(self, elm):
        print('compile_let_statement')

        if self._is_retVal_array(elm):
            self._parse_let_statement_elm_with_array(elm)
        else:
            iter_elm = iter(elm)

            letElm = next(iter_elm)
            assert letElm.text.strip() == 'let'

            varElm = next(iter_elm)
            retVal = varElm.text.strip()
            assert varElm.tag == 'identifier'

            symElm = next(iter_elm)
            assert symElm.text.strip() == '='

            expElm = next(iter_elm)
            assert expElm.tag == 'expression'

            self._parse_expression_elm(expElm)
            self._write_pop(retVal)

    def _parse_let_statement_elm_with_array(self, elm):
        print('compile_let_with_array_statement')

        iter_elm = iter(elm)

        letElm = next(iter_elm)
        assert letElm.text.strip() == 'let'

        varElm = next(iter_elm)
        retVal = varElm.text.strip()
        assert varElm.tag == 'identifier'

        lBracketElm = next(iter_elm)
        assert lBracketElm.text.strip() == '['

        bracketExpElm = next(iter_elm)
        assert bracketExpElm.tag == 'expression'

        rBracketElm = next(iter_elm)
        assert rBracketElm.text.strip() == ']'

        symElm = next(iter_elm)
        assert symElm.text.strip() == '='

        expElm = next(iter_elm)
        assert expElm.tag == 'expression'


        # 配列操作は変数とは宣言〜値の代入までの根本的な処理が異なる。
        self._write_push(retVal)
        self._parse_expression_elm(bracketExpElm)
        self._write_arithmetic('+')
        self._write_pop('pointer')

        self._parse_expression_elm(expElm)

        self._write_pop('that')

    # while statement tokens:
    # 'while' '(' expression ')' '{' statements '}'
    def _parse_while_statement_elm(self, elm):
        print('compile_do_statement')

        iter_elm = iter(elm)

        whileElm = next(iter_elm)
        assert whileElm.text.strip() == 'while'

        assert next(iter_elm).text.strip() == '('
        expElm = next(iter_elm)
        assert next(iter_elm).text.strip() == ')'

        assert next(iter_elm).text.strip() == '{'
        statementElm = next(iter_elm)
        assert next(iter_elm).text.strip() == '}'

        self._write_label('WHILE_EXP')
        self._parse_expression_elm(expElm)
        self._write_arithmetic('not')
        self._write_if('WHILE_END')
        self._parse_statements_elm(statementElm)
        self._write_goto('WHILE_EXP')
        self._write_label('WHILE_END')

        self._label_count += 1


    # subroutineCall tokens:
    # subroutineName '(' expressionList ')' ';' | (className | varName) '.' subroutineName '(' expressionList ')' ';'
    def _parse_subroutine_call_elm(self, elm):
        print('compile_subroutine_call')

        assert 'expressionList' in self._extract_chileElms_tagList(elm)

        subroutineName = ''
        childTextList = self._extract_childElms_textList(elm)

        assert elm.tag in ['term', 'doStatement']
        iter_elm = iter(elm)

        if elm.tag == 'doStatement':
            next(iter_elm) # skip 'do'

        if '.' in childTextList:
            subroutineName += next(iter_elm).text.strip()
            dotElm = next(iter_elm)
            assert dotElm.text.strip() == '.'
            subroutineName += dotElm.text.strip()

        subroutineName += next(iter_elm).text.strip()

        symbolElm = next(iter_elm)
        assert symbolElm.text.strip() == '('

        expressionListElm = next(iter_elm)
        assert expressionListElm.tag == 'expressionList'

        self._parse_expression_list_elm(expressionListElm)    # eval expressionList first!
        self._write_call(subroutineName)                      # Then eval surbroutine!

    # expressionList tokens:
    # (expression (',' expression)* )?
    def _parse_expression_list_elm(self, elm):

        assert elm.tag == 'expressionList'
        print('start compile_expression_list')

        print(elm, elm.tag, elm.text.strip())

        for childElm in elm:
            tag, text = childElm.tag, childElm.text.strip()

            if tag == 'expression':
                self._parse_expression_elm(childElm)

        print('end compile_expression_list')

    # expression tokens:
    # term (op term)*
    def _parse_expression_elm(self, elm):
        print('start compile_expression')

        print(elm, elm.tag, elm.text.strip())

        termList = [childElm for childElm in elm if childElm.tag == 'term']
        opList = [childElm for childElm in elm if childElm.tag == 'symbol']

        for term in termList:
            self._parse_term_elm(term)

        for op in reversed(opList):
            self._parse_op_elm(op)

        print('end compile_expression')

    def _parse_op_elm(self, elm):
        print('start compile_op')

        operator = elm.text.strip()
        assert operator in ['+', '-', '*', '/', '&', '|', '<', '>', '=']

        if operator in ['+', '-', '<', '>']:
            self._write_arithmetic(operator)

        elif operator == '*':
            self._write_call('Math.multiply')

        elif operator == '/':
            self._write_call('Math.divide')

        print('end compile_op')

    # term tokens:
    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall |\
    #  '(' expression ')' | unaryOp term
    def _parse_term_elm(self, elm):
        print('start compile_term')
        print(elm.tag, elm.text.strip())

        assert elm.tag == 'term'

        print(self._extract_chileElms_tagList(elm))
        if 'expressionList' in self._extract_chileElms_tagList(elm) :
            self._parse_subroutine_call_elm(elm)
            print('end compile_term')
            return

        if '[' in self._extract_childElms_textList(elm):

            iter_elm = iter(elm)

            varElm = next(iter_elm)
            varName = varElm.text.strip()
            assert varElm.tag  == 'identifier'

            assert next(iter_elm).text.strip() == '['

            expElm = next(iter_elm)
            assert expElm.tag == 'expression'

            assert next(iter_elm).text.strip() == ']'

            self._write_push(varName)
            self._parse_expression_elm(expElm)
            self._write_arithmetic('+')
            self._write_pop('pointer')
            self._write_push('that')

            return

        # in case of 'term' 'symbol' 'term'
        for childElm in elm:
            tag, text = childElm.tag, childElm.text.strip()
            print(tag, text)

            if tag == 'stringConstant':
                self._parse_stringConstant_elm(text)

            elif tag == 'integerConstant':
                self._parse_integerConstant_elm(text)

            elif tag == 'expression':
                self._parse_expression_elm(childElm)

            elif tag == 'identifier':
                if next(iter(childElm), 'varOnly') == 'varOnly':
                    self._currentVariable = text
                    self._write_push(text)
                else:
                    self._parse_subroutine_call_elm(elm)

        print('end compile_term')

    def _parse_stringConstant_elm(self, text):

        str_len = len(text) + 1 # 1 for space.
        self._write_push(str_len)
        self._write_call('String.new')

        ascii_char_list = self._text_2_ascii_code(text + ' ')

        for code in ascii_char_list:
            self._write_push(code)
            self._write_call('String.appendChar')

    def _parse_integerConstant_elm(self, text):

        self._write_push(int(text))

    def _write_push(self, var):

        if var == 'that':
            self._vmLines.append('push' + ' ' + str(var) + ' ' + str(0))

        elif type(var) is int:
            self._vmLines.append('push' + ' ' + 'constant' + ' ' + str(var))

        elif type(var) is str:
            kind = self._symbolTable.kind_of(var)
            index = self._symbolTable.index_of(var)
            segment = self._get_segment(kind)
            self._vmLines.append('push' + ' ' + segment + ' ' + str(index))

    def _write_pop(self, var):

        if var == 'pointer':
            self._vmLines.append('pop' + ' ' + var + ' ' + str(1))

        elif var == 'that':
            self._vmLines.append('pop' + ' ' + var + ' ' + str(0))

        elif var == 'temp':
            self._vmLines.append('pop' + ' ' + var + ' ' + str(0))

        elif type(var) is str:
            kind = self._symbolTable.kind_of(var)
            index = self._symbolTable.index_of(var)
            segment = self._get_segment(kind)
            self._vmLines.append('pop' + ' ' + segment + ' ' + str(index))

    def _get_segment(self, kind):

        if kind == 'var':
            return 'local'

    def _write_arithmetic(self, operator):

        if operator in ['+', '-', '<', '>']:
            operator = const.ARITHMETIC_OP_2_CMD[operator]

        self._vmLines.append(operator)

    def _write_label(self, label):
        self._vmLines.append('label' + ' ' + label + str(self._label_count))

    def _write_goto(self, label):
        self._vmLines.append('goto' + ' ' + label + str(self._label_count))

    def _write_if(self, label):
        self._vmLines.append('if-goto' + ' ' + label + str(self._label_count))

    def _write_call(self, subroutine_name):

        arg = const.API_ARG[subroutine_name]
        self._vmLines.append('call' + ' ' + subroutine_name + ' ' + arg)

        if subroutine_name in const.VOID_SUBROUTINES:
            self._write_pop('temp')

    def _write_function(self):
        self._vmLines.insert(0, (
                'function' + ' ' + self._fileName.split('.')[0] + '.' + self._subroutineName + ' ' + str(self._localVarCount)))

    def _write_return(self):
        self._write_push(0)
        self._vmLines.append('return')

    def _write_file(self):

        self._write_function()
        self._write_return()

        vmFile = self._filePath + self._className + '.vm'

        with open(vmFile, 'w') as f:
            for line in self._vmLines:
                f.write(line + '\n')

    def _extract_childElms_textList(self, elm):

        return [text.strip() for text in elm.itertext() if text.strip()]

    def _extract_chileElms_tagList(self, elm):

        return [child_elm.tag for child_elm in elm]

    def _text_2_ascii_code(self, list):

        return [ord(c) for c in list]

    def _is_retVal_array(self, elm):

        textList = self._extract_childElms_textList(elm)

        if not '=' in textList:
            return False

        if not '[' in textList:
            return False

        eqIndex = textList.index('=')
        bracketIndex = textList.index('[')

        if eqIndex < bracketIndex:
            return False

        if bracketIndex < eqIndex:
            return True