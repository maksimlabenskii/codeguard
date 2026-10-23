import ast
import re

SNAKE_CASE_REGEX = re.compile(r"^[a-z_][a-z0-9_]*$")
PASCAL_CASE_REGEX = re.compile(r"^[A-Z][a-zA-Z0-9]*$")

def _is_snake_case(name: str) -> bool:
    return bool(SNAKE_CASE_REGEX.match(name))


def _is_pascal_case(name: str) -> bool:
    return bool(PASCAL_CASE_REGEX.match(name))

def check_naming_convention(tree):
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if not _is_pascal_case(node.name):
                issues.append({
                    "line": node.lineno,
                    "rule": "05_CLASS_NAMING",
                    "message": f"Класс '{node.name}' должен быть в PascalCase"
                })

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not _is_snake_case(node.name):
                issues.append({
                    "line": node.lineno,
                    "rule": "05_FUNC_NAMING",
                    "message": f"Функция '{node.name}' должна быть в snake_case"
                })

        elif isinstance(node, ast.Name):
            if not _is_snake_case(node.id):
                issues.append({
                    "line": node.lineno,
                    "rule": "05_VAR_NAMING",
                    "message": f"Переменная '{node.id}' должна быть в snake_case"
                })

        elif isinstance(node, ast.arg):
            if not _is_snake_case(node.arg):
                issues.append({
                    "line": node.lineno,
                    "rule": "05_ARG_NAMING",
                    "message": f"Аргумент '{node.arg}' должен быть в snake_case"
                })

    return issues