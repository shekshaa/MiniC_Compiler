from symbol_table import *


class CodeGenerator(object):
    def __init__(self, symbol_table):
        self.while_switch_stack = []
        self.while_stack = []
        self.declaration_stack = []
        self.semantic_stack = []
        self.temp_pointer = 500
        self.pb = []
        self.i = 0
        self.data = []
        self.data_pointer = 100
        self.symbol_table = symbol_table
        self.scope_stack = [0]

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

    def add_single_symbol_table(self):
        d = self.get_data(1)
        self.symbol_table.append(IDRow(self.declaration_stack[-1], 'id_single', self.declaration_stack[-2], d))
        self.declaration_pop(2)

    def declaration_push_num(self, num):
        self.declaration_stack.append(num)

    def add_array_symbol_table(self):
        d = self.get_data(self.declaration_stack[-1])
        self.symbol_table.append(ArrayRow(self.declaration_stack[-2], 'id_array', self.declaration_stack[-3], d,
                                          self.declaration_stack[-1]))
        self.declaration_pop(3)

    def mult(self):
        t = self.get_temp()
        self.pb[self.i] = ('*', self.semantic_stack[-1], self.semantic_stack[-2], t)
        self.pop(2)
        self.push(t)
        self.i += 1

    def save_operator(self, operator):
        self.push(operator)

    def add_sub_compare(self):
        t = self.get_temp()
        self.pb[self.i] = (self.semantic_stack[-2], self.semantic_stack[-3], self.semantic_stack[-1], t)
        self.pop(3)
        self.push(t)
        self.i += 1

    def push_num(self, num):
        self.semantic_stack.append('#' + str(num))

    def addr_finder(self):
        t = self.get_temp()
        self.pb[self.i] = ('*', '#4', self.semantic_stack[-1], t)
        self.i += 1
        t1 = self.get_temp()
        self.pb[self.i] = ('+', t, self.semantic_stack[-2], t1)
        self.i += 1
        self.pop(2)
        self.push(t1)

    def assign(self):
        self.pb[self.i] = ('=', self.semantic_stack[-1], self.semantic_stack[-2], )
        self.i += 1
        self.pop(2)

    def save(self):
        self.push(self.i)
        self.i += 1

    def if_jpf_save(self):
        self.pb[self.semantic_stack[-1]] = ('jpf', self.semantic_stack[-2], self.i + 1)
        self.pop(2)
        self.save()

    def if_jp(self):
        self.pb[self.semantic_stack[-1]] = ('jp', self.i,)
        self.pop(1)

    def while_label(self):
        self.pb[self.i] = ('jp', self.i + 2,)
        self.i += 1
        self.while_switch_stack.append(('w', self.i))
        self.while_stack.append(('w', self.i))
        self.i += 1

    def break_jp(self):
        top = self.top_while_switch()
        if top is not None:
            self.pb[self.i] = ('jp', top, )
            self.i += 1

    def continue_jp(self):
        top = self.top_while()
        if top is not None:
            self.pb[self.i] = ('jp', top + 1,)
            self.i += 1

    def top_while(self):
        top = None
        try:
            top = self.while_stack[-1][1]
        except:
            print("Semantic error no while")
        return top

    def top_while_switch(self):
        top = None
        try:
            top = self.while_switch_stack[-1][1]
        except:
            print("Semantic error no while or case")
        return top

    def while_end(self):
        self.pb[self.semantic_stack[-1]] = ('jpf', self.semantic_stack[-2], self.i + 1, )
        top = self.top_while()
        self.pb[self.i] = ('jp', top + 1,)
        self.i += 1
        self.pb[top] = ('jp', self.i,)
        self.pop(2)
        self.while_stack.pop(-1)
        self.while_switch_stack.pop(-1)

    def switch_label(self):
        self.pb[self.i] = ('jp', self.i + 2,)
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
        self.pb[self.semantic_stack[-1]] = ('jpf', self.semantic_stack[-2], self.i, )
        self.pop(2)

    def end_switch(self):
        self.pop(1)
        top = self.top_while_switch()
        self.pb[top] = ('jp', self.i)
        self.while_switch_stack.pop(-1)
