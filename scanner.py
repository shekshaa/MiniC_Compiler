class Scanner(object):
    keywords = ['case', 'if', 'else', 'continue', 'void', 'int', 'while', 'return', 'switch', 'default', 'break']
    reserved_id = ['output']
    whitespace = ['\t', '\n', '\r', ' ']
    # pre_num = ['-', '+', '*', 'case', '[']
    pre_num = ['id', 'num']
    other_op = ['<', '*', ';', ':', ',', '(', ')', '[', ']', '{', '}']
    typ_dict = {'<': 'lt', '+': 'sum', '-': 'sub', '*': 'mult',
                ';': 'semicolon', ':': 'colon', ',': 'comma',
                '(': 'po', ')': 'pc',
                '[': 'bo', ']': 'bc',
                '{': 'ao', '}': 'ac'}

    def __init__(self, code_address, symbol_table):
        self.code = open(code_address).read()
        self.code += '\0'
        self.last_token = None
        self.symbol_table = symbol_table
        self.pointer = 0
        self.begin = 0
        self.current_scope = 0
        self.stack = [('c', 0)]
        self.last_valid_token = None

    def get_next_token(self):
        self.scan()
        while self.last_token == 'comment' or self.last_token == 'whitespace':
            self.scan()
        self.last_valid_token = self.last_token
        return self.last_token

    def scan(self):
        state = 0
        while True:
            if state == 0:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char == '/':
                    state = 1
                elif next_char in self.whitespace:
                    state = 5
                elif next_char.isalpha():
                    state = 7
                elif next_char == '+' or next_char == '-':
                    if self.last_valid_token in self.pre_num:
                        state = 12
                    else:
                        state = 9
                elif next_char.isdigit():
                    state = 10
                elif next_char == '=':
                    state = 13
                elif next_char in self.other_op:
                    if next_char == '{':
                        if self.stack[-1] == ('switch', 0):
                            self.stack[-1] = ('switch', 1)
                        else:
                            self.stack.append(('c', 0))
                            self.current_scope += 1
                    elif next_char == '}':
                        if self.stack[-1] == ('switch', 1):
                            self.stack.pop(1)
                        else:
                            self.stack.pop(1)
                            self.current_scope -= 1
                    state = 12
                elif next_char == '\0':
                    state = 16
                else:
                    raise Exception("Error in scanning")
            elif state == 1:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char == '*':
                    state = 2
                else:
                    raise Exception("Error in scanning")
            elif state == 2:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char == '*':
                    state = 3
                else:
                    state = 2
            elif state == 3:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char == '*':
                    state = 3
                elif next_char == '/':
                    state = 4
                else:
                    state = 2
            elif state == 4:
                self.begin = self.pointer
                self.last_token = 'comment'
                break
            elif state == 5:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char in self.whitespace:
                    state = 5
                else:
                    state = 6
            elif state == 6:
                self.pointer -= 1
                self.begin = self.pointer
                self.last_token = 'whitespace'
                break
            elif state == 7:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char.isalpha() or next_char.isdigit():
                    state = 7
                else:
                    state = 8
            elif state == 8:
                self.pointer -= 1
                self.last_token = self.code[self.begin:self.pointer]
                self.begin = self.pointer
                self.symbol_table.add_table(self.last_token,
                                            type='keyword' if self.last_token in self.keywords else 'id',
                                            scope=self.current_scope)
                if self.last_token not in self.keywords:
                    self.last_token = 'id'
                if self.last_token == 'switch':
                    self.stack.append(('switch', 0))
                break
            elif state == 9:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char.isdigit():
                    state = 10
                else:
                    raise Exception("Error in scanning")
            elif state == 10:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char.isdigit():
                    state = 10
                else:
                    state = 11
            elif state == 11:
                self.pointer -= 1
                self.last_token = self.code[self.begin:self.pointer]
                self.begin = self.pointer
                self.symbol_table.add_table(self.last_token, type='num', scope=self.current_scope)
                self.last_token = 'num'
                break
            elif state == 12:
                self.last_token = self.code[self.begin:self.pointer]
                self.begin = self.pointer
                self.symbol_table.add_table(self.last_token, type=self.typ_dict[self.last_token],
                                            scope=self.current_scope)
                break
            elif state == 13:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char == '=':
                    state = 14
                else:
                    state = 15
            elif state == 14:
                self.last_token = self.code[self.begin:self.pointer]
                self.begin = self.pointer
                self.symbol_table.add_table(self.last_token, type='eq', scope=self.current_scope)
                break
            elif state == 15:
                self.pointer -= 1
                self.last_token = self.code[self.begin:self.pointer]
                self.begin = self.pointer
                self.symbol_table.add_table(self.last_token, type='assign', scope=self.current_scope)
                break
            elif state == 16:
                self.last_token = 'EOF'
                self.symbol_table.add_table(self.last_token, type='EOF', scope=self.current_scope)
                break
