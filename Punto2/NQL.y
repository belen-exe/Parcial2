%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "NQL_types.h" 

extern int yylex();
extern FILE *yyin;
void yyerror(const char *s);

Table tables[MAX_TABLES];
int table_count = 0;

Record temp_record;
int temp_field_count = 0;

char current_table[MAX_FIELD_NAME];
char where_field[MAX_FIELD_NAME];
char where_op[10];
Value where_value;
int has_where = 0;

Table* find_table(const char* name) {
    for (int i = 0; i < table_count; i++) {
        if (strcmp(tables[i].name, name) == 0) return &tables[i];
    }
    return NULL;
}

Table* create_table_if_not_exists(const char* name) {
    Table* t = find_table(name);
    if (t) return t;
    if (table_count >= MAX_TABLES) return NULL;
    strcpy(tables[table_count].name, name);
    tables[table_count].record_count = 0;
    tables[table_count].next_id = 1;
    return &tables[table_count++];
}

void print_value(Value* v) {
    switch (v->type) {
        case TYPE_NUMBER: printf("%.2f", v->data.num); break;
        case TYPE_STRING: printf("\"%s\"", v->data.str); break;
        case TYPE_BOOL:   printf("%s", v->data.boolean ? "true" : "false"); break;
        case TYPE_NULL:   printf("null"); break;
    }
}

int compare_values(Value* a, Value* b, const char* op) {
    if (strcmp(op, "=") == 0) {
        if (a->type == TYPE_NUMBER && b->type == TYPE_NUMBER) return a->data.num == b->data.num;
        if (a->type == TYPE_STRING && b->type == TYPE_STRING) return strcmp(a->data.str, b->data.str) == 0;
        if (a->type == TYPE_BOOL && b->type == TYPE_BOOL) return a->data.boolean == b->data.boolean;
    } else if (strcmp(op, "!=") == 0) {
        if (a->type == TYPE_NUMBER && b->type == TYPE_NUMBER) return a->data.num != b->data.num;
        if (a->type == TYPE_STRING && b->type == TYPE_STRING) return strcmp(a->data.str, b->data.str) != 0;
    } else if (a->type == TYPE_NUMBER && b->type == TYPE_NUMBER) {
        if (strcmp(op, ">") == 0) return a->data.num > b->data.num;
        if (strcmp(op, "<") == 0) return a->data.num < b->data.num;
        if (strcmp(op, ">=") == 0) return a->data.num >= b->data.num;
        if (strcmp(op, "<=") == 0) return a->data.num <= b->data.num;
    }
    return 0;
}

int evaluate_where(Record* r) {
    if (!has_where) return 1;
    for (int i = 0; i < r->field_count; i++) {
        if (strcmp(r->fields[i].name, where_field) == 0)
            return compare_values(&r->fields[i].value, &where_value, where_op);
    }
    return 0;
}

void insert_record() {
    Table* t = create_table_if_not_exists(current_table);
    if (!t || t->record_count >= MAX_RECORDS) {
        printf("Error: No se puede insertar\n\n");
        return;
    }
    Record* r = &t->records[t->record_count];
    r->id = t->next_id++;
    r->active = 1;
    r->field_count = temp_field_count;
    for (int i = 0; i < temp_field_count; i++)
        r->fields[i] = temp_record.fields[i];
    t->record_count++;

    printf("INSERT → '%s' (ID: %d)\n", current_table, r->id);
    for (int i = 0; i < r->field_count; i++) {
        printf(" %s: ", r->fields[i].name);
        print_value(&r->fields[i].value);
        printf("\n");
    }
    printf("\n");
}

void select_records() {
    Table* t = find_table(current_table);
    if (!t) {
        printf("Tabla '%s' vacía\n\n", current_table);
        return;
    }
    int found = 0;
    printf("SELECT → '%s'\n", current_table);
    if (has_where) {
        printf(" WHERE %s %s ", where_field, where_op);
        print_value(&where_value);
        printf("\n");
    }
    printf("════════════════════════════════════════\n");
    for (int i = 0; i < t->record_count; i++) {
        if (!t->records[i].active) continue;
        if (has_where && !evaluate_where(&t->records[i])) continue;
        found++;
        printf("\n[ID: %d]\n", t->records[i].id);
        for (int j = 0; j < t->records[i].field_count; j++) {
            printf(" %s: ", t->records[i].fields[j].name);
            print_value(&t->records[i].fields[j].value);
            printf("\n");
        }
    }
    printf("\n════════════════════════════════════════\n");
    printf("Total: %d registro(s)\n\n", found);
}

