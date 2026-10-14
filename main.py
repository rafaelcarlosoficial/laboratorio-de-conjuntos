from __future__ import annotations

import math
import re
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from typing import TypeAlias


Elemento: TypeAlias = int | str


def ordenar_conjunto(conjunto: set[Elemento]) -> str:
    if not conjunto:
        return "∅"
    elementos = sorted(
        conjunto,
        key=lambda item: (0, item) if isinstance(item, int) else (1, str(item)),
    )
    return "{" + ", ".join(str(item) for item in elementos) + "}"


def ler_conjunto(texto: str) -> set[Elemento]:
    resultado: set[Elemento] = set()
    for parte in texto.split(","):
        item = parte.strip()
        if not item:
            continue
        try:
            resultado.add(int(item))
        except ValueError:
            resultado.add(item)
    return resultado


def uniao_manual(a: set[Elemento], b: set[Elemento]) -> set[Elemento]:
    resultado = set(a)
    for elemento in b:
        if elemento not in resultado:
            resultado.add(elemento)
    return resultado


def intersecao_manual(a: set[Elemento], b: set[Elemento]) -> set[Elemento]:
    resultado: set[Elemento] = set()
    for elemento in a:
        if elemento in b:
            resultado.add(elemento)
    return resultado


def diferenca_manual(a: set[Elemento], b: set[Elemento]) -> set[Elemento]:
    resultado: set[Elemento] = set()
    for elemento in a:
        if elemento not in b:
            resultado.add(elemento)
    return resultado


def diferenca_simetrica_manual(
    a: set[Elemento], b: set[Elemento]
) -> set[Elemento]:
    resultado = diferenca_manual(a, b)
    for elemento in diferenca_manual(b, a):
        resultado.add(elemento)
    return resultado


def esta_contido_manual(a: set[Elemento], b: set[Elemento]) -> bool:
    for elemento in a:
        if elemento not in b:
            return False
    return True


def e_subconjunto_proprio_manual(a: set[Elemento], b: set[Elemento]) -> bool:
    return esta_contido_manual(a, b) and len(a) < len(b)


def operacoes_manualmente(a: set[Elemento], b: set[Elemento]) -> dict[str, set[Elemento]]:
    return {
        "uniao": uniao_manual(a, b),
        "intersecao": intersecao_manual(a, b),
        "A - B": diferenca_manual(a, b),
        "B - A": diferenca_manual(b, a),
        "diferenca simetrica": diferenca_simetrica_manual(a, b),
    }


def demonstrar_comparacao(a: set[Elemento], b: set[Elemento]) -> None:
    manuais = operacoes_manualmente(a, b)
    nativas = {
        "uniao": a | b,
        "intersecao": a & b,
        "A - B": a - b,
        "B - A": b - a,
        "diferenca simetrica": a ^ b,
    }
    print(f"A = {ordenar_conjunto(a)}; B = {ordenar_conjunto(b)}")
    for nome, resultado_manual in manuais.items():
        resultado_nativo = nativas[nome]
        confere = resultado_manual == resultado_nativo
        print(
            f"{nome}: manual = {ordenar_conjunto(resultado_manual)}; "
            f"nativa = {ordenar_conjunto(resultado_nativo)}; "
            f"confere = {'sim' if confere else 'NAO'}"
        )
    inclusao = esta_contido_manual(a, b)
    inclusao_nativa = a <= b
    proprio = e_subconjunto_proprio_manual(a, b)
    proprio_nativo = a < b
    print(f"A ⊆ B: manual = {inclusao}; nativa = {inclusao_nativa}")
    print(f"A ⊂ B: manual = {proprio}; nativa = {proprio_nativo}")


