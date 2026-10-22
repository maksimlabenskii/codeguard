import ast

class ScopeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.scopes = []
        self.issues = []

    def _current_scope(self):
        return self.scopes[-1] if self.scopes else None

    def _enter_function(self, node):
        args = set()
        for arg in node.args.args + node.args.kwonlyargs + node.args.posonlyargs:
            args.add(arg.arg)
        if node.args.vararg:
            args.add(node.args.vararg.arg)
        if node.args.kwarg:
            args.add(node.args.kwarg.arg)

        self.scopes.append({
            "node": node,
            "name": getattr(node, "name"),
            "assigned": {},
            "loaded": set(),
            "args": args
        })

        self.generic_visit(node)

        scope = self.scopes.pop()
        self._check_scope(scope)

    def _check_scope(self, scope):
        for name, lineno in scope["assigned"].items():
            if name.startswith("_"):
                continue
            if name.startswith("__") and name.endswith("__"):
                continue
            if name in scope["args"]:
                continue
            if name in scope["loaded"]:
                continue

            self.issues.append({
                "line": lineno,
                "rule": "03_UNUSED_VAR",
                "message": "",
            })

    def visit_Name(self, node):
        scope = self._current_scope()
        if scope is None:
            return

        if isinstance(node.ctx, ast.Store):
            scope["assigned"][node.id] = node.lineno
        elif isinstance(node.ctx, ast.Load):
            scope["loaded"].add(node.id)

    def visit_FunctionDef(self, node):
        self._enter_function(node)

    def visit_AsyncFunctionDef(self, node):
        self._enter_function(node)

    def visit_Module(self, node):
        self.scopes.append({
            "node": node,
            "name": "<module>",
            "assigned": {},
            "loaded": set(),
            "args": set()
        })

        self.generic_visit(node)

        scope = self.scopes.pop()
        self._check_scope(scope)

def check_unused_var(tree):
    visitor = ScopeVisitor()
    visitor.visit(tree)
    return visitor.issues



