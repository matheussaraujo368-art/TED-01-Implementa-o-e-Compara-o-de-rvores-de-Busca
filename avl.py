"""
avl.py - Árvore AVL (árvore binária de busca auto-balanceada).

TED 01 - Estrutura de Dados - UNIBALSAS
Dupla: Rafael Rodrigues Pontara e Mateus Brito

Convenções usadas:
    altura(None)  = 0
    altura(folha) = 1
    fator de balanceamento (FB) = altura(esq) - altura(dir)

    Um nó está balanceado quando FB ∈ {-1, 0, +1}.
    FB = +2  -> pesado à ESQUERDA  (caso LL ou LR)
    FB = -2  -> pesado à DIREITA   (caso RR ou RL)

    Caso | Situação                                  | Correção
    -----|-------------------------------------------|-------------------------------
    LL   | FB(no) = +2 e inserção na esq. do filho esq| rotação simples à DIREITA
    RR   | FB(no) = -2 e inserção na dir. do filho dir| rotação simples à ESQUERDA
    LR   | FB(no) = +2 e inserção na dir. do filho esq| rotação dupla esquerda-direita
    RL   | FB(no) = -2 e inserção na esq. do filho dir| rotação dupla direita-esquerda
"""


class NoAVL:
    __slots__ = ("chave", "esq", "dir", "altura")

    def __init__(self, chave):
        self.chave = chave
        self.esq = None
        self.dir = None
        self.altura = 1  # um nó novo é sempre folha


