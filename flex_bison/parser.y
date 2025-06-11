%{
#include <stdio.h>
#include <stdlib.h>

extern int yylineno;
extern char* yytext;

void yyerror(const char *s);
int yylex(void);

%}

%union {
    int num;
    char* str;
}

%token <num> NUM
%token <str> ID
%token <str> DATA

%token ABRE_CHAVE FECHA_CHAVE ABRE_PAREN FECHA_PAREN VIRGULA NOVA_LINHA ATRIBUI OR AND COMPARA_IGUAL MAIOR MENOR MAIS MENOS MULT DIV NOT

%token ENTRADA RECEBER ALOCAR VENDER DESCARTAR EXIBIR CONFERIR VALIDADE HOJE MOVER ENQUANTO SE SENAO

%token BOOL_VAR INT_VAR TRUE FALSE

%start program

%%

program:
    bloco
    ;

bloco:
    ABRE_CHAVE NOVA_LINHA lista_statements FECHA_CHAVE
    ;

lista_statements:
    | NOVA_LINHA lista_statements
    | statement NOVA_LINHA lista_statements
    ;

statement:
      ENTRADA_ABRE
    | RECEBER ABRE_PAREN NUM VIRGULA expressao FECHA_PAREN
    | ALOCAR ABRE_PAREN NUM VIRGULA expressao VIRGULA ID FECHA_PAREN
    | VENDER ABRE_PAREN NUM VIRGULA expressao vender_pos FECHA_PAREN
    | DESCARTAR ABRE_PAREN NUM VIRGULA expressao descartar_pos FECHA_PAREN
    | EXIBIR ABRE_PAREN exibir_arg FECHA_PAREN
    | CONFERIR ABRE_PAREN NUM conferir_pos FECHA_PAREN
    | MOVER ABRE_PAREN NUM VIRGULA expressao VIRGULA ID VIRGULA ID FECHA_PAREN
    | VARDEC
    | VARASSIGN
    | ENQUANTO ABRE_PAREN bexpression FECHA_PAREN bloco
    | SE ABRE_PAREN bexpression FECHA_PAREN bloco
    | SE ABRE_PAREN bexpression FECHA_PAREN bloco SENAO bloco
    ;

ENTRADA_ABRE:
    ABRE_PAREN ID VIRGULA NUM FECHA_PAREN ATRIBUI ABRE_PAREN expressao VIRGULA DATA FECHA_PAREN
    ;

vender_pos:
      /* vazio */
    | VIRGULA ID
    ;

descartar_pos:
      /* vazio */
    | VIRGULA ID
    ;

exibir_arg:
      NUM
    | ID
    ;

conferir_pos:
      /* vazio */
    | VIRGULA ID
    ;

VARDEC:
      BOOL_VAR ID varinit
    | INT_VAR ID varinit
    ;

varinit:
      /* vazio */
    | ATRIBUI bexpression
    ;

VARASSIGN:
      ID ATRIBUI bexpression
    ;

bexpression:
      bterm
    | bexpression OR bterm
    ;

bterm:
    rexpre
    | bterm AND rexpre
    ;

rexpre:
    expressao
    | expressao COMPARA_IGUAL expressao
    | expressao MAIOR expressao
    | expressao MENOR expressao
    ;

expressao:
    termo
    | expressao MAIS termo
    | expressao MENOS termo
    ;

termo:
    fator
    | termo MULT fator
    | termo DIV fator
    ;

fator:
      MAIS fator
    | MENOS fator
    | NOT fator
    | NUM
    | ID
    | TRUE
    | FALSE
    | ABRE_PAREN expressao FECHA_PAREN
    | CONFERIR ABRE_PAREN NUM FECHA_PAREN
    | CONFERIR ABRE_PAREN NUM VIRGULA ID FECHA_PAREN
    | VALIDADE ABRE_PAREN NUM VIRGULA ID VIRGULA NUM FECHA_PAREN
    | HOJE ABRE_PAREN FECHA_PAREN
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Verifique o trecho '%s': %s\n", 
            yytext, s);
}