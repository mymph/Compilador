from lexer.lexer import Lexer
from parser.parser import Parser

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

 
# Inicialização do Parser com o Lexer
parser = Parser(lexer)


# Execução do Parser
try:
    parser.programa()  # Inicia a análise sintática a partir do ponto de entrada 'programa'
    print("Parsing completed successfully!")
except SyntaxError as e:
    print(f"Syntax error: {e}")