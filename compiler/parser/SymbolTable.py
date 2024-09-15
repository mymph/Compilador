class SymbolTable:
    def __init__(self):
        self.table = {}

    def insert(self, identifier, symbol_info):
        if identifier in self.table:
            raise Exception(f"Erro Semantico: Variavel '{identifier}' ja declarada.")
        self.table[identifier] = symbol_info

    def verify(self, identifier):
        if identifier not in self.table:
            raise Exception(f"Erro Semantico: Variavel '{identifier}' nao declarada.")
        return self.table[identifier]

    def get(self, identifier):
        if identifier not in self.table:
            raise Exception(f"Erro Semantico: Simbolo '{identifier}' nao declarado.")
        return self.table[identifier]
    
    def print_table(self):
        print("Tabela de Simbolos:")
        for identifier, symbol_info in self.table.items():
            print('\n')
            print(f"Nome: {identifier}")
            print(f"  Tipo: {symbol_info['tipo']}")
            
            if symbol_info['tipo'] == 'HEADER_FUNC':
                print(f"  Retorno: {symbol_info['retorno']}")
                print(f"  Parametros:")
                for param in symbol_info['parametros']:
                    print(f"    - {param['nome']}: {param['tipo']}")
            
            elif symbol_info['tipo'] == 'HEADER_PROC':
                print(f"  Parametros:")
                for param in symbol_info['parametros']:
                    print(f"    - {param['nome']}: {param['tipo']}")
            
            else:  # Variável
                #print(f"  Tipo da Variavel: {symbol_info}")
                pass