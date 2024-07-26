from lexer.Lexer import Lexer

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

 
