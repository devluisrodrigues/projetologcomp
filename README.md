# Projeto Logcomp

Para a atividade supervisionada da matéria, o aluno idealizou uma linguagem voltada para o controle e gerenciamento do fluxo de estoque de um galpão logístico. A ideia seria criar uma linguagem capaz de interpretar as atividades realizadas em ambientes logísticos como recebimento de produtos, estocagem e venda dos produtos, por exemplo.

A operação logística imaginada pode ser quebrada em três etapas macros:

- **Entrada**: Etapa inicial, onde os produtos são recebidos e registrados no sistema, incluindo informações como nome, SKU (identificador único), quantidade e data de validade.

- **Recebimento**: Etapa inicial, entrada de produtos na cadeia logística, atua em cima dos produtos que deram entrada no sistema, essa etapa acompanha um quality check, onde é verificado se os produtos estão em conformidade com o esperado. Assim, a quantidade recebida não é necessariamente a mesma que a quantidade registrada na entrada.
  
- **Alocação**: Feito o recebimento, é reconhecida a entrada dos produtos na cadeia, mas ainda é necessário atribuir uma posição.

- **Movimentação**: Após a alocação, é possível mover os produtos para outras posições, caso necessário.
  
- **Venda/Descarte** : Feita a alocação, é necessário remover o item do estoque em caso de venda, ou descartá-lo.
  
Observação: Para a operação imaginada, cada produto dispõe de:

**Nome, SKU ( identificador único), quantidade e data de validade.**

---

## Antes de continuar:

Para o melhor entendimento do projeto, é recomendado a leitura do conceito 5, uma apresentação de Power Point disponibilizada na raíz do projeto sob o nome de `Linguagem de controle de estoque.pptx`, que contém uma visão geral da linguagem, suas principais características, curiosidades e um exemplo de uso.

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

Acesse o diretório `flex_bison` para encontrar os arquivos `scanner.l` e `parser.y`.

Os arquivos do Flex e Bison foram criados para serem utilizados em conjunto, o arquivo `scanner.l` é o Scanner, que realiza o papel de tokenizer através do Flex, e o arquivo `parser.y` é o Parser, que realiza a análise sintática através do Bison. O arquivo `main.c` é o ponto de entrada do programa, onde o Scanner e o Parser são inicializados e executados.

Para compilar foram usados os seguintes comandos:

```bash
flex scanner.l

bison -d parser.y

gcc -o projeto main.c parser.tab.c lex.yy.c
```
Após a compilação, o executável `projeto` será gerado. Para executar o programa, basta rodar o seguinte comando:

```bash
./projeto < entrada.txt
```

----

3. **VM capaz de interpretar um programa da linguagem:**

Para essa VM foi feita uma adaptação do compilador usado na matéria, o código foi disponibilizado no arquivo `main.py`. A VM é capaz de interpretar um programa escrito na linguagem definida pela EBNF e executá-lo, manipulando o estado do estoque conforme as operações definidas.

Para essa adaptação foi necessário alterar todo o funcionamneto da symbol table, que agora armazena os produtos e suas respectivas posições no estoque, além de armazenar as variáveis definidas pelo usuário. A VM também implementa as operações de entrada, recebimento, alocação, movimentação, venda e descarte de produtos.

Assim, para executar a VM, basta rodar o seguinte comando:

```bash
python main.py entrada.txt
```

No caso acima, o compilador irá partir de um **estoque inicial vazio** e irá processar as operações definidas no arquivo `entrada.txt`, retornando o estado final do no arquivo `estoque.txt`.

De forma semelhante, é possível interpretar um programa a partir de um **estado inicial de estoque já definido**. Assim, é possível utilizar uma saída anterior gerada na execução da VM como arquivo de entrada para a próxima execução, permitindo a continuidade do fluxo logístico. Um exemplo de uso seria:

```bash
python main.py entrada.txt estoque.txt
```

Onde o `estoque.txt` contém o estado inicial do estoque, e o `entrada.txt` contém as operações a serem realizadas sobre esse estoque.

**Observação:** Foi adaptado o Parser e o Tokenizer do compilador da matéria para que a linguagem criado possa ser interpretada pela VM. Assim, o Flex e o Bison desenvolvidos para a linguagem acabaram não sendo utilizados, mas estão disponíveis no diretório `flex_bison` caso seja necessário.

**Observação 2:** Os produtos que não foram recebidos no estoque não serão passados para o estoque final, ou seja, se determinado produto deu entrada, mas não foi recebido até o fim do programa, ele não será considerado no estoque final. Isso é importante para garantir que apenas os produtos que passaram pelo processo de recebimento sejam considerados no estoque.

----

4. **Criar um exemplo de testes que demonstre as características da sua Linguagem**

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

