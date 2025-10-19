# Python implementation for the
# CYK Algorithm
import time
tiempos = []  # Lista vacía

non_terminals = [
    "E", "E1", "E2", "T", "T1",
    "T2", "F", "E3", "PLUS", "MULT",
    "LP", "RP", "ID"
]

terminals = ["(", ")", "+", "*", "id"]

R = {
    # Producciones para terminales
    "ID": [["id"]],
    "PLUS": [["+"]],
    "MULT": [["*"]],
    "LP": [["("]],
    "RP": [[")"]],
    
    # F -> id (expandido: F puede derivar todo lo que ID deriva)
    "F": [["id"], ["LP", "E3"]],
    
    # T -> F (expandido: T puede derivar todo lo que F deriva)
    "T": [["id"], ["LP", "E3"], ["F", "T1"]],
    
    # E -> T (expandido: E puede derivar todo lo que T deriva)
    "E": [["id"], ["LP", "E3"], ["F", "T1"], ["T", "E1"]],
    
    # Producciones de dos símbolos
    "E3": [["E", "RP"]],
    "T1": [["MULT", "T2"]],
    "T2": [["id"], ["LP", "E3"], ["F", "T1"]],
    "E1": [["PLUS", "E2"]],
    "E2": [["id"], ["LP", "E3"], ["F", "T1"], ["T", "E1"]],
}



# Function to perform the CYK Algorithm
def cykParse(w):
    n = len(w)
    
    # Initialize the table
    T = [[set([]) for j in range(n)] for i in range(n)]

    # Filling in the table
    for j in range(0, n):

        # Iterate over the rules
        for lhs, rule in R.items():
            for rhs in rule:
                
                # If a terminal is found
                if len(rhs) == 1 and \
                rhs[0] == w[j]:
                    T[j][j].add(lhs)

        for i in range(j, -1, -1):   
             
            # Iterate over the range i to j + 1   
            for k in range(i, j):

                # Iterate over the rules
                for lhs, rule in R.items():
                    for rhs in rule:
                        
                        # If a production has two non-terminals
                        if len(rhs) == 2 and \
                        rhs[0] in T[i][k] and \
                        rhs[1] in T[k + 1][j]:
                            T[i][j].add(lhs)
    
    # If word can be formed by rules 
    # of given grammar
    if "E" in T[0][n-1]:
        print("True")
    else:
        print("False")
    
# Driver Code

def generar_expresion(n_operadores):
    """Genera una expresión con n operadores"""
    expr = "id"
    for i in range(n_operadores):
        if i % 2 == 0:
            expr += " + id"
        else:
            expr += " * id"
    return expr

test_cases = [
    # Casos pequeños (baseline)
    generar_expresion(0),   # 1 token
    generar_expresion(1),   # 3 tokens
    generar_expresion(2),   # 5 tokens
    generar_expresion(5),   # 11 tokens
    generar_expresion(10),  # 21 tokens
    
    # Casos medianos - aquí empieza a notarse
    generar_expresion(20),  # 41 tokens
    generar_expresion(30),  # 61 tokens
    generar_expresion(40),  # 81 tokens
    generar_expresion(50),  # 101 tokens
    
    # Casos grandes - GRAN diferencia
    generar_expresion(75),   # 151 tokens
    generar_expresion(100),  # 201 tokens
    generar_expresion(150),  # 301 tokens
    generar_expresion(200),  # 401 tokens (esto puede tardar varios segundos)
]

for i in range(len(test_cases)):
    w = test_cases[i].split()
    start = time.perf_counter()
    cykParse(w)
    end = time.perf_counter()
    tiempo_total = end - start
    tiempos.append(tiempo_total)
    print(f"Tiempo para el caso de prueba {i+1} (longitud {len(w)} tokens): {tiempo_total} segundos")
    
print(tiempos)  