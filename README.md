# Projeto Logcomp

Para a atividade supervisionada da matéria, o aluno idealizou uma linguagem voltada para o controle e gerenciamento do fluxo de estoque de um galpão logístico. A ideia seria criar uma linguagem capaz de interpretar as atividades realizadas em ambientes logísticos como recebimento de produtos, estocagem e venda dos produtos, por exemplo.

A operação logística imaginada pode ser quebrada em três etapas macros:

- Recebimento: Etapa inicial, entrada de produtos na cadeia logística, geralmente essa etapa é acompanhada de um check de qualidade e quantidade
  
- Alocação: Feito o recebimento, é reconhecida a entrada dos produtos na cadeia, mas ainda é necessário atribuir uma posição.
  
- Venda/Descarte : Feita a alocação, é necessário remover o item do estoque em caso de venda, ou descartá-lo.
  
Observação: Para a operação imaginada, cada produto dispõe de:

**Nome, SKU ( identificador único), quantidade e data de validade.**

---

**EBNF pensada:**

BLOCO = "{", "\n", { STATEMENT }, "}";

STATEMENT = ( λ | ENTRADA | RECEBER | ALOCAR | VENDER | DESCARTAR | EXIBIR | CONFERIR | VALIDADE | MOVER |ENQUANTO | SE), "\n" ;

ENTRADA = "(",NOME, ",", SKU, ")", "=", "(", EXPRESSION, ",", DATA_VALIDADE, ")”;

RECEBER = "receber", "(", SKU, ",", EXPRESSION, ")";

MOVER = "mover", "(", SKU, ",", EXPRESSION, POSICAO,",", POSICAO ")" ;

ALOCAR = "alocar", "(", SKU, ",", EXPRESSION, ",", POSICAO, ")";

VENDER = "vender", "(", SKU, ",", EXPRESSION, ")";

DESCARTAR = "descartar", "(", SKU, ",", EXPRESSION, ")";

EXIBIR = "exibir", "(", SKU | POSICAO, ")" ;

CONFERIR = "estoque, "(", SKU, ")";

VALIDADE = "validade” , "(", SKU, ")";

ENQUANTO = "enquanto", "(", CONDICAO, ")", BLOCO ;

SE = "se", "(", CONDICAO, ")", BLOCO, [ "senao", BLOCO ]

CONDICAO = BTERM, { "||", BTERM } ;

BTERM = REXPRE, { "&&", REXPRE } ;

REXPRE = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;

EXPRESSION = TERM, { ("+" | "-"), TERM } ;

TERM = FACTOR, { ("*" | "/"), FACTOR } ;

FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | CONFERIR| VALIDADE | HOJE;

DATA_VALIDADE = DIGIT, DIGIT, "/”, DIGIT, DIGIT, "/”, DIGIT, DIGIT, DIGIT, DIGIT;

HOJE = "hoje", "(", ")" ;

POSICAO = LETTER, { LETTER | DIGIT | "_" } ;

NOME = LETTER, { LETTER | DIGIT | "_" } ;

NUMBER = DIGIT, { DIGIT } ;

SKU = DIGIT, { DIGIT } ;

LETTER = ( a | ... | z | A | ... | Z ) ;

DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
