producciones = [
    "E -> T X",         
    "X -> + T X",       
    "X -> ε",          
    "T -> F Y",        
    "Y -> * F Y",       
    "Y -> ε",           
    "F -> ( E )",       
    "F -> id"           
]

def parsear_produccion(produccion):
    if '->' in produccion:
        partes = produccion.split('->')
    else:
        partes = produccion.split('=')
    
    lado_izq = partes[0].strip()
    lado_der = partes[1].strip()
    
    if lado_der in ['ε', 'epsilon', '#', '']:
        return (lado_izq, ['ε'])
    
    simbolos = lado_der.split()
    return (lado_izq, simbolos)

def es_no_terminal(simbolo):
    return len(simbolo) == 1 and simbolo.isupper()

def es_terminal(simbolo):
    return simbolo != 'ε' and not es_no_terminal(simbolo)

def obtener_producciones(no_terminal, producciones_parseadas):
    return [(i, prod) for i, prod in enumerate(producciones_parseadas) if prod[0] == no_terminal]

def calcular_primeros_cadena(cadena, primeros_nt):
    if not cadena or cadena == ['ε']:
        return {'ε'}
    
    primeros = set()
    
    for i, simbolo in enumerate(cadena):
        if es_terminal(simbolo):
            primeros.add(simbolo)
            return primeros
        
        if simbolo in primeros_nt:
            primeros_simbolo = primeros_nt[simbolo]
        else:
            return set()
        primeros.update(primeros_simbolo - {'ε'})
        
        if 'ε' in primeros_simbolo:
            if i == len(cadena) - 1:
                primeros.add('ε')
        else:
            break
    
    return primeros

def calcular_primeros_no_terminales(producciones_parseadas):
    no_terminales = []
    for izq, _ in producciones_parseadas:
        if izq not in no_terminales:
            no_terminales.append(izq)
    
    primeros_nt = {}
    
    for nt in no_terminales:
        primeros_nt[nt] = set()
    
    cambios = True
    iteraciones = 0
    max_iter = 100
    
    while cambios and iteraciones < max_iter:
        cambios = False
        iteraciones += 1
        
        for nt in no_terminales:
            anterior = primeros_nt[nt].copy()
            
            for _, (lado_izq, lado_der) in obtener_producciones(nt, producciones_parseadas):
                
                if lado_der and es_no_terminal(lado_der[0]) and lado_der[0] == nt:
                    if 'ε' in primeros_nt[nt] and len(lado_der) > 1:
                        resto = lado_der[1:]
                        primeros_resto = calcular_primeros_cadena(resto, primeros_nt)
                        primeros_nt[nt].update(primeros_resto)
                else:
                    primeros_prod = calcular_primeros_cadena(lado_der, primeros_nt)
                    primeros_nt[nt].update(primeros_prod)
            
            if primeros_nt[nt] != anterior:
                cambios = True
    
    return primeros_nt


def calcular_siguientes(producciones_parseadas, primeros_nt, simbolo_inicial):
    no_terminales = []
    for izq, _ in producciones_parseadas:
        if izq not in no_terminales:
            no_terminales.append(izq)
    
    siguientes = {}
    for nt in no_terminales:
        siguientes[nt] = set()
    
    siguientes[simbolo_inicial].add('$')
    
    cambios = True
    iteraciones = 0
    max_iter = 100
    
    while cambios and iteraciones < max_iter:
        cambios = False
        iteraciones += 1
        
        for lado_izq, lado_der in producciones_parseadas:
            for i, simbolo in enumerate(lado_der):
                if not es_no_terminal(simbolo):
                    continue
                anterior = siguientes[simbolo].copy()
                
                if i + 1 < len(lado_der):
                    resto = lado_der[i + 1:]
                    primeros_resto = calcular_primeros_cadena(resto, primeros_nt)
                    
                    siguientes[simbolo].update(primeros_resto - {'ε'})
                    
                    if 'ε' in primeros_resto:
                        siguientes[simbolo].update(siguientes[lado_izq])
                else:
                    siguientes[simbolo].update(siguientes[lado_izq])
                
                if siguientes[simbolo] != anterior:
                    cambios = True
    
    return siguientes

