import unittest
from fractions import Fraction

from main import (
    calcular_jaccard,
    classificar_numero,
    diferenca_manual,
    diferenca_simetrica_manual,
    divisores,
    esta_contido_manual,
    e_subconjunto_proprio_manual,
    intersecao_manual,
    ler_conjunto,
    primos_ate,
    uniao_manual,
)


class TestOperacoesDeConjuntos(unittest.TestCase):
    def test_entrada_remove_repetidos(self) -> None:
        self.assertEqual(ler_conjunto("1, 1, 1, 2"), {1, 2})

    def test_conjunto_vazio(self) -> None:
        vazio: set[int] = set()
        b = {1, 2}
        self.assertEqual(uniao_manual(vazio, b), b)
        self.assertEqual(intersecao_manual(vazio, b), vazio)
        self.assertEqual(diferenca_manual(vazio, b), vazio)
        self.assertEqual(diferenca_simetrica_manual(vazio, b), b)
        self.assertTrue(esta_contido_manual(vazio, b))

    def test_conjuntos_iguais(self) -> None:
        a = {1, 2, 3}
        self.assertEqual(diferenca_manual(a, a), set())
        self.assertEqual(diferenca_simetrica_manual(a, a), set())
        self.assertTrue(esta_contido_manual(a, a))
        self.assertFalse(e_subconjunto_proprio_manual(a, a))

    def test_conjuntos_disjuntos(self) -> None:
        a = {1, 2}
        b = {3, 4}
        self.assertEqual(intersecao_manual(a, b), set())
        self.assertEqual(uniao_manual(a, b), {1, 2, 3, 4})
        self.assertEqual(diferenca_simetrica_manual(a, b), {1, 2, 3, 4})

    def test_subconjunto_proprio(self) -> None:
        self.assertTrue(e_subconjunto_proprio_manual({1, 2}, {1, 2, 3}))
        self.assertFalse(esta_contido_manual({1, 2, 3}, {1, 2}))


class TestClassificador(unittest.TestCase):
    def test_inteiros_e_fracoes(self) -> None:
        self.assertEqual(classificar_numero("-3").conjuntos, ("Z", "Q", "R"))
        self.assertEqual(classificar_numero("0").conjuntos, ("N", "Z", "Q", "R"))
        self.assertEqual(classificar_numero("3/4").valor, Fraction(3, 4))
        self.assertEqual(classificar_numero("1,25").valor, Fraction(5, 4))

    def test_dizimas_periodicas(self) -> None:
        exemplos = {
            "0,(3)": Fraction(1, 3),
            "2,(7)": Fraction(25, 9),
            "1,2(5)": Fraction(113, 90),
            "0,(9)": Fraction(1, 1),
        }
        for entrada, esperado in exemplos.items():
            with self.subTest(entrada=entrada):
                resultado = classificar_numero(entrada)
                self.assertEqual(resultado.valor, esperado)
                esperado_conjuntos = (
                    ("N", "Z", "Q", "R")
                    if entrada == "0,(9)"
                    else ("Q", "R")
                )
                self.assertEqual(resultado.conjuntos, esperado_conjuntos)
        self.assertEqual(classificar_numero("0,(9)").conjuntos, ("N", "Z", "Q", "R"))

    def test_raizes(self) -> None:
        self.assertEqual(classificar_numero("sqrt(9)").valor, Fraction(3))
        self.assertEqual(classificar_numero("√2").conjuntos, ("I", "R"))

    def test_rejeita_fracao_com_denominador_zero(self) -> None:
        with self.assertRaises(ValueError):
            classificar_numero("1/0")

    def test_bonuses(self) -> None:
        self.assertEqual(
            primos_ate(30), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        )
        self.assertEqual(divisores(36), [1, 2, 3, 4, 6, 9, 12, 18, 36])


class TestRecomendacao(unittest.TestCase):
    def test_jaccard_dos_exemplos(self) -> None:
        ana = {"rock", "jazz", "cinema", "games"}
        bia = {"jazz", "cinema", "series", "viagens"}
        caio = {"games", "tecnologia", "cinema"}
        self.assertAlmostEqual(calcular_jaccard(ana, bia)[2], 2 / 6)
        self.assertAlmostEqual(calcular_jaccard(ana, caio)[2], 2 / 5)
        self.assertAlmostEqual(calcular_jaccard(bia, caio)[2], 1 / 6)
        intersecao, uniao, indice = calcular_jaccard(
            {"xadrez", "musica", "trilhas"}, {"musica", "fotografia"}
        )
        self.assertEqual(intersecao, {"musica"})
        self.assertEqual(uniao, {"xadrez", "musica", "trilhas", "fotografia"})
        self.assertEqual(indice, 1 / 4)


if __name__ == "__main__":
    unittest.main()