def executar_parte1() -> None:
    print("\n=== Parte 1: Teoria dos Conjuntos ===")
    a = ler_conjunto(input("Elementos de A (separados por virgula): "))
    b = ler_conjunto(input("Elementos de B (separados por virgula): "))
    universo = ler_conjunto(input("Elementos do universo U: "))
    while True:
        print(
            "\n1 Uniao  2 Intersecao  3 A-B  4 B-A  5 Diferenca simetrica\n"
            "6 Pertinencia em A  7 Inclusao  8 Cardinalidade e complemento\n"
            "9 Comparar implementacao manual com a nativa  0 Voltar"
        )
        opcao = input("Escolha: ").strip()
        if opcao == "0":
            return
        if opcao == "1":
            print(ordenar_conjunto(uniao_manual(a, b)))
        elif opcao == "2":
            print(ordenar_conjunto(intersecao_manual(a, b)))
        elif opcao == "3":
            print(ordenar_conjunto(diferenca_manual(a, b)))
        elif opcao == "4":
            print(ordenar_conjunto(diferenca_manual(b, a)))
        elif opcao == "5":
            print(ordenar_conjunto(diferenca_simetrica_manual(a, b)))
        elif opcao == "6":
            x = ler_conjunto(input("Elemento x: "))
            if len(x) != 1:
                print("Informe exatamente um elemento.")
            else:
                elemento = next(iter(x))
                print(f"{elemento} pertence a A? {elemento in a}")
        elif opcao == "7":
            print(f"A ⊆ B? {esta_contido_manual(a, b)}")
            print(f"A ⊂ B? {e_subconjunto_proprio_manual(a, b)}")
        elif opcao == "8":
            print(f"|A| = {len(a)}; |B| = {len(b)}")
            print(
                "Complemento de A em U = "
                f"{ordenar_conjunto(diferenca_manual(universo, a))}"
            )
        elif opcao == "9":
            demonstrar_comparacao(a, b)
        else:
            print("Opcao invalida.")


@dataclass(frozen=True)
class Classificacao:
    entrada: str
    valor: Fraction | None
    justificativa: str
    tipo: str

    @property
    def conjuntos(self) -> tuple[str, ...]:
        if self.valor is None:
            return ("I", "R")
        if self.valor.denominator != 1:
            return ("Q", "R")
        if self.valor.numerator < 0:
            return ("Z", "Q", "R")
        return ("N", "Z", "Q", "R")

    @property
    def nao_pertence(self) -> tuple[str, ...]:
        return tuple(nome for nome in ("N", "Z", "Q", "I", "R") if nome not in self.conjuntos)

    def valor_formatado(self) -> str:
        if self.valor is None:
            return "irracional"
        if self.valor.denominator == 1:
            return str(self.valor.numerator)
        return f"{self.valor.numerator}/{self.valor.denominator}"


def fracao_periodica(texto: str) -> Fraction | None:
    correspondencia = re.fullmatch(r"([+-]?)(\d+)[,.](\d*)\((\d+)\)", texto)
    if correspondencia is None:
        return None

    sinal, parte_inteira, parte_nao_periodica, periodo = correspondencia.groups()
    prefixo = int(parte_inteira + parte_nao_periodica)
    repetido = int(parte_inteira + parte_nao_periodica + periodo)
    denominador = (10 ** len(parte_nao_periodica)) * (10 ** len(periodo) - 1)
    valor = Fraction(repetido - prefixo, denominador)
    return -valor if sinal == "-" else valor


def classificar_numero(entrada: str) -> Classificacao:
    texto = entrada.strip().replace(" ", "")
    if not texto:
        raise ValueError("A entrada nao pode ficar vazia.")

    periodica = fracao_periodica(texto)
    if periodica is not None:
        return Classificacao(
            entrada,
            periodica,
            "Dizima periodica; a fracao geratriz foi calculada e simplificada.",
            "dizima periodica",
        )

    raiz = re.fullmatch(r"(?:√(\d+)|sqrt\((\d+)\))", texto, flags=re.IGNORECASE)
    if raiz is not None:
        radicando = int(raiz.group(1) or raiz.group(2))
        raiz_inteira = math.isqrt(radicando)
        if raiz_inteira * raiz_inteira == radicando:
            valor = Fraction(raiz_inteira)
            return Classificacao(
                entrada,
                valor,
                f"Raiz exata: {raiz_inteira} x {raiz_inteira} = {radicando}.",
                "raiz exata",
            )
        return Classificacao(
            entrada,
            None,
            f"{radicando} nao e quadrado perfeito; sua raiz e irracional.",
            "raiz irracional",
        )

    if "/" in texto:
        partes = texto.split("/")
        if len(partes) != 2:
            raise ValueError("Use uma fracao no formato a/b.")
        try:
            valor = Fraction(int(partes[0]), int(partes[1]))
        except (ValueError, ZeroDivisionError) as erro:
            raise ValueError("Fracao invalida; confira numerador e denominador.") from erro
        return Classificacao(
            entrada,
            valor,
            f"Fracao exata, simplificada para {valor}.",
            "fracao",
        )

    formato_decimal = texto.replace(",", ".")
    try:
        decimal = Decimal(formato_decimal)
    except InvalidOperation as erro:
        raise ValueError(
            "Formato nao reconhecido. Exemplos: -3, 3/4, 1,25, 0,(3), sqrt(2)."
        ) from erro
    if not decimal.is_finite():
        raise ValueError("Informe um numero real finito.")
    valor = Fraction(decimal)
    tipo = "inteiro" if valor.denominator == 1 else "decimal exato"
    return Classificacao(
        entrada,
        valor,
        "Representacao finita/exata; todo decimal exato e racional.",
        tipo,
    )


