#responsável por analisar a sequência de tokens gerada pelo analisador léxico.
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

    #esse método vai consumir o token atual se ele corresponder ao tipo esperado
    def consume_token(self, token_type): #recebe um tipo como parâmetro

        #verifica se existe um token atual e se o tipo do token atual (current_token.token) corresponde ao token_type recebido como parâmetro
        if self.current_token and self.current_token.token == token_type:
            #se a condição for verdadeira, chama o next_token simbolizando que aquele token foi consumido
            self.next_token()
        else: ##gera um erro indicando que o token esperado não foi encontrado
            self.error(f"Esperado token {token_type}, mas foi encontrado {self.current_token}")

    #método chamado quando ocorre um erro durante a análise sintática
    def error(self, message): #parâmetro mensagem de erro
        #lança uma exceção SyntaxError com a mensagem de erro formatada, incluindo a linha onde o erro ocorreu (se disponível)
        raise SyntaxError(f"Erro na linha {self.current_token.line if self.current_token else 'unknown'}: {message}")

    #o ponto de entrada para a análise sintática, chamando o método programa()
    def parse(self):
        self.programa()

    #método que representa a regra de análise para o início do programa.
    def programa(self):
        self.consume_token('HEADER_PROGRAM') #Consome o token de cabeçalho do programa.
        self.consume_token('IDENTIFIER') #Consome o identificador do programa.
        self.consume_token('SEMICOLON') #Consome o ponto e vírgula após o identificador.
        self.corpo() #Chama o método corpo para analisar o corpo do programa.

    #método p corpo do programa, pode incluir declarações de variáveis, sub-rotinas e comandos.
    def corpo(self):
        #if self.current_token.token == 'IDENTIFIER':
        #    self.declaracao_de_variaveis()
        #if self.current_token.token == 'HEADER_VAR':
        #    self.declaracao_de_variaveis()
        if self.current_token.token in ('int', 'bool'): #INT or BOOL"
            self.declaracao_de_variaveis()

        #Se o token atual for 'HEADER_FUNC' ou 'HEADER_PROC', ele chama declaracao_de_sub_rotinas()
        if self.current_token.token == 'HEADER_FUNC' or self.current_token.token == 'HEADER_PROC':
            self.declaracao_de_sub_rotinas()
        self.comandos()


    def declaracao_de_variaveis(self): #lida com a declaração de variáveis
        self.tipo() #chama a função tipo p analisar o tipo da variável
        self.lista_de_identificadores() 
        self.consume_token('SEMICOLON') #consome o token 'SEMICOLON'.

    def tipo(self): #analisa o tipo da variável
        if self.current_token.token in {'INT', 'BOOL'}: 
            #Se o token atual estiver em {'int', 'bool'}, consome o token correspondente
            #self.consume_token(self.current_token.token)
            self.next_token()
        else:
            #Caso contrário, gera um erro indicando que o tipo esperado é 'int' ou 'bool'.
            self.error("Tipo esperado: 'int' ou 'bool'")

    def lista_de_identificadores(self): #lida com a análise da lista de identificadores (nomes de variáveis)
        self.consume_token('IDENTIFIER')
        #consome um token 'IDENTIFIER', que representa o nome de uma variável
        #entra em um loop que verifica se o token atual é vírgula
        while self.current_token.token == 'COMMA':
            #Se for, consome a vírgula e, em seguida, consome outro token 'IDENTIFIER'. Esse processo continua enquanto houver vírgulas na lista de identificadores
            self.consume_token('COMMA')
            self.consume_token('IDENTIFIER')

    #método lida com a declaração de sub-rotinas (funções ou procedimentos)
    def declaracao_de_sub_rotinas(self):
        #Ele verifica o tipo de cabeçalho atual (se é 'HEADER_PROC' ou 'HEADER_FUNC') e chama o método respectivo
        if self.current_token.token == 'HEADER_PROC':
            self.declaracao_de_procedimento()
        elif self.current_token.token == 'HEADER_FUNC':
            self.declaracao_de_funcao()

    def declaracao_de_procedimento(self): #lida com a declaração de procedimentos
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
        self.consume_token('HEADER_FUNC')
        self.consume_token('IDENTIFIER')
        self.consume_token('OPEN_PARENTHESES')
        if self.current_token.token != 'CLOSE_PARENTHESES':
            self.lista_de_parametros()
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('COLON') #indica o tipo de retorno da função, dois pontos
        self.tipo() #tipo do retorno
        self.consume_token('OPEN_BRACKET')
        self.corpo() #o método corpo analisa o corpo da função
        self.retorno() #analisa a expressão de retorno da função
        self.consume_token('CLOSE_BRACKET')

    def lista_de_parametros(self):
        self.parametro()
        while self.current_token.token == 'COMMA':
            self.consume_token('COMMA')
            self.parametro() #Esse processo continua enquanto houver vírgulas na lista de parâmetros

    def parametro(self): #Este método lida com a análise de um único parâmetro
        self.tipo()
        self.consume_token('IDENTIFIER')

    def comandos(self): #entra em loop enquanto o token atual estiver em {'IDENTIFIER', 'IF', 'WHILE', 'RETURN', 'INPUT', 'PRINT'}.
        while self.current_token.token in {'IDENTIFIER', 'IF', 'WHILE', 'RETURN', 'INPUT', 'PRINT'}:
            self.comando() #Para cada token válido, chama o método comando()

    def comando(self): #ida com um comando específico com base no tipo de token atual
        if self.current_token.token == 'IDENTIFIER':
            self.atribuicao_ou_chamada()
        elif self.current_token.token == 'IF':
            self.comando_condicional()
        elif self.current_token.token == 'WHILE':
            self.comando_enquanto()
        elif self.current_token.token == 'RETURN':
            self.retorno()
        elif self.current_token.token == 'INPUT':
            self.comando_leitura()
        elif self.current_token.token == 'PRINT':
            self.comando_escrita()

    def atribuicao_ou_chamada(self): #lida com a análise de uma atribuição ou chamada de procedimento
        if self.current_token.token == 'IDENTIFIER':
            self.consume_token('IDENTIFIER')
            #verifica se o próximo token é operador de atribuição. Se for, chama o método atribuicao
            if self.current_token.token == 'ASSIGNMENT_OP':
                self.atribuicao()
            elif self.current_token.token == 'OPEN_PARENTHESES': #se for abre parenteses, chamada de proc
                self.chamada_de_procedimento()

    def atribuicao(self): #Este método lida com a análise de uma atribuição
        self.consume_token('ASSIGNMENT_OP')
        self.expressao() #para analisar a expressão à direita da atribuição
        self.consume_token('SEMICOLON')

    def chamada_de_procedimento(self): #lida com a chamada de um procedimento
        self.consume_token('OPEN_PARENTHESES')
        if self.current_token.token != 'CLOSE_PARENTHESES':
            self.lista_de_expressoes()
        self.consume_token('CLOSE_PARENTHESES') #indicando o fim dos argumentos da chamada
        self.consume_token('SEMICOLON')

    def chamada_de_funcao(self): #lida com a chamada de uma função
        self.consume_token('OPEN_PARENTHESES')
        if self.current_token.token != 'CLOSE_PARENTHESES':
            self.lista_de_expressoes()
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('SEMICOLON')

    def comando_condicional(self): #lida com a estrutura condicional if
        self.consume_token('IF')
        self.consume_token('OPEN_PARENTHESES')
        self.expressao() #Em seguida, analisa a expressão entre parênteses (condição do if)
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('OPEN_BRACKET') #consome o token 'OPEN_BRACKET', indicando o início do bloco de código do if
        self.comandos() #Chama o método comandos() para analisar os comandos dentro do bloco
        self.consume_token('CLOSE_BRACKET') #consome o token 'CLOSE_BRACKET', indicando o fim do bloco do if
        if self.current_token.token == 'ELSE': #Se houver um else, consome o token 'ELSE', analisa o bloco de código do else e consome o token de fechamento do bloco
            self.consume_token('ELSE')
            self.consume_token('OPEN_BRACKET')
            self.comandos()
            self.consume_token('CLOSE_BRACKET')

    def comando_enquanto(self): #Este método lida com a estrutura de loop while
        self.consume_token('WHILE')
        self.consume_token('OPEN_PARENTHESES')
        self.expressao() #analisa a expressão entre parênteses (condição do while) usando o método expressao()
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('OPEN_BRACKET')
        self.comandos() #chama o método comandos() para analisar os comandos dentro do bloco
        if self.current_token.token == 'BREAK': 
            self.comando_de_parada() #Se houver um token break, chama o comando_de_parada()
        if self.current_token.token == 'CONTINUE':
            self.comando_de_continuacao() #Se houver continue, chama o método comando_de_continuacao()
        self.consume_token('CLOSE_BRACKET')

    def comando_leitura(self): #lida com a operação de leitura de entrada.
        self.consume_token('INPUT')
        self.consume_token('OPEN_PARENTHESES')
        #n devia ter nada aqui???
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('SEMICOLON')

    def comando_escrita(self): #lida com a operação de escrita de saída (impressão)
        self.consume_token('PRINT')
        self.consume_token('OPEN_PARENTHESES')
        self.expressao() #analisa a expressão dentro dos parênteses usando o método expressao()
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('SEMICOLON')

    def comando_de_parada(self): #lida com o comando break dentro de um loop
        self.consume_token('BREAK')
        self.consume_token('SEMICOLON')

    def comando_de_continuacao(self): #lida com o comando continue dentro de um loop
        self.consume_token('CONTINUE')
        self.consume_token('SEMICOLON')

    def retorno(self): #lida com a análise de uma instrução de retorno
        self.consume_token('RETURN')
        self.expressao() #analisa a expressão usando o método expressao()
        self.consume_token('SEMICOLON')

    def lista_de_expressoes(self): #lida com a análise de uma lista de expressões
        self.expressao() #Começa chamando o método expressao()
        while self.current_token.token == 'COMMA': #Entra em um loop while que verifica se o token atual é 'COMMA'
            self.consume_token('COMMA') #Se for, consome a vírgula e chama dnv o método expressao() para analisar a próxima expressão
            self.expressao()

    def expressao(self): #lida com a análise de uma expressão
        self.expressao_simples() #chama o método expressao_simples()
        # verifica se o token atual está em (operadores de comparação)
        if self.current_token.token in {'EQUALS_OP', 'NOT_EQUAL_OP', 'LESS_THAN_OP', 'LESS_OR_EQ_OP', 'GREATER_THAN_OP', 'GREATER_OR_EQ_OP'}:
            #Se for o caso, chama novamente o método expressao_simples() para analisar a segunda parte da expressão
            self.consume_token(self.current_token.token)
            self.expressao_simples()

    def expressao_simples(self): #lida com a análise de uma expressão simples.
        if self.current_token.token in {'ADD', 'LESS'}: #Verifica se o token atual está em (operadores de adição ou subtração)
            self.consume_token(self.current_token.token)
        self.termo() #Chama o método termo() para analisar o token atual (ou próximo se tiver sido consumido)
        while self.current_token.token in {'ADD', 'LESS', 'OR'}:
            #Entra em um loop que verifica se o token atual está em (operadores lógicos)
            self.consume_token(self.current_token.token)
            self.termo() #consome o operador e chama novamente o método termo() para analisar o próximo termo

    def termo(self): #Este método lida com a análise de termos em expressões
        self.fator() #Começa chamando o método fator()
        while self.current_token.token in {'MULT', 'DIV', 'AND'}:
            #Entra em um loop que verifica se o token atual está em (operadores de multiplicação, divisão ou lógicos)
            #Se for o caso, consome o operador e chama novamente o método fator() para analisar o próximo fator
            self.consume_token(self.current_token.token)
            self.fator()

    def fator(self): #lida com a análise de fatores em expressões
        if self.current_token.token == 'NUMERIC': #Se for 'NUMERIC', consome o token (representando um valor numérico)
            self.consume_token('NUMERIC') 
        elif self.current_token.token == 'IDENTIFIER':
            self.consume_token('IDENTIFIER')
        #Se for 'OPEN_PARENTHESES', consome o parêntese de abertura, analisa a expressão dentro dos parênteses usando o método expressao(), e consome o parêntese de fechamento
        elif self.current_token.token == 'OPEN_PARENTHESES':
            self.consume_token('OPEN_PARENTHESES')
            self.expressao()
            self.consume_token('CLOSE_PARENTHESES')
        
        #Se for 'true' ou 'false', consome o token (representando valores booleanos). Se for 'NOT', consome o token e chama novamente o método fator()
        elif self.current_token.token == 'true' or self.current_token.token == 'false':
            self.consume_token(self.current_token.token)
        elif self.current_token.token == 'NOT':
            self.consume_token('NOT')
            self.fator()
        else:
            self.error("Token inesperado em fator")