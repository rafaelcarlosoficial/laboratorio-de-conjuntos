# Laboratorio de Conjuntos

Atividade pratica de Teoria dos Conjuntos e Conjuntos Numericos para o curso de Desenvolvimento de Software Multiplataforma — Fatec Osasco.

## Requisitos

- Python 3.10 ou superior
- Nenhuma biblioteca externa: o projeto usa apenas a biblioteca padrao.

## Como executar

No terminal, dentro da pasta do projeto:

```powershell
python main.py
```

O menu permite abrir cada parte do trabalho. Para reproduzir de uma vez os exemplos documentados abaixo:

```powershell
python main.py --demo
```

Para rodar os testes:

```powershell
python -m unittest -v
```

## Decisoes do projeto

- Na Parte 1, as operacoes solicitadas sao implementadas com lacos e condicionais. A opcao 9 e a demonstracao comparam os resultados com os operadores nativos de `set`.
- A entrada de conjuntos aceita itens separados por virgula; numeros inteiros sao convertidos para `int`, os demais itens sao tratados como texto e repeticoes sao removidas.
- O conjunto dos naturais **inclui o zero**: `N = {0, 1, 2, ...}`, conforme os exemplos fornecidos no enunciado.
- Fracoes e decimais sao calculados exatamente com `fractions.Fraction` e `decimal.Decimal`, sem erros de arredondamento binario.
- Dizímas periodicas aceitam virgula ou ponto decimal, por exemplo `0,(3)`, `2,(7)` e `1,2(5)`. A fracao geratriz e exibida simplificada; por isso `0,(9)` resulta em `1`, equivalente a `9/9`.
- Raizes quadradas aceitam `sqrt(2)` ou `√2`. Raizes de quadrados perfeitos sao racionais; as demais sao classificadas em `I` e `R`.
- A Parte 3 escolhida e o sistema de recomendacao pelo indice de Jaccard. Para dois conjuntos vazios, o programa convenciona o indice como `1.0`, pois ambos possuem os mesmos interesses.

## Parte 1 — Teoria dos Conjuntos

As operacoes disponiveis sao uniao, intersecao, diferencas direcionais, diferenca simetrica, pertinencia, inclusao propria/impropria, cardinalidade e complemento relativo a `U`.

### Execucoes demonstrativas

Comando: `python main.py --demo`

```text
=== Parte 1: implementacao manual x Python ===

Caso geral (com repetidos removidos):
A = {1, 2, 3, 4}; B = {3, 4, 5, 6}
uniao: manual = {1, 2, 3, 4, 5, 6}; nativa = {1, 2, 3, 4, 5, 6}; confere = sim
intersecao: manual = {3, 4}; nativa = {3, 4}; confere = sim
A - B: manual = {1, 2}; nativa = {1, 2}; confere = sim
B - A: manual = {5, 6}; nativa = {5, 6}; confere = sim
diferenca simetrica: manual = {1, 2, 5, 6}; nativa = {1, 2, 5, 6}; confere = sim
A ⊆ B: manual = False; nativa = False
A ⊂ B: manual = False; nativa = False

Conjunto vazio:
A = ∅; B = {1, 2}
uniao: manual = {1, 2}; nativa = {1, 2}; confere = sim
intersecao: manual = ∅; nativa = ∅; confere = sim
A - B: manual = ∅; nativa = ∅; confere = sim
B - A: manual = {1, 2}; nativa = {1, 2}; confere = sim
diferenca simetrica: manual = {1, 2}; nativa = {1, 2}; confere = sim
A ⊆ B: manual = True; nativa = True
A ⊂ B: manual = True; nativa = True

Conjuntos disjuntos:
A = {1, 2}; B = {3, 4}
uniao: manual = {1, 2, 3, 4}; nativa = {1, 2, 3, 4}; confere = sim
intersecao: manual = ∅; nativa = ∅; confere = sim
A - B: manual = {1, 2}; nativa = {1, 2}; confere = sim
B - A: manual = {3, 4}; nativa = {3, 4}; confere = sim
diferenca simetrica: manual = {1, 2, 3, 4}; nativa = {1, 2, 3, 4}; confere = sim
A ⊆ B: manual = False; nativa = False
A ⊂ B: manual = False; nativa = False

Conjuntos iguais:
A = {1, 2, 3}; B = {1, 2, 3}
uniao: manual = {1, 2, 3}; nativa = {1, 2, 3}; confere = sim
intersecao: manual = {1, 2, 3}; nativa = {1, 2, 3}; confere = sim
A - B: manual = ∅; nativa = ∅; confere = sim
B - A: manual = ∅; nativa = ∅; confere = sim
diferenca simetrica: manual = ∅; nativa = ∅; confere = sim
A ⊆ B: manual = True; nativa = True
A ⊂ B: manual = False; nativa = False

Exemplo criado pela equipe:
A = {2, 4, 6}; B = {4, 6, 8, 10}
uniao: manual = {2, 4, 6, 8, 10}; nativa = {2, 4, 6, 8, 10}; confere = sim
intersecao: manual = {4, 6}; nativa = {4, 6}; confere = sim
A - B: manual = {2}; nativa = {2}; confere = sim
B - A: manual = {8, 10}; nativa = {8, 10}; confere = sim
diferenca simetrica: manual = {2, 8, 10}; nativa = {2, 8, 10}; confere = sim
A ⊆ B: manual = False; nativa = False
A ⊂ B: manual = False; nativa = False
Complemento de A em U = {5, 6, 7, 8, 9, 10}
|A| = 4; 3 pertence a A? True; 5 pertence a A? False
```

