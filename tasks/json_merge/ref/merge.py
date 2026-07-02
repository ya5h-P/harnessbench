import copy
def deep_merge(a, b):
    result = copy.deepcopy(a)
    for k, vb in b.items():
        if k in result:
            va = result[k]
            if isinstance(va, dict) and isinstance(vb, dict):
                result[k] = deep_merge(va, vb)
            elif isinstance(va, list) and isinstance(vb, list):
                result[k] = copy.deepcopy(va) + copy.deepcopy(vb)
            else:
                result[k] = copy.deepcopy(vb)
        else:
            result[k] = copy.deepcopy(vb)
    return result
