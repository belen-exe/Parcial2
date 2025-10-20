%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex();
extern int yylineno;
extern FILE *yyin;
void yyerror(const char *s);

int error_count = 0;
int statement_count = 0;
%}

%union {
    int bval;
    double fval;
    char *sval;
}

%token <sval> IDENTIFIER STRING
%token <fval> NUMBER
%token <bval> TRUE FALSE
%token NEW GET SET DROP WHERE SORT LIMIT ASC DESC NUL
%token EQ NE GT LT GE LE CONTAINS
%token AND OR NOT
%token PLUS MINUS MULT DIV
%token LBRACE RBRACE LPAREN RPAREN LBRACKET RBRACKET COMMA COLON

%type <sval> valor operador filtro condicion expresion_comp

%left OR
%left AND
%left NOT
%left EQ NE GT LT GE LE CONTAINS
%left PLUS MINUS
%left MULT DIV

%%

programa:
    /* vacío */
    | sentencias
    ;

sentencias:
    sentencia
    | sentencias sentencia
    ;

sentencia:
    create_op { statement_count++; printf("\n"); }
    | read_op   { statement_count++; printf("\n"); }
    | update_op { statement_count++; printf("\n"); }
    | delete_op { statement_count++; printf("\n"); }
    ;

/* ===== CREATE ===== */
create_op:
    NEW IDENTIFIER LBRACE pares RBRACE {
        printf("\n[CREATE]\n");
        printf("   INSERT INTO %s\n", $2);
        free($2);
    }
    ;

/* ===== READ ===== */
read_op:
    GET IDENTIFIER {
        printf("\n[READ]\n");
        printf("   SELECT * FROM %s;\n", $2);
        free($2);
    }
    | GET IDENTIFIER filtro {
        printf("\n[READ]\n");
        printf("   SELECT * FROM %s\n", $2);
        printf("   %s;\n", $3);
        free($2);
        free($3);
    }
    | GET IDENTIFIER opciones {
        printf("\n[READ]\n");
        printf("   SELECT * FROM %s\n", $2);
        free($2);
    }
    | GET IDENTIFIER filtro opciones {
        printf("\n[READ]\n");
        printf("   SELECT * FROM %s\n", $2);
        printf("   %s\n", $3);
        free($2);
        free($3);
    }
    ;

/* ===== UPDATE ===== */
update_op:
    SET IDENTIFIER LBRACE pares RBRACE {
        printf("\n  [UPDATE]\n");
        printf("     UPDATE %s\n", $2);
        printf("     SIN FILTRO - Actualizará TODOS los registros\n");
        free($2);
    }
    | SET IDENTIFIER LBRACE pares RBRACE filtro {
        printf("\n[UPDATE]\n");
        printf("   UPDATE %s\n", $2);
        printf("   %s;\n", $6);
        free($2);
        free($6);
    }
    ;

/* ===== DELETE ===== */
delete_op:
    DROP IDENTIFIER {
        printf("\n[DELETE]\n");
        printf("   DELETE FROM %s;\n", $2);
        printf("   SIN FILTRO - Eliminará TODOS los registros\n");
        free($2);
    }
    | DROP IDENTIFIER filtro {
        printf("\n[DELETE]\n");
        printf("   DELETE FROM %s\n", $2);
        printf("   %s;\n", $3);
        free($2);
        free($3);
    }
    ;

/* ===== FILTROS ===== */
filtro:
    WHERE condicion {
        size_t len = strlen($2) + 10;
        $$ = malloc(len);
        snprintf($$, len, "WHERE %s", $2);
        free($2);
    }
    ;

condicion:
    expresion_comp {
        $$ = $1;
    }
    | condicion AND condicion { 
        size_t len = strlen($1) + strlen($3) + 10;
        $$ = malloc(len);
        snprintf($$, len, "%s AND %s", $1, $3);
        free($1);
        free($3);
    }
    | condicion OR condicion  { 
        size_t len = strlen($1) + strlen($3) + 10;
        $$ = malloc(len);
        snprintf($$, len, "%s OR %s", $1, $3);
        free($1);
        free($3);
    }
    | NOT condicion { 
        size_t len = strlen($2) + 10;
        $$ = malloc(len);
        snprintf($$, len, "NOT %s", $2);
        free($2);
    }
    | LPAREN condicion RPAREN {
        size_t len = strlen($2) + 5;
        $$ = malloc(len);
        snprintf($$, len, "(%s)", $2);
        free($2);
    }
    ;