O programa remove as entradas repetidas antes de realizar as operacoes. As implementacoes manuais e nativas coincidem nos cinco casos, inclusive nos casos de borda. No exemplo criado pela equipe, `A = {2, 4, 6}` e `B = {4, 6, 8, 10}`: a intersecao e `{4, 6}`, a uniao e `{2, 4, 6, 8, 10}` e a diferenca simetrica e `{2, 8, 10}`.

## Parte 2 — Conjuntos Numericos

O classificador apresenta representacao exata, conjuntos a que o numero pertence e justificativa. `N` inclui zero; `Z` sao os inteiros; `Q` sao os racionais; `I` sao os irracionais; e `R` sao os reais.

### Execucao demonstrativa

O demo classifica doze entradas (mais que as oito exigidas):

```text
=== Parte 2: classificacoes ===
-3       -> -3           Pertence a: Z, Q, R
           Justificativa: Representacao finita/exata; todo decimal exato e racional.
0        -> 0            Pertence a: N, Z, Q, R
           Justificativa: Representacao finita/exata; todo decimal exato e racional.
7        -> 7            Pertence a: N, Z, Q, R
           Justificativa: Representacao finita/exata; todo decimal exato e racional.
3/4      -> 3/4          Pertence a: Q, R
           Justificativa: Fracao exata, simplificada para 3/4.
-5/2     -> -5/2         Pertence a: Q, R
           Justificativa: Fracao exata, simplificada para -5/2.
1,25     -> 5/4          Pertence a: Q, R
           Justificativa: Representacao finita/exata; todo decimal exato e racional.
0,(3)    -> 1/3          Pertence a: Q, R
           Fracao geratriz: 1/3
           Justificativa: Dizima periodica; a fracao geratriz foi calculada e simplificada.
2,(7)    -> 25/9         Pertence a: Q, R
           Fracao geratriz: 25/9
           Justificativa: Dizima periodica; a fracao geratriz foi calculada e simplificada.
1,2(5)   -> 113/90       Pertence a: Q, R
           Fracao geratriz: 113/90
           Justificativa: Dizima periodica; a fracao geratriz foi calculada e simplificada.
0,(9)    -> 1            Pertence a: N, Z, Q, R
           Fracao geratriz: 1
           Justificativa: Dizima periodica; a fracao geratriz foi calculada e simplificada.
sqrt(9)  -> 3            Pertence a: N, Z, Q, R
           Justificativa: Raiz exata: 3 x 3 = 9.
sqrt(2)  -> irracional   Pertence a: I, R
           Justificativa: 2 nao e quadrado perfeito; sua raiz e irracional.
Primos de N ate 30: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
Divisores de 36: [1, 2, 3, 4, 6, 9, 12, 18, 36]
```

No modo interativo, as opcoes extras geram primos pelo crivo de Eratostenes e listam divisores positivos.

## Parte 3 — Mini-projeto: recomendacao por interesses

O indice de Jaccard e `|A ∩ B| / |A ∪ B|`. Os interesses iniciais sao os do enunciado. A tabela mostra tres cenarios e permite conferir as cardinalidades e o calculo.

| Par | Intersecao | Uniao | Calculo manual | Saida |
|---|---|---|---:|---:|
| Ana e Bia | `{jazz, cinema}` (2) | `{rock, jazz, cinema, games, series, viagens}` (6) | 2/6 = 0,33 | 0.33 |
| Ana e Caio | `{games, cinema}` (2) | `{rock, jazz, cinema, games, tecnologia}` (5) | 2/5 = 0,40 | 0.40 |
| Bia e Caio | `{cinema}` (1) | `{jazz, cinema, series, viagens, games, tecnologia}` (6) | 1/6 = 0,17 | 0.17 |

```text
=== Parte 3: recomendacao por Jaccard ===
Ana e Bia: intersecao {cinema, jazz} (2); uniao {cinema, games, jazz, rock, series, viagens} (6); Jaccard = 2/6 = 0.33
Ana e Caio: intersecao {cinema, games} (2); uniao {cinema, games, jazz, rock, tecnologia} (5); Jaccard = 2/5 = 0.40
Bia e Caio: intersecao {cinema} (1); uniao {cinema, games, jazz, series, tecnologia, viagens} (6); Jaccard = 1/6 = 0.17
Recomendacao para Ana: Caio (maior indice: 0.40).
Exemplo criado pela equipe (Lia e Rui): intersecao {musica} (1); uniao {fotografia, musica, trilhas, xadrez} (4); Jaccard = 1/4 = 0.25
```

Conclusao calculada a mao: entre os perfis comparados, Caio tem maior afinidade com Ana (`0,40`), portanto e a recomendacao mais forte.
No exemplo criado pela equipe, Lia possui `{xadrez, musica, trilhas}` e Rui possui `{musica, fotografia}`. A intersecao tem um elemento e a uniao quatro; portanto, o resultado calculado a mao e `1/4 = 0,25`, igual ao programa.

## Testes

Os testes automatizados cobrem conjunto vazio, conjuntos iguais, conjuntos disjuntos, subconjunto proprio, entradas repetidas, numeros inteiros e racionais, dizimas, raizes, erro de denominador zero, primos, divisores e os tres indices de Jaccard.
