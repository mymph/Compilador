from pickle import NONE
from lexer.Token import Token
from lexer.Symbol import Symbol
from lexer.reserverd_keywords import RESERVED_KEYWORDS
from lexer.delimiters import DELIMITERS 

'''O Analisador léxico pega os caracteres de entrada e os trasnforma em tokens
- Lê os caracteres de entrada e os agrupa em lexemas
- Ignora espaços, tabulações e saltos de linha.
Ex.: o número 25432 de entrada será um token, em vez de cada número ser um token
- Token é um terminal. Possui atributos com informações adicionais sobre o símbolo.
Ex.: valor, tipo, escopo, etc.'''

class Lexer:
  def __init__(self,code: str):
    self.tokens: list[Token] = []
    self.symbols_table: list[Symbol] = []
    self.char_index = 0 # index do caractere que esta sendo lido
    self.current_line = 1 #linha do caractere que esta sendo lido
    self.code = code

  def is_delimiter(self,char: str):
    for key_token, lexeme_value in DELIMITERS.items():
      if (char == lexeme_value):
        return key_token
    return None   

  #começar a ler os tokens
  def read_next_token(self):
    state = None #tipo de token, delimitador, letra ou numero
    term = '' # armazena cada caractere por caractere e depois soma para formar um token
    end_of_file = False # fim do arquivo 

    while 1:
      if (self.char_index == len(self.code)):
         end_of_file = True
         break
      
      char = self.code[self.char_index]  # pega o caracteree marca sua posicao
      term += char  # incrementa o caractere no token(o termo) atual que esta sendo lido
      self.char_index += 1
      print(f"state anterior: {state} - char '{char}'")      


      # IGNORE CHAR
      if (char == ' ' or char == '\n'):
        term = term[:-1] # apaga o caractere vazio
        break


      elif (state==None): #enquanto ainda não tem o tipo do token
        # FOR EXAMPLE: ; { } ( ) 
        if (self.is_delimiter(term)):
          state = 'DELIMITER'
          continue
        if (char.isalpha()):
          state = 'ALPHA'
          continue
        elif (char.isnumeric()):
          state = 'NUMERIC'
          continue
        elif (char == "!" or char == '|' or char == '&'): 
            continue
        else:
            print("erro")
          

      elif (state=='ALPHA'):
        if (char.isalpha()):
          continue
        elif (char.isnumeric()):
          state = 'ALPHANUM'
          continue
        elif (self.is_delimiter(char)):
            term = term[:-1]
            self.char_index-=1          
            break
        elif (char == "!" or char == '|' or char == '&'): 
            term = term[:-1]
            self.char_index-=1          
            break
        else:
            print("erro")

      elif (state=='ALPHANUM'):
        if (char.isalnum()): continue
        elif (self.is_delimiter(char)):
            term = term[:-1]
            self.char_index-=1
            break
         
        elif (char == "!" or char == '|' or char == '&'): 
          term = term[:-1]
          self.char_index-=1          
          break
        else:
          print("erro")
        
      elif (state == 'NUMERIC'):
          if (char.isnumeric()):
            continue
          elif (self.is_delimiter(char)):
            term = term[:-1]
            self.char_index-=1
            break
          else:
            print("erro")
      elif(state == 'DELIMITER'):
        if (not self.is_delimiter(term)):
            term = term[:-1]
            self.char_index-=1
            break        
      if (state == None):
        if (not (term == ' ' or term == '\n' or term=='' or term =='\t')):
          print("erro")

    self.add_token_based_on_state(term, state)

    if (not end_of_file):
      if (char == '\n'):
        self.current_line+= 1

      self.read_next_token()
  
  # #colocar o termo na lista de tokens
  #   #palavra reservada ou delimitador
  #   if (state == 'ALPHA'): #verifica se tem palavras reservadas
  #     keyword = False
  #     for key_token, lexeme_value in RESERVED_KEYWORDS.items():
  #       if (term == lexeme_value):
  #         self.tokens.append(Token(token=key_token, lexeme=term, line=self.current_line))
  #         keyword = True
  #         break
  #     if (not keyword):
  #       self.tokens.append(Token(token='IDENTIFIER', lexeme=term, line=self.current_line))
  #   # IDENTIFIER
  #   elif (state == 'ALPHANUM'):
  #     self.tokens.append(Token(token='IDENTIFIER', lexeme=term, line=self.current_line))
  #   # NUMERIC
  #   elif (state == 'NUMERIC'):
  #     self.tokens.append(Token(token='NUMERIC', lexeme=term, line=self.current_line))

  #   if (not end_of_file):
  #     self.read_next_token(code)
  
  # 
  
  def run(self):
    self.read_next_token()
    return self.tokens, self.symbols_table

  def add_token_based_on_state(self, lexeme: str, state: str):
     # CAN BE RESERVED KEY_WORD OR Symbol
    if (state == 'ALPHA'):
      keyword = False
      for key_token, lexeme_value in RESERVED_KEYWORDS.items():
        if (lexeme == lexeme_value):
          self.tokens.append(Token(token=key_token, lexeme=lexeme, line=self.current_line))
          keyword = True
          break
      if (not keyword):
        self.tokens.append(Token(token='IDENTIFIER', lexeme=lexeme, line=self.current_line))
        self.symbols_table.append(Symbol(lexeme=lexeme, line=self.current_line))
    # Symbol
    elif (state == 'ALPHANUM'):
      self.tokens.append(Token(token='IDENTIFIER',lexeme=lexeme, line=self.current_line))
      self.symbols_table.append(Symbol(lexeme=lexeme, line=self.current_line))
    # NUMERIC
    elif (state == 'NUMERIC'):
      self.tokens.append(Token(token='NUMERIC', lexeme=lexeme, line=self.current_line))
    elif (state == 'DELIMITER'):
      self.tokens.append(Token(token=self.is_delimiter(lexeme), lexeme=lexeme, line=self.current_line))

  def __str__(self):
    str = '--------------\n'
    for token in self.tokens:
      str += f'({token.token}: "{token.lexeme}" - {token.line}), '

    return str