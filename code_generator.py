from symbol_table import *


class CodeGenerator(object):
    def __init__(self):
        self.while_switch_stack = []
        self.while_stack = []
        self.declaration_stack = []
        self.function_stack = []
        self.semantic_stack = []
        self.temp_pointer = 1000
        self.pb = [(None, None) for _ in range(1000)]
        self.i = 0
        self.data = []
        self.data_pointer = 500
        self.symbol_table = [FunctionRow('output', 'id_function', 'void', -1, -1, -1)]
        d = self.get_data(1)
        self.pb[self.i] = ('ASSIGN', '#0', d)
        self.i += 1
        self.symbol_table[0].param_list.append(IDRow('output_in', 'id_single', 'int', d))
        self.scope_stack = [-1]

    def push_scope(self):
        self.scope_stack.append(len(self.symbol_table))

    def pop_scope(self):
        self.symbol_table = self.symbol_table[:self.scope_stack[-1]]
        self.scope_stack.pop(-1)

    def get_temp(self):
        t = self.temp_pointer
        self.temp_pointer += 4
        return t

    def get_data(self, size):
        d = self.data_pointer
        self.data_pointer += size * 4
        return d

    def declaration_pop(self, k):
        self.declaration_stack = self.declaration_stack[:-k]

    def pop(self, k):
        self.semantic_stack = self.semantic_stack[:-k]

    def push(self, item):
        self.semantic_stack.append(item)

    def push_type(self, type):
        self.declaration_stack.append(type)

    def push_id(self, id):
        self.declaration_stack.append(id)

    def check_same_scope_id(self, id):
        for i in range(self.scope_stack[-1], len(self.symbol_table)):
            if self.symbol_table[i].token == id:
                raise Exception('Id declared in same scope')

    def add_single_symbol_table(self):
        self.check_same_scope_id(self.declaration_stack[-1])
        if self.declaration_stack[-2] == 'void':
            raise Exception('Invalid type')
        d = self.get_data(1)
        self.symbol_table.append(IDRow(self.declaration_stack[-1], 'id_single', self.declaration_stack[-2], d))
        self.pb[self.i] = ('ASSIGN', '#0', d)
        self.i += 1
        self.declaration_pop(2)

    def declaration_push_num(self, num):
        self.declaration_stack.append('#' + str(num))

    def add_array_symbol_table(self):
        self.check_same_scope_id(self.declaration_stack[-2])
        if self.declaration_stack[-3] == 'void':
            raise Exception('Invalid type')
        d = self.get_data(int(self.declaration_stack[-1][1:]))
        d1 = self.get_data(1)
        self.pb[self.i] = ('ASSIGN', '#' + str(d), d1)
        self.i += 1
        for j in range(int(self.declaration_stack[-1][1:])):
            self.pb[self.i] = ('ASSIGN', '#0', d + j * 4)
            self.i += 1
        self.symbol_table.append(ArrayRow(self.declaration_stack[-2], 'id_array', self.declaration_stack[-3], d1,
                                          self.declaration_stack[-1]))
        self.declaration_pop(3)

    def mult(self):
        t = self.get_temp()
        self.pb[self.i] = ('*', self.semantic_stack[-1], self.semantic_stack[-2], t)
        self.pop(2)
        self.push(t)
        self.i += 1

    def save_operator(self, operator):
        if operator == '<':
            self.push('LT')
        elif operator == '==':
            self.push('ASSIGN')
        elif operator == '-':
            self.push('SUB')
        elif operator == '+':
            self.push('ADD')

    def add_sub_compare(self):
        t = self.get_temp()
        self.pb[self.i] = (self.semantic_stack[-2], self.semantic_stack[-3], self.semantic_stack[-1], t)
        self.pop(3)
        self.push(t)
        self.i += 1

    def push_num(self, num):
        self.semantic_stack.append('#' + str(num))

    def search(self, id):
        for i in range(len(self.symbol_table) - 1, -1, -1):
            if self.symbol_table[i].token == id:
                return i, self.symbol_table[i].address
            if type(self.symbol_table[i]) == FunctionRow and not self.symbol_table[i].is_closed:
                for param in self.symbol_table[i].param_list:
                    if param.token == id:
                        return i, param.address
        return -1, -1

    def push_id_row_address(self, id):
        row, address = self.search(id)
        if row == -1:
            # for i in range(len(self.symbol_table)):
                # print(self.symbol_table[i].token)
            # print(self.symbol_table[-1].param_list)
            raise Exception('Semantic Error not defined parameter')
        self.push(row)
        self.push(address)

    def remove_line(self):
        self.semantic_stack.pop(-2)

    def pop_exp(self):
        self.pop(1)

    def array_addr_finder(self):
        t = self.get_temp()
        self.pb[self.i] = ('MULT', '#4', self.semantic_stack[-1], t)
        self.i += 1
        t1 = self.get_temp()
        self.pb[self.i] = ('ADD', t, self.semantic_stack[-2], t1)
        self.i += 1
        # t2 = self.get_temp()
        # self.pb[self.i] = ('=', '@' + str(t), t2)
        # self.i += 1
        self.pop(2)
        self.push('@' + str(t1))

    def assign(self):
        self.pb[self.i] = ('ASSIGN', self.semantic_stack[-1], self.semantic_stack[-2])
        self.i += 1
        self.pop(1)

    def save(self):
        self.push(self.i)
        self.i += 1

    def if_jpf_save(self):
        self.pb[self.semantic_stack[-1]] = ('JPF', self.semantic_stack[-2], self.i + 1)
        self.pop(2)
        self.save()

    def if_jp(self):
        self.pb[self.semantic_stack[-1]] = ('JP', self.i)
        self.pop(1)

    def while_label(self):
        self.pb[self.i] = ('JP', self.i + 2)
        self.i += 1
        self.while_switch_stack.append(('w', self.i))
        self.while_stack.append(('w', self.i))
        self.i += 1

    def break_jp(self):
        top = self.top_while_switch()
        if top is not None:
            self.pb[self.i] = ('JP', top)
            self.i += 1

    def continue_jp(self):
        top = self.top_while()
        if top is not None:
            self.pb[self.i] = ('JP', top + 1)
            self.i += 1

    def top_while(self):
        top = None
        try:
            top = self.while_stack[-1][1]
        except:
            raise Exception("Semantic error no while")
        return top

    def top_while_switch(self):
        top = None
        try:
            top = self.while_switch_stack[-1][1]
        except:
            raise Exception("Semantic error no while or case")
        return top

    def while_end(self):
        self.pb[self.semantic_stack[-1]] = ('JPF', self.semantic_stack[-2], self.i + 1)
        top = self.top_while()
        self.pb[self.i] = ('JP', top + 1)
        self.i += 1
        self.pb[top] = ('JP', self.i)
        self.pop(2)
        self.while_stack.pop(-1)
        self.while_switch_stack.pop(-1)

    def switch_label(self):
        self.pb[self.i] = ('JP', self.i + 2)
        self.i += 1
        self.while_switch_stack.append(('s', self.i))
        self.i += 1

    def cmp_save(self):
        t = self.get_temp()
        self.pb[self.i] = ('EQ', self.semantic_stack[-1], self.semantic_stack[-2], t)
        self.i += 1
        self.pop(1)
        self.push(t)
        self.save()

    def end_case(self):
        self.pb[self.semantic_stack[-1]] = ('JPF', self.semantic_stack[-2], self.i)
        self.pop(2)

    def end_switch(self):
        self.pop(1)
        top = self.top_while_switch()
        self.pb[top] = ('JP', self.i)
        self.while_switch_stack.pop(-1)

    def print_symbol_table(self):
        for i in range(len(self.symbol_table)):
            print(self.symbol_table[i].token)

    def param_assign(self):
        row_num = self.semantic_stack[-3]
        self.pb[self.i] = ('ASSIGN', self.semantic_stack[-1], self.symbol_table[row_num].param_list[self.symbol_table[row_num].counter].address)
        self.symbol_table[row_num].counter += 1
        self.i += 1
        self.pop(1)

    def jump_func_assign_return(self):
        row_num = self.semantic_stack[-2]
        if self.symbol_table[row_num].counter != len(self.symbol_table[row_num].param_list):
            raise Exception('Need more arguments')
        if self.symbol_table[row_num].token == 'output':
            self.pb[self.i] = ('PRINT', self.symbol_table[row_num].param_list[0].address)
            self.i += 1
            self.pop(1)
            self.symbol_table[row_num].counter = 0
        else:
            self.pb[self.i] = ('ASSIGN', "#" + str(self.i + 2), self.symbol_table[row_num].return_place)
            self.i += 1
            self.pb[self.i] = ('JP', self.semantic_stack[-1])
            self.i += 1
            self.pop(2)
            t = self.get_temp()
            if self.symbol_table[row_num].return_type != 'void':
                self.pb[self.i] = ('ASSIGN', self.symbol_table[row_num].return_param, t)
                self.i += 1
            self.push(t)
            self.symbol_table[row_num].counter = 0

    def error_void_type(self):
        raise Exception('Invalid input type')

    def add_func(self):
        d1 = self.get_data(1)
        d2 = self.get_data(2)
        if self.declaration_stack[-1] != 'main':
            self.save()
        elif self.declaration_stack[-2] != 'void':
            raise Exception('Main has no return')
        self.pb[self.i] = ('ASSIGN', '#0', d1)
        self.i += 1
        if self.declaration_stack[-1] != 'main':
            self.pb[self.i] = ('ASSIGN', '#0', d2)
            self.i += 1
        else:
            self.save()
        self.symbol_table.append(FunctionRow(self.declaration_stack[-1], 'id_func', self.declaration_stack[-2], None, d1, d2))
        self.declaration_pop(2)
        self.function_stack.append(len(self.symbol_table) - 1)

    def add_single_id_param(self):
        d = self.get_data(1)
        self.pb[self.i] = ('ASSIGN', '#0', d)
        self.i += 1
        self.symbol_table[self.function_stack[-1]].param_list.append(
            IDRow(self.declaration_stack[-1], 'id_single', self.declaration_stack[-2], d))
        self.declaration_pop(2)

    def add_array_id_param(self):
        d = self.get_data(1)
        self.pb[self.i] = ('ASSIGN', '#0', d)
        self.i += 1
        self.symbol_table[self.function_stack[-1]].param_list.append(
            ArrayRow(self.declaration_stack[-1], 'id_array', self.declaration_stack[-2], d, None))
        self.declaration_pop(2)

    def pop_func_stack(self):
        if self.symbol_table[self.function_stack[-1]].return_type == 'void' and self.symbol_table[self.function_stack[-1]].token != 'main':
            self.pb[self.i] = ('JP', '@' + str(self.symbol_table[self.function_stack[-1]].return_place))
            self.i += 1
        if self.symbol_table[self.function_stack[-1]].token != 'main':
            self.pb[self.semantic_stack[-1]] = ('JP', self.i)
        else:
            self.pb[self.semantic_stack[-1]] = ('ASSIGN', '#' + str(self.i), self.symbol_table[self.function_stack[-1]].return_place)
        self.pop(1)
        self.symbol_table[self.function_stack[-1]].is_closed = True
        self.function_stack.pop(-1)

    def set_return(self):
        self.pb[self.i] = ('ASSIGN', self.semantic_stack[-1], self.symbol_table[self.function_stack[-1]].return_param)
        self.i += 1
        row_num = self.function_stack[-1]
        self.pb[self.i] = ('JP', '@' + str(self.symbol_table[row_num].return_place))
        self.i += 1
        self.pop(1)

    def set_jump_address(self):
        self.symbol_table[self.function_stack[-1]].address = self.i

    def empty_return(self):
        self.pb[self.i] = ('JP', '@' + str(self.symbol_table[self.function_stack[-1]].return_place))
        self.i += 1
