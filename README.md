# Parcial 2

## Punto 1

### Notación BNF Extendida

- `|` : alternativa (OR)
- `[]` : opcional (0 o 1 vez)
- `{}` : repetición (0 o más veces)
- `()` : agrupación
- `<>` : símbolo no terminal
- `""` : símbolo terminal (literal)

---

### Gramática Completa

```bnf
# ===== PROGRAMA =====

<programa> ::= { <sentencia> }

<sentencia> ::= <create_op>
              | <read_op>
              | <update_op>
              | <delete_op>

# ===== OPERACIONES CRUD =====

# CREATE (INSERT)
<create_op> ::= "new" <identificador> "{" <pares> "}"

# READ (SELECT)
<read_op> ::= "get" <identificador> [ <filtro> ] [ <opciones> ]

# UPDATE
<update_op> ::= "set" <identificador> "{" <pares> "}" [ <filtro> ]

# DELETE
<delete_op> ::= "drop" <identificador> [ <filtro> ]

# ===== FILTROS Y CONDICIONES =====

<filtro> ::= "where" <condicion>

<condicion> ::= <expresion_comp>
              | <condicion> "&" <condicion>      # AND
              | <condicion> "|" <condicion>      # OR
              | "!" <condicion>                  # NOT
              | "(" <condicion> ")"

<expresion_comp> ::= <identificador> <operador> <valor>

<operador> ::= "=" | "!=" | ">" | "<" | ">=" | "<=" | "~"

# ===== OPCIONES DE CONSULTA =====

<opciones> ::= <opcion> { <opcion> }

<opcion> ::= "sort" <identificador> [ <direccion> ]
           | "limit" <numero>

<direccion> ::= "asc" | "desc"

# ===== VALORES Y EXPRESIONES =====

<pares> ::= <par> { "," <par> }

<par> ::= <identificador> ":" <valor>

<valor> ::= <numero>
          | <cadena>
          | <booleano>
          | <nulo>
          | <arreglo>
          | <identificador>                     # Referencia a campo
          | <valor> <op_aritmetico> <identificador>
          | "(" <valor> ")"

<op_aritmetico> ::= "+" | "-" | "*" | "/"

<arreglo> ::= "[" [ <lista_valores> ] "]"

<lista_valores> ::= <valor_simple> { "," <valor_simple> }

<valor_simple> ::= <numero> | <cadena> | <booleano> | <identificador>

# ===== ELEMENTOS LÉXICOS =====

<numero> ::= <digito>+ [ "." <digito>+ ]

<cadena> ::= '"' <caracter>* '"' | "'" <caracter>* "'"

<booleano> ::= "true" | "false"

<nulo> ::= "null"

<identificador> ::= <letra> { <letra> | <digito> | "_" }

<letra> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" | "_"

<digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

<caracter> ::= cualquier carácter Unicode excepto comillas o caracteres de escape

# ===== COMENTARIOS =====

<comentario> ::= "#" <cualquier_caracter_hasta_fin_de_linea>
               | "//" <cualquier_caracter_hasta_fin_de_linea>
```

---

### Palabras Reservadas

```
new get set drop where sort limit asc desc true false null
```

---

### Operadores

#### Comparación
- `=` : Igual a
- `!=` : Diferente de
- `>` : Mayor que
- `<` : Menor que
- `>=` : Mayor o igual que
- `<=` : Menor o igual que
- `~` : Contiene (búsqueda de texto)

#### Lógicos
- `&` : AND (y lógico)
- `|` : OR (o lógico)
- `!` : NOT (negación)

#### Aritméticos
- `+` : Suma
- `-` : Resta
- `*` : Multiplicación
- `/` : División

---

### Símbolos Especiales

```
{  }  [  ]  (  )  ,  :
```

---

### Precedencia de Operadores

De mayor a menor precedencia:

1. `()` - Paréntesis
2. `!` - NOT (negación)
3. `*`, `/` - Multiplicación, división
4. `+`, `-` - Suma, resta
5. `=`, `!=`, `>`, `<`, `>=`, `<=`, `~` - Operadores de comparación
6. `&` - AND
7. `|` - OR

---

### Asociatividad

- Operadores aritméticos: **Izquierda a derecha**
- Operadores lógicos: **Izquierda a derecha**
- Operadores de comparación: **No asociativos** (no se pueden encadenar)

---

### Reglas Semánticas

#### 1. Identificadores
- Deben comenzar con letra o guión bajo
- Pueden contener letras, dígitos y guiones bajos
- Son case-sensitive (sensibles a mayúsculas/minúsculas)

#### 2. Cadenas
- Pueden usar comillas dobles `"` o simples `'`
- No soportan caracteres de escape en esta versión

#### 3. Números
- Pueden ser enteros: `42`, `0`, `999`
- Pueden ser decimales: `3.14`, `0.5`, `99.99`
- No soportan notación científica en esta versión