expresion_comp:
    IDENTIFIER operador valor {
        size_t len = strlen($1) + strlen($2) + strlen($3) + 5;
        $$ = malloc(len);
        snprintf($$, len, "%s%s%s", $1, $2, $3);
        free($1);
        free($2);
        free($3);
    }
    ;

operador:
    EQ       { $$ = strdup(" = "); }
    | NE     { $$ = strdup(" != "); }
    | GT     { $$ = strdup(" > "); }
    | LT     { $$ = strdup(" < "); }
    | GE     { $$ = strdup(" >= "); }
    | LE     { $$ = strdup(" <= "); }
    | CONTAINS { $$ = strdup(" LIKE "); }
    ;

/* ===== OPCIONES ===== */
opciones:
    opcion
    | opciones opcion
    ;

opcion:
    SORT IDENTIFIER { 
        printf("   ORDER BY %s ASC\n", $2); 
        free($2); 
    }
    | SORT IDENTIFIER ASC { 
        printf("   ORDER BY %s ASC\n", $2); 
        free($2); 
    }
    | SORT IDENTIFIER DESC { 
        printf("   ORDER BY %s DESC\n", $2); 
        free($2); 
    }
    | LIMIT NUMBER { 
        printf("   LIMIT %.0f\n", $2); 
    }
    ;

/* ===== VALORES ===== */
pares:
    par
    | pares COMMA par
    ;

par:
    IDENTIFIER COLON valor {
        printf("      %s = %s\n", $1, $3);
        free($1);
        free($3);
    }
    ;

valor:
    NUMBER      { 
        $$ = malloc(50);
        snprintf($$, 50, "%.0f", $1);
    }
    | STRING    { 
        size_t len = strlen($1) + 10;
        $$ = malloc(len);
        snprintf($$, len, "'%s'", $1);
        free($1);
    }
    | TRUE      { $$ = strdup("TRUE"); }
    | FALSE     { $$ = strdup("FALSE"); }
    | NUL       { $$ = strdup("NULL"); }
    | IDENTIFIER { 
        $$ = $1;
    }
    | arreglo   { $$ = strdup("[ARRAY]"); }
    | valor PLUS valor  { 
        size_t len = strlen($1) + strlen($3) + 10;
        $$ = malloc(len);
        snprintf($$, len, "%s + %s", $1, $3);
        free($1);
        free($3);
    }
    | valor MINUS valor { 
        size_t len = strlen($1) + strlen($3) + 10;
        $$ = malloc(len);
        snprintf($$, len, "%s - %s", $1, $3);
        free($1);
        free($3);
    }
    | valor MULT valor  { 
        size_t len = strlen($1) + strlen($3) + 10;
        $$ = malloc(len);
        snprintf($$, len, "%s * %s", $1, $3);
        free($1);
        free($3);
    }
    | valor DIV valor   { 
        size_t len = strlen($1) + strlen($3) + 10;
        $$ = malloc(len);
        snprintf($$, len, "%s / %s", $1, $3);
        free($1);
        free($3);
    }
    | LPAREN valor RPAREN    { $$ = $2; }
    ;

arreglo:
    LBRACKET lista_valores RBRACKET 
    | LBRACKET RBRACKET
    ;

lista_valores:
    valor_array
    | lista_valores COMMA valor_array
    ;

valor_array:
    NUMBER      { }
    | STRING    { free($1); }
    | TRUE      { }
    | FALSE     { }
    | IDENTIFIER { free($1); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "\nERROR DE SINTAXIS (línea %d): %s\n\n", yylineno, s);
    error_count++;
}

int main(int argc, char **argv) {
    printf("║   NQL   ║\n");

    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("Error abriendo archivo");
            return 1;
        }
        yyin = file;
        printf("Archivo: %s\n", argv[1]);
        printf("─────────────────────────────────────────\n");
    } else {
        printf("Modo interactivo (Ctrl+D para terminar)\n");
        printf("─────────────────────────────────────────\n");
    }

    int result = yyparse();

    if (result == 0 && error_count == 0) {
        printf("║  ANÁLISIS COMPLETADO EXITOSAMENTE  ║\n");
        printf("║  Sentencias procesadas: %-3d        ║\n", statement_count);
        printf("║  Errores encontrados: 0            ║\n");
    } else {
        printf("║  ANÁLISIS COMPLETADO CON ERRORES   ║\n");
        printf("║  Sentencias procesadas: %-3d        ║\n", statement_count);
        printf("║  Errores encontrados: %-3d         ║\n", error_count);
    }
    if (argc > 1) {
        fclose(yyin);
    }

    return result;
}
