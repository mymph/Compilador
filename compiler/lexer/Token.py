class Token:
  
  def __init__(self, token: str, lexeme: str, line: int):
    self.token = token
    self.lexeme = lexeme
    self.line = line

  def __str__(self):
    str = f'(token: "{self.token}"; lexema: "{self.lexeme}" - Linha {self.line}), '
    
    return str