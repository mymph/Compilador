class ThreeAddressCode:
    def __init__(self, file_name, SymbolTable):
        self.temp_count = 0
        self.if_count = 0
        self.while_count = 0
        self.code = []
        self.file_name = file_name
        self.SymbolTable = SymbolTable

    def new_temp(self):
        self.temp_count += 1
        return f"temp{self.temp_count}"
    
    def generate_simple_atribution(self, generate):
        temp = self.new_temp()
        self.code.append(f"{temp} = {generate}")

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

    def generate_print(self):
        self.code.append(f"PRINT(temp{self.temp_count})")

    def generate_if(self):
        self.code.append(f"IF temp{self.temp_count} GOTO IFA{self.if_count}_1")
        self.code.append(f"IF !temp{self.temp_count} GOTO IFB{self.if_count}_1")
        
    
    def generate_if_a1(self):
        self.code.append(f"IFA{self.if_count}_1:")

    def generate_if_b1(self):
        self.code.append(f"IFB{self.if_count}_1:")

    def generate_GOTO_if_a2(self):
        self.code.append(f"GOTO IFA{self.if_count}_2")

    def generate_if_a2(self):
        self.code.append(f"IFA{self.if_count}_2:")
        self.if_count += 1

        
    def generate_while(self):
        self.code.append(f"w{self.while_count}: while !temp{self.temp_count} GOTO fw{self.while_count}")
    
    def generate_while_end(self):
        self.code.append(f"GOTO w{self.while_count}")
        self.code.append(f"fw{self.while_count}:")
        self.while_count +=1

    def generate_break(self):
        self.code.append(f"break")

    def generate_continue(self):
        self.code.append(f"continue")




    def print_code(self):
        for line in self.code:
            print(line)

    def append_code_to_file(self):
        with open(self.file_name, 'a') as file:
            for line in self.code:
                file.write(line + '\n')
        self.code.clear()