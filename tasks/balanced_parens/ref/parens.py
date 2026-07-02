def is_balanced(s):
    pairs={")":"(","]":"[","}":"{"}
    stack=[]
    for c in s:
        if c in "([{": stack.append(c)
        elif c in ")]}":
            if not stack or stack.pop()!=pairs[c]: return False
    return not stack
