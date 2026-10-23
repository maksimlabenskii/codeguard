import ast

MAX_ARGUMENTS = 4
SELF_LIKE = {"self", "cls"}


def count_arguments(func_node):
    args = func_node.args
    count = 0

    positional = list(args.posonlyargs) + list(args.args)
    count += len(positional)

    if args.vararg is not None:
        count += 1

    count += len(args.kwonlyargs)

    if args.kwarg is not None:
        count += 1

    if positional and positional[0].arg in SELF_LIKE:
        count -= 1

    return count


def check_many_arguments(tree):
    issues = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        count = count_arguments(node)
        if count > MAX_ARGUMENTS:
            issues.append({
                "line": node.lineno,
                "rule": "06_TOO_MANY_ARGUMENTS",
                "message": "",
            })

    return issues