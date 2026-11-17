# **Relatório \- Tema 1: Matrículas duplicadas**

Projeto e Análise de Algoritmos · CIESA · Trabalho Prático: Contagem de Operações

Equipe: Andrey, Logan e Eduardo

## **1\. Cenário e formato da entrada**

A secretaria juntou as matrículas de 2026.2 de duas planilhas e suspeita que alguns alunos foram cadastrados duas vezes. O problema é: dada uma lista de n matrículas, decidir se existe alguma repetida e, se existir, devolver uma delas.

Entrada. Lista de n inteiros , gerada por matriculas(n, semente, repetidas) da base comum, com semente fixa. O parâmetro repetidas diz quantas posições recebem cópia de outra matrícula.

Operação básica contada. Comparação entre duas matrículas. Na versão esperta, as comparações do mergesort (fase de ordenação) e as da varredura são contadas separadamente e somadas no final.

## **2\. Pseudocódigo comentado**

Versão ingênua (ing)

para i de 0 até n-1:                    \# cada matrícula...  
    para j de i+1 até n-1:              \# ...contra as seguintes  
        compara v\[i\] com v\[j\]           \# \<- operação contada  
        se forem iguais: devolve v\[i\]   \# para na 1ª repetição  
devolve "não há repetida"

Versão esperta (esp)

w \= mergesort(v)                        \# fase 1: comparações da ordenação  
para i de 1 até n-1:                    \# fase 2: varredura  
    compara w\[i-1\] com w\[i\]             \# \<- operação contada  
    se forem iguais: devolve w\[i\]  
devolve "não há repetida"

A ideia: depois de ordenar, matrículas iguais ficam lado a lado, então basta olhar vizinhos. Se houvesse duas iguais afastadas, algo entre elas teria de ser ≥ a primeira e ≤ a segunda, ou seja, igual a elas, e então já haveria um par de vizinhos iguais.

## **3\. Contagem à mão**

### **3.1 Ingênua**

Para um valor de i, o laço interno roda n − i − 1 vezes. No pior caso (nenhuma repetida) nunca para antes:

T(n) \= Σ (i=0 até n-1) (n \- i \- 1\) \= (n-1) \+ (n-2) \+ ... \+ 1 \+ 0 \= n(n-1)/2

T(n) \= n²/2 − n/2, logo Θ(n²).

### **3.2 Esperta**

Ordenação (mergesort). Para n \= 2^k, a intercalação de duas metades de tamanho m gasta no máximo 2m − 1 comparações:

M(n) \= 2·M(n/2) \+ n \- 1,    M(1) \= 0

Desenrolando pela árvore de recursão: no nível k há 2^k subproblemas de tamanho n/2^k, cada um custando n/2^k − 1, então o nível inteiro custa n − 2^k. Com log₂n níveis:

M(n) \= Σ (k=0 até log2(n)-1) (n \- 2^k) \= n·log2(n) \- (n \- 1\) \= n·log2(n) \- n \+ 1

Para n que não é potência de 2, entram os pisos e tetos do log: M(n) \= n·⌈log₂n⌉ − 2^⌈log₂n⌉ \+ 1\.

Varredura. No pior caso: Σ (i=1 até n-1) 1 \= n − 1\.

Total no pior caso (n \= 2^k):

E(n) \= (n·log2(n) \- n \+ 1\) \+ (n \- 1\) \= n·log2(n)

Logo a esperta é Θ(n log n).

Por que a varredura não define a classe. A varredura é linear (n − 1\) e a ordenação é n log n. Como Θ(n) \+ Θ(n log n) \= Θ(n log n), quem manda é a ordenação. A contagem separada mostra isso: com n \= 100 000, a varredura fez 99 999 comparações e a ordenação 1 568 929, ou seja, a varredura é só 6% do total, e essa fatia diminui conforme n cresce (seção 5.3).

## **4\. Melhor e pior caso**

| Versão | Caso | Entrada que produz | Contagem |
| :---- | :---- | :---- | :---- |
| Ingênua | pior | nenhuma repetida (distintos(n)): todos os pares são testados | n(n−1)/2 → Θ(n²) |
| Ingênua | melhor | as duas primeiras iguais (v\[1\] \= v\[0\]): acha na 1ª comparação | 1 → Θ(1) |
| Esperta | pior | sem repetidas e em ordem ruim para o mergesort (função mistura) | n log₂n → Θ(n log n) |
| Esperta | melhor | já ordenada, com v\[1\] \= v\[0\] | (n/2)·log₂n \+ 1 → Θ(n log n) |

Por que cada entrada.