def exibir_classificacao(resultado: Classificacao) -> None:
    print(f"Entrada: {resultado.entrada}")
    print(f"Tipo: {resultado.tipo}")
    print(f"Valor exato: {resultado.valor_formatado()}")
    if resultado.tipo == "dizima periodica":
        print(f"Fracao geratriz: {resultado.valor_formatado()}")
    print("Pertence a: " + ", ".join(resultado.conjuntos))
    print("Nao pertence a: " + ", ".join(resultado.nao_pertence))
    print(f"Justificativa: {resultado.justificativa}")


def primos_ate(limite: int) -> list[int]:
    if limite < 2:
        return []
    eh_primo = [True] * (limite + 1)
    eh_primo[0] = eh_primo[1] = False
    for candidato in range(2, math.isqrt(limite) + 1):
        if eh_primo[candidato]:
            for multiplo in range(candidato * candidato, limite + 1, candidato):
                eh_primo[multiplo] = False
    return [numero for numero in range(2, limite + 1) if eh_primo[numero]]


def divisores(numero: int) -> list[int]:
    if numero <= 0:
        raise ValueError("Informe um inteiro positivo para listar divisores.")
    resultado: list[int] = []
    for candidato in range(1, math.isqrt(numero) + 1):
        if numero % candidato == 0:
            resultado.append(candidato)
            outro_divisor = numero // candidato
            if outro_divisor != candidato:
                resultado.append(outro_divisor)
    return sorted(resultado)


