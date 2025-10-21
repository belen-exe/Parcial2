# Parcial 2

## Punto 1

### Operaciones Implementadas

- CREATE (`new`) - Insertar registros
- READ (`get`) - Consultar registros
- UPDATE (`set`) - Actualizar registros
- DELETE (`drop`) - Eliminar registros
- WHERE - Filtros condicionales en todas las operaciones
- Múltiples tablas - Hasta 10 tablas simultáneas
- Tipos de datos - Números, strings, booleanos, null
- Persistencia en sesión - Los datos se mantienen durante la ejecución

### Operadores Soportados

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `=` | Igual | `age = 25` |
| `!=` | Diferente | `status != "inactive"` |
| `>` | Mayor que | `price > 100` |
| `<` | Menor que | `stock < 10` |
| `>=` | Mayor o igual | `age >= 18` |
| `<=` | Menor o igual | `quantity <= 50` |

---

### Notación BNF

```bnf
# ===== PROGRAMA =====

<programa> ::= { <sentencia> }

<sentencia> ::= <create_op>
              | <read_op>
              | <update_op>
              | <delete_op>

# ===== CREATE (INSERT) =====

<create_op> ::= "new" <identificador> "{" <pares> "}"

# ===== READ (SELECT) =====

<read_op> ::= "get" <identificador> [ <opt_where> ]

# ===== UPDATE =====

<update_op> ::= "set" <identificador> "{" <pares> "}" [ <opt_where> ]

# ===== DELETE =====

<delete_op> ::= "drop" <identificador> [ <opt_where> ]

# ===== CLÁUSULA WHERE =====

<opt_where> ::= ε                                          # Vacío (opcional)
              | "where" <identificador> <operador> <valor>

<operador> ::= "=" | "!=" | ">" | "<" | ">=" | "<="

# ===== VALORES =====

<pares> ::= <par> { "," <par> }

<par> ::= <identificador> ":" <valor>

<valor> ::= <numero>
          | <cadena>
          | <booleano>
          | <nulo>

<numero> ::= [0-9]+ [ "." [0-9]+ ]

<cadena> ::= '"' <caracter>* '"' | "'" <caracter>* "'"

<booleano> ::= "true" | "false"

<nulo> ::= "null"

<identificador> ::= [a-zA-Z_] [a-zA-Z0-9_]*

# ===== COMENTARIOS =====

<comentario> ::= "#" <resto_de_linea>
               | "//" <resto_de_linea>
```


---


### Comparación con SQL

| Característica | NQL | SQL |
|----------------|-------|-----|
| Sintaxis | Minimalista | Completa |
| CREATE TABLE | Implícito | Explícito |
| INSERT | `new` | `INSERT INTO` |
| SELECT | `get` | `SELECT * FROM` |
| UPDATE | `set` | `UPDATE ... SET` |
| DELETE | `drop` | `DELETE FROM` |
| WHERE | Simple | Complejo |


---

### Notas Adicionales

1. **Espacios en blanco**: Pueden aparecer entre cualquier token y son ignorados
2. **Comentarios**: Pueden aparecer en cualquier lugar y son ignorados
3. **Case sensitivity**: Las palabras clave son case-sensitive (deben estar en minúsculas)
4. **Terminación**: Las sentencias no requieren punto y coma (`;`)
5. **Nuevas líneas**: Son tratadas como espacios en blanco

---

## Punto 2

### NQL - Lenguaje CRUD Simplificado

NQL (NoSQL Query Language) es un lenguaje de programación diseñado para realizar operaciones CRUD (Create, Read, Update, Delete) sobre bases de datos de manera simple e intuitiva. 

---

#### Estructura del Proyecto

```
punto2_NQL/
├── NQL.l           # Analizador léxico (Flex)
├── NQL.y           # Analizador sintáctico (Bison)
├── test.nql        # Archivo de pruebas
└── nql             # Ejecutable compilado
```

---

#### Compilación

```bash
bison -d NQL.y
flex NQL.l
gcc -o nql NQL.tab.c lex.yy.c -lfl
./nql test.nql
```
---


#### Gramática

**Estructura general:**

```
programa → sentencias
sentencias → sentencia | sentencias sentencia
sentencia → create_op | read_op | update_op | delete_op
```

#### Pruebas Realizadas

#### Conjunto de Pruebas Completo (test.nql)

