# Parcial 2

## Punto 1

## etc

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

### Transformar:

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
Para realizar el ascendente se debe tener en cuenta que este se construye de abajo hacia arriba, desde las hojas hasta la raíz (contraria al descendente que es de arriba a abajo) 
