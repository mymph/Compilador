#analisador sintático e semântico acoplados
from parser.SymbolTable import SymbolTable
from three_address_code import Three_address_code


YELLOW = '\033[33m'
RESET = '\033[0m'
RED = '\033[31m'

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens, _ = self.lexer.run()  #recebe os tokens aqui
        self.symbols_table = SymbolTable()  #inicializando a tabela de símbolos
        self.current_token = None
        self.token_index = -1
        self.next_token()

    def next_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None
        print(f"{YELLOW}[next_token] Indice: {self.token_index}, Token: {self.current_token}{RESET}")

    def consume_token(self, token_type):
        if self.current_token and self.current_token.token == token_type:
            print(f"[consume_token] Consumindo token: {self.current_token}")
            self.next_token()
        else:
            self.error(f"{YELLOW}Esperado token {token_type}, mas foi encontrado {self.current_token}{RESET}")

    def error(self, message):
        raise SyntaxError(f"{RED}Erro na linha {self.current_token.line if self.current_token else 'unknown'}: {message}{RESET}")

    def parse(self):
        print("[parse] Iniciando análise sintática")
        self.programa()

    def programa(self):
        print("[programa] Analisando programa")
        self.consume_token('HEADER_PROGRAM')
        self.consume_token('IDENTIFIER')
        self.consume_token('SEMICOLON')
        self.corpo()

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

    def declaracao_de_variaveis(self):
        print("[declaracao_de_variaveis] Analisando declaracao de variaveis")
        tipo_variavel = self.current_token.token  # INT, FLOAT, BOOL, etc.
        self.consume_token(tipo_variavel)
        while self.current_token.token == 'IDENTIFIER': #semantico
            var_name = self.current_token.lexeme
            # Insere a variável na tabela de símbolos
            try:
                self.symbols_table.insert(var_name, {'tipo': tipo_variavel, 'id': 'VARIABLE', 'valor': None})
            except Exception as e:
                self.error(str(e))  # Chama função de erro e interrompe execução
                return
            
            self.consume_token('IDENTIFIER')
            if self.current_token.token == 'COMMA':
                self.consume_token('COMMA')
            else:
                break
        self.consume_token('SEMICOLON')


    def tipo(self):
        if self.current_token.token in {'INT', 'BOOL'}:
            tipo = self.current_token.token
            print(f"[tipo] Tipo encontrado: {tipo}")
            self.next_token()
            return tipo
        else:
            self.error("Tipo esperado: 'int' ou 'bool'")

    def lista_de_identificadores(self, tipo):
        print("[lista_de_identificadores] Analisando lista de identificadores")
        identifier = self.current_token.lexeme
        self.consume_token('IDENTIFIER')
        
        # Semantica: Inserir a variável na tabela de símbolos
        try:
            self.symbols_table.insert(identifier, {'tipo': tipo})

        except Exception as e:
            print(e)
        
        while self.current_token.token == 'COMMA':
            self.consume_token('COMMA')
            identifier = self.current_token.lexeme
            self.consume_token('IDENTIFIER')

            # Inserir a variável na tabela de símbolos
            try:
                self.symbols_table.insert(identifier, {'tipo': tipo})
            except Exception as e:
                print(e)

    #método lida com a declaração de sub-rotinas (funções ou procedimentos)
    def declaracao_de_sub_rotinas(self):
        print("[declaracao_de_sub_rotinas] Analisando declaracao de sub-rotinas")
        #Ele verifica o tipo de cabeçalho atual (se é 'HEADER_PROC' ou 'HEADER_FUNC') e chama o método respectivo
        if self.current_token.token == 'HEADER_PROC':
            self.declaracao_de_procedimento()
        elif self.current_token.token == 'HEADER_FUNC':
            self.declaracao_de_funcao()

    '''Acoplando o analisador semântico à análise da declaração de procedimentos, verificar se o identificador do procedimento já foi declarado na tabela de símbolos. registrar o nome do procedimento na tabela de símbolos, como uma entrada especial que indica que é um procedimento (não retorna valor).'''
    def declaracao_de_procedimento(self):
        print("[declaracao_de_procedimento] Analisando procedimento")
        self.consume_token('HEADER_PROC')
        identifier = self.current_token.lexeme
        self.consume_token('IDENTIFIER')

        # Coletar a lista de parâmetros
        parametros = []
        self.consume_token('OPEN_PARENTHESES')
        if self.current_token.token != 'CLOSE_PARENTHESES':
            parametros = self.lista_de_parametros()  # Coleta os parâmetros
        self.consume_token('CLOSE_PARENTHESES')

        # Checagem semântica: registrar o procedimento com seus parâmetros
        try:
            self.symbols_table.insert(identifier, {'id': 'HEADER_PROC','tipo': 'HEADER_PROC', 'parametros': parametros})
        except Exception as e:
            print(e)

        self.consume_token('OPEN_BRACKET')
        self.corpo()
        self.consume_token('CLOSE_BRACKET')


    '''A declaração de funções precisa lidar com a verificação semântica de dois pontos importantes:
    O nome da função precisa ser registrado na tabela de símbolos.
    O tipo de retorno da função também precisa ser registrado e verificado.
    Modificações: adicionar a função na tabela de símbolos com o tipo de retorno e
    Verificar se o identificador já foi declarado.'''

    def declaracao_de_funcao(self):
        print("[declaracao_de_funcao] Analisando funcao")
        
        self.current_function_type = self.current_token.token
        self.consume_token('HEADER_FUNC')
        identifier = self.current_token.lexeme
        self.consume_token('IDENTIFIER')
        self.consume_token('OPEN_PARENTHESES')
        
        parametros = []  # Lista para armazenar os parâmetros
        if self.current_token.token != 'CLOSE_PARENTHESES':
            parametros = self.lista_de_parametros()
        
        self.consume_token('CLOSE_PARENTHESES')
        self.consume_token('COLON')
        tipo = self.tipo()
        
        # Registra a função na tabela de símbolos
        try:
            self.symbols_table.insert(identifier, {'id': 'HEADER_FUNC','tipo': tipo, 'retorno': tipo, 'parametros': parametros})
        except Exception as e:
            print(e)

        self.consume_token('OPEN_BRACKET')
        self.corpo_funcao()
        self.consume_token('CLOSE_BRACKET')
        self.current_function_type = None


    '''Esse método deve garantir que uma função tenha sempre um comando RETURN, já que a gramática obriga as funções a retornarem um valor. Modificações: Verificar se o retorno está de acordo com o tipo da função. O valor retornado deve ser do mesmo tipo que o declarado na função.'''

    def corpo_funcao(self):
        print("[corpo_funcao] Analisando corpo da funcao")
        return_found = False

        while self.current_token.token != 'CLOSE_BRACKET':
            if self.current_token.token in ('INT', 'BOOL'):  #tipos permitidos aqui
                self.declaracao_de_variaveis()
            elif self.current_token.token == 'RETURN':
                self.retorno()
                return_found = True
            else:
                self.comandos()

        if not return_found:
            self.error("Funcao deve ter um comando RETURN")

    def retorno(self):
        print("[retorno] Analisando retorno")
        self.consume_token('RETURN')

        # Aqui se deve garantir que a expressão seja compatível com o tipo de retorno da função
        tipo_expressao = self.expressao()  # Analisa a expressão e retorna seu tipo
        # Checagem semântica: verificar se o tipo da expressão é compatível com o tipo da função
        if tipo_expressao != self.current_function_type:
            self.error(f"Tipo de retorno incompatível. Esperado: {self.current_function_type}, encontrado: {tipo_expressao}")

        self.consume_token('SEMICOLON')

    '''O método lista_de_parametros() analisa a lista de parâmetros de uma sub-rotina (função ou procedimento). Para a análise semântica, você precisa garantir que cada parâmetro seja devidamente inserido na tabela de símbolos e que não haja duplicatas (dupla declaração)'''
    
    def lista_de_parametros(self):
        print("[lista_de_parametros] Analisando lista de parametros")
        parametros = []
        parametros.append(self.parametro())
        
        while self.current_token.token == 'COMMA':
            self.consume_token('COMMA')
            parametros.append(self.parametro())  # Continua analisando os próximos parâmetros
        return parametros

    def parametro(self):
        print("[parametro] Analisando parametro")
        tipo_parametro = self.tipo()  # Obtenha o tipo do parâmetro
        identifier = self.current_token.lexeme
        self.consume_token('IDENTIFIER')

        # Insere o parâmetro na tabela de símbolos
        '''try:
            self.symbols_table.insert(identifier, {'tipo': tipo_parametro})
        except Exception as e:
            print(e)'''
        
        return {'nome': identifier, 'tipo': tipo_parametro}

    def comandos(self): #entra em loop enquanto o token atual estiver em {'IDENTIFIER', 'IF', 'WHILE', 'RETURN', 'INPUT', 'PRINT'}.
        print("[comandos] Analisando comandos")
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
        elif self.current_token.token == 'INPUT':
            self.comando_leitura()
        elif self.current_token.token == 'PRINT':
            self.comando_escrita()
        elif self.current_token.token == 'BREAK':
            self.comando_de_parada()
        elif self.current_token.token == 'CONTINUE':
            self.comando_de_continuacao()
        # Verifica se há mais declarações ou atribuições a serem processadas
        #if self.current_token is not None:
        #    self.comando()  # Continua para a próxima declaração ou instrução

    def get_next_token(self):
        if self.token_index + 1 < len(self.tokens):
            return self.tokens[self.token_index + 1]
        return None  # Se não houver mais tokens

    def atribuicao_ou_chamada(self):
        print("[atribuicao_ou_chamada] Analisando atribuicao ou chamada")
        
        if self.current_token.token == 'IDENTIFIER':
            identifier_token = self.current_token.lexeme  # Captura o nome do identificador
            
            # Verifica se a variável foi declarada
            try:
                self.symbols_table.verify(identifier_token)
            except Exception as e:
                self.error(str(e))  # Lança erro se a variável não foi declarada
                return

            # Obtém o próximo token sem consumir o IDENTIFIER
            next_token = self.get_next_token()

            if next_token and next_token.token == 'ASSIGNMENT_OP':
                # Se for uma atribuição, consome o IDENTIFIER e trata a atribuição
                self.consume_token('IDENTIFIER')
                self.atribuicao(identifier_token)
            elif next_token and next_token.token == 'OPEN_PARENTHESES':
                # Se for uma chamada de função ou procedimento, não consome o IDENTIFIER aqui
                if self.get_next_token().token == 'CLOSE_PARENTHESES' or self.get_next_token().token == 'IDENTIFIER':
                    self.chamada_de_funcao(identifier_token)  # Passa o identificador capturado
                else:
                    self.chamada_de_procedimento()  # Passa o identificador capturado


    def atribuicao(self, identifier_token):
        print(f"[atribuicao] Analisando atribuicao para a variavel '{identifier_token}'")

        # Verifica se o identificador foi declarado na tabela de símbolos
        try:
            symbol_info = self.symbols_table.get(identifier_token)  # Verifica se a variável foi declarada
        except Exception as e:
            self.error(str(e))
            return

        # Consome o operador de atribuição
        if self.current_token.token != 'ASSIGNMENT_OP':
            self.error(f"Esperado operador de atribuição '=' para a variável '{identifier_token}'")
            return
        self.consume_token('ASSIGNMENT_OP')

        # Analisa a expressão do lado direito da atribuição
        expr = self.expressao()
        if expr is None:
            self.error(f"Erro ao analisar a expressão do lado direito da atribuição")
            return
        # set a expressao como valor da atribuição 
        symbol = self.symbols_table.get(identifier_token)
        symbol['valor'] = expr


        # Consome o ponto e vírgula no final da atribuição
        if self.current_token.token == 'SEMICOLON':
            self.consume_token('SEMICOLON')
        else:
            self.error("Esperado ';' após a expressão")


    def chamada_de_procedimento(self):
        print("[chamada_de_procedimento] Analisando chamada de procedimento")

        identifier = self.current_token.lexeme
        self.consume_token('IDENTIFIER')

        # Verifica se o procedimento foi declarado
        try:
            proc_info = self.symbols_table.get(identifier)
            print(proc_info['id'])
            if proc_info['id'] != 'HEADER_PROC':
                self.error(f"'{identifier}' nao e um procedimento declarado")
                return
        except Exception as e:
            self.error(str(e))
            return

        # Verifica se o procedimento tem a chave 'parametros'
        if 'parametros' not in proc_info:
            self.error(f"Procedimento '{identifier}' nao possui parametros declarados.")
            return

        # Verifica a lista de argumentos passados
        self.consume_token('OPEN_PARENTHESES')
        argumentos = []

        if self.current_token.token != 'CLOSE_PARENTHESES':
            expr = self.expressao()
            
            # Verificar se a expressão retornou um valor válido
            if expr is None:
                self.error(f"Erro ao analisar a expressão como argumento do procedimento '{identifier}'")
                return
            else:
                argumentos.append(expr)

            while self.current_token.token == 'COMMA':
                self.consume_token('COMMA')
                expr = self.expressao()

                # Verificar se a expressão retornou um valor válido
                if expr is None:
                    self.error(f"Erro ao analisar a expressão como argumento do procedimento '{identifier}'")
                    return
                else:
                    argumentos.append(expr)

        self.consume_token('CLOSE_PARENTHESES')

        # Verifica o número de parâmetros
        expected_param_count = len(proc_info['parametros'])
        if len(argumentos) != expected_param_count:
            self.error(f"Procedimento '{identifier}' esperava {expected_param_count} argumentos, mas foram fornecidos {len(argumentos)}.")

        # Verifica os tipos dos parâmetros
        for i, argumento in enumerate(argumentos):
            if 'tipo' not in argumento:
                self.error(f"Tipo do argumento {i+1} não pôde ser determinado.")
                return
            expected_type = proc_info['parametros'][i]['tipo']
            if argumento['tipo'] != expected_type:
                self.error(f"Tipo do argumento {i+1} incorreto. Esperado: {expected_type}, Fornecido: {argumento['tipo']}")

        self.consume_token('SEMICOLON')

    def chamada_de_funcao(self, identifier):
        print(f"[chamada_de_funcao] Analisando chamada de funcao '{identifier}'")

        try:
            func_info = self.symbols_table.get(identifier)
            if func_info['id'] != 'HEADER_FUNC':
                self.error(f"'{identifier}' nao e uma funcao declarada")
                return
        except Exception as e:
            self.error(str(e))
            return

        self.consume_token('OPEN_PARENTHESES')
        argumentos = []

        if self.current_token.token != 'CLOSE_PARENTHESES':
            expr = self.expressao()

            if expr is None:
                self.error(f"Erro ao analisar a expressao como argumento da funcao '{identifier}'")
                return None
            else:
                argumentos.append(expr)

            while self.current_token.token == 'COMMA':
                self.consume_token('COMMA')
                expr = self.expressao()

                if expr is None:
                    self.error(f"Erro ao analisar a expressao como argumento da funcao '{identifier}'")
                    return None
                else:
                    argumentos.append(expr)

        self.consume_token('CLOSE_PARENTHESES')

        # Verifica o número de parâmetros
        expected_param_count = len(func_info['parametros'])
        if len(argumentos) != expected_param_count:
            self.error(f"Funcao '{identifier}' esperava {expected_param_count} argumentos, mas foram fornecidos {len(argumentos)}.")
            return None

        # Verifica os tipos dos parâmetros
        for i, argumento in enumerate(argumentos):
            if 'tipo' not in argumento:
                self.error(f"Tipo do argumento {i+1} nao pode ser determinado.")
                return None
            expected_type = func_info['parametros'][i]['tipo']
            if argumento['tipo'] != expected_type:
                self.error(f"Tipo do argumento {i+1} incorreto. Esperado: {expected_type}, Fornecido: {argumento['tipo']}")
                return None

        print(f"Chamada da funcao '{identifier}' com {len(argumentos)} argumentos valida.")
        return func_info  # Retorna todas as informações da função, não apenas o tipo de retorno

    def comando_condicional(self): #lida com a estrutura condicional if
        print("[comando_condicional] Analisando comando condicional")
        self.consume_token('IF')
        self.consume_token('OPEN_PARENTHESES')
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

    def inferir_tipo(self, operando_esq, operando_dir, operador):
        """Função que infere o tipo da expressão com base nos operandos e operadores.
        Retorna o tipo da expressão resultante.
        operando_esq: Dicionário com informações sobre o operando esquerdo.
        operando_dir: Dicionário com informações sobre o operando direito (ou None, em caso de funções).
        operador: String que representa o operador entre os operandos (ou None, em caso de funções).
        """
        
        tipo_esq = operando_esq.get('tipo')
        tipo_dir = operando_dir.get('tipo') if operando_dir else None

        # Caso 1: Verificação de funções ou procedimentos
        if operador is None:
            if tipo_esq == 'HEADER_FUNC':
                #return 'HEADER_FUNC'  
                return operando_esq.get('retorno') # Funções têm um retorno, portanto o tipo é da função
            elif tipo_esq == 'HEADER_PROC':
                return 'HEADER_PROC'  # Procedimentos não têm retorno
            else:
                raise TypeError(f"Erro: tipo inesperado '{tipo_esq}' em chamada de função/procedimento.")
        
        # Caso 2: Operações entre dois inteiros
        if (tipo_esq == 'INT' and (tipo_dir == 'INT' or tipo_dir == 'NUMERIC')) or (tipo_dir == 'INT' and (tipo_esq == 'INT' or tipo_esq == 'NUMERIC')) or tipo_esq == 'NUMERIC' and tipo_dir == 'NUMERIC': #??????????
            if operador in ('ADD', 'SUB', 'MULT', 'DIV'):
                return 'INT'  # Operações aritméticas entre inteiros retornam inteiros
        

        # Caso 3: Operações de comparação (retornam booleano)
        if operador in ('LESS_THAN_OP', 'GREATER_THAN_OP', 'EQUALS_OP', 'NOT_EQUAL_OP', 'LESS_EQUAL_OP', 'GREATER_EQUAL_OP'):
            return 'BOOL'  # Comparações retornam booleanos independentemente dos tipos

        # Caso 4: Tipos incompatíveis
        raise TypeError(f"Semantica: tipos incompativeis '{tipo_esq}' e '{tipo_dir}' com o operador '{operador}'.")

    def lista_de_expressoes(self):
        print("[lista_de_expressoes] Analisando lista de expressoes")
        
        # Inicializando uma lista para armazenar as expressões
        expressoes = []
        
        # Começa chamando o método expressao() e adiciona o retorno à lista
        expr = self.expressao()
        if expr is None:
            self.error("Semantica: Erro ao analisar a expressao na lista de expressoes")
            return None
        expressoes.append(expr)
        
        # Verifica se há mais expressões separadas por vírgula
        while self.current_token.token == 'COMMA':
            self.consume_token('COMMA')
            expr = self.expressao()  # Chama o método expressao() para analisar a próxima expressão
            if expr is None:
                self.error("Semantica: Erro ao analisar a expressao apos a virgula")
                return None
            expressoes.append(expr)
        
        return expressoes

    def expressao(self):
        print("[expressao] Analisando expressao")
        # código de 3 endereços
        tac = Three_address_code('tac.txt', self.symbols_table)


        # Chama o método expressao_simples e armazena o resultado
        expr1 = self.expressao_simples()
        
        # Verificação básica: se expr1 for None, há um erro
        if expr1 is None:
            self.error("Semantica: Erro ao analisar expressao_simples")
            return None
        
        # Verifica se o token atual é um operador de comparação
        if self.current_token and self.current_token.token in ('LESS_THAN_OP', 'GREATER_THAN_OP', 'EQUALS_OP', 'NOT_EQUAL_OP', 'LESS_EQUAL_OP', 'GREATER_EQUAL_OP'):
            operador = self.current_token.token
            self.consume_token(operador)
            
            # Chama expressao_simples novamente para o segundo operando
            expr2 = self.expressao_simples()
            
            # Se expr2 for None, algo deu errado
            if expr2 is None:
                self.error("Semantica: Erro ao analisar a segunda expressao_simples apos o operador")
                return None
            
            # Retorna uma estrutura representando a expressão composta (binária)
            expressao ={
                'tipo': self.inferir_tipo(expr1, expr2, operador),
                'operador': operador,
                'esquerda': expr1,
                'direita': expr2
                }
            print("============================================= expressao ==============================================")
            print(expressao)

            tac.generate(expressao)
            tac.print_code()
            tac.append_code_to_file()

            return expressao
        
        print("============================================= expressao expr1 ==============================================")
        
        print(expr1)
        
        tac.generate(expr1)
        tac.print_code()
        tac.append_code_to_file()

        
        # Se não houver um operador de comparação, retorna apenas expr1
        return expr1

    def expressao_simples(self):
        print("[expressao_simples] Analisando expressao_simples")
        
        # Chama termo() para começar a análise
        termo1 = self.termo()
        
        if termo1 is None:
            self.error("Semantica: Erro ao analisar termo na expressao_simples")
            return None
        
        # Inicializa a expressão simples com o primeiro termo
        expr_simples = termo1
        
        # Loop para operadores de adição/subtração
        while self.current_token and self.current_token.token in ('ADD', 'SUB'):
            operador = self.current_token.token
            print(f"[expressao_simples] Operador encontrado: {operador}")
            self.consume_token(operador)
            
            # Chama termo() para obter o próximo termo
            termo2 = self.termo()
            if termo2 is None:
                self.error(f"Semantica: Erro ao analisar termo apos operador {operador}")
                return None
            
            # Cria uma nova estrutura representando a expressão
            expr_simples = {
                'tipo': self.inferir_tipo(expr_simples, termo2, operador),
                'operador': operador,
                'esquerda': expr_simples,
                'direita': termo2
            }
        print("============================================= expr_simples ==============================================")
        print(expr_simples)
        
        return expr_simples

    def termo(self):
        print("[termo] Analisando termo")
        
        # Chama fator() para começar a análise
        fator1 = self.fator()
        
        if fator1 is None:
            self.error("Erro ao analisar fator no termo")
            return None
        
        # Inicializa o termo com o primeiro fator
        termo = fator1
        
        # Loop para operadores de multiplicação/divisão
        while self.current_token and self.current_token.token in {'MULT', 'DIV'}:
            operador = self.current_token.token
            print(f"[termo] Operador encontrado: {operador}")
            self.consume_token(operador)
            
            # Chama fator() para obter o próximo fator
            fator2 = self.fator()
            if fator2 is None:
                self.error(f"Erro ao analisar fator após operador {operador}")
                return None
            
            # Cria uma nova estrutura representando o termo
            termo = {
                'tipo': self.inferir_tipo(termo, fator2, operador),
                'operador': operador,
                'esquerda': termo,
                'direita': fator2
            }
        
        return termo

    def fator(self):
        print("[fator] Analisando fator")
        
        # Verifica se é um identificador
        if self.current_token.token == 'IDENTIFIER':
            identifier = self.current_token.lexeme
            self.consume_token('IDENTIFIER')
            
            simbolo = self.symbols_table.get(identifier)
            if simbolo is None:
                raise Exception(f"Erro Semantico: Simbolo '{identifier}' nao declarado.")
            
            # Verificar se é uma chamada de função
            if self.current_token.token == 'OPEN_PARENTHESES':
                self.consume_token('OPEN_PARENTHESES')
                argumentos = []
                if self.current_token.token != 'CLOSE_PARENTHESES':
                    argumentos = self.lista_de_expressoes()
                self.consume_token('CLOSE_PARENTHESES')
                
                if simbolo['id'] == 'HEADER_FUNC':
                    return {
                        'tipo': 'HEADER_FUNC',
                        'identificador': identifier,
                        'argumentos': argumentos
                    }
                elif simbolo['id'] == 'HEADER_PROC':
                    raise Exception(f"Procedimento '{identifier}' não pode ser usado em uma expressão.")
            
            return {'tipo': simbolo['tipo'], 'identificador': identifier}
        
        # Verifica se é um número
        elif self.current_token.token == 'NUMERIC':
            valor_numerico = self.current_token.lexeme
            self.consume_token('NUMERIC')
            return {'tipo': 'NUMERIC', 'valor': valor_numerico}

        # Verifica se é uma subexpressão entre parênteses
        elif self.current_token.token == 'OPEN_PARENTHESES':
            self.consume_token('OPEN_PARENTHESES')
            resultado = self.expressao()
            self.consume_token('CLOSE_PARENTHESES')
            return resultado

        else:
            raise SyntaxError(f"Erro na linha {self.current_token.line}: Erro ao analisar fator no termo")