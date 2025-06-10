# Projeto Logcomp

Para a atividade supervisionada da matéria, o aluno idealizou uma linguagem voltada para o controle e gerenciamento do fluxo de estoque de um galpão logístico. A ideia seria criar uma linguagem capaz de interpretar as atividades realizadas em ambientes logísticos como recebimento de produtos, estocagem e venda dos produtos, por exemplo.

A operação logística imaginada pode ser quebrada em três etapas macros:

- Entrada: Etapa inicial, onde os produtos são recebidos e registrados no sistema, incluindo informações como nome, SKU (identificador único), quantidade e data de validade.

- Recebimento: Etapa inicial, entrada de produtos na cadeia logística, atua em cima dos produtos que deram entrada no sistema, essa etapa acompanha um quality check, onde é verificado se os produtos estão em conformidade com o esperado. Assim, a quantidade recebida não é necessariamente a mesma que a quantidade registrada na entrada.
  
- Alocação: Feito o recebimento, é reconhecida a entrada dos produtos na cadeia, mas ainda é necessário atribuir uma posição.

- Movimentação: Após a alocação, é possível mover os produtos para outras posições, caso necessário.
  
- Venda/Descarte : Feita a alocação, é necessário remover o item do estoque em caso de venda, ou descartá-lo.
  
Observação: Para a operação imaginada, cada produto dispõe de:

**Nome, SKU ( identificador único), quantidade e data de validade.**

Assim, a linguagem poderia operar a partir de um estado inicial recebido, compilar e retornar o estado da logística após as operações realizadas.

---

## Entregáveis

1. **EBNF pensada:**

BLOCO = "{", "\n", { STATEMENT }, "}";

STATEMENT = ( λ | ENTRADA | RECEBER | ALOCAR | MOVER | VENDER | DESCARTAR | EXIBIR | VARDEC | VARASSIGN | ENQUANTO | SE ), "\n" ;

ENTRADA = "(", NOME, ",", SKU, ")", "=", "(", EXPRESSION, ",", DATA_VALIDADE, ")";

RECEBER = "receber", "(", SKU, ",", EXPRESSION, ")";

ALOCAR = "alocar", "(", SKU, ",", EXPRESSION, ",", POSICAO, ")";

MOVER = "mover", "(", SKU, ",", EXPRESSION, ",", POSICAO, ",", POSICAO, ")";

VENDER = "vender", "(", SKU, ",", EXPRESSION, [",", POSICAO], ")";

DESCARTAR = "descartar", "(", SKU, ",", EXPRESSION, [",", POSICAO], ")";

EXIBIR = "exibir", "(", SKU | POSICAO, ")";

VARDEC = ("bool_var" | "int_var"), NOME, [ "=", BEXPRESSION ];

VARASSIGN = NOME, "=", BEXPRESSION ;

ENQUANTO = "enquanto", BEXPRESSION, BLOCO ;

SE = "se", BEXPRESSION, BLOCO, [ "senao", BLOCO ];

BEXPRESSION = BTERM, { "||", BTERM } ;

BTERM = REXPRE, { "&&", REXPRE } ;

REXPRE = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;

EXPRESSION = TERM, { ("+" | "-"), TERM } ;

TERM = FACTOR, { ("*" | "/"), FACTOR } ;

FACTOR = (("+" | "-" | "!"), FACTOR)
       | NUMBER
       | "(", BEXPRESSION, ")"
       | CONFERIR
       | VALIDADE
       | VAR
       | BOOL ;

VALIDADE = "validade", "(", SKU, ",", POSICAO, ",", NUMBER, ")";

CONFERIR = "estoque", "(", SKU, [",", POSICAO], ")";

VAR = NOME;

DATA_VALIDADE = NUMBER, "/", NUMBER, "/", NUMBER ;

BOOL = "true" | "false" ;

POSICAO = NOME ;

NOME = LETTER, { LETTER | DIGIT | "_" } ;

NUMBER = DIGIT, { DIGIT } ;

SKU = NUMBER ;

LETTER = ( a | ... | z | A | ... | Z ) ;

DIGIT = ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ) ;

---

2. **Flex e Bison:**


Os arquivos do Flex e Bison foram criados para serem utilizados em conjunto, o arquivo `scanner.l` é o Scanner, que realiza o papel de tokenizer através do Flex, e o arquivo `parser.y` é o Parser, que realiza a análise sintática através do Bison. O arquivo `main.c` é o ponto de entrada do programa, onde o Scanner e o Parser são inicializados e executados.

Para compilar foram usados os seguintes comandos:

```bash
flex scanner.l

bison -d parser.y

gcc -o projeto main.c parser.tab.c lex.yy.c

./projeto < entrada.txt
```

----

3. **VM capaz de interpretar um programa da linguagem:**

Para essa VM foi feita uma adaptação do compilador usado na matéria, o código foi disponibilizado no arquivo `main.py`. A VM é capaz de interpretar um programa escrito na linguagem definida pela EBNF e executá-lo, manipulando o estado do estoque conforme as operações definidas.

Assim, para executar a VM, basta rodar o seguinte comando:

```bash
python main.py entrada.txt
```

No caso acima, o compilador irá partir de um estoque inicial vazio e irá processar as operações definidas no arquivo `entrada.txt`, retornando o estado final do no arquivo `estoque.txt`.

De forma semelhante, é possível interpretar um programa a partir de um estado inicial de estoque já definido. Assim, é possível utilizar uma saída anterior gerada na execução da VM como arquivo de entrada para a próxima execução, permitindo a continuidade do fluxo logístico. Um exemplo de uso seria:

