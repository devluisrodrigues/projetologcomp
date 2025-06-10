#include <stdio.h>

int yyparse(void);
// yyparse é uma função do analisador sintático gerado pelo Bison, servirá para analizar o código fonte

int main() {
    // se o analisador sintático retornar 0, significa que o código fonte é válido
    if (yyparse() == 0) {
        printf("Programa válido!\n");
    } else {
        printf("Erro na análise, programa não é válido.\n");
    }
    return 0;
}