```nql

# 1. CREATE - Insertar registros

# Insertar usuarios
new users { name: "Ana", age: 25, active: true }
new users { name: "Carlos", age: 30, active: true }
new users { name: "María", age: 22, active: false }
new users { name: "Pedro", age: 17, active: true }

# Insertar productos
new products { name: "Laptop", price: 1200000, stock: 15 }
new products { name: "Mouse", price: 25000, stock: 50 }
new products { name: "Teclado", price: 88000, stock: 0 }

```

<img width="655" height="788" alt="image" src="https://github.com/user-attachments/assets/5e858f07-39e0-41fe-a506-1c8dd2dbc1d5" />


```nql

# 2. READ - Consultar registros

# Leer todos los usuarios
get users

# Leer todos los productos
get products

```

<img width="655" height="857" alt="image" src="https://github.com/user-attachments/assets/889a6327-b906-404f-9a7b-fed5749c523f" />

```nql

# 3. READ con WHERE - Consultas filtradas

# Usuarios mayores de edad
get users where age >= 18

# Usuarios activos
get users where active = true

# Productos sin stock
get products where stock = 0

# Productos económicos
get products where price < 100000

```

<img width="655" height="797" alt="image" src="https://github.com/user-attachments/assets/fbe28383-f4fc-4615-b6d7-475706f37ed7" />

<img width="655" height="518" alt="image" src="https://github.com/user-attachments/assets/8c2439af-bad5-4183-8a8d-d8985b753068" />


```nql

# 4. UPDATE - Actualizar registros

# Actualizar edad de Ana
set users { age: 26 } where name = "Ana"

# Ver cambio
get users where name = "Ana"

# Actualizar precio del Mouse
set products { price: 29000 } where name = "Mouse"

# Ver cambio
get products where name = "Mouse"

# Desactivar usuario específico
set users { active: false } where name = "Carlos"

# Ver cambio
get users where name = "Carlos"

# Reabastecer producto
set products { stock: 25 } where name = "Teclado"

# Ver cambio
get products where name = "Teclado"

```
<img width="655" height="862" alt="image" src="https://github.com/user-attachments/assets/f756f0c2-9519-437e-927f-2b85931505a2" />

<img width="655" height="293" alt="image" src="https://github.com/user-attachments/assets/8fb3a99c-48a8-4487-beae-1b9d39205dbf" />


```
# 5. DELETE - Eliminar registros

# Eliminar usuario menor de edad
drop users where age < 18

# Verificar que se eliminó
get users

# Eliminar productos sin stock (antes del reabastecimiento habría funcionado)
drop products where stock = 0

# Ver productos restantes
get products
```

<img width="655" height="899" alt="image" src="https://github.com/user-attachments/assets/a176d6df-f906-4816-870e-90fa46bcfba4" />

---

## Punto 3

Analizador sintáctico ascendente en python.

### Gramática:

```
E -> E + T  
E -> T 
T -> T * F 
T -> F 
F -> ( E ) 
F -> id 
```

### Transformación:

Eliminación de recursión a la izquierda para que sea LL(1): 

```
E -> T E’ 
E’ -> + T E’ 
E’ -> ℇ 
T -> F T’ 
T’ -> * F T’ 
T’ -> ℇ 
F -> ( E ) 
F -> id 
```

### Conjuntos:

Conjunto de primeros: 

- Primeros(F) = {(, id}
- Primeros(T’) = {*, ℇ }
- Primeros(T) = {(, id}
- Primeros(E’) = {+, ℇ }
- Primeros(E) = {(, id} 


Conjuntos de siguientes: 

- Siguientes(E) = {$, )}
- Siguientes(E’) = {$, )}
- Siguientes(T) = {+, $, )}
- Siguientes(T’) = {+, $, )}
- Siguientes(F) = {*, +, $, )} 


Conjunto de predicción: 

