# Projeto Logcomp

Para a atividade supervisionada da matéria, o aluno idealizou uma linguagem voltada para o controle e gerenciamento do fluxo de estoque de um galpão logístico. A ideia seria criar uma linguagem capaz de interpretar as atividades realizadas em ambientes logísticos como recebimento de produtos, estocagem e venda dos produtos, por exemplo.

A operação logística imaginada pode ser quebrada em três etapas macros:

- Recebimento: Etapa inicial, entrada de produtos na cadeia logística, geralmente essa etapa é acompanhada de um check de qualidade e quantidade
  
- Alocação: Feito o recebimento, é reconhecida a entrada dos produtos na cadeia, mas ainda é necessário atribuir uma posição.
  
- Venda/Descarte : Feita a alocação, é necessário remover o item do estoque em caso de venda, ou descartá-lo.
  
Observação: Para a operação imaginada, cada produto dispõe de:

**Nome, SKU ( identificador único), quantidade e data de validade.**

Assim, a linguagem poderia operar a partir de um estado inicial recebido, compilar e retornar o estado da logística após as operações realizadas.

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

CONFERIR = "estoque", "(", SKU, ")";

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


---

Entrada:

Uma possível entrada:
```
{
  "B2": [
    {
      "nome": "Feijao_Preto",
      "sku": "67890",
      "quantidade": 50,
      "validade": "15/11/2024"
    }
  ]
}

```
Com as seguintes operações:
```
{
(Arroz_Integral, 12345) = (100, 01/12/2025)
(Feijao_Preto, 67890) = (50, 15/11/2024)

receber(12345, 100)
receber(67890, 50)

alocar(12345, 100, A1)
alocar(67890, 50, B2)

exibir(A1)
exibir(B2)

se (validade(67890) < hoje()) {
    descartar(67890, 100)
} senao {
    vender(67890, 10)
}

vender(12345, 20)

estoque(12345)
estoque(67890)

exibir(12345)
}
```

Levaria a uma saída:

```
{
  "A1": [
    {
      "nome": "Arroz_Integral",
      "sku": "12345",
      "quantidade": 80,
      "validade": "01/12/2025"
    }
  ],
  "B2": []
}
```


---

** Flex e Bison**

Os arquivos do Flex e Bison foram criados para serem utilizados em conjunto, o arquivo `scanner.l` é o Scanner, que realiza o papel de tokenizer através do Flex, e o arquivo `parser.y` é o Parser, que realiza a análise sintática através do Bison. O arquivo `main.c` é o ponto de entrada do programa, onde o Scanner e o Parser são inicializados e executados.

Para compilar foram usados os seguintes comandos:

```bash
flex scanner.l

bison -d parser.y

gcc -o projeto main.c parser.tab.c lex.yy.c

./projeto < entrada.txt
```