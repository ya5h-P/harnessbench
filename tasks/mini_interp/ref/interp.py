import re
def _tokenize(expr):
    return re.findall(r"\d+|[A-Za-z_]\w*|[()+\-*]", expr)
def _parse(tokens, env):
    pos = [0]
    def peek(): return tokens[pos[0]] if pos[0] < len(tokens) else None
    def nxt(): t = tokens[pos[0]]; pos[0]+=1; return t
    def atom():
        t = nxt()
        if t == "(":
            v = expr(); nxt()  # consume ')'
            return v
        if t.isdigit(): return int(t)
        if t in env: return env[t]
        raise NameError("undefined variable %r" % t)
    def term():
        v = atom()
        while peek() == "*":
            nxt(); v = v * atom()
        return v
    def expr():
        v = term()
        while peek() in ("+", "-"):
            op = nxt()
            v = v + term() if op == "+" else v - term()
        return v
    return expr()
def run(program):
    env = {}; out = []
    for line in program.splitlines():
        line = line.strip()
        if not line: continue
        if line.startswith("print "):
            out.append(_parse(_tokenize(line[6:]), env))
        else:
            name, rhs = line.split("=", 1)
            env[name.strip()] = _parse(_tokenize(rhs), env)
    return out
