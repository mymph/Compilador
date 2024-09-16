class CodeGenerator:
    def __init__(self):
        self.instructions = []

    def generate_code(self, ast):
        """
        Gera código de três endereços (ou outro código intermediário) a partir da AST.
        """
        print("[CodeGenerator] Iniciando geração de código")
        self.visit_node(ast)

    def visit_node(self, node):
        """
        Visita cada nó da AST e gera as instruções.
        """
        # Por exemplo, para uma atribuição:
        if node.type == "assignment":
            self.generate_assignment(node)

    def generate_assignment(self, node):
        """
        Gera código de três endereços para atribuição.
        """
        var = node.left.value
        expr = self.evaluate_expression(node.right)
        instruction = f"{var} = {expr}"
        self.instructions.append(instruction)
        print(f"Geração de código: {instruction}")

    def evaluate_expression(self, expr_node):
        """
        Avalia uma expressão e retorna o código intermediário para ela.
        """
        # Isso geraria o código de três endereços para expressões
        return expr_node.value

    def get_instructions(self):
        """
        Retorna as instruções geradas em formato de código intermediário.
        """
        return "\n".join(self.instructions)