Execute com
```bash
python3 main.py testes/teste1.txt
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

Ao executar o comando:
```bash
python3 main.py testes/teste2.txt
```

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

O programa irá executar e printar o seguinte resultado:

```
Nenhum produto encontrado com o SKU 67890
Posição: C1, Produto: Arroz_Integral, SKU: 12345, Quantidade: 90, Validade: 2025-06-09
```

O primeiro print ocorre, pois todos os produtos com SKU 67890 foram vendidos através do loop criado no teste 2, e ao tentar exibir o produto com SKU 67890, o programa não encontra nenhum produto com esse SKU no estoque. Isso não levanta nenhum erro, apenas informa para o usuário que não há produtos com o SKU especificado.

Saída do estoque após a execução do segundo teste:

```
C1: Produto(nome=Arroz_Integral, sku=12345, quantidade=90, validade=2025-06-09)
E2: Produto(nome=Sal, sku=54321, quantidade=30, validade=2025-10-20)
```

- teste/teste3.txt

```
{
    (Arroz_Integral, 12345) = (100, 09/06/2025)
    (Arroz_Integral, 12345) = (100, 28/06/2025)

    receber(12345, 100)
    alocar(12345, 100, A1)

    int_var quantidade_quase_vencida = -validade(12345, A1, 10)

    se (quantidade_quase_vencida > 0) {
        descartar(12345, 10, A1)
    } senao {
        vender(12345, 15, A1)
    }

    int_var total_arroz = estoque(12345, A1)

    se (total_arroz > 60) {
        int_var quantidade_para_mover = total_arroz - 60
        mover(12345, quantidade_para_mover, A1, A10)
    }

    exibir(12345)
}
```

Execute com o comando:
```bash
python3 main.py testes/teste3.txt
```

Esse teste exemplifica o recebimento de um produto com o mesmo SKU, mas com uma data de validade diferente. O programa irá receber duas entradas do produto "Arroz Integral" com o SKU 12345, uma com validade para 09/06/2025 e outra para 28/06/2025. Como foi feito o recebimento parcial, apenas a quantidade do produto com a data de validade mais recente será considerada no estoque, as demais serão devolvidas.

Caso quisesse receber o produto com a data de validade mais antiga, seria necessário realizar duas operações de recebimento entre as entradas. Assim, o primeiro recebimento seria feito com a data de validade mais antiga, e o segundo recebimento seria feito com a data de validade mais recente, garantindo que o estoque seja atualizado corretamente.

Em seguida, foi colocado um exemplo de controle de quantidade de produtos nas posições de estoque, caso determinada posição tenha mais de 60 unidades do produto, o programa irá mover a quantidade excedente para a posição A10.

O print do programa após a execução do teste será:

```
Posição: A1, Produto: Arroz_Integral, SKU: 12345, Quantidade: 60, Validade: 2025-06-09 Posição: A10, Produto: Arroz_Integral, SKU: 12345, Quantidade: 25, Validade: 2025-06-09
```

E a saída do estoque após a execução do teste será:

```
A1: Produto(nome=Arroz_Integral, sku=12345, quantidade=60, validade=2025-06-09)
A10: Produto(nome=Arroz_Integral, sku=12345, quantidade=25, validade=2025-06-09)
```

- testes/teste4.txt

```
{
    (Lasanha, 12345) = (100, 28/06/2025)

    receber(12345, 100)
    alocar(12345, 100, A1)

    mover(12345, 150, A1, C1)
}
```

Resulta em um erro, pois o programa tenta mover uma quantidade maior do que a disponível no estoque. O comando para executar esse teste é:

```bash
python3 main.py testes/teste4.txt
```

O programa irá levantar a seguinte exceção:

```
Exception: Não foi possível mover 150 unidades do SKU 12345 da posição A1 para a posição C1, quantidade insuficiente
```

O mesmo iria ocorrer caso fosse tentado vender ou descartar uma quantidade maior do que a disponível no estoque, garantindo que o programa não permita operações inválidas.

- testes/teste5.txt

```
{
    (Lasanha, 80333) = (100, 28/06/2025)

    receber(80333, 100)
    alocar(80333, 100, A1)
    mover(80333, 20, A1, B2)

    vender(80333, 10)
}
```

O teste acima mostra o processo de venda sem declaração de posição, nesse caso, o produto vendido será retirado conforme a ordem que as posições foram inseridas no estoque. Ou seja, como o produto com SKU 80333 foi alocado na posição A1 e depois movido para a posição B2, ao vender 10 unidades, o programa irá retirar as unidades da posição A1 primeiro, e se não houver unidades suficientes nessa posição, irá retirar da posição B2.

O comando para executar esse teste é:

```bash
python3 main.py testes/teste5.txt
```

O output do estoque após a execução do teste será:

```
A1: Produto(nome=Lasanha, sku=80333, quantidade=70, validade=2025-06-28)
B2: Produto(nome=Lasanha, sku=80333, quantidade=10, validade=2025-06-28)
```


----

5. **Montar uma apresentação de slides sobre a linguagem criada.**

A apresentação de slides foi criada e está disponível no arquivo `Linguagem de controle de estoque.pptx`. Ela contém uma visão geral da linguagem, esse slide mostra como a linguagem foi projetada, suas principais características, curiosidades e um exemplo de uso.

----