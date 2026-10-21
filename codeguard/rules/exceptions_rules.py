import ast

class TransactionChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Transaction(self, node):
        for handler in node.handlers:
            caught_type = ""
            if isinstance(handler.type, ast.Name):
                caught_type = handler.type.id


