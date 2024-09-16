class Three_address_code:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        if 'identificador' in node:
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

        return ''

    def print_code(self):
        for line in self.code:
            print(line)