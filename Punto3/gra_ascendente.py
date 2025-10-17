def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        elif c.isalpha():
            j = i
            while j < len(expr) and expr[j].isalpha():
                j += 1
            tokens.append('id')
            i = j
        elif c == '+':
            tokens.append('+')
            i += 1
        elif c == '*':
            tokens.append('*')
            i += 1
        elif c == '(':
            tokens.append('(')
            i += 1
        elif c == ')':
            tokens.append(')')
            i += 1
        else:
            raise ValueError(f"Caracter invalido: {c}")
    tokens.append('$')
    return tokens


productions = [
    ('E', ['E', '+', 'T']),
    ('E', ['T']),
    ('T', ['T', '*', 'F']),
    ('T', ['F']),
    ('F', ['(', 'E', ')']),
    ('F', ['id'])
]


def parse(expr):
    stack = []
    tokens = tokenize(expr)
    i = 0
    
    while True:
        if stack == ['E'] and i < len(tokens) and tokens[i] == '$':
            print(f"{expr} -> Acepta")
            return True
        
        reduced = False
        priority_order = [4, 0, 2, 1, 3, 5]
        
        for prod_idx in priority_order:
            A, beta = productions[prod_idx]
            k = len(beta)
            if k <= len(stack) and stack[-k:] == beta:
                if A == 'E' and i < len(tokens):
                    next_token = tokens[i]
                    if next_token not in ['+', '$', ')']:
                        continue
                if A == 'T' and i < len(tokens):
                    next_token = tokens[i]
                    if next_token not in ['*', '+', '$', ')']:
                        continue
                
                stack = stack[:-k]
                stack.append(A)
                reduced = True
                break
        
        if reduced:
            continue
        
        if i < len(tokens):
            token = tokens[i]
            stack.append(token)
            i += 1
        else:
            break
    
    print(f"{expr} -> No acepta")
    return False

print("Analizador sintáctico ascendente:\n")

parse("id + id * id")
parse("( id + id ) * id")
parse("id * id + id")
parse("id")
parse("( id )")
parse("id + id + id")
parse("id +")
parse("id + * id")