```bash
python main.py entrada.txt estoque.txt
```

Onde o `estoque.txt` contém o estado inicial do estoque, e o `entrada.txt` contém as operações a serem realizadas sobre esse estoque.

----

4. Criar um exemplo de testes que demonstre as características da sua Linguagem.

Para demonstrar as características da linguagem, foram criados programas de teste que realizam operações de entrada, recebimento, alocação, movimentação, venda e descarte de produtos. Esses testes foram desenvolvidos para mostrar como a linguagem pode ser utilizada para gerenciar o fluxo de estoque de um galpão logístico.

Os testes feitos estão disponíveis no diretório `testes`. Eles incluem exemplos de como adicionar produtos ao estoque, receber produtos, alocar produtos em posições específicas, mover produtos entre posições, vender produtos e descartar produtos que não são mais necessários.

- testes/teste1.txt
```
{
    (Arroz_Integral, 12345) = (100, 09/06/2025)
    (leite, 67890) = (200, 15/11/2025)
    (Sal, 54321) = (50, 20/10/2025)

    receber(12345, 100)
    receber(67890, 200)
    receber(54321, 30)

    alocar(67890, 200, B2)
    alocar(12345, 100, A1)

    exibir(A1)

    bool_var teste2 = true

    int_var quantidade_quase_vencida = validade(12345, A1, 10)

    se (quantidade_quase_vencida > 10) {
        descartar(12345, 10, A1)
    } senao {
        vender(12345, 5, A1)
    }

    exibir(12345)

    int_var teste = estoque(12345)

    enquanto (teste > 0) {
        teste = teste - 10
        mover(12345, 5, A1, C1)
    }

    exibir(12345)
}
```

Durante sua execução, o programa irá printar para o usuário, por conta dos tokens `exibir`:
```
Produto: Arroz_Integral, SKU: 12345, Quantidade: 100, Validade: 2025-06-09
Posição: A1, Produto: Arroz_Integral, SKU: 12345, Quantidade: 90, Validade: 2025-06-09
Posição: A1, Produto: Arroz_Integral, SKU: 12345, Quantidade: 45, Validade: 2025-06-09 Posição: C1, Produto: Arroz_Integral, SKU: 12345, Quantidade: 45, Validade: 2025-06-09
```

Perceba, o primeiro print é referente ao `exibir(A1)`, que mostra o produto alocado na posição A1, e os outros prints são referentes ao `exibir(12345)`, que mostra o estado do produto com SKU 12345 após as operações de venda e movimentação. No segundo print, o produto estava todo alocado na posição A1, após o descarte de 10 unidades, o estoque foi reduzido para 90 unidades, em seguida, parte do estoque foi movido para a posição C1, resultando em 45 unidades na posição A1 e 45 unidades na posição C1.

Após a execução do programa, o estado final do estoque será salvo no arquivo `estoque.txt`:
```
A1: Produto(nome=Arroz_Integral, sku=12345, quantidade=45, validade=2025-06-09)
B2: Produto(nome=leite, sku=67890, quantidade=200, validade=2025-11-15)
C1: Produto(nome=Arroz_Integral, sku=12345, quantidade=45, validade=2025-06-09)
recebimento: Produto(nome=Sal, sku=54321, quantidade=30, validade=2025-10-20)
```

- testes/teste2.txt

```
{
    alocar(54321, 30 , E2)

    enquanto(estoque(67890, B2) > 0) {
        vender(67890, 10, B2)
    }

    exibir(67890)

    mover(12345, 45, A1, C1)
}
```

Perceba que o segundo teste, tenta alocar o produto com SKU 54321, porém, em nenhum momento foi feito o recebimento desse produto, logo, o programa irá falhar caso seja executado sem nenhum estoque inicial definido.

O usuário irá receber a seguinte mensagem de erro:

```
raise Exception(f"Não é possível alocar o produto {key}, nada foi recebido no estoque")
Exception: Não é possível alocar o produto 54321, nada foi recebido no estoque
```

Por outro lado, caso seja passado o estoque obtido do primeiro teste como entrada, o programa irá executar normalmente, alocando o produto na posição E2 e vendendo as unidades do produto com SKU 67890 alocado na posição B2, até que o estoque desse produto se esgote.

Assim, o comando para executar o segundo teste com o estoque do primeiro teste seria:

```bash
python3 main.py testes/teste2.txt estoque.txt 
```

O programa irá printar o seguinte resultado:

```
Nenhum produto encontrado com o SKU 67890
```

Isso ocorre, pois todos os produtos com SKU 67890 foram vendidos através do loop criado no teste 2, e ao tentar exibir o produto com SKU 67890, o programa não encontra nenhum produto com esse SKU no estoque. Isso não levanta nenhum erro, apenas informa para o usuário que não há produtos com o SKU especificado.

Saída do estoque após a execução do segundo teste:

```
C1: Produto(nome=Arroz_Integral, sku=12345, quantidade=90, validade=2025-06-09)
E2: Produto(nome=Sal, sku=54321, quantidade=30, validade=2025-10-20)
```

----

5. Montar uma apresentação de slides sobre a linguagem criada.

A apresentação de slides foi criada e está disponível no arquivo `apresentacao.pptx`. Ela contém uma visão geral da linguagem, esse slide mostra como a linguagem foi projetada, suas principais características, curiosidades e um exemplo de uso.

----