- Predicción(F -> id) = {id}
- Predicción(F -> ( E )) = {(}
- Predicción(T’ -> ℇ ) = {+, $, )}
- Predicción(T’ -> * F T’) = {*}
- Predicción(T -> F T’) = {(, id}
- Predicción(E’ -> ℇ ) = {$, )}
- Predicción(E’ -> + T E’) = {+}
- Predicción(E -> T E’) = {(, id} 

Con la predicción se comprueba de que es LL(1), en esta no se repiten entre reglas.

### Algoritmo:

Para realizar el ascendente se debe tener en cuenta que este se construye de abajo hacia arriba, desde las hojas hasta la raíz (contrario al descendente que es de arriba a abajo). Para este algoritmo se hacen dos operaciones básicas:

SHIFT (Desplazar)
- Toma el siguiente token de la entrada.
- Lo coloca en la pila.

REDUCE (Reducir)
- Busca el extremo derecho de una producción en el tope de la pila.
- Reemplaza esos símbolos por el símbolo del lado izquierdo.

<br>

**Ejemplo:**

- Paso 1: Pila=[] Entrada=[id, +, id, $]
  - -> SHIFT id

- Paso 2: Pila=[id] Entrada=[+, id, $]
  -  -> REDUCE F->id (porque 'id' está en el tope)

- Paso 3: Pila=[F] Entrada=[+, id, $]
  - -> REDUCE T->F (porque 'F' está en el tope)

- Paso 4: Pila=[T] Entrada=[+, id, $]
  - -> REDUCE E->T (viene '+' después, es seguro reducir)

- Paso 5: Pila=[E] Entrada=[+, id, $]
  - -> SHIFT +

- Paso 6: Pila=[E, +] Entrada=[id, $]
  - -> SHIFT id

- Paso 7: Pila=[E, +, id] Entrada=[$]
  - -> REDUCE F->id

- Paso 8: Pila=[E, +, F] Entrada=[$]
  - -> REDUCE T->F

- Paso 9: Pila=[E, +, T] Entrada=[$]
  - -> REDUCE E->E+T (se encuentra la reglas original)

- Paso 10: Pila=[E] Entrada=[$]
  - -> ACEPTAR

La pregunta principal de este algoritmo es ¿Qué producciones me llevan a E? para ir subiendo hasta llegar al tope. Lo fácil de esta técnica es que no cae en bucles infinitos como en el descendente ni necesita una gramática modificada (E -> E + T e imprime infinitamente E), el ascendente lee primero el token, luego reduce. Nunca cae en bucles porque trabaja con lo que ya tiene.

### Resultados

<img width="586" height="172" alt="image" src="https://github.com/user-attachments/assets/66939ad9-9ae9-4baf-92ae-030351141741" />

## Punto 4

Implemente un parser usando el algoritmo CYK. Realice pruebas sobre el rendimiento de este algoritmo comparándolo con un parser de tipo predictivo. Realice una comparación entre el rendimiento de los dos parser.


**Analizador predictivo:**

Un analizador predictivo es un **analizador descendente recursivo** sin backtracking ni copia de seguridad. El parser predictivo intenta predecir qué producción usar basándose en el símbolo actual de entrada y el siguiente token (lookahead).
Construye el árbol de derivación desde la raíz hacia las hojas.

El parser predictivo solo funciona con gramáticas LL(1) (sin recursión izquierda, deterministas).

**Algoritmo CYK:**

El algoritmo CYK (Cocke–Younger–Kasami) intenta reconstruir el árbol de derivación desde las hojas (símbolos terminales) hasta la raíz (símbolo inicial).
requiere gramáticas en Forma Normal de Chomsky (FNC).

Por tanto no se puede usar literalmente la misma gramática para ambos parsers porque deben tener formas diferentes. Así se usarám gramáticas equivalentes que generen el mismo lenguaje.


Para comparar el rendimeinto se usarán diferentes longitudes de cadenas (tokens), y asi verificar que tanto crece el coste de parsing con el tamaño de la entrada.

Complejidad	

CYK	-> O(n³)
Predictivo (LL(1)) -> O(n)


<img width="1216" height="489" alt="image" src="https://github.com/user-attachments/assets/386cc2a7-2f5d-43b0-a7d7-8bb6c81d9fea" />

incluso usando entradas que requieran anifamiento y priofundidad 

    
     [
        ("( ( ( id ) ) )", 7),
        ("( ( ( id + id ) ) )", 9),
        ("( ( id ) + ( id ) )", 9),
        ("( ( ( id ) + ( id ) ) * id )", 13),
    ]
  

<img width="758" height="486" alt="image" src="https://github.com/user-attachments/assets/32c176f9-eb2c-4e8c-ae75-77e360292ed5" />



---

## Bibliografía 
- https://www.geeksforgeeks.org/python/compiler-design-ll1-parser-in-python/
- https://www.geeksforgeeks.org/compiler-design/cocke-younger-kasami-cyk-algorithm/
