from pickle import NONE
from lexer.Token import Token
from lexer.Symbol import Symbol
from lexer.reserverd_keywords import RESERVED_KEYWORDS
from lexer.delimiters import DELIMITERS 

'''O Analisador léxico pega os caracteres de entrada e os transforma em tokens
- Lê os caracteres de entrada e os agrupa em lexemas
- Ignora espaços, tabulações e saltos de linha.
Ex.: o número 25432 de entrada será um token, em vez de cada número ser um token
- Token é um terminal. Possui atributos com informações adicionais sobre o símbolo.
Ex.: valor, tipo, escopo, etc.'''

class Lexer:
    def __init__(self, code: str):
        self.tokens: list[Token] = []
        self.symbols_table: list[Symbol] = []
        self.char_index = 0  # Índice do caractere que está sendo lido
        self.current_line = 1  # Linha do caractere que está sendo lido
        self.code = code

    def is_delimiter(self, char: str):
        for key_token, lexeme_value in DELIMITERS.items():
            if char == lexeme_value:
                return key_token
        return None   

    # Começar a ler os tokens
    def read_next_token(self):
        state = None  # Tipo de token: delimitador, letra ou número
        term = ''  # Armazena cada caractere e depois forma um token
        end_of_file = False  # Fim do arquivo 

        while True:
            if self.char_index == len(self.code):
                end_of_file = True
                break

            char = self.code[self.char_index]  # Pega o caractere e marca sua posição
            term += char  # Incrementa o caractere no token (termo) atual que está sendo lido
            self.char_index += 1
            print(f"Estado anterior: {state} - char '{char}'")

            # Verifica o estado atual
            match state:
                case None:
                    if char.isspace():
                        term = term[:-1]  # Remove o caractere de espaço ou nova linha
                    elif self.is_delimiter(term):
                        state = 'DELIMITER'
                    elif char.isalpha():
                        state = 'ALPHA'
                    elif char.isnumeric():
                        state = 'NUMERIC'
                    elif char in ("!", '|', '&'):
                        continue
                    else:
                        print("Erro")
                        term = term[:-1]  # Remove o caractere inválido
                        break

                case 'ALPHA':
                    if char.isalpha():
                        continue
                    elif char.isnumeric():
                        state = 'ALPHANUM'
                    elif self.is_delimiter(char) or char in ("!", '|', '&'):
                        term = term[:-1]
                        self.char_index -= 1
                        break
                    else:
                        print("Erro")
                        term = term[:-1]  # Remove o caractere inválido
                        break

                case 'ALPHANUM':
                    if char.isalnum():
                        continue
                    elif self.is_delimiter(char) or char in ("!", '|', '&'):
                        term = term[:-1]
                        self.char_index -= 1
                        break
                    else:
                        print("Erro")
                        term = term[:-1]  # Remove o caractere inválido
                        break
                
                case 'NUMERIC':
                    if char.isnumeric():
                        continue
                    elif self.is_delimiter(char):
                        term = term[:-1]
                        self.char_index -= 1
                        break
                    else:
                        print("Erro")
                        term = term[:-1]  # Remove o caractere inválido
                        break

                case 'DELIMITER':
                    if not self.is_delimiter(term):
                        term = term[:-1]
                        self.char_index -= 1
                        break

            if state is None and term not in (' ', '\n', '', '\t'):
                print("Erro")

        self.add_token_based_on_state(term, state)

        if not end_of_file:
            if char == '\n':
                self.current_line += 1

            self.read_next_token()

    def run(self):
        self.read_next_token()
        return self.tokens, self.symbols_table

    def add_token_based_on_state(self, lexeme: str, state: str):
        match state:
            case 'ALPHA':
                keyword = False
                for key_token, lexeme_value in RESERVED_KEYWORDS.items():
                    if lexeme == lexeme_value:
                        self.tokens.append(Token(token=key_token, lexeme=lexeme, line=self.current_line))
                        keyword = True
                        break
                if not keyword:
                    self.tokens.append(Token(token='IDENTIFIER', lexeme=lexeme, line=self.current_line))
                    self.symbols_table.append(Symbol(lexeme=lexeme, line=self.current_line))
            
            case 'ALPHANUM':
                self.tokens.append(Token(token='IDENTIFIER', lexeme=lexeme, line=self.current_line))
                self.symbols_table.append(Symbol(lexeme=lexeme, line=self.current_line))
            
            case 'NUMERIC':
                self.tokens.append(Token(token='NUMERIC', lexeme=lexeme, line=self.current_line))
            
            case 'DELIMITER':
                self.tokens.append(Token(token=self.is_delimiter(lexeme), lexeme=lexeme, line=self.current_line))

    def __str__(self):
        result = '-------------- Lexer ----------------\n'
        for token in self.tokens:
            result += f'(token: {token.token}; lexema: "{token.lexeme}" - linha {token.line}),\n '
        return result
