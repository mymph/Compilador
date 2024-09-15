class Token:
  
  def __init__(self, token: str, lexeme: str, line: int):
    self.token = token
    self.lexeme = lexeme
    self.line = line

  def __str__(self):
    return f'(token: "{self.token}"; lexema: "{self.lexeme}" - Linha {self.line}), '