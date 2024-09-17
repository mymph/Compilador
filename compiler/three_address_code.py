class Three_address_code:
    def __init__(self, file_name, SymbolTable):
        self.temp_count = 0
        self.code = []
        self.file_name = file_name
        self.SymbolTable = SymbolTable

    def new_temp(self):
        self.temp_count += 1
        return f"temp{self.temp_count}"

    def generate(self, node):
        if 'identificador' in node:
            expressao = (self.SymbolTable.get(node['identificador']))
            if expressao['id'] == "VARIABLE":
                variable = self.generate(expressao)
                return ( node['identificador'],variable)
                
            return node['identificador']
        elif 'valor' in node:
            return node['valor']
        else:
            left = self.generate(node['esquerda'])
            right = self.generate(node['direita'])
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {self.get_operator(node['operador'])} {right}")
            return temp

    def get_operator(self, op):
        if op == 'ADD':
            return '+'
        if op == 'SUB':
            return '-'
        if op == 'MULT':
            return '*'
        if op == 'DIV':
            return '/'
        if op == 'GREATER_THAN_OP':
            return '>'
        if op == 'LESS_THAN_OP':
            return '<'
        if op == 'NOT_EQUAL_OP':
            return '!='
        if op == 'EQUALS_OP':
            return '=='
        if op == 'LESS_EQUAL_OP':
            return '<='
        if op == 'GREATER_EQUAL_OP':
            return '>='
        if op == 'AND':
            return '&&'
        if op == 'OR':
            return '||'
        return ''

    def print_code(self):
        for line in self.code:
            print(line)

    def append_code_to_file(self):
        with open(self.file_name, 'a') as file:
            for line in self.code:
                file.write(line + '\n')
        self.code.clear()