%{
#include "parser.tab.h"
#include <string.h>
#include <stdlib.h>

%}

DIGITO     [0-9]
LETRA      [a-zA-Z]
ID         {LETRA}({LETRA}|{DIGITO}|_)*
NUM        {DIGITO}+
DATA       {DIGITO}{DIGITO}\/{DIGITO}{DIGITO}\/{DIGITO}{DIGITO}{DIGITO}{DIGITO}

%%
"\n"             return NOVA_LINHA;
"{"              return ABRE_CHAVE;
"}"              return FECHA_CHAVE;
","              return VIRGULA;
"("              return ABRE_PAREN;
")"              return FECHA_PAREN;
"="              return IGUAL;
"||"             return OR;
"&&"             return AND;
"=="             return COMPARA_IGUAL;
">"              return MAIOR;
"<"              return MENOR;
"+"              return MAIS;
"-"              return MENOS;
"*"              return MULT;
"/"              return DIV;
"!"              return NOT;

"entrada"        return ENTRADA;
"receber"        return RECEBER;
"alocar"         return ALOCAR;
"vender"         return VENDER;
"descartar"      return DESCARTAR;
"exibir"         return EXIBIR;
"estoque"        return CONFERIR;
"validade"       return VALIDADE;
"hoje"           return HOJE;
"mover"          return MOVER;
"enquanto"       return ENQUANTO;
"se"             return SE;
"senao"          return SENAO;

{DATA}           { yylval.str = strdup(yytext); return DATA; }
{NUM}            { yylval.num = atoi(yytext); return NUM; }
{ID}             { yylval.str = strdup(yytext); return ID; }

[ \t\r]+         ;

.                return yytext[0];

%%

int yywrap() { return 1; }