def calcular_prediccion(lado_der, lado_izq, primeros_nt, siguientes):
    primeros_alfa = calcular_primeros_cadena(lado_der, primeros_nt)
    
    if 'ε' in primeros_alfa:
        return (primeros_alfa - {'ε'}) | siguientes.get(lado_izq, set())
    else:
        return primeros_alfa


# NUEVA FUNCIÓN: CONSTRUIR TABLA DE PARSEO LL(1)
def construir_tabla_parseo(producciones_parseadas, primeros_nt, siguientes):
    """
    Construye la tabla de parseo LL(1) usando los conjuntos de predicción
    """
    # Obtener todos los no-terminales
    no_terminales = []
    for izq, _ in producciones_parseadas:
        if izq not in no_terminales:
            no_terminales.append(izq)
    
    # Obtener todos los terminales
    terminales = set()
    for _, lado_der in producciones_parseadas:
        for simbolo in lado_der:
            if es_terminal(simbolo):
                terminales.add(simbolo)
    terminales.add('$')  # Agregar marcador de fin
    terminales = sorted(list(terminales))
    
    # Inicializar tabla vacía
    tabla = {}
    for nt in no_terminales:
        tabla[nt] = {}
    
    # Llenar la tabla usando conjuntos de predicción
    conflictos = []
    for i, (lado_izq, lado_der) in enumerate(producciones_parseadas):
        pred = calcular_prediccion(lado_der, lado_izq, primeros_nt, siguientes)
        
        for terminal in pred:
            if terminal in tabla[lado_izq]:
                # Hay un conflicto - la gramática NO es LL(1)
                conflictos.append({
                    'no_terminal': lado_izq,
                    'terminal': terminal,
                    'prod_existente': tabla[lado_izq][terminal],
                    'prod_nueva': (i, lado_der)
                })
            else:
                tabla[lado_izq][terminal] = (i, lado_der)
    
    return tabla, terminales, conflictos


# NUEVA FUNCIÓN: ALGORITMO DE MATCHING CON PILA
def algoritmo_matching(cadena, tabla, producciones_parseadas, simbolo_inicial='S'):
    # Preparar entrada
    entrada = cadena.split() + ['$']
    posicion = 0
    
    # Inicializar pila
    pila = ['$', simbolo_inicial]
    
    # Almacenar pasos para el análisis
    pasos = []
    
    print(f"ANÁLISIS SINTÁCTICO DE: '{cadena}'")
    
    paso_num = 1
    
    # Bucle principal
    while len(pila) > 0:
        tope = pila[-1]
        actual = entrada[posicion]
        
        # Guardar estado actual
        pila_str = ' '.join(pila)
        entrada_str = ' '.join(entrada[posicion:])
        
        # CASO 1: Tope y símbolo actual son '$' -> ACEPTAR
        if tope == '$' and actual == '$':
            accion = 'ACEPTAR - Cadena válida'
            pasos.append((paso_num, pila_str, entrada_str, accion))
            print(" CADENA ACEPTADA")
            return True, pasos
        
        # CASO 2: Tope es terminal
        elif not es_no_terminal(tope) and tope != '$':
            if tope == actual:
                accion = f'MATCH: {tope} == {actual} → POP y AVANZAR'
                pila.pop()
                posicion += 1
            else:
                accion = f'ERROR: Esperaba "{tope}", encontró "{actual}"'
                pasos.append((paso_num, pila_str, entrada_str, accion))
                return False, pasos
        
        # CASO 3: Tope es no-terminal
        elif es_no_terminal(tope):
            if tope in tabla and actual in tabla[tope]:
                prod_num, prod_der = tabla[tope][actual]
                prod_der_str = ' '.join(prod_der)
                accion = f'EXPANDIR: Usar producción {prod_num+1}: {tope} → {prod_der_str}'
                
                pila.pop()  # Sacar el no-terminal
                
                # Insertar producción en orden inverso (excepto si es ε)
                if prod_der != ['ε']:
                    for simbolo in reversed(prod_der):
                        pila.append(simbolo)
            else:
                accion = f'ERROR: No hay entrada en tabla[{tope}, {actual}]'
                pasos.append((paso_num, pila_str, entrada_str, accion))
                print("CADENA RECHAZADA ")
                return False, pasos
        
        else:
            accion = 'ERROR: Símbolo desconocido'
            pasos.append((paso_num, pila_str, entrada_str, accion))
            return False, pasos
        
        pasos.append((paso_num, pila_str, entrada_str, accion))
        paso_num += 1

    return False, pasos


