#responsável por analisar a sequência de tokens gerada pelo analisador léxico.

YELLOW = '\033[33m'
RESET = '\033[0m'
RED = '\033[31m'

class Parser:
    def __init__(self, lexer): #lexer no main = Lexer(raw_code) ou seja, o codigo-fonte executado no lexer
        self.lexer = lexer #armazena aqui
        #Executa o lexer p obter a lista de tokens e a tabela de símbolos
        self.tokens, self.symbols_table = self.lexer.run()
        self.current_token = None #token atual a ser analisado
        self.token_index = -1 #Índice do token atual, -1 p facilitar o avanço no primeiro next_token
        self.next_token() #Chama o método next_token() para avançar para o primeiro token

    #o método avança p próximo token na lista, mantendo o controle do índice e atualizando o token atual. permitindo que o analisador percorra os tokens sequencialmente
    def next_token(self):
        self.token_index += 1 #Incrementa o índice do token
        
        #Verifica se o índice do token é menor que o tamanho da lista de tokens. Se for verdadeiro, significa que ainda há tokens a serem processados.
        if self.token_index < len(self.tokens):
            #Atualiza o token atual p acessar o token na posição do índice atual
            self.current_token = self.tokens[self.token_index] 
        else: #Caso n haja mais tokens, self.current_token como None indicará o fim dos tokens
            self.current_token = None
        print(f"{YELLOW}[next_token] Indice: {self.token_index}, Token: {self.current_token}{RESET}")

    #esse método vai consumir o token atual se ele corresponder ao tipo esperado
    def consume_token(self, token_type): #recebe um tipo como parâmetro

        #verifica se existe um token atual e se o tipo do token atual (current_token.token) corresponde ao token_type recebido como parâmetro
        if self.current_token and self.current_token.token == token_type:
            #se a condição for verdadeira, chama o next_token simbolizando que aquele token foi consumido
            print(f"[consume_token] Consumindo token: {self.current_token}")
            self.next_token()
        else: ##gera um erro indicando que o token esperado não foi encontrado
            self.error(f"{YELLOW}Esperado token {token_type}, mas foi encontrado {self.current_token}{RESET}")

    #método chamado quando ocorre um erro durante a análise sintática
    def error(self, message): #parâmetro mensagem de erro
        #lança uma exceção SyntaxError com a mensagem de erro formatada, incluindo a linha onde o erro ocorreu (se disponível)
        raise SyntaxError(f"{RED}Erro na linha {self.current_token.line if self.current_token else 'unknown'}: {message}{RESET}")

    #o ponto de entrada para a análise sintática, chamando o método programa()
    def parse(self):
        print("[parse] Iniciando análise sintática")
        self.programa()

    #método que representa a regra de análise para o início do programa.
    def programa(self):
        print("[programa] Analisando programa")
        self.consume_token('HEADER_PROGRAM') #Consome o token de cabeçalho do programa.
        self.consume_token('IDENTIFIER') #Consome o identificador do programa.
        self.consume_token('SEMICOLON') #Consome o ponto e vírgula após o identificador.
        self.corpo() #Chama o método corpo para analisar o corpo do programa.

    #método p corpo do programa, pode incluir declarações de variáveis, sub-rotinas e comandos.
    def corpo(self):
        print("[corpo] Analisando corpo")
        while self.current_token:
            if self.current_token.token in ('INT', 'BOOL'):
                self.declaracao_de_variaveis()
            elif self.current_token.token in ('HEADER_FUNC', 'HEADER_PROC'):
                self.declaracao_de_sub_rotinas()
            else:
                break
        self.comandos()


    def declaracao_de_variaveis(self): #lida com a declaração de variáveis
        print("[declaracao_de_variaveis] Analisando declaracao de variaveis")
        self.tipo() #chama a função tipo p analisar o tipo da variável
        self.lista_de_identificadores() 
        self.consume_token('SEMICOLON') #consome o token 'SEMICOLON'.

    def tipo(self): #analisa o tipo da variável
        if self.current_token.token in {'INT', 'BOOL'}:
            print(f"[tipo] Tipo encontrado: {self.current_token.token}")
            #Se o token atual estiver em {'int', 'bool'}, consome o token correspondente
            #self.consume_token(self.current_token.token)
            self.next_token()
        else:
            #Caso contrário, gera um erro indicando que o tipo esperado é 'int' ou 'bool'.
            self.error("Tipo esperado: 'int' ou 'bool'")

    def lista_de_identificadores(self): #lida com a análise da lista de identificadores (nomes de variáveis)
        print("[lista_de_identificadores] Analisando lista de identificadores")
        self.consume_token('IDENTIFIER')
        #consome um token 'IDENTIFIER', que representa o nome de uma variável
        #entra em um loop que verifica se o token atual é vírgula
        while self.current_token.token == 'COMMA':
            #Se for, consome a vírgula e, em seguida, consome outro token 'IDENTIFIER'. Esse processo continua enquanto houver vírgulas na lista de identificadores
            self.consume_token('COMMA')
            self.consume_token('IDENTIFIER')

    #método lida com a declaração de sub-rotinas (funções ou procedimentos)
    def declaracao_de_sub_rotinas(self):
        print("[declaracao_de_sub_rotinas] Analisando declaracao de sub-rotinas")
        #Ele verifica o tipo de cabeçalho atual (se é 'HEADER_PROC' ou 'HEADER_FUNC') e chama o método respectivo
        if self.current_token.token == 'HEADER_PROC':
            self.declaracao_de_procedimento()
        elif self.current_token.token == 'HEADER_FUNC':
            self.declaracao_de_funcao()

    def declaracao_de_procedimento(self): #lida com a declaração de procedimentos
        print("[declaracao_de_procedimento] Analisando procedimento")
        self.consume_token('HEADER_PROC')
        self.consume_token('IDENTIFIER')
        self.consume_token('OPEN_PARENTHESES')
        if self.current_token.token != 'CLOSE_PARENTHESES': #caso contrário, significa que não há parâmetros
            self.lista_de_parametros()
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('OPEN_BRACKET')
        self.corpo()
        self.consume_token('CLOSE_BRACKET')

    def declaracao_de_funcao(self): #lida com a declaração de funções.
        print("[declaracao_de_funcao] Analisando funcao")
        self.consume_token('HEADER_FUNC')
        self.consume_token('IDENTIFIER')
        self.consume_token('OPEN_PARENTHESES')
        if self.current_token.token != 'CLOSE_PARENTHESES':
            self.lista_de_parametros()
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('COLON') #indica o tipo de retorno da função, dois pontos
        self.tipo() #tipo do retorno
        self.consume_token('OPEN_BRACKET')
        self.corpo_funcao()
        self.consume_token('CLOSE_BRACKET')

    def corpo_funcao(self):
        print("[corpo_funcao] Analisando corpo da funcao")
        # Analisando comandos dentro do corpo da função
        '''self.comandos()
        # Verifica se há uma declaração de retorno ao final do corpo da função
        if self.current_token.token == 'RETURN':
            self.retorno()
        else:
            print("Aviso: Funcao sem comando RETURN")
        self.retorno()'''

        return_found = False

        while self.current_token.token != 'CLOSE_BRACKET':
            if self.current_token.token == 'INT' or self.current_token.token == 'FLOAT':
                self.declaracao_de_variaveis()
            elif self.current_token.token == 'RETURN':
                self.retorno()
                return_found = True
            else:
                self.comandos()
        
        if not return_found:
            self.error("Funcao deve ter um comando RETURN")


    def retorno(self): #lida com a análise de uma instrução de retorno
        print("[retorno] Analisando retorno")
        self.consume_token('RETURN')
        self.expressao() #analisa a expressão usando o método expressao()
        self.consume_token('SEMICOLON')

    def lista_de_parametros(self):
        print("[lista_de_parametros] Analisando lista de parametros")
        self.parametro()
        while self.current_token.token == 'COMMA':
            self.consume_token('COMMA')
            self.parametro() #Esse processo continua enquanto houver vírgulas na lista de parâmetros

    def parametro(self): #Este método lida com a análise de um único parâmetro
        print("[parametro] Analisando parametro")
        self.tipo()
        self.consume_token('IDENTIFIER')

    def comandos(self): #entra em loop enquanto o token atual estiver em {'IDENTIFIER', 'IF', 'WHILE', 'RETURN', 'INPUT', 'PRINT'}.
        print("[comandos] Analisando comandos")
         #!!!!!!!!! essa verificação de return não seria aqui e sim em da função de FUNCTION
        # Verifica se current_token é None antes de acessar o atributo token (p impedir a análise de continuar se o current_token for none)
        while self.current_token and self.current_token.token in {'IDENTIFIER', 'IF', 'WHILE', 'INPUT', 'PRINT', 'BREAK', 'CONTINUE'}:
            self.comando() #Para cada token válido, chama o método comando()

    def comando(self): #ida com um comando específico com base no tipo de token atual
        print(f"[comando] Analisando comando: {self.current_token.token}")
        if self.current_token.token == 'IDENTIFIER':
            self.atribuicao_ou_chamada()
        elif self.current_token.token == 'IF':
            self.comando_condicional()
        elif self.current_token.token == 'WHILE':
            self.comando_enquanto()
        # elif self.current_token.token == 'RETURN': # !!!!! de acordo com a gramatica a verificação de return fica dentro de <declaração de função>
        #     self.retorno()
        elif self.current_token.token == 'INPUT':
            self.comando_leitura()
        elif self.current_token.token == 'PRINT':
            self.comando_escrita()
        elif self.current_token.token == 'BREAK':
            self.comando_de_parada()
        elif self.current_token.token == 'CONTINUE':
            self.comando_de_continuacao()

    def atribuicao_ou_chamada(self):
        print("[atribuicao_ou_chamada] Analisando atribuicao ou chamada")
        if self.current_token.token == 'IDENTIFIER':
            # Salva o identificador atual para determinar se é uma função ou um procedimento.
            identifier_token = self.current_token
            self.consume_token('IDENTIFIER')
            if self.current_token.token == 'ASSIGNMENT_OP':
                self.atribuicao()
            elif self.current_token.token == 'OPEN_PARENTHESES': 
                # Verificar se é uma chamada de função ou procedimento
                if self.next_token.token == 'CLOSE_PARENTHESES' or self.next_token.token == 'IDENTIFIER':
                    self.chamada_de_funcao()  # Chamada de função
                else:
                    self.chamada_de_procedimento()  # Chamada de procedimento

    def atribuicao(self): #Este método lida com a análise de uma atribuição
        print("[atribuicao] Analisando atribuicao")
        self.consume_token('ASSIGNMENT_OP')
        self.expressao() #para analisar a expressão à direita da atribuição
        self.consume_token('SEMICOLON')

    def chamada_de_procedimento(self): #lida com a chamada de um procedimento
        print("[chamada_de_procedimento] Analisando chamada de procedimento")
        self.consume_token('OPEN_PARENTHESES')
        if self.current_token.token != 'CLOSE_PARENTHESES':
            self.lista_de_expressoes()
        self.consume_token('CLOSE_PARENTHESES') #indicando o fim dos argumentos da chamada
        self.consume_token('SEMICOLON')

    def chamada_de_funcao(self): #lida com a chamada de uma função
        print("[chamada_de_funcao] Analisando chamada de funcao")
        self.consume_token('OPEN_PARENTHESES')
        if self.current_token.token != 'CLOSE_PARENTHESES':
            self.lista_de_expressoes()
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('SEMICOLON')

    def comando_condicional(self): #lida com a estrutura condicional if
        print("[comando_condicional] Analisando comando condicional")
        self.consume_token('IF')
        self.consume_token('OPEN_PARENTHESES')
        '''self.expressao() #Em seguida, analisa a expressão entre parênteses (condição do if)
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('OPEN_BRACKET') #consome o token 'OPEN_BRACKET', indicando o início do bloco de código do if
        self.comandos() #Chama o método comandos() para analisar os comandos dentro do bloco
        self.consume_token('CLOSE_BRACKET') #consome o token 'CLOSE_BRACKET', indicando o fim do bloco do if
        if self.current_token.token == 'ELSE': #Se houver um else, consome o token 'ELSE', analisa o bloco de código do else e consome o token de fechamento do bloco
            self.consume_token('ELSE')
            self.consume_token('OPEN_BRACKET')
            self.comandos()
            self.consume_token('CLOSE_BRACKET')'''

        # Verifica se há uma expressão válida após '('
        if self.is_valid_expression_start(self.current_token.token):
            self.expressao()  # Analisa a expressão condicional
        else:
            self.error("Esperada expressao condicional valida apos 'if ('")

        if self.current_token.token == 'CLOSE_PARENTHESES':
            self.consume_token('CLOSE_PARENTHESES')
        else:
            self.error("Esperado ')' apos expressao condicional")
        
        self.consume_token('OPEN_BRACKET')
        self.comandos()
        self.consume_token('CLOSE_BRACKET')

        if self.current_token.token == 'ELSE':
            self.consume_token('ELSE')
            self.consume_token('OPEN_BRACKET')
            self.comandos()
            self.consume_token('CLOSE_BRACKET')

    '''Verificar se o token atual pode ser o início de uma expressão válida.
    Uma expressão válida pode começar com IDENTIFIER, NUMERIC, BOOL, OPEN_PARENTHESES
    Argumento: token: O token atual a ser verificado.
    Retorno bool: True se o token pode iniciar uma expressão válida, False caso contrário.'''
    def is_valid_expression_start(self, token):
        valid_starts = [
            'IDENTIFIER',
            'NUMERIC',
            'BOOL',
            'OPEN_PARENTHESES',
        ]
        return token in valid_starts

    '''Verificar se a expressão é uma expressão completa com pelo menos um operador p garantir que a expressão não seja apenas um único identificador, etc
    Retorno: True se for uma expressão completa, False se for um literal isolado.'''
    def is_valid_complete_expression(self):
        # Salva o token inicial e sua posição
        start_token = self.current_token
        token_index = self.token_index
        
        # Analisa uma expressão completa
        self.expressao()
        
        # Verifica se a expressão consiste em apenas um token
        if token_index == self.token_index or self.current_token.token == 'CLOSE_PARENTHESES':
            # Se o índice do token não mudou, a expressão é inválida
            return False
            # A expressão é válida se o índice do token mudou
        return True

    def comando_enquanto(self): #Este método lida com a estrutura de loop while
        print("[comando_enquanto] Analisando loop enquanto")
        self.consume_token('WHILE')
        self.consume_token('OPEN_PARENTHESES')
        self.expressao() #analisa a expressão entre parênteses (condição do while) usando o método expressao()
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('OPEN_BRACKET')
        self.comandos() #chama o método comandos() para analisar os comandos dentro do bloco
        self.consume_token('CLOSE_BRACKET')

    def comando_leitura(self): #lida com a operação de leitura de entrada.
        print("[comando_leitura] Analisando comando de leitura")
        self.consume_token('INPUT')
        self.consume_token('OPEN_PARENTHESES')
        #n devia ter nada aqui???
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('SEMICOLON')

    def comando_escrita(self): #lida com a operação de escrita de saída (impressão)
        print("[comando_escrita] Analisando comando de escrita")
        self.consume_token('PRINT')
        self.consume_token('OPEN_PARENTHESES')
        self.expressao() #analisa a expressão dentro dos parênteses usando o método expressao()
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('SEMICOLON')

    def comando_de_parada(self): #lida com o comando break dentro de um loop
        print("[comando_de_parada] Analisando comando de parada")
        self.consume_token('BREAK')
        self.consume_token('SEMICOLON')

    def comando_de_continuacao(self): #lida com o comando continue dentro de um loop
        print("[comando_de_continuacao] Analisando comando de continuacao")
        self.consume_token('CONTINUE')
        self.consume_token('SEMICOLON')

    def retorno(self): #lida com a análise de uma instrução de retorno
        print("[retorno] Analisando retorno")
        self.consume_token('RETURN')
        self.expressao() #analisa a expressão usando o método expressao()
        self.consume_token('SEMICOLON')

    def lista_de_expressoes(self): #lida com a análise de uma lista de expressões
        print("[lista_de_expressoes] Analisando lista de expressoes")
        self.expressao() #Começa chamando o método expressao()
        while self.current_token.token == 'COMMA': #Entra em um loop while que verifica se o token atual é 'COMMA'
            self.consume_token('COMMA') #Se for, consome a vírgula e chama dnv o método expressao() para analisar a próxima expressão
            self.expressao()

    def expressao(self): #lida com a análise de uma expressão
        print("[expressao] Analisando expressao")
        self.expressao_simples() #chama o método expressao_simples()
        # verifica se o token atual é um operador de comparação
        if self.current_token and self.current_token.token in ('LESS_THAN_OP', 'GREATER_THAN_OP', 'EQUALS_OP', 'NOT_EQUAL_OP', 'LESS_EQUAL_OP', 'GREATER_EQUAL_OP'):
            operador = self.current_token.token
            self.consume_token(operador)
            self.expressao_simples()

            '''# Após um operador de comparação, deve haver outra expressão simples ou um literal booleano
            if self.is_valid_expression_start(self.current_token.token):
                self.expressao_simples()
            elif self.current_token.token != 'CLOSE_PARENTHESES':
                self.error(f"Esperada expressao valida apos o operador '{operador}', mas encontrado '{self.current_token.lexeme}'")'''

    def expressao_simples(self): #lida com a análise de uma expressão simples
        print("[termo] Analisando expressao_simples")
        self.termo()
        while self.current_token.token in ('ADD', 'SUB'):
            print(f"[expressao_simples] Operador encontrado: {self.current_token.token}")
            operador = self.current_token.token
            self.consume_token(operador)
            self.termo()

    def termo(self): #Este método lida com a análise de termos em expressões
        print("[termo] Analisando termo")
        self.fator() #Começa chamando o método fator()
        while self.current_token.token in {'MULT', 'DIV'}:
            print(f"[termo] Operador encontrado: {self.current_token.token}")
            operador = self.current_token.token
            self.consume_token(operador)
            self.fator()

    def fator(self): #lida com a análise de fatores em expressões
        print("[fator] Analisando fator")
        if self.current_token.token == 'IDENTIFIER':
            self.consume_token('IDENTIFIER')
            if self.current_token.token == 'OPEN_PARENTHESES':
                self.consume_token('OPEN_PARENTHESES')
                if self.current_token.token != 'CLOSE_PARENTHESES':
                    self.lista_de_expressoes()
                self.consume_token('CLOSE_PARENTHESES')
        elif self.current_token.token == 'NUMERIC':
            self.consume_token('NUMERIC')
        #elif self.current_token.token == 'BOOL':  # Novo caso para booleanos
        #    self.consume_token('BOOL')
        elif self.current_token.token == 'OPEN_PARENTHESES':
            self.consume_token('OPEN_PARENTHESES')
            self.expressao()
            self.consume_token('CLOSE_PARENTHESES')
        else:
            raise SyntaxError(f"{RED}Erro na linha {self.current_token.line}: token inesperado '{self.current_token.lexeme}'{RESET}")