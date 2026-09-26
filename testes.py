"""
testes.py - Testes automáticos da BST e da AVL (usa apenas a biblioteca padrão).

Execução:  python testes.py
"""
import random
import unittest

from avl import AVL
from bst import BST


def pre(t):
    return t.pre_ordem()


class TestesRotacoesAVL(unittest.TestCase):
    """Cada caso de desbalanceamento deve disparar a rotação correta e
    resultar na árvore esperada (conferida pelo percurso pré-ordem)."""

    def _montar(self, seq):
        t = AVL()
        for x in seq:
            t.inserir(x)
        t.verificar()
        return t

    def test_LL_rotacao_simples_direita(self):
        t = self._montar([30, 20, 10])
        self.assertEqual(pre(t), [20, 10, 30])
        self.assertEqual(t.rotacoes["LL (simples dir.)"], 1)
        self.assertEqual(sum(t.rotacoes.values()), 1)

    def test_RR_rotacao_simples_esquerda(self):
        t = self._montar([10, 20, 30])
        self.assertEqual(pre(t), [20, 10, 30])
        self.assertEqual(t.rotacoes["RR (simples esq.)"], 1)
        self.assertEqual(sum(t.rotacoes.values()), 1)

    def test_LR_rotacao_dupla_esquerda_direita(self):
        t = self._montar([30, 10, 20])
        self.assertEqual(pre(t), [20, 10, 30])
        self.assertEqual(t.rotacoes["LR (dupla esq-dir)"], 1)
        self.assertEqual(sum(t.rotacoes.values()), 1)

    def test_RL_rotacao_dupla_direita_esquerda(self):
        t = self._montar([10, 30, 20])
        self.assertEqual(pre(t), [20, 10, 30])
        self.assertEqual(t.rotacoes["RL (dupla dir-esq)"], 1)
        self.assertEqual(sum(t.rotacoes.values()), 1)

    def test_rotacao_com_subarvores(self):
        # LL com subárvore T2 não vazia: 50,30,70,20,40,10
        # antes: 50(30(20(10),40),70) -> FB(50)=+2 -> rotação direita em 50
        t = self._montar([50, 30, 70, 20, 40, 10])
        self.assertEqual(pre(t), [30, 20, 10, 50, 40, 70])  # 40 (T2) virou filho esq. de 50

    def test_LR_com_subarvores(self):
        # 50,20,70,10,30,25 -> FB(50)=+2, FB(20)=-1 -> caso LR
        t = self._montar([50, 20, 70, 10, 30, 25])
        self.assertEqual(t.rotacoes["LR (dupla esq-dir)"], 1)
        self.assertEqual(pre(t), [30, 20, 10, 25, 50, 70])

    def test_RL_com_subarvores(self):
        # 20,10,50,40,60,45 -> FB(20)=-2, FB(50)=+1 -> caso RL
        t = self._montar([20, 10, 50, 40, 60, 45])
        self.assertEqual(t.rotacoes["RL (dupla dir-esq)"], 1)
        self.assertEqual(pre(t), [40, 20, 10, 50, 45, 60])


class TestesGerais(unittest.TestCase):
    def test_crescente_e_decrescente_balanceadas(self):
        for seq in (range(1, 1001), range(1000, 0, -1)):
            t = AVL()
            for x in seq:
                t.inserir(x)
            t.verificar()
            self.assertEqual(t.altura(), 10)  # árvore quase completa: ceil(log2(1001)) = 10

    def test_aleatorio_contra_set(self):
        rng = random.Random(2026)
        for _ in range(30):
            dados = [rng.randint(0, 5000) for _ in range(rng.randint(1, 800))]
            avl, bst, ref = AVL(), BST(), set()
            for x in dados:
                self.assertEqual(avl.inserir(x), x not in ref)
                bst.inserir(x)
                ref.add(x)
                avl.verificar()  # propriedades válidas após CADA inserção
            self.assertEqual(avl.em_ordem(), sorted(ref))
            self.assertEqual(bst.em_ordem(), sorted(ref))
            for q in range(-5, 5006, 37):
                self.assertEqual(avl.contem(q), q in ref)
                self.assertEqual(bst.contem(q), q in ref)

    def test_bst_degenera_em_lista(self):
        b = BST()
        for x in range(1, 501):
            b.inserir(x)
        self.assertEqual(b.altura(), 500)
        self.assertEqual(b.buscar(500), (True, 500))

    def test_contagem_de_comparacoes(self):
        b, a = BST(), AVL()
        for x in [1, 2, 3, 4, 5, 6, 7]:
            b.inserir(x)
            a.inserir(x)
        # BST: lista 1->2->...->7 ; AVL: árvore perfeita com raiz 4
        self.assertEqual(b.buscar(7), (True, 7))
        self.assertEqual(a.buscar(4), (True, 1))
        self.assertEqual(a.buscar(7), (True, 3))
        self.assertEqual(a.buscar(8), (False, 3))
        self.assertEqual(BST().buscar(1), (False, 0))

    def test_duplicatas(self):
        a = AVL()
        self.assertTrue(a.inserir(5))
        self.assertFalse(a.inserir(5))
        self.assertEqual(len(a), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
