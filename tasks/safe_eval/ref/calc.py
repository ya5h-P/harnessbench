import ast, operator
_BIN = {ast.Add:operator.add, ast.Sub:operator.sub, ast.Mult:operator.mul,
        ast.Div:operator.truediv, ast.FloorDiv:operator.floordiv,
        ast.Mod:operator.mod, ast.Pow:operator.pow}
_UN = {ast.UAdd:operator.pos, ast.USub:operator.neg}
def _ev(node):
    if isinstance(node, ast.Expression): return _ev(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value,(int,float)) and not isinstance(node.value,bool):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN:
        return _BIN[type(node.op)](_ev(node.left), _ev(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UN:
        return _UN[type(node.op)](_ev(node.operand))
    raise ValueError("disallowed expression")
def safe_eval(expr):
    try: tree = ast.parse(expr, mode="eval")
    except SyntaxError: raise ValueError("syntax error")
    return _ev(tree)