void update_records() {
    Table* t = find_table(current_table);
    if (!t) {
        printf("Tabla '%s' no existe\n\n", current_table);
        return;
    }
    int updated = 0;
    for (int i = 0; i < t->record_count; i++) {
        if (!t->records[i].active) continue;
        if (has_where && !evaluate_where(&t->records[i])) continue;
        for (int j = 0; j < temp_field_count; j++) {
            int found = 0;
            for (int k = 0; k < t->records[i].field_count; k++) {
                if (strcmp(t->records[i].fields[k].name, temp_record.fields[j].name) == 0) {
                    t->records[i].fields[k].value = temp_record.fields[j].value;
                    found = 1;
                    break;
                }
            }
            if (!found && t->records[i].field_count < MAX_FIELDS)
                t->records[i].fields[t->records[i].field_count++] = temp_record.fields[j];
        }
        updated++;
    }
    printf("UPDATE → '%s'\n Actualizados: %d registro(s)\n", current_table, updated);
    if (has_where) {
        printf(" WHERE %s %s ", where_field, where_op);
        print_value(&where_value);
        printf("\n");
    }
    printf("\n");
}

void delete_records() {
    Table* t = find_table(current_table);
    if (!t) {
        printf("Tabla '%s' no existe\n\n", current_table);
        return;
    }
    int deleted = 0;
    for (int i = 0; i < t->record_count; i++) {
        if (!t->records[i].active) continue;
        if (has_where && !evaluate_where(&t->records[i])) continue;
        t->records[i].active = 0;
        deleted++;
    }
    printf("DELETE → '%s'\n Eliminados: %d registro(s)\n", current_table, deleted);
    if (has_where) {
        printf(" WHERE %s %s ", where_field, where_op);
        print_value(&where_value);
        printf("\n");
    }
    printf("\n");
}
%}

%union {
    int bval;
    double fval;
    char *sval;
    Value val;
}

%token <sval> IDENTIFIER STRING
%token <fval> NUMBER
%token <bval> TRUE FALSE
%token NEW GET SET DROP WHERE NUL
%token EQ NE GT LT GE LE
%token LBRACE RBRACE LPAREN RPAREN COMMA COLON
%type <val> valor

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
    create_op
  | read_op
  | update_op
  | delete_op
;

create_op:
    NEW IDENTIFIER LBRACE { strcpy(current_table, $2); temp_field_count = 0; free($2); } pares RBRACE { insert_record(); }
;

read_op:
    GET IDENTIFIER { strcpy(current_table, $2); has_where = 0; free($2); select_records(); }
  | GET IDENTIFIER WHERE IDENTIFIER operador valor {
        strcpy(current_table, $2);
        strcpy(where_field, $4);
        where_value = $6;
        has_where = 1;
        free($2);
        free($4);
        select_records();
    }
;

update_op:
    SET IDENTIFIER LBRACE { strcpy(current_table, $2); temp_field_count = 0; free($2); } pares RBRACE opt_where { update_records(); }
;

opt_where:
    /* vacío */ { has_where = 0; }
  | WHERE IDENTIFIER operador valor {
        strcpy(where_field, $2);
        where_value = $4;
        has_where = 1;
        free($2);
    }
;

delete_op:
    DROP IDENTIFIER { strcpy(current_table, $2); has_where = 0; free($2); delete_records(); }
  | DROP IDENTIFIER WHERE IDENTIFIER operador valor {
        strcpy(current_table, $2);
        strcpy(where_field, $4);
        where_value = $6;
        has_where = 1;
        free($2);
        free($4);
        delete_records();
    }
;

operador:
    EQ { strcpy(where_op, "="); }
  | NE { strcpy(where_op, "!="); }
  | GT { strcpy(where_op, ">"); }
  | LT { strcpy(where_op, "<"); }
  | GE { strcpy(where_op, ">="); }
  | LE { strcpy(where_op, "<="); }
;

pares:
    par
  | pares COMMA par
;

par:
    IDENTIFIER COLON valor {
        strcpy(temp_record.fields[temp_field_count].name, $1);
        temp_record.fields[temp_field_count].value = $3;
        temp_field_count++;
        free($1);
    }
;

valor:
    NUMBER { $$.type = TYPE_NUMBER; $$.data.num = $1; }
  | STRING { $$.type = TYPE_STRING; strncpy($$.data.str, $1, MAX_VALUE_LEN - 1); free($1); }
  | TRUE { $$.type = TYPE_BOOL; $$.data.boolean = 1; }
  | FALSE { $$.type = TYPE_BOOL; $$.data.boolean = 0; }
  | NUL { $$.type = TYPE_NULL; }
;

%%

void yyerror(const char *s) {
    fprintf(stderr, "ERROR: %s\n\n", s);
}

int main(int argc, char **argv) {
    printf("║ NQL ║\n");
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            printf("Error: No se puede abrir '%s'\n", argv[1]);
            return 1;
        }
        yyin = file;
        printf("Ejecutando: %s\n\n", argv[1]);
        yyparse();
        fclose(yyin);
    } else {
        printf("Modo interactivo (Ctrl+D para salir)\n\n");
        yyparse();
    }
    return 0;
}

