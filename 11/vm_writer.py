import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

OSVMFILES = ['Array', 'Keyboard', 'Math', 'Memory', 'Output', 'Screen', 'String', 'Sys']

class VMWriter:

    def __init__(self, xmlFilePath):

        print('VMWriter:' + xmlFilePath)

        self._xmlFilePath = xmlFilePath
        self.className = ''

        self._read_txmlFile()
        self._compile_class()
        # self._write_file()

    def _read_txmlFile(self):
        # print(self._xmlFilePath)
        tree = ET.parse(self._xmlFilePath)
        self._root = tree.getroot()

    # class tokens:
    # 'class' className '{' classVarDec* subroutineDec* '}'
    def _compile_class(self):
        # assert self._root.tag == 'class'
        # assert self._root[0].text.strip() == 'class'

        print('start compile_class')

        self.className = self._root[1].text.strip()

        for child_tree in self._root:
            if child_tree.tag == 'classVarDec':
                # self._compile_class_var_dec(child_tree)
                pass
            if child_tree.tag == 'subroutineDec':
                Subroutine(child_tree, self.className)

        print('end compile_class')


class ClassVarDec:

    def __init__(self):
        pass

    # classVarDec tokens.
    # ( 'static' | 'field' ) type varName ( ',' varName )* ';'
    def _compile_class_var_dec(self):
        pass

class Subroutine:

    def __init__(self, tree, className):

        self._className = className
        self._subroutineName = ''
        self._localVarCount = 0

        self._compile_subroutine_dec(tree)

    def _compile_class_var_dec(self, tree):
        print(tree)

    # subroutine token:
    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subrutineBody
    def _compile_subroutine_dec(self, tree):
        print('start compile_subroutine_dec')

        for index, child_tree in enumerate(tree):
            tag, text = child_tree.tag.strip(), child_tree.text.strip()
            print(' elem: subroutinedec tag: %s text: %s' % (tag, text))

            if index == 2:
                self._subroutineName = text
                print('subroutineName...%s' % self._subroutineName)

            if tag == 'subroutineBody':
                l =(child_tree.iter())
                for a in l:
                    print(a.tag)
                #print(next(l))
                #print(hoge.__next__())
                #print(hoge.__next__())
                self._compile_subroutine_body(child_tree)

        self._write_file('function ' + self._className + '.' + self._subroutineName + ' ' + str(self._localVarCount))
        self._write_file('return')
        print('end compile_subroutine_dec')

    # subroutineBody tokens:
    # '{' varDec* statements* '}'
    def _compile_subroutine_body(self, tree):
        print('compile_subroutine_body')

        for child_tree in tree:
            tag, text = child_tree.tag.strip(), child_tree.text.strip()

            if tag =='varDec':
                print('varDec...%s' % tag)
                self._compile_var_dec(child_tree)

            if tag == 'statements':
                self._compile_statements(child_tree)

    # varDec tokens:
    # 'var' type typeName '(' ',' varName ')'* ':'
    def _compile_var_dec(self, tree):
        print('compile_var_dec')

        self._localVarCount += 1

        for child_tree in tree:
            text = child_tree.tag.strip(), child_tree.text.strip()
            if text == ',':
                self._localVarCount += 1

    # statements tokens:
    # statement*
    def _compile_statements(self, tree):
        print('compile_statements')

        for child_tree in tree:
            tag, text = child_tree.tag.strip(), child_tree.text.strip()
            if tag == 'doStatement':
                self._compile_do_statement(tree)


    # doStatement tokens:
    # 'do' subroutineCall ';'
    def _compile_do_statement(self, tree):
        print('compile_do_statement')

        for child_tree in tree:
            tag, text = child_tree.tag.strip(), child_tree.text.strip()
            if tag == 'do':
                continue
            else:
                self._compile_subroutine_call(child_tree)
                break

    # subroutineCall tokens:
    # subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
    def _compile_subroutine_call(self, tree):
        print('compile_subroutine_call')

        subroutineName = ''
        className = ''
        argument = ''

        for child_tree in tree:
            tag, text = child_tree.tag.strip(), child_tree.text.strip()

            if tag == 'identifier':
                if text in OSVMFILES:
                    className = text
                else:
                    subroutineName = text
                    self._write_file('call' + ' ' + className + '.' + subroutineName)

            if tag == 'expressionList':
                self._compile_expression_list(child_tree)

    # expressionList tokens:
    # (expression (',' expression)* )?
    def _compile_expression_list(self, tree):
        print('compile_expression_list')

        for child_tree in tree:
            tag, text = child_tree.tag.strip(), child_tree.text.strip()

            if tag == 'expression':
                self._compile_expression(child_tree)

    # expression tokens:
    # term (op term)*
    def _compile_expression(self, tree):
        print('compile_expression')

        leftLeaf = tree[0]
        assert leftLeaf.tag == 'term'

        node = tree[1]
        assert node.tag == 'symbol'

        rightLeaf = tree[2]
        assert rightLeaf.tag == 'term'

        self._compile_term(leftLeaf)
        self._compile_term(rightLeaf)
        self._compile_op(node)

    def _compile_op(self, tree):
        print('compile_op')

        operator = tree.text.strip()

        if operator == '+':
            self._write_file('add')

        elif operator == '*':
            self._write_file('mult')


    # symbol tokens:
    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall |\
    #  '(' expression ')' | unaryOp term
    def _compile_term(self, tree):
        print('compile_term')

        # in case of 'term' 'symbol' 'term'
        for child_tree in tree:
            tag, text = child_tree.tag.strip(), child_tree.text.strip()

            if tag == 'integerConstant':
                self._write_file('push' + ' ' + text)

            elif tag == 'stringConstant':
                self._write_file('push' + ' ' + text)

            elif tag == 'expression':
                self._compile_expression(child_tree)

    def write_push(self):
        pass

    def write_pop(self):
        pass

    def write_arithmetic(self):
        pass

    def write_label(self):
        pass

    def write_goto(self):
        pass

    def write_if(self):
        pass

    def write_call(self):
        pass

    def write_function(self):
        pass

    def write_return(self):
        pass

    def _write_file(self, line):

        # if os.path.isfile(filePath):
        #     outFilePath = filePath.split('.')[0] + '.' + 'asm'
        # elif os.path.isdir(filePath):
        #     outFilePath = filePath + filePath.split('/')[-2] + '.' + 'asm'

        with open('test.vm', 'a') as f:
            print('code: %s' % line)
            f.write(line + '\n')
