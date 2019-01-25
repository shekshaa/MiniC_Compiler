class SymbolTableRow(object):
    def __init__(self, token, type):
        self.type = type
        self.token = token
        self.value = None


class IDRow(SymbolTableRow):
    def __init__(self, token, type, var_type, address):
        super(IDRow, self).__init__(token, type)
        self.var_type = var_type
        self.address = address


class ArrayRow(IDRow):
    def __init__(self, token, type, var_type, address, size):
        super(ArrayRow, self).__init__(token, type, var_type, address)
        self.size = size


class NumRow(SymbolTableRow):
    def __init__(self, token, type):
        super(NumRow, self).__init__(token, type)
        self.var_type = 'int'


class FunctionRow(SymbolTableRow):
    def __init__(self, token, type, return_type, address, return_param, return_place):
        super(FunctionRow, self).__init__(token, type)
        self.return_type = return_type
        self.address = address
        self.param_list = []
        self.return_param = return_param
        self.return_place = return_place
        self.is_closed = False
        self.counter = 0

    def add_param_single(self, token, type, var_type, address):
        self.param_list.append(IDRow(token, type, var_type, address))

    def add_param_array(self, token, type, var_type, address, size):
        self.param_list.append(ArrayRow(token, type, var_type, address, size))
