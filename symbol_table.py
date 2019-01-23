class SymbolTableRow(object):
    def __init__(self, token, type, scope):
        self.type = type
        self.token = token
        self.scope = scope
        self.value = None


class SymbolTable(object):
    def __init__(self):
        self.table = []

    def add_table(self, token, type, scope):
        if type == 'id':
            id_row = -1
            id_scope = -1
            for i, row in enumerate(self.table):
                if row.token == token and scope >= row.scope > id_scope:
                    id_row = i
                    id_scope = row.scope
            if id_row == -1:
                self.table.append(SymbolTableRow(token, type, scope))
                return len(self.table) - 1
            else:
                return id_row
        else:
            for i, row in enumerate(self.table):
                if row.token == token:
                    return i
            self.table.append(SymbolTableRow(token, type, scope))
            return len(self.table) - 1
