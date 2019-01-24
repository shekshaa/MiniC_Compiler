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


class SymbolTable(object):
    def __init__(self):
        self.table = []

