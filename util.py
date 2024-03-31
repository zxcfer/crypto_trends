def is_min(x, d):
    for v in d:
        if x >= v:
            return False

    return True

def is_max(x, d):
    for v in d:
        if x <= v:
            return False
        
    return True

