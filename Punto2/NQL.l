%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "NQL.tab.h"
%}

%option noyywrap

%%

[ \t\r]+            { /* ignorar espacios */ }
\n                  { yylineno++; }
#.*                 { /* comentarios */ }
"//".*              { /* comentarios */ }

"new"               { return NEW; }
"get"               { return GET; }
"set"               { return SET; }
"drop"              { return DROP; }
"where"             { return WHERE; }
"sort"              { return SORT; }
"limit"             { return LIMIT; }
"asc"               { return ASC; }
"desc"              { return DESC; }

"true"              { yylval.bval = 1; return TRUE; }
"false"             { yylval.bval = 0; return FALSE; }
"null"              { return NUL; }

"="                 { return EQ; }
"!="                { return NE; }
">"                 { return GT; }
"<"                 { return LT; }
">="                { return GE; }
"<="                { return LE; }
"~"                 { return CONTAINS; }

"&"                 { return AND; }
"|"                 { return OR; }
"!"                 { return NOT; }

"+"                 { return PLUS; }
"-"                 { return MINUS; }
"*"                 { return MULT; }
"/"                 { return DIV; }

"{"                 { return LBRACE; }
"}"                 { return RBRACE; }
"("                 { return LPAREN; }
")"                 { return RPAREN; }
"["                 { return LBRACKET; }
"]"                 { return RBRACKET; }
","                 { return COMMA; }
":"                 { return COLON; }

[a-zA-Z_][a-zA-Z0-9_]*  { yylval.sval = strdup(yytext); return IDENTIFIER; }
[0-9]+(\.[0-9]+)?       { yylval.fval = atof(yytext); return NUMBER; }
\"[^\"]*\"|'[^']*'      { 
                          yylval.sval = strndup(yytext + 1, strlen(yytext) - 2); 
                          return STRING; 
                        }

.                   { printf("Error: caracter desconocido '%s' línea %d\n", yytext, yylineno); }

%%

