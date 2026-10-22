import ast

def check_empty_except(tree):
    issues = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue

        if (
            len(node.body) == 1 and
            isinstance(node.body[0], ast.Pass)
        ):
            issues.append({
                "line": node.lineno,
                "rule": "01_EMPTY_EXCEPTION",
                "message": ""
            })

    return issues

def _contains_logging(body):
    for statement in body:
        for child in ast.walk(statement):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr in {"error", "debug", "warning", "exception", "critical", "info"}:
                        return True
                    elif isinstance(child.func, ast.Name):
                        if child.func.id == "print":
                            return True
    return False

def check_missing_raise(tree):
    issues = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue

        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            continue

        has_raise = any(
            isinstance(child, ast.Raise)
            for statement in node.body
            for child in ast.walk(statement)
        )

        if not has_raise and not _contains_logging(node.body):
            issues.append({
                "line": node.lineno,
                "rule": "01_MISSING_RAISE_EXCEPTION",
                "message": ""
            })

    return issues

def check_broad_except(tree):
    issues = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue

        if isinstance(node.type, ast.Name):
            if node.type.id in ("Exception", "BaseException"):
                issues.append({
                    "line": node.lineno,
                    "rule": "01_BROAD_EXCEPTION",
                    "message": ""
                })

    return issues


