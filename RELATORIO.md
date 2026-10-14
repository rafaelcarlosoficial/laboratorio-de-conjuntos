# Relatorio — Laboratorio de Conjuntos

## Onde a teoria dos conjuntos apareceu no codigo?

A teoria dos conjuntos foi usada diretamente na primeira parte do programa. Os conjuntos `A`, `B` e o universo `U` armazenam elementos sem repeticao. A partir deles, funcoes implementadas com lacos e condicionais calculam uniao, intersecao, diferencas, diferenca simetrica, pertinencia, inclusao e complemento. A comparacao com os operadores nativos do Python serve como validacao independente dos algoritmos manuais. A cardinalidade e obtida contando os elementos distintos.

Na classificacao numerica, os conjuntos `N`, `Z`, `Q`, `I` e `R` organizam os numeros por propriedades. Por exemplo, um inteiro negativo pertence a `Z`, `Q` e `R`, mas nao a `N`; uma dizima periodica pertence a `Q` e `R`; e uma raiz quadrada nao exata pertence a `I` e `R`. O projeto adota `0 ∈ N`, conforme os exemplos do enunciado. A Parte 3 aplica intersecao e uniao ao conjunto de interesses para calcular o indice de Jaccard.

## Qual operacao foi mais dificil de implementar e por que?

A diferenca simetrica foi a operacao mais dificil. Ela precisa reunir os elementos que aparecem em apenas um dos conjuntos, mas excluir os elementos compartilhados. Para implementar sem o operador pronto, primeiro calculamos `A - B` e `B - A` com lacos; em seguida, reunimos os resultados. O caso de conjuntos iguais foi importante para verificar que o resultado deve ser vazio, enquanto conjuntos disjuntos devem produzir a uniao completa.

Na parte numerica, as dizimas periodicas tambem exigiram cuidado: a parte nao periodica e o periodo podem ter comprimentos diferentes. A formula calcula a fracao geratriz com potencias de dez e `Fraction` simplifica o resultado sem aproximacao decimal. Os testes automatizados conferem os exemplos, inclusive `1,2(5) = 113/90` e `0,(9) = 1`.

## Validacao

Os testes com `unittest` cobrem os casos de borda exigidos, os calculos do classificador e os exemplos do mini-projeto. A demonstracao `python main.py --demo` tambem exibe comparacao manual/nativa para cinco pares de conjuntos e resultados conferiveis a mao para as demais partes.
