'''O Analisador léxico pega os caracteres de entrada e os trasnforma em tokens
- Lê os caracteres de entrada e os agrupa em lexemas
- Ignora espaços, tabulações e saltos de linha.
Ex.: o número 25432 de entrada será um token, em vez de cada número ser um token
- Token é um terminal. Possui atributos com informações adicionais sobre o símbolo.
Ex.: valor, tipo, escopo, etc.'''