def mostrar_tabla_parseo(tabla, no_terminales, terminales):

    print("\nTABLA DE PARSEO LL(1):")
    print("=" * 100)
    
    # Encabezado
    header = f"{'NT':<5}"
    for terminal in terminales:
        header += f"{terminal:<15}"
    print(header)
    print("-" * 100)
    
    # Filas
    for nt in no_terminales:
        fila = f"{nt:<5}"
        for terminal in terminales:
            if nt in tabla and terminal in tabla[nt]:
                prod_num, prod_der = tabla[nt][terminal]
                prod_str = f"{nt}→{' '.join(prod_der)}"
                fila += f"{prod_str[:14]:<15}"
            else:
                fila += f"{'---':<15}"
        print(fila)
    
    print("=" * 100)


def main():  
    producciones_parseadas = [parsear_produccion(p) for p in producciones]
    
    print("\nGRAMÁTICA:")
    for i, (izq, der) in enumerate(producciones_parseadas, 1):
        der_str = ' '.join(der)
        print(f"  {i}. {izq} → {der_str}")
    
    no_terminales = []
    for izq, _ in producciones_parseadas:
        if izq not in no_terminales:
            no_terminales.append(izq)
    
    simbolo_inicial = no_terminales[0]
    
    print("\n")
    print("    CONJUNTOS PRIMEROS:")
    
    primeros_nt = calcular_primeros_no_terminales(producciones_parseadas)
    
    for nt in no_terminales:
        primeros_list = sorted(list(primeros_nt[nt]))
        print(f"PRIMEROS({nt}) = {{ {', '.join(primeros_list)} }}")
    
    print("\n")
    print("    CONJUNTOS SIGUIENTES:")
    
    siguientes = calcular_siguientes(producciones_parseadas, primeros_nt, simbolo_inicial)
    
    for nt in no_terminales:
        siguientes_list = sorted(list(siguientes[nt]))
        print(f"SIGUIENTES({nt}) = {{ {', '.join(siguientes_list)} }}")
    
    print("\n")
    print("    CONJUNTOS DE PREDICCIÓN:")
    
    for i, (lado_izq, lado_der) in enumerate(producciones_parseadas, 1):
        pred = calcular_prediccion(lado_der, lado_izq, primeros_nt, siguientes)
        pred_list = sorted(list(pred))
        der_str = ' '.join(lado_der)
        print(f"PRED({i}. {lado_izq} → {der_str}) = {{ {', '.join(pred_list)} }}")
    
    # CONSTRUIR TABLA DE PARSEO
    print("\n")
    tabla, terminales, conflictos = construir_tabla_parseo(producciones_parseadas, primeros_nt, siguientes)
    
    if conflictos:
        print("ADVERTENCIA: La gramática NO es LL(1):")
        for conf in conflictos:
            print(f"  En [{conf['no_terminal']}, {conf['terminal']}]:")
            print(f"    Producción existente: {conf['prod_existente']}")
            print(f"    Producción nueva: {conf['prod_nueva']}")
    else:
        print(" La gramática ES LL(1)\n")
    
    mostrar_tabla_parseo(tabla, no_terminales, terminales)
    
    # PROBAR ALGORITMO DE MATCHING
    print("PRUEBAS DEL ALGORITMO DE MATCHING")
    
    # Cadenas de prueba (ajusta según tu gramática)
    cadenas_prueba = [
        "id",                           # Solo identificador
        "id + id",                    # Suma simple
        "id * id",
        "( id + id ) * id",           # Expresión con paréntesis
        "id ) id ",               # Suma y multiplicación
    ]
    
    for cadena in cadenas_prueba:
        resultado, pasos = algoritmo_matching(cadena, tabla, producciones_parseadas, simbolo_inicial)
        
        print(f"{'Paso':<6}{'Pila':<30}{'Entrada':<30}{'Acción':<40}")
        for paso in pasos: 
            print(f"{paso[0]:<6}{paso[1][:29]:<30}{paso[2][:29]:<30}{paso[3][:39]:<40}")

if __name__ == "__main__":
    main()