class CodeGenerator(object):
    def __init__(self, symbol_table):
        self.while_switch_stack = []
        self.while_stack = []
        self.semantic_stack = []
        # self.temp = []
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

    def pop(self, k):
        self.semantic_stack.pop(-k)

    def push(self, item):
        self.semantic_stack.append(item)

    def get_id_addr(self, id, scope):
        return 0 # later developed!

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

    def push_id_addr(self, id):
        addr = self.get_id_addr(id, self.scope_stack[-1])
        self.semantic_stack.append(addr)

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