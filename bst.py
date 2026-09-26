"""
bst.py - Árvore Binária de Busca (BST) sem balanceamento.

TED 01 - Estrutura de Dados - UNIBALSAS
Dupla: Rafael Rodrigues Pontara e Mateus Brito

Observação de implementação:
    A inserção e a busca são ITERATIVAS (laço while) e não recursivas.
    Motivo: quando os dados chegam em ordem crescente/decrescente a BST
    vira uma "lista" com altura n. Com n = 10.000, uma versão recursiva
    estouraria o limite de recursão do Python (~1000 chamadas).
"""


class NoBST:
    """Nó da BST: guarda a chave e os ponteiros para os filhos."""

    __slots__ = ("chave", "esq", "dir")

    def __init__(self, chave):
        self.chave = chave
        self.esq = None
        self.dir = None


class BST:
    def __init__(self):
        self.raiz = None
        self.tamanho = 0

    # ------------------------------------------------------------------ #
    # Inserção
    # ------------------------------------------------------------------ #
    def inserir(self, chave):
        """Insere 'chave' na árvore. Chaves repetidas são ignoradas.
        Retorna True se inseriu, False se a chave já existia."""
        novo = NoBST(chave)
        if self.raiz is None:
            self.raiz = novo
            self.tamanho = 1
            return True

        atual = self.raiz
        while True:
            if chave < atual.chave:
                if atual.esq is None:
                    atual.esq = novo
                    break
                atual = atual.esq
            elif chave > atual.chave:
                if atual.dir is None:
                    atual.dir = novo
                    break
                atual = atual.dir
            else:  # chave duplicada
                return False
        self.tamanho += 1
        return True

    # ------------------------------------------------------------------ #
    # Busca com contagem de comparações
    # ------------------------------------------------------------------ #
    def buscar(self, chave):
        """Procura 'chave' e retorna a tupla (encontrou, comparacoes).

        Critério de contagem (o mesmo usado na AVL): cada nó visitado
        conta como UMA comparação, pois em cada nó decidimos entre
        "igual", "menor" ou "maior" comparando a chave buscada com a
        chave do nó."""
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
    # Métricas e percursos (para visualizar/verificar a estrutura)
    # ------------------------------------------------------------------ #
    def altura(self):
        """Altura da árvore (árvore vazia = 0; só a raiz = 1).
        Calculada por níveis (BFS) para não usar recursão."""
        if self.raiz is None:
            return 0
        h, nivel = 0, [self.raiz]
        while nivel:
            h += 1
            nivel = [f for n in nivel for f in (n.esq, n.dir) if f is not None]
        return h

    def em_ordem(self):
        """Percurso em-ordem (esq, raiz, dir): devolve as chaves ordenadas."""
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
        """Percurso pré-ordem (raiz, esq, dir)."""
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
        """Percurso em largura: lista de níveis, cada nível é uma lista de chaves."""
        niveis, nivel = [], [self.raiz] if self.raiz else []
        while nivel:
            niveis.append([n.chave for n in nivel])
            nivel = [f for n in nivel for f in (n.esq, n.dir) if f is not None]
        return niveis

    def desenhar(self):
        """Desenho em texto da árvore (girada 90°: a raiz fica à esquerda,
        o filho direito aparece acima e o esquerdo abaixo). Indicado para
        árvores pequenas."""
        linhas, pilha = [], [(self.raiz, 0, False)] if self.raiz else []
        # percurso "direita-raiz-esquerda" iterativo
        while pilha:
            no, prof, visitado = pilha.pop()
            if no is None:
                continue
            if visitado:
                linhas.append("    " * prof + str(no.chave))
            else:
                pilha.append((no.esq, prof + 1, False))
                pilha.append((no, prof, True))
                pilha.append((no.dir, prof + 1, False))
        return "\n".join(linhas)

    def __len__(self):
        return self.tamanho


if __name__ == "__main__":
    # Pequena demonstração
    t = BST()
    for x in [50, 30, 70, 20, 40, 60, 80]:
        t.inserir(x)
    print("BST balanceada por acaso (50,30,70,20,40,60,80):")
    print(t.desenhar())
    print("Em-ordem:", t.em_ordem(), "| altura:", t.altura())
    print("Buscar 60 ->", t.buscar(60), "(encontrou, comparações)")

    t2 = BST()
    for x in [1, 2, 3, 4, 5, 6, 7]:
        t2.inserir(x)
    print("\nBST com inserção crescente (1..7) -> vira uma lista:")
    print(t2.desenhar())
    print("Altura:", t2.altura(), "| buscar 7 ->", t2.buscar(7))
