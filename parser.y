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
    ABRE_PAREN ID VIRGULA NUM FECHA_PAREN ATRIBUI ABRE_PAREN expressao VIRGULA DATA FECHA_PAREN
    | RECEBER ABRE_PAREN NUM VIRGULA expressao FECHA_PAREN
    | ALOCAR ABRE_PAREN NUM VIRGULA expressao VIRGULA ID FECHA_PAREN
    | VENDER ABRE_PAREN NUM VIRGULA expressao FECHA_PAREN
    | DESCARTAR ABRE_PAREN NUM VIRGULA expressao FECHA_PAREN
    | EXIBIR ABRE_PAREN NUM FECHA_PAREN
    | EXIBIR ABRE_PAREN ID FECHA_PAREN
    | CONFERIR ABRE_PAREN NUM FECHA_PAREN
    | VALIDADE ABRE_PAREN NUM FECHA_PAREN
    | MOVER ABRE_PAREN NUM VIRGULA expressao VIRGULA ID VIRGULA ID FECHA_PAREN
    | ENQUANTO ABRE_PAREN condicao FECHA_PAREN bloco
    | SE ABRE_PAREN condicao FECHA_PAREN bloco
    | SE ABRE_PAREN condicao FECHA_PAREN bloco SENAO bloco
    ;

condicao:
    bterm
    | condicao OR bterm
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
    | ABRE_PAREN expressao FECHA_PAREN
    | CONFERIR ABRE_PAREN NUM FECHA_PAREN
    | VALIDADE ABRE_PAREN NUM FECHA_PAREN
    | HOJE ABRE_PAREN FECHA_PAREN
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Verifique o trecho '%s': %s\n", 
            yytext, s);
}