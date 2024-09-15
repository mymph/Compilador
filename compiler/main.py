from lexer.lexer import Lexer
from parser.parser import Parser

GREEN = '\033[32m'
RESET = '\033[0m'
RED = '\033[31m'

lraw_code = ''

with open('teste.txt', 'r') as f:
  raw_code = f.read()

lexer = Lexer(raw_code)

tokens, symbols = lexer.run()
print(lexer)

print("---------------------TOKENS---------------------")
for token in tokens:
    print(token)
    print('\n')


print("************************************* parser ************************************")
# Inicialização do Parser com o Lexer
parser = Parser(lexer)
# Execução do Parser
try:
    parser.programa()  # Inicia a análise sintática a partir do ponto de entrada 'programa'
    print(f"{GREEN}Parsing completed successfully!{RESET}")

    parser.symbols_table.print_table()

except SyntaxError as e:
        print(f"{RED}Syntax error: {e}{RESET}")