* Ingênua: o custo depende de onde está a primeira repetição. Se está logo no começo, para na hora; se não existe, percorre todos os pares. Por isso a classe da ingênua muda com o caso: usamos o pior (quadrática) para classificá-la.

* Esperta, pior caso: mistura monta a lista de modo que toda intercalação fique alternando esquerda e direita, que é o pior caso do mergesort (2m − 1 por intercalação). Sem repetidas, a varredura também vai até o fim.

* Esperta, melhor caso: numa lista já ordenada, cada intercalação esgota a metade esquerda antes de tocar na direita, gastando só m comparações. Em cada nível isso soma n/2, e com log₂n níveis dá (n/2)·log₂n. A varredura para na 1ª comparação por causa de v\[1\] \= v\[0\].

* Mesmo no melhor caso a esperta continua n log n, porque ela ordena tudo antes de olhar qualquer coisa e não pode parar cedo. Só a varredura para cedo.

Caso médio. Hipótese declarada: n matrículas distintas e depois uma posição recebe a cópia de outra (repetidas=1). Como o gerador sorteia i e j, às vezes i \= j e não sobra repetida nenhuma. Usamos 30 entradas (sementes 0 a 29\) e reportamos a média.

Para a ingênua dá para prever o resultado: com i e j sorteados uniformemente, a primeira repetição aparece na linha m \= min(i, j), e até lá foram gastas cerca de n·m − m²/2 comparações. Com E\[m\] \= n/3 e E\[m²\] \= n²/6, o esperado é cerca de n/3·n − n²/12 \= n²/4. Os valores medidos (c/n² entre 0,21 e 0,27) giram em torno desse 0,25, longe do 0,5 do pior caso.

## **5\. Teste do dobro**

Tabelas completas (com todas as colunas) estão em saida.txt e os dados brutos em medicoes.csv. Aqui, c \= contagem e "dobro" \= c(n) / c(n/2).

### **5.1 Ingênua**

Pior caso

| n | c | c/n² | dobro |
| :---- | :---- | :---- | :---- |
| 100 | 4 950 | 0,4950 | \- |
| 200 | 19 900 | 0,4975 | 4,02 |
| 400 | 79 800 | 0,4988 | 4,01 |
| 800 | 319 600 | 0,4994 | 4,01 |
| 1 600 | 1 279 200 | 0,4997 | 4,00 |

A razão que estabiliza é c/n² (vai para 0,5, o coeficiente de n²/2) e o dobro vai para 4\. Quadrática.

Melhor caso: c \= 1 para todo n, dobro \= 1\. Constante.

Caso médio (30 amostras):

| n | c | c/n² | dobro |
| :---- | :---- | :---- | :---- |
| 100 | 2 736,47 | 0,2736 | \- |
| 200 | 10 304,60 | 0,2576 | 3,77 |
| 400 | 33 432,17 | 0,2090 | 3,24 |
| 800 | 165 791 | 0,2590 | 4,96 |
| 1 600 | 628 826,73 | 0,2456 | 3,79 |

A razão c/n² oscila em torno de 0,25, como previsto (n²/4), e o dobro fica em torno de 4: quadrática também na média. A oscilação é esperada: com só 30 amostras e a repetição caindo em posições sorteadas, uma entrada "azarada" (cópia no fim da lista) muda bastante a média.

### **5.2 Esperta**

Pior caso, total (ordenação \+ varredura)

| n | c | c/(n·log₂n) | dobro |
| :---- | :---- | :---- | :---- |
| 100 | 672 | 1,011 | \- |
| 200 | 1 544 | 1,010 | 2,30 |
| 400 | 3 488 | 1,009 | 2,26 |
| 800 | 7 776 | 1,008 | 2,23 |
| 1 600 | 17 152 | 1,007 | 2,21 |

Série maior (também dobrando)

| n | c | c/(n·log₂n) | dobro |
| :---- | :---- | :---- | :---- |
| 12 500 | 171 116 | 1,006 | \- |
| 25 000 | 367 232 | 1,005 | 2,15 |
| 50 000 | 784 464 | 1,005 | 2,14 |
| 100 000 | 1 668 928 | 1,005 | 2,13 |

A razão que estabiliza é c/(n·log₂n), perto de 1\. O dobro desce devagar rumo a 2 e fica um pouco acima porque o log também cresce a cada dobramento (2·(1 \+ 1/log₂n)). Com a série maior a tendência fica mais clara: 2,30 → 2,21 → 2,13.

Outros casos da esperta