def executar_parte2() -> None:
    print("\n=== Parte 2: Classificador de Numeros ===")
    while True:
        print("\n1 Classificar numero  2 Primos ate n  3 Divisores  0 Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "0":
            return
        try:
            if opcao == "1":
                entrada = input("Numero: ")
                exibir_classificacao(classificar_numero(entrada))
            elif opcao == "2":
                limite = int(input("Limite n: "))
                print(f"Primos ate {limite}: {primos_ate(limite)}")
            elif opcao == "3":
                numero = int(input("Inteiro positivo: "))
                print(f"Divisores de {numero}: {divisores(numero)}")
            else:
                print("Opcao invalida.")
        except ValueError as erro:
            print(f"Erro: {erro}")


INTERESSES: dict[str, set[str]] = {
    "Ana": {"rock", "jazz", "cinema", "games"},
    "Bia": {"jazz", "cinema", "series", "viagens"},
    "Caio": {"games", "tecnologia", "cinema"},
}


def calcular_jaccard(a: set[str], b: set[str]) -> tuple[set[str], set[str], float]:
    intersecao = intersecao_manual(a, b)
    uniao = uniao_manual(a, b)
    indice = len(intersecao) / len(uniao) if uniao else 1.0
    return intersecao, uniao, indice


def executar_parte3() -> None:
    print("\n=== Parte 3: Recomendacao por interesses (Jaccard) ===")
    for primeiro, segundo in (("Ana", "Bia"), ("Ana", "Caio"), ("Bia", "Caio")):
        intersecao, uniao, indice = calcular_jaccard(
            INTERESSES[primeiro], INTERESSES[segundo]
        )
        print(
            f"{primeiro} e {segundo}: intersecao {ordenar_conjunto(intersecao)} "
            f"({len(intersecao)}); uniao {ordenar_conjunto(uniao)} "
            f"({len(uniao)}); Jaccard = {len(intersecao)}/{len(uniao)} "
            f"= {indice:.2f}"
        )
    print("Recomendacao para Ana: Caio (maior indice: 0.40).")

    if input("Comparar interesses personalizados? (s/n): ").strip().lower() == "s":
        interesses_a = set(ler_conjunto(input("Interesses da pessoa A: ")))
        interesses_b = set(ler_conjunto(input("Interesses da pessoa B: ")))
        intersecao, uniao, indice = calcular_jaccard(interesses_a, interesses_b)
        print(
            f"Intersecao = {ordenar_conjunto(intersecao)}; "
            f"uniao = {ordenar_conjunto(uniao)}; Jaccard = {indice:.2f}"
        )


def executar_demo() -> None:
    print("DEMONSTRACAO DO LABORATORIO DE CONJUNTOS")
    print("\n=== Parte 1: implementacao manual x Python ===")
    casos = (
        (
            "Caso geral (com repetidos removidos)",
            ler_conjunto("1, 2, 2, 3, 4"),
            ler_conjunto("3, 4, 5, 6"),
        ),
        ("Conjunto vazio", set(), ler_conjunto("1, 2")),
        ("Conjuntos disjuntos", ler_conjunto("1, 2"), ler_conjunto("3, 4")),
        ("Conjuntos iguais", ler_conjunto("1, 2, 3"), ler_conjunto("1, 2, 3")),
        (
            "Exemplo criado pela equipe",
            ler_conjunto("2, 4, 6"),
            ler_conjunto("4, 6, 8, 10"),
        ),
    )
    for titulo, a, b in casos:
        print(f"\n{titulo}:")
        demonstrar_comparacao(a, b)
    universo = ler_conjunto("1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
    a = ler_conjunto("1, 2, 2, 3, 4")
    print(f"Complemento de A em U = {ordenar_conjunto(diferenca_manual(universo, a))}")
    print(f"|A| = {len(a)}; 3 pertence a A? {3 in a}; 5 pertence a A? {5 in a}")

    print("\n=== Parte 2: classificacoes ===")
    entradas = (
        "-3",
        "0",
        "7",
        "3/4",
        "-5/2",
        "1,25",
        "0,(3)",
        "2,(7)",
        "1,2(5)",
        "0,(9)",
        "sqrt(9)",
        "sqrt(2)",
    )
    for entrada in entradas:
        resultado = classificar_numero(entrada)
        print(
            f"{entrada:8} -> {resultado.valor_formatado():12} "
            f"Pertence a: {', '.join(resultado.conjuntos)}"
        )
        if resultado.tipo == "dizima periodica":
            print(f"           Fracao geratriz: {resultado.valor_formatado()}")
        print(f"           Justificativa: {resultado.justificativa}")
    print(f"Primos de N ate 30: {primos_ate(30)}")
    print(f"Divisores de 36: {divisores(36)}")

    print("\n=== Parte 3: recomendacao por Jaccard ===")
    for primeiro, segundo in (("Ana", "Bia"), ("Ana", "Caio"), ("Bia", "Caio")):
        intersecao, uniao, indice = calcular_jaccard(
            INTERESSES[primeiro], INTERESSES[segundo]
        )
        print(
            f"{primeiro} e {segundo}: intersecao {ordenar_conjunto(intersecao)} "
            f"({len(intersecao)}); uniao {ordenar_conjunto(uniao)} "
            f"({len(uniao)}); Jaccard = {len(intersecao)}/{len(uniao)} "
            f"= {indice:.2f}"
        )
    print("Recomendacao para Ana: Caio (maior indice: 0.40).")
    interesses_lia = {"xadrez", "musica", "trilhas"}
    interesses_rui = {"musica", "fotografia"}
    intersecao, uniao, indice = calcular_jaccard(interesses_lia, interesses_rui)
    print(
        "Exemplo criado pela equipe (Lia e Rui): "
        f"intersecao {ordenar_conjunto(intersecao)} ({len(intersecao)}); "
        f"uniao {ordenar_conjunto(uniao)} ({len(uniao)}); "
        f"Jaccard = {len(intersecao)}/{len(uniao)} = {indice:.2f}"
    )


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        executar_demo()
        return
    if len(sys.argv) != 1:
        print("Uso: python main.py [--demo]")
        raise SystemExit(2)

    while True:
        print(
            "\nLABORATORIO DE CONJUNTOS\n"
            "1 Teoria dos Conjuntos\n"
            "2 Classificador de Numeros\n"
            "3 Recomendacao por interesses (Jaccard)\n"
            "0 Sair"
        )
        opcao = input("Escolha: ").strip()
        if opcao == "0":
            print("Programa encerrado.")
            return
        if opcao == "1":
            executar_parte1()
        elif opcao == "2":
            executar_parte2()
        elif opcao == "3":
            executar_parte3()
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
