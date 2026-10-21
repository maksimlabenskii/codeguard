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

def check_missing_raise(tree):
    issues = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue

        has_raise = any(
            isinstance(child, ast.Raise)
            for statement in node.body
            for child in ast.walk(statement)
        )

        if not has_raise:
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