* Melhor caso: c/(n·log₂n) sobe devagar de 0,477 a 0,485, rumo a 0,5 (que é o (n/2)·log₂n).

* Caso médio: c/(n·log₂n) entre 0,89 e 0,93. É menor que o do pior caso porque o mergesort em entrada aleatória não gasta o máximo em toda intercalação. Continua n log n.

### **5.3 Peso de cada fase (esperta, pior caso)**

| n | ordenação | varredura | varredura / total |
| :---- | :---- | :---- | :---- |
| 100 | 573 | 99 | 14,7% |
| 1 600 | 15 553 | 1 599 | 9,3% |
| 100 000 | 1 568 929 | 99 999 | 6,0% |

Na varredura, c/n vale 1,000 em todas as linhas (linear). Na ordenação, c/n sobe de 5,7 (n \= 100\) até 15,7 (n \= 100 000): é o log₂n aparecendo. Por isso a fatia da varredura encolhe e a ordenação define a classe.

## **6\. Confronto: medido × fórmula**

| n | o que | medido | fórmula |
| :---- | :---- | :---- | :---- |
| 100 | ingênua pior | 4 950 | n(n−1)/2 \= 4 950 |
| 400 | ingênua pior | 79 800 | 79 800 |
| 1 600 | ingênua pior | 1 279 200 | 1 279 200 |
| 128 | esperta pior (ordenação) | 769 | n·log₂n − n \+ 1 \= 769 |
| 256 | esperta pior (ordenação) | 1 793 | 1 793 |
| 1 024 | esperta pior (ordenação) | 9 217 | 9 217 |
| 128 | esperta pior (varredura) | 127 | n − 1 \= 127 |
| 1 024 | esperta pior (varredura) | 1 023 | 1 023 |
| 128 | esperta melhor (ordenação) | 448 | (n/2)·log₂n \= 448 |
| 1 024 | esperta melhor (ordenação) | 5 120 | 5 120 |
| 100 | esperta pior (ordenação) | 573 | n⌈log₂n⌉ − 2^⌈log₂n⌉ \+ 1 \= 573 |
| 1 600 | esperta pior (ordenação) | 15 553 | 15 553 |

Todos os valores bateram exatamente. Para n \= 100 e n \= 1 600 (que não são potência de 2), a fórmula simples n·log₂n − n \+ 1 não serve: só bate usando o teto do log, como na seção 3.2. É também por isso que c/(n·log₂n) da esperta fica em 1,00x e não em 1 exato: sobra um termo de ordem n que a razão não cancela.

## **7\. Conclusão crítica**

* Classes. A ingênua é Θ(n²) no pior caso e a esperta é Θ(n log n). Em n \= 1 600, a ingênua fez 1 279 200 comparações contra 17 152 da esperta, cerca de 75 vezes menos. Em n \= 100 000, a ingênua faria quase 5 bilhões (n(n−1)/2 \= 4 999 950 000\) e a esperta fez 1,67 milhão.

* Como decidir a classe. Olhando a razão que estabiliza quando n dobra várias vezes, e não um n só. A coluna "dobro" ajuda: 4 indica quadrática e perto de 2 (um pouco acima) indica n log n.

* Erro clássico evitado. Contar só a varredura (linear) e esquecer o mergesort daria a classe errada, Θ(n). A contagem separada mostra que a ordenação responde por 90% a 94% do custo e define a classe.

* Quando a esperta compensa. No pior caso, a partir de n \= 8 (ingênua 28 comparações contra 24 da esperta; em n \= 4 a ingênua ainda ganha, 6 contra 8). Mas no melhor caso a ingênua faz 1 comparação e a esperta nunca faz menos que (n/2)·log₂n. A esperta tem, porém, a garantia de nunca ser quadrática, o que importa quando não se sabe onde está a repetição, como no cenário da secretaria.

* Limitações.

  * O caso médio depende da hipótese escolhida (uma única repetição). Com outra hipótese, o número muda, e no caso médio da ingênua há ruído com 30 amostras.

  * Contamos só comparações. O mergesort também copia elementos e usa memória extra de ordem n, custos que a ingênua não tem e que não aparecem no contador.

  * Não cronometramos. Para tempo real, esses custos pesariam a favor da ingênua em listas pequenas.

## **8\. Referências**

* Enunciado do Trabalho Prático: Contagem de Operações: Lineares, Quadráticos e Logarítmicos (PAA, CIESA, 4º e 6º períodos).

* trabalho\_base.py: base comum (mergesort instrumentado, geradores, teste\_do\_dobro, salvar\_csv).

* Anotações das aulas 03 (busca binária) e 04 (mergesort).