from scanner import Scanner
from grammar import First, Follow
from code_generator import CodeGenerator


class Parser(object):
    def __init__(self, code_address, code_generated_address):
        self.scanner = Scanner(code_address)
        self.semantic_stack = []
        self.code_generator = CodeGenerator()
        self.code_generated_address = code_generated_address
        self.stack = []
        self.state = 0
        self.lexeme, self.token = self.get_next_token()

    def move_back(self):
        self.state = self.stack.pop(-1)

    def get_next_token(self):
        lexeme, token = self.scanner.get_next_token()
        return lexeme, token

    def invalid_input_error(self):
        print('Invalid input {}'.format(self.token))
        self.get_next_token()

    def parse(self):
        self.state = 0
        while True:
            # print(self.state)
            # print(self.token)
            # print('Semantic stack: ', self.code_generator.semantic_stack)
            # print('Declaration stack: ', self.code_generator.declaration_stack)
            # print('Function stack: ', self.code_generator.function_stack)
            # print('While switch stack:', self.code_generator.while_switch_stack)
            if self.state == 0:
                if self.token == 'EOF':
                    self.state = 2
                elif self.token in First['declaration']:
                    self.stack.append(0)
                    self.state = 8
                elif self.token in Follow['declaration']:
                    self.state = 0
                    print('Missing term')
                else:
                    self.invalid_input_error()
            elif self.state == 2:
                break
            elif self.state == 8:
                if self.token in First['type_sepc']:
                    self.stack.append(9)
                    self.state = 19
                elif self.token in Follow['type_spec']:
                    self.state = 9
                    print('Missing term')
                else:
                    self.invalid_input_error()
            elif self.state == 9:
                if self.token == 'id':
                    self.code_generator.push_id(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 10
                else:
                    self.invalid_input_error()
            elif self.state == 10:
                if self.token == '(':
                    self.code_generator.add_func()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 11
                elif self.token == '[':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 15
                elif self.token == ';':
                    self.code_generator.add_single_symbol_table()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 18
                else:
                    self.invalid_input_error()
            elif self.state == 11:
                if self.token in First['params']:
                    self.stack.append(12)
                    self.state = 21
                elif self.token in Follow['params']:
                    self.state = 14
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 12:
                if self.token == ')':
                    self.code_generator.set_jump_address()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 14
                else:
                    self.invalid_input_error()
            elif self.state == 14:
                if self.token in First['cmpd_stmt']:
                    self.stack.append(18)
                    self.state = 37
                elif self.token in Follow['cmpd_stmt']:
                    self.state = 18
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 15:
                if self.token == 'num':
                    self.code_generator.declaration_push_num(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 16
                else:
                    self.invalid_input_error()
            elif self.state == 16:
                if self.token == ']':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 17
                else:
                    self.invalid_input_error()
            elif self.state == 17:
                if self.token == ';':
                    self.code_generator.add_array_symbol_table()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 18
                else:
                    self.invalid_input_error()
            elif self.state == 18:
                self.move_back()
            elif self.state == 19:
                if self.token == 'void':
                    self.code_generator.push_type('void')
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 20
                elif self.token == 'int':
                    self.code_generator.push_type('int')
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 20
                else:
                    self.invalid_input_error()
            elif self.state == 20:
                self.move_back()
                if self.state == 31 and self.code_generator.declaration_stack[-1] == 'void':
                    self.code_generator.error_void_type()
            elif self.state == 21:
                if self.token == 'void':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 22
                elif self.token == 'int':
                    self.code_generator.push_type('int')
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 25
                else:
                    self.invalid_input_error()
            elif self.state == 22:
                if self.token == 'id':
                    self.code_generator.error_void_type()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 23
                elif self.token in Follow['params']:
                    self.state = 26
                else:
                    self.invalid_input_error()
            elif self.state == 23:
                if self.token in First['Y']:
                    self.stack.append(24)
                    self.state = 34
                elif self.token in Follow['Y']:
                    self.stack.append(24)
                    self.state = 34
                else:
                    self.invalid_input_error()
            elif self.state == 24:
                if self.token in First['X']:
                    self.stack.append(26)
                    self.state = 27
                elif self.token in Follow['X']:
                    self.state = 26
                else:
                    self.invalid_input_error()
            elif self.state == 25:
                if self.token == 'id':
                    self.code_generator.push_id(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 23
                else:
                    self.invalid_input_error()
            elif self.state == 26:
                self.move_back()
            elif self.state == 27:
                if self.token == ',':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 28
                elif self.token in Follow['X']:
                    self.state = 29
                else:
                    self.invalid_input_error()
            elif self.state == 28:
                if self.token in First['param']:
                    self.stack.append(27)
                    self.state = 30
                elif self.token in Follow['param']:
                    self.state = 27
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 29:
                self.move_back()
            elif self.state == 30:
                if self.token in First['type_sepc']:
                    self.stack.append(31)
                    self.state = 19
                elif self.token in Follow['type_spec']:
                    self.state = 31
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 31:
                if self.token == 'id':
                    self.code_generator.push_id(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 32
                else:
                    self.invalid_input_error()
            elif self.state == 32:
                if self.token in First['Y']:
                    self.stack.append(33)
                    self.state = 34
                elif self.token in Follow['Y']:
                    self.stack.append(33)
                    self.state = 34
                else:
                    self.invalid_input_error()
            elif self.state == 33:
                self.move_back()
            elif self.state == 34:
                if self.token == '[':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 35
                elif self.token in Follow['Y']:
                    self.code_generator.add_single_id_param()
                    self.state = 36
                else:
                    self.invalid_input_error()
            elif self.state == 35:
                if self.token == ']':
                    self.code_generator.add_array_id_param()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 36
                else:
                    self.invalid_input_error()
            elif self.state == 36:
                self.move_back()
            elif self.state == 37:
                if self.token == '{':
                    self.code_generator.push_scope()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 38
                else:
                    self.invalid_input_error()
            elif self.state == 38:
                if self.token in First['declaration']:
                    self.stack.append(38)
                    self.state = 8
                elif self.token in First['stmt_list']:
                    self.stack.append(39)
                    self.state = 41
                elif self.token in Follow['stmt_list']:
                    self.state = 39
                elif self.token in Follow['declaration']:
                    self.state = 38
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 39:
                if self.token == '}':
                    self.code_generator.pop_scope()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 40
                else:
                    self.invalid_input_error()
            elif self.state == 40:
                self.move_back()
                if self.state == 18:
                    self.code_generator.pop_func_stack()
            elif self.state == 41:
                if self.token in First['stmt']:
                    self.stack.append(41)
                    self.state = 43
                elif self.token in Follow['stmt_list']:
                    self.state = 42
                elif self.token in Follow['stmt']:
                    self.state = 41
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 42:
                self.move_back()
            elif self.state == 43:
                if self.token in First['sel-stmt']:
                    self.stack.append(44)
                    self.state = 48
                elif self.token in First['cmpd_stmt']:
                    self.stack.append(44)
                    self.state = 37
                elif self.token in First['itr-stmt']:
                    self.stack.append(44)
                    self.state = 56
                elif self.token in First['exp-stmt']:
                    self.stack.append(44)
                    self.state = 45
                elif self.token in First['ret-stmt']:
                    self.stack.append(44)
                    self.state = 62
                elif self.token in First['swt-stmt']:
                    self.stack.append(44)
                    self.state = 66
                elif self.token in Follow['cmpd_stmt'] or self.token in Follow['ret-stmt']:
                    self.state = 44
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 44:
                self.move_back()
                if self.state == 55:
                    self.code_generator.if_jp()
                if self.state == 61:
                    self.code_generator.while_end()
            elif self.state == 45:
                if self.token == ';':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 47
                elif self.token in First['exp']:
                    self.stack.append(46)
                    self.state = 83
                elif self.token == 'break':
                    self.code_generator.break_jp()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 46
                elif self.token == 'continue':
                    self.code_generator.continue_jp()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 46
                elif self.token in Follow['exp']:
                    self.state = 46
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 46:
                if self.token == ';':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 47
                else:
                    self.invalid_input_error()
            elif self.state == 47:
                self.move_back()
            elif self.state == 48:
                if self.token == 'if':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 49
                else:
                    self.invalid_input_error()
            elif self.state == 49:
                if self.token == '(':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 50
                else:
                    self.invalid_input_error()
            elif self.state == 50:
                if self.token in First['exp']:
                    self.stack.append(51)
                    self.state = 83
                elif self.token in Follow['exp']:
                    self.state = 51
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 51:
                if self.token == ')':
                    self.code_generator.save()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 52
                else:
                    self.invalid_input_error()
            elif self.state == 52:
                if self.token in First['stmt']:
                    self.stack.append(53)
                    self.state = 43
                elif self.token in Follow['stmt']:
                    self.state = 53
                    print('Missing')
            elif self.state == 53:
                if self.token == 'else':
                    self.code_generator.if_jpf_save()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 54
                else:
                    self.invalid_input_error()
            elif self.state == 54:
                if self.token in First['stmt']:
                    self.stack.append(55)
                    self.state = 43
                elif self.token in Follow['stmt']:
                    self.state = 55
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 55:
                self.move_back()
            elif self.state == 56:
                if self.token == 'while':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 57
                else:
                    self.invalid_input_error()
            elif self.state == 57:
                if self.token == '(':
                    self.code_generator.while_label()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 58
                else:
                    self.invalid_input_error()
            elif self.state == 58:
                if self.token in First['exp']:
                    self.stack.append(59)
                    self.state = 83
                elif self.token in Follow['exp']:
                    self.state = 59
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 59:
                if self.token in ')':
                    self.code_generator.save()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 60
                else:
                    self.invalid_input_error()
            elif self.state == 60:
                if self.token in First['stmt']:
                    self.stack.append(61)
                    self.state = 43
                elif self.token in Follow['stmt']:
                    self.state = 61
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 61:
                self.move_back()
            elif self.state == 62:
                if self.token == 'return':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 63
                else:
                    self.invalid_input_error()
            elif self.state == 63:
                if self.token == ';':
                    self.code_generator.empty_return()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 64
                elif self.token in First['exp']:
                    self.stack.append(65)
                    self.state = 83
                elif self.token in Follow['exp']:
                    self.state = 65
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 64:
                self.move_back()
            elif self.state == 65:
                if self.token == ';':
                    self.code_generator.set_return()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 64
                else:
                    self.invalid_input_error()
            elif self.state == 66:
                if self.token == 'switch':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 67
                else:
                    self.invalid_input_error()
            elif self.state == 67:
                if self.token == '(':
                    self.code_generator.switch_label()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 68
                else:
                    self.invalid_input_error()
            elif self.state == 68:
                if self.token in First['exp']:
                    self.stack.append(69)
                    self.state = 83
                elif self.token in Follow['exp']:
                    self.state = 69
                    print('Missing')
            elif self.state == 69:
                if self.token == ')':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 70
                else:
                    self.invalid_input_error()
            elif self.state == 70:
                if self.token == '{':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 71
                else:
                    self.invalid_input_error()
            elif self.state == 71:
                if self.token in First['case-stmt']:
                    self.stack.append(71)
                    self.state = 74
                elif self.token in First['default-stmt']:
                    self.stack.append(72)
                    self.state = 79
                elif self.token in Follow['default-stmt']:
                    self.state = 72
                elif self.token in Follow['case-stmt']:
                    self.state = 71
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 72:
                if self.token == '}':
                    self.code_generator.end_switch()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 73
                else:
                    self.invalid_input_error()
            elif self.state == 73:
                self.move_back()
            elif self.state == 74:
                if self.token == 'case':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 75
                else:
                    self.invalid_input_error()
            elif self.state == 75:
                if self.token == 'num':
                    self.code_generator.push_num(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 76
                else:
                    self.invalid_input_error()
            elif self.state == 76:
                if self.token == ':':
                    self.code_generator.cmp_save()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 77
                else:
                    self.invalid_input_error()
            elif self.state == 77:
                if self.token in First['stmt_list']:
                    self.stack.append(78)
                    self.state = 41
                elif self.token in Follow['stmt_list']:
                    self.state = 78
                else:
                    self.invalid_input_error()
            elif self.state == 78:
                self.move_back()
                if self.state == 71:
                    self.code_generator.end_case()
            elif self.state == 79:
                if self.token == 'default':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 80
                elif self.token in Follow['default-stmt']:
                    self.state = 82
                else:
                    self.invalid_input_error()
            elif self.state == 80:
                if self.token == ':':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 81
                else:
                    self.invalid_input_error()
            elif self.state == 81:
                if self.token in First['stmt_list']:
                    self.stack.append(82)
                    self.state = 41
                elif self.token in Follow['stmt_list']:
                    self.state = 82
                else:
                    self.invalid_input_error()
            elif self.state == 82:
                self.move_back()
            elif self.state == 83:
                if self.token == '(':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 84
                elif self.token == 'num':
                    self.code_generator.push_num(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 86
                elif self.token == 'id':
                    self.code_generator.push_id_row_address(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 88
                else:
                    self.invalid_input_error()
            elif self.state == 84:
                if self.token in First['exp']:
                    self.stack.append(85)
                    self.state = 83
                elif self.token in Follow['exp']:
                    self.state = 85
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 85:
                if self.token == ')':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 86
                else:
                    self.invalid_input_error()
            elif self.state == 86:
                if self.token in First['E']:
                    self.stack.append(87)
                    self.state = 116
                elif self.token in Follow['E']:
                    self.state = 87
                else:
                    self.invalid_input_error()
            elif self.state == 87:
                if self.token in First['M']:
                    self.stack.append(88.5)
                    self.state = 107
                elif self.token in Follow['M']:
                    self.state = 88.5
                else:
                    self.invalid_input_error()
            elif self.state == 88.5:
                if self.token in First['J']:
                    self.stack.append(93)
                    self.state = 104
                elif self.token in Follow['J']:
                    self.state = 93
                else:
                    self.invalid_input_error()
            elif self.state == 88:
                if self.token == '(':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 89
                elif self.token in First['K']:
                    self.stack.append(91)
                    self.state = 97
                elif self.token in Follow['K']:
                    self.stack.append(91)
                    self.state = 97
                else:
                    self.invalid_input_error()
            elif self.state == 89:
                if self.token in First['args']:
                    self.stack.append(90)
                    self.state = 130
                elif self.token in Follow['args']:
                    self.stack.append(90)
                    self.state = 130
                else:
                    self.invalid_input_error()
            elif self.state == 90:
                if self.token == ')':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 86
                else:
                    self.invalid_input_error()
            elif self.state == 91:
                if self.token == '=':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 92
                elif self.token in First['E']:
                    self.stack.append(87)
                    self.state = 116
                elif self.token in Follow['E']:
                    self.state = 87
                else:
                    self.invalid_input_error()
            elif self.state == 92:
                if self.token in First['exp']:
                    self.stack.append(93)
                    self.state = 83
                elif self.token in Follow['exp']:
                    self.state = 93
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 93:
                self.move_back()
                if self.state == 46:
                    self.code_generator.pop_exp()
                if self.state == 93:
                    self.code_generator.assign()
            # elif self.state == 94:
            #     if self.token == 'id':
            #         self.lexeme, self.token = self.get_next_token()
            #         self.state = 95
            #     else:
            #         self.invalid_input_error()
            # elif self.state == 95:
            #     if self.token in First['K']:
            #         self.stack.append(96)
            #         self.state = 97
            #     elif self.token in Follow['K']:
            #         self.state = 96
            #     else:
            #         self.invalid_input_error()
            # elif self.state == 96:
            #     self.move_back()
            elif self.state == 97:
                if self.token == '[':
                    self.code_generator.remove_line()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 98
                elif self.token in Follow['K']:
                    self.code_generator.remove_line()
                    self.state = 100
                else:
                    self.invalid_input_error()
            elif self.state == 98:
                if self.token in First['exp']:
                    self.stack.append(99)
                    self.state = 83
                elif self.token in Follow['exp']:
                    self.state = 99
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 99:
                if self.token == ']':
                    self.code_generator.array_addr_finder()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 100
                else:
                    self.invalid_input_error()
            elif self.state == 100:
                self.move_back()
            # elif self.state == 101:
            #     if self.token in First['add-exp']:
            #         self.stack.append(102)
            #         self.state = 110
            #     else: raise Exception('error')
            # elif self.state == 102:
            #     if self.token in First['J']:
            #         self.stack.append(103)
            #         self.state = 104
            #     elif self.token in Follow['J']:
            #         self.state = 103
            #     else: raise Exception('error')
            # elif self.state == 103:
            #     self.move_back()
            elif self.state == 104:
                if self.token == '<':
                    self.code_generator.save_operator(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 105
                elif self.token == '==':
                    self.code_generator.save_operator(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 105
                elif self.token in Follow['J']:
                    self.state = 106
                else:
                    self.invalid_input_error()
            elif self.state == 105:
                if self.token in First['add-exp']:
                    self.stack.append(106)
                    self.state = 110
                elif self.token in Follow['add-exp']:
                    self.state = 106
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 106:
                self.move_back()
            elif self.state == 107:
                if self.token == '+':
                    self.code_generator.save_operator(self.token)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 108
                elif self.token == '-':
                    self.code_generator.save_operator(self.token)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 108
                elif self.token in Follow['M']:
                    self.state = 109
                else:
                    self.invalid_input_error()
            elif self.state == 108:
                if self.token in First['term']:
                    self.stack.append(107)
                    self.state = 113
                elif self.token in Follow['term']:
                    self.state = 107
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 109:
                self.move_back()
            elif self.state == 110:
                if self.token in First['term']:
                    self.stack.append(111)
                    self.state = 113
                elif self.token in Follow['term']:
                    self.state = 111
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 111:
                if self.token in First['M']:
                    self.stack.append(112)
                    self.state = 107
                elif self.token in Follow['M']:
                    self.state = 112
                else:
                    self.invalid_input_error()
            elif self.state == 112:
                self.move_back()
                if self.state == 106:
                    self.code_generator.add_sub_compare()
            elif self.state == 113:
                if self.token in First['factor']:
                    self.stack.append(114)
                    self.state = 119
                elif self.token in Follow['factor']:
                    self.state = 114
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 114:
                if self.token in First['E']:
                    self.stack.append(115)
                    self.state = 116
                elif self.token in Follow['E']:
                    self.state = 115
                else:
                    self.invalid_input_error()
            elif self.state == 115:
                self.move_back()
                if self.state == 107:
                    self.code_generator.add_sub_compare()
            elif self.state == 116:
                if self.token == '*':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 117
                elif self.token in Follow['E']:
                    self.state = 118
                else:
                    self.invalid_input_error()
            elif self.state == 117:
                if self.token in First['factor']:
                    self.stack.append(116)
                    self.state = 119
                elif self.token in Follow['factor']:
                    self.state = 116
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 118:
                self.move_back()
            elif self.state == 119:
                if self.token == 'num':
                    self.code_generator.push_num(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 122
                elif self.token == '(':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 120
                elif self.token == 'id':
                    self.code_generator.push_id_row_address(self.lexeme)
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 123
                else:
                    self.invalid_input_error()
            elif self.state == 120:
                if self.token in First['exp']:
                    self.stack.append(121)
                    self.state = 83
                elif self.token in Follow['exp']:
                    self.state = 121
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 121:
                if self.token == ')':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 122
                else:
                    self.invalid_input_error()
            elif self.state == 122:
                self.move_back()
                if self.state == 116:
                    self.code_generator.mult()
            elif self.state == 123:
                if self.token == '(':
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 124
                elif self.token in First['K']:
                    self.stack.append(122)
                    self.state = 97
                elif self.token in Follow['K']:
                    self.stack.append(122)
                    self.state = 97
                else:
                    self.invalid_input_error()
            elif self.state == 124:
                if self.token in First['args']:
                    self.stack.append(121)
                    self.state = 130
                elif self.token in Follow['args']:
                    self.stack.append(121)
                    self.state = 130
                else:
                    self.invalid_input_error()
            # elif self.state == 125:
            #     if self.token == 'id':
            #         self.lexeme, self.token = self.get_next_token()
            #         self.state = 126
            #     else: raise Exception('error')
            # elif self.state == 126:
            #     if self.token == '(':
            #         self.lexeme, self.token = self.get_next_token()
            #         self.state = 127
            #     else: raise Exception('error')
            # elif self.state == 127:
            #     if self.token in First['args']:
            #         self.stack.append(128)
            #         self.state = 130
            #     elif self.token in Follow['args']:
            #         self.state = 128
            #     else: raise Exception('error')
            # elif self.state == 128:
            #     if self.token == ')':
            #         self.lexeme, self.token = self.get_next_token()
            #         self.state = 129
            #     else: raise Exception('error')
            # elif self.state == 129:
            #     self.move_back()
            elif self.state == 130:
                if self.token in First['exp']:
                    self.stack.append(131)
                    self.state = 83
                elif self.token in Follow['args']:
                    self.state = 133
                elif self.token in Follow['exp']:
                    self.state = 131
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 131:
                if self.token == ',':
                    self.code_generator.param_assign()
                    self.lexeme, self.token = self.get_next_token()
                    self.state = 132
                elif self.token in Follow['args']:
                    self.code_generator.param_assign()
                    self.state = 133
                else:
                    self.invalid_input_error()
            elif self.state == 132:
                if self.token in First['exp']:
                    self.stack.append(131)
                    self.state = 83
                elif self.token in Follow['exp']:
                    self.state = 131
                    print('Missing')
                else:
                    self.invalid_input_error()
            elif self.state == 133:
                self.move_back()
                if self.state == 90 or self.state == 121:
                    self.code_generator.jump_func_assign_return()

        final_code = ""
        for i, pb in enumerate(self.code_generator.pb):
            if pb == (None, None):
                break
            final_code += str(i) + '\t('
            for j in range(len(pb)):
                final_code += str(pb[j]) + ', '
            if len(pb) == 4:
                final_code = final_code[:-2]
                final_code += ')'
            else:
                for j in range(3 - len(pb)):
                    final_code += ', '
                final_code += ')'
            final_code += '\n'
        with open(self.code_generated_address, mode='w') as file:
            file.write(final_code)
            file.close()