#### 4. Arrays
- Pueden contener valores de cualquier tipo
- Elementos separados por comas
- Pueden estar vacíos: `[]`

#### 5. Comentarios
- Desde `#` o `//` hasta el fin de línea
- Son ignorados por el parser
- No hay comentarios multilínea en esta versión

---

### Tabla de Tokens

| Token | Tipo | Patrón Léxico | Ejemplo |
|-------|------|---------------|---------|
| `NEW` | Palabra clave | `new` | `new` |
| `GET` | Palabra clave | `get` | `get` |
| `SET` | Palabra clave | `set` | `set` |
| `DROP` | Palabra clave | `drop` | `drop` |
| `WHERE` | Palabra clave | `where` | `where` |
| `SORT` | Palabra clave | `sort` | `sort` |
| `LIMIT` | Palabra clave | `limit` | `limit` |
| `ASC` | Palabra clave | `asc` | `asc` |
| `DESC` | Palabra clave | `desc` | `desc` |
| `TRUE` | Booleano | `true` | `true` |
| `FALSE` | Booleano | `false` | `false` |
| `NULL` | Nulo | `null` | `null` |
| `IDENTIFIER` | Identificador | `[a-zA-Z_][a-zA-Z0-9_]*` | `users`, `age_2` |
| `NUMBER` | Número | `[0-9]+(\.[0-9]+)?` | `42`, `3.14` |
| `STRING` | Cadena | `"[^"]*"` o `'[^']*'` | `"Ana"`, `'texto'` |
| `EQ` | Operador | `=` | `=` |
| `NE` | Operador | `!=` | `!=` |
| `GT` | Operador | `>` | `>` |
| `LT` | Operador | `<` | `<` |
| `GE` | Operador | `>=` | `>=` |
| `LE` | Operador | `<=` | `<=` |
| `CONTAINS` | Operador | `~` | `~` |
| `AND` | Lógico | `&` | `&` |
| `OR` | Lógico | `\|` | `\|` |
| `NOT` | Lógico | `!` | `!` |
| `PLUS` | Aritmético | `+` | `+` |
| `MINUS` | Aritmético | `-` | `-` |
| `MULT` | Aritmético | `*` | `*` |
| `DIV` | Aritmético | `/` | `/` |
| `LBRACE` | Delimitador | `{` | `{` |
| `RBRACE` | Delimitador | `}` | `}` |
| `LPAREN` | Delimitador | `(` | `(` |
| `RPAREN` | Delimitador | `)` | `)` |
| `LBRACKET` | Delimitador | `[` | `[` |
| `RBRACKET` | Delimitador | `]` | `]` |
| `COMMA` | Delimitador | `,` | `,` |
| `COLON` | Delimitador | `:` | `:` |

---

### Ejemplos Completos de Sentencias Válidas

```NQL
# CREATE
new users { name: "Ana", age: 25, active: true }
new products { name: "Laptop", price: 999.99, tags: ["tech", "computer"] }

# READ
get users
get users where age > 18
get users where age >= 21 & active = true
get products where price < 1000 sort price desc
get posts where published = true sort views desc limit 10
get users where (role = "admin" | role = "mod") & active = true

# UPDATE
set users { age: 26 } where id = 1
set products { stock: stock - 1 } where id = 42
set users { last_login: "2025-10-19", login_count: login_count + 1 } where email = "ana@test.com"

# DELETE
drop users where id = 999
drop logs where created_at < "2024-01-01" & level = "debug"
drop sessions where expired = true
```

---

### Comparación con SQL

| Operación | SQL | NQL |
|-----------|-----|-------|
| INSERT | `INSERT INTO users VALUES (...)` | `new users { ... }` |
| SELECT ALL | `SELECT * FROM users` | `get users` |
| SELECT WHERE | `SELECT * FROM users WHERE age > 18` | `get users where age > 18` |
| UPDATE | `UPDATE users SET age = 26 WHERE id = 1` | `set users { age: 26 } where id = 1` |
| DELETE | `DELETE FROM users WHERE id = 1` | `drop users where id = 1` |
| ORDER BY | `SELECT * FROM users ORDER BY age DESC` | `get users sort age desc` |
| LIMIT | `SELECT * FROM users LIMIT 10` | `get users limit 10` |
| AND | `WHERE age > 18 AND active = true` | `where age > 18 & active = true` |
| OR | `WHERE role = 'admin' OR role = 'mod'` | `where role = "admin" \| role = "mod"` |
| LIKE | `WHERE name LIKE '%text%'` | `where name ~ "text"` |

---

### Notas Adicionales

1. **Espacios en blanco**: Pueden aparecer entre cualquier token y son ignorados
2. **Comentarios**: Pueden aparecer en cualquier lugar y son ignorados
3. **Case sensitivity**: Las palabras clave son case-sensitive (deben estar en minúsculas)
4. **Terminación**: Las sentencias no requieren punto y coma (`;`)
5. **Nuevas líneas**: Son tratadas como espacios en blanco

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

enfin