class AVL:
    def __init__(self, registrar_rotacoes=False):
        self.raiz = None
        self.tamanho = 0
        # contadores de rotações (úteis no relatório e nos testes)
        self.rotacoes = {"LL (simples dir.)": 0, "RR (simples esq.)": 0,
                         "LR (dupla esq-dir)": 0, "RL (dupla dir-esq)": 0}
        # se True, guarda um texto descrevendo cada rotação feita
        self.registrar_rotacoes = registrar_rotacoes
        self.log = []

    # ------------------------------------------------------------------ #
    # Auxiliares: altura e fator de balanceamento
    # ------------------------------------------------------------------ #
    @staticmethod
    def _h(no):
        return no.altura if no is not None else 0

    def _atualizar_altura(self, no):
        no.altura = 1 + max(self._h(no.esq), self._h(no.dir))

    def fator_balanceamento(self, no):
        """FB = altura(subárvore esquerda) - altura(subárvore direita)."""
        return self._h(no.esq) - self._h(no.dir) if no is not None else 0

    # ------------------------------------------------------------------ #
    # Rotações
    # ------------------------------------------------------------------ #
    def rotacao_direita(self, y):
        """Rotação simples à DIREITA em torno de y (corrige o caso LL).

                y                x
               / \\             /  \\
              x   T3   ==>    T1    y
             / \\                   / \\
            T1  T2                T2  T3

        x sobe, y desce para a direita, e a subárvore T2 (que estava à
        direita de x) passa a ser filha esquerda de y. A ordem em-ordem
        T1 < x < T2 < y < T3 é preservada."""
        x = y.esq
        T2 = x.dir
        x.dir = y
        y.esq = T2
        self._atualizar_altura(y)   # y agora está abaixo de x: atualiza primeiro
        self._atualizar_altura(x)
        return x                    # nova raiz desta subárvore

    def rotacao_esquerda(self, x):
        """Rotação simples à ESQUERDA em torno de x (corrige o caso RR).

              x                    y
             / \\                  /  \\
            T1  y      ==>       x    T3
               / \\              / \\
              T2  T3           T1  T2
        """
        y = x.dir
        T2 = y.esq
        y.esq = x
        x.dir = T2
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        return y

    def rotacao_esquerda_direita(self, z):
        """Rotação dupla ESQUERDA-DIREITA (LR).
        1º) rotação à esquerda no filho esquerdo de z (transforma LR em LL);
        2º) rotação à direita em z.

                z               z                y
               /               /                / \\
              x      ==>      y       ==>      x   z
               \\             /
                y           x
        """
        z.esq = self.rotacao_esquerda(z.esq)
        return self.rotacao_direita(z)

    def rotacao_direita_esquerda(self, z):
        """Rotação dupla DIREITA-ESQUERDA (RL).
        1º) rotação à direita no filho direito de z (transforma RL em RR);
        2º) rotação à esquerda em z.

              z              z                  y
               \\              \\                / \\
                x    ==>       y      ==>     z   x
               /                \\
              y                  x
        """
        z.dir = self.rotacao_direita(z.dir)
        return self.rotacao_esquerda(z)

    # ------------------------------------------------------------------ #
    # Balanceamento: identifica o caso e aplica a rotação correta
    # ------------------------------------------------------------------ #
    def _balancear(self, no):
        self._atualizar_altura(no)
        fb = self.fator_balanceamento(no)

        if fb > 1:  # pesado à esquerda
            if self.fator_balanceamento(no.esq) >= 0:
                caso, nova = "LL (simples dir.)", self.rotacao_direita(no)
            else:
                caso, nova = "LR (dupla esq-dir)", self.rotacao_esquerda_direita(no)
        elif fb < -1:  # pesado à direita
            if self.fator_balanceamento(no.dir) <= 0:
                caso, nova = "RR (simples esq.)", self.rotacao_esquerda(no)
            else:
                caso, nova = "RL (dupla dir-esq)", self.rotacao_direita_esquerda(no)
        else:
            return no  # já balanceado: nada a fazer

        self.rotacoes[caso] += 1
        if self.registrar_rotacoes:
            self.log.append(f"desbalanceamento no nó {no.chave} (FB={fb:+d}) "
                            f"-> caso {caso}; nova raiz da subárvore: {nova.chave}")
        return nova

    # ------------------------------------------------------------------ #
    # Inserção
    # ------------------------------------------------------------------ #
    def inserir(self, chave):
        """Insere 'chave' (duplicatas são ignoradas). Retorna True se inseriu."""
        antes = self.tamanho
        self.raiz = self._inserir(self.raiz, chave)
        return self.tamanho > antes

    def _inserir(self, no, chave):
        # 1) inserção normal de BST
        if no is None:
            self.tamanho += 1
            return NoAVL(chave)
        if chave < no.chave:
            no.esq = self._inserir(no.esq, chave)
        elif chave > no.chave:
            no.dir = self._inserir(no.dir, chave)
        else:
            return no  # duplicata
        # 2) na volta da recursão: atualiza altura, calcula FB e rotaciona se preciso
        return self._balancear(no)

    # ------------------------------------------------------------------ #
    # Busca com contagem de comparações (mesmo critério da BST)
    # ------------------------------------------------------------------ #
    def buscar(self, chave):
        """Retorna (encontrou, comparacoes). Cada nó visitado = 1 comparação."""
        comparacoes = 0
        atual = self.raiz
        while atual is not None:
            comparacoes += 1
            if chave == atual.chave:
                return True, comparacoes
            atual = atual.esq if chave < atual.chave else atual.dir
        return False, comparacoes

    def contem(self, chave):
        return self.buscar(chave)[0]

    # ------------------------------------------------------------------ #
    # Métricas, percursos e verificação
    # ------------------------------------------------------------------ #
    def altura(self):
        return self._h(self.raiz)

    def em_ordem(self):
        resultado, pilha, atual = [], [], self.raiz
        while pilha or atual is not None:
            while atual is not None:
                pilha.append(atual)
                atual = atual.esq
            atual = pilha.pop()
            resultado.append(atual.chave)
            atual = atual.dir
        return resultado

    def pre_ordem(self):
        resultado, pilha = [], [self.raiz] if self.raiz else []
        while pilha:
            n = pilha.pop()
            resultado.append(n.chave)
            if n.dir:
                pilha.append(n.dir)
            if n.esq:
                pilha.append(n.esq)
        return resultado

    def por_niveis(self):
        niveis, nivel = [], [self.raiz] if self.raiz else []
        while nivel:
            niveis.append([n.chave for n in nivel])
            nivel = [f for n in nivel for f in (n.esq, n.dir) if f is not None]
        return niveis

    def desenhar(self, mostrar_fb=True):
        """Desenho em texto (girado 90°: direita em cima, esquerda embaixo).
        Mostra o fator de balanceamento de cada nó entre colchetes."""
        linhas = []

        def rec(no, prof):
            if no is None:
                return
            rec(no.dir, prof + 1)
            fb = f" [{self.fator_balanceamento(no):+d}]" if mostrar_fb else ""
            linhas.append("    " * prof + f"{no.chave}{fb}")
            rec(no.esq, prof + 1)

        rec(self.raiz, 0)
        return "\n".join(linhas)

    def verificar(self):
        """Confere as propriedades da AVL. Lança AssertionError se algo falhar:
          - propriedade de BST (em-ordem estritamente crescente);
          - altura armazenada em cada nó está correta;
          - |FB| <= 1 em todos os nós."""
        def rec(no):
            if no is None:
                return 0
            he, hd = rec(no.esq), rec(no.dir)
            h = 1 + max(he, hd)
            assert no.altura == h, f"altura errada no nó {no.chave}"
            assert abs(he - hd) <= 1, f"nó {no.chave} desbalanceado (FB={he - hd})"
            return h

        rec(self.raiz)
        chaves = self.em_ordem()
        assert all(a < b for a, b in zip(chaves, chaves[1:])), "propriedade de BST violada"
        assert len(chaves) == self.tamanho
        return True

    def __len__(self):
        return self.tamanho


if __name__ == "__main__":
    print("Demonstração das 4 rotações da AVL\n")
    casos = {
        "LL -> rotação simples à direita":       [30, 20, 10],
        "RR -> rotação simples à esquerda":      [10, 20, 30],
        "LR -> rotação dupla esquerda-direita":  [30, 10, 20],
        "RL -> rotação dupla direita-esquerda":  [10, 30, 20],
    }
    for titulo, seq in casos.items():
        t = AVL(registrar_rotacoes=True)
        for x in seq:
            t.inserir(x)
        print(f"== {titulo} | inserindo {seq}")
        for linha in t.log:
            print("   ", linha)
        print(t.desenhar())
        print()

    t = AVL()
    for x in range(1, 16):
        t.inserir(x)
    print("AVL com inserção crescente 1..15 (altura =", t.altura(), "):")
    print(t.desenhar())
