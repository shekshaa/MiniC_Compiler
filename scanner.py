class Scanner(object):
    keywords = ['case', 'if', 'else', 'continue', 'void', 'int', 'while', 'return', 'switch', 'default', 'break']
    reserved_id = ['output']
    whitespace = ['\t', '\n', '\r', ' ']
    # pre_num = ['-', '+', '*', 'case', '[']
    pre_num = ['id', 'num', ')', ']']
    other_op = ['<', '*', ';', ':', ',', '(', ')', '[', ']', '{', '}']
    typ_dict = {'<': 'lt', '+': 'sum', '-': 'sub', '*': 'mult',
                ';': 'semicolon', ':': 'colon', ',': 'comma',
                '(': 'po', ')': 'pc',
                '[': 'bo', ']': 'bc',
                '{': 'ao', '}': 'ac'}

    def __init__(self, code_address):
        self.code = open(code_address).read()
        self.code += '\0'
        self.last_token = (None, None)
        self.pointer = 0
        self.begin = 0
        self.last_valid_token = None

    def get_next_token(self):
        self.scan()
        while self.last_token[1] == 'comment' or self.last_token[1] == 'whitespace':
            self.scan()
        self.last_valid_token = self.last_token
        return self.last_token

    def scan(self):
        state = 0
        while self.pointer <= len(self.code):
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
                    if self.last_valid_token[1] in self.pre_num:
                        state = 12
                    else:
                        state = 9
                elif next_char.isdigit():
                    state = 10
                elif next_char == '=':
                    state = 13
                elif next_char in self.other_op:
                    state = 12
                elif next_char == '\0':
                    state = 16
                else:
                    print('Scanner Error')
                    self.begin = self.pointer
                    state = 0
            elif state == 1:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char == '*':
                    state = 2
                else:
                    print('Scanner Error')
                    self.begin = self.pointer
                    state = 0
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
                self.last_token = ('comment', 'comment')
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
                self.last_token = ('whitespace', 'whitespace')
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
                if self.code[self.begin:self.pointer] not in self.keywords:
                    self.last_token = (self.code[self.begin:self.pointer], 'id')
                else:
                    self.last_token = (self.code[self.begin:self.pointer], self.code[self.begin:self.pointer])
                self.begin = self.pointer
                break
            elif state == 9:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char.isdigit():
                    state = 10
                else:
                    print('Scanner Error')
                    self.begin = self.pointer
                    state = 0
            elif state == 10:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char.isdigit():
                    state = 10
                else:
                    state = 11
            elif state == 11:
                self.pointer -= 1
                self.last_token = (self.code[self.begin:self.pointer], 'num')
                self.begin = self.pointer
                break
            elif state == 12:
                self.last_token = (self.code[self.begin:self.pointer], self.code[self.begin:self.pointer])
                self.begin = self.pointer
                break
            elif state == 13:
                next_char = self.code[self.pointer]
                self.pointer += 1
                if next_char == '=':
                    state = 14
                else:
                    state = 15
            elif state == 14:
                self.last_token = (self.code[self.begin:self.pointer], self.code[self.begin:self.pointer])
                self.begin = self.pointer
                break
            elif state == 15:
                self.pointer -= 1
                self.last_token = (self.code[self.begin:self.pointer], self.code[self.begin:self.pointer])
                self.begin = self.pointer
                break
            elif state == 16:
                self.last_token = ('EOF', 'EOF')
                break
            else:
                print('Scanner Error')
                self.pointer += 1
                self.begin = self.pointer
                state = 0
