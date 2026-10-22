import ast

LOOP_NODES = {ast.For, ast.While, ast.AsyncFor}

class LoopChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.current_depth = 0

    def _visit_loop(self, node):
        self.current_depth += 1

        if self.current_depth > 2:
            self.issues.append({
                "line": node.lineno,
                "rule": "02_TOO_MANY_LOOPS",
                "message": ""
            })

        self.generic_visit(node)

        self.current_depth -= 1

    def visit_For(self, node):
        self._visit_loop(node)

    def visit_While(self, node):
        self._visit_loop(node)

    def visit_AsyncFor(self, node):
        self._visit_loop(node)

def check_loops(tree):
    checker = LoopChecker()
    checker.visit(tree)
    return checker.issues
