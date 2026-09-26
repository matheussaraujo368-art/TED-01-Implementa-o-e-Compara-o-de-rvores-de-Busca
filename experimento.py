"""
experimento.py - Comparação de desempenho de busca: BST x AVL.

TED 01 - Estrutura de Dados - UNIBALSAS
Dupla: Rafael Rodrigues Pontara e Mateus Brito

O que o experimento faz, para cada tamanho n:
  1. gera a sequência 1..n em ordem CRESCENTE (e também DECRESCENTE);
  2. insere exatamente a mesma sequência na BST e na AVL;
  3. busca TODAS as n chaves nas duas árvores (buscas bem-sucedidas) e
     também n chaves que NÃO existem (buscas malsucedidas);
  4. conta as comparações (1 comparação = 1 nó visitado) e resume em
     média, máximo e total;
  5. como controle, repete com uma sequência ALEATÓRIA (semente fixa).

Saídas:
  - tabelas no terminal;
  - resultados/resultados.csv       (todas as medições)
  - resultados/buscas_exemplo.csv   (buscas individuais para n = 1000)
  - resultados/grafico_comparacoes.png (se o matplotlib estiver instalado)

Uso:
  python experimento.py            # n = 100, 500, 1000, 2000, 5000, 10000
  python experimento.py --rapido   # n = 100, 500, 1000 (roda em ~1 s)
"""
import csv
import math
import os
import random
import sys
import time

from avl import AVL
from bst import BST

SEMENTE = 2026
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")


def gerar_sequencia(n, ordem):
    if ordem == "crescente":
        return list(range(1, n + 1))
    if ordem == "decrescente":
        return list(range(n, 0, -1))
    seq = list(range(1, n + 1))
    random.Random(SEMENTE + n).shuffle(seq)
    return seq


def medir_buscas(arvore, chaves):
    """Busca cada chave e devolve (total, média, máximo) de comparações."""
    total, maximo = 0, 0
    for k in chaves:
        _, c = arvore.buscar(k)
        total += c
        if c > maximo:
            maximo = c
    return total, total / len(chaves), maximo


def rodar(tamanhos, ordens=("crescente", "decrescente", "aleatória")):
    linhas = []
    for ordem in ordens:
        for n in tamanhos:
            seq = gerar_sequencia(n, ordem)
            bst, avl = BST(), AVL()

            t0 = time.perf_counter()
            for x in seq:
                bst.inserir(x)
            t_ins_bst = time.perf_counter() - t0

            t0 = time.perf_counter()
            for x in seq:
                avl.inserir(x)
            t_ins_avl = time.perf_counter() - t0

            existentes = list(range(1, n + 1))
            # chaves inexistentes: valores "entre" e "fora" das chaves (x + 0.5)
            inexistentes = [k + 0.5 for k in range(0, n)]

            tb, mb, xb = medir_buscas(bst, existentes)
            ta, ma, xa = medir_buscas(avl, existentes)
            _, mb_f, xb_f = medir_buscas(bst, inexistentes)
            _, ma_f, xa_f = medir_buscas(avl, inexistentes)

            linhas.append({
                "ordem": ordem, "n": n,
                "log2_n": round(math.log2(n), 2),
                "altura_bst": bst.altura(), "altura_avl": avl.altura(),
                "media_comp_bst": round(mb, 2), "media_comp_avl": round(ma, 2),
                "max_comp_bst": xb, "max_comp_avl": xa,
                "total_comp_bst": tb, "total_comp_avl": ta,
                "razao_bst_avl": round(tb / ta, 1),
                "media_falha_bst": round(mb_f, 2), "media_falha_avl": round(ma_f, 2),
                "max_falha_bst": xb_f, "max_falha_avl": xa_f,
                "rotacoes_avl": sum(avl.rotacoes.values()),
                "tempo_insercao_bst_s": round(t_ins_bst, 4),
                "tempo_insercao_avl_s": round(t_ins_avl, 4),
            })
            print(f"  [ok] {ordem:<11} n={n:<6} "
                  f"(altura BST={bst.altura():<6} AVL={avl.altura()})", flush=True)
    return linhas


def buscas_exemplo(n=1000):
    """Algumas buscas individuais em árvores montadas com a sequência crescente."""
    bst, avl = BST(), AVL()
    for x in range(1, n + 1):
        bst.inserir(x)
        avl.inserir(x)
    alvos = [1, n // 4, n // 2, 3 * n // 4, n, n + 1]
    res = []
    for k in alvos:
        eb, cb = bst.buscar(k)
        ea, ca = avl.buscar(k)
        res.append({"chave": k, "encontrada": "sim" if eb else "não",
                    "comp_bst": cb, "comp_avl": ca})
    return res


def imprimir_tabela(linhas, ordem):
    print(f"\n=== Sequência {ordem.upper()} - buscas bem-sucedidas (todas as n chaves) ===")
    cab = (f"{'n':>6} | {'log2 n':>6} | {'alt BST':>7} | {'alt AVL':>7} | "
           f"{'méd BST':>8} | {'méd AVL':>7} | {'máx BST':>7} | {'máx AVL':>7} | {'BST/AVL':>7}")
    print(cab)
    print("-" * len(cab))
    for l in linhas:
        if l["ordem"] != ordem:
            continue
        print(f"{l['n']:>6} | {l['log2_n']:>6} | {l['altura_bst']:>7} | {l['altura_avl']:>7} | "
              f"{l['media_comp_bst']:>8} | {l['media_comp_avl']:>7} | "
              f"{l['max_comp_bst']:>7} | {l['max_comp_avl']:>7} | {l['razao_bst_avl']:>6}x")


def salvar_csv(caminho, linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(linhas)


def gerar_grafico(linhas, caminho):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(matplotlib não instalado: gráfico não gerado - "
              "instale com 'pip install matplotlib' se quiser o PNG)")
        return False

    cres = [l for l in linhas if l["ordem"] == "crescente"]
    ns = [l["n"] for l in cres]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    ax1.plot(ns, [l["media_comp_bst"] for l in cres], "o-", color="#c0392b", label="BST")
    ax1.plot(ns, [l["media_comp_avl"] for l in cres], "s-", color="#1f6fb2", label="AVL")
    ax1.set_title("Média de comparações por busca (inserção crescente)")
    ax1.set_xlabel("n (número de elementos)")
    ax1.set_ylabel("comparações")
    ax1.grid(alpha=.3)
    ax1.legend()

    ax2.plot(ns, [l["max_comp_avl"] for l in cres], "s-", color="#1f6fb2", label="AVL (máximo)")
    ax2.plot(ns, [l["media_comp_avl"] for l in cres], "^--", color="#5dade2", label="AVL (média)")
    ax2.plot(ns, [math.log2(n) for n in ns], ":", color="#555", label="log₂ n")
    ax2.plot(ns, [1.44 * math.log2(n + 2) for n in ns], "-.", color="#999",
             label="limite teórico 1,44·log₂(n+2)")
    ax2.set_xscale("log")
    ax2.set_title("AVL: comparações crescem como log n")
    ax2.set_xlabel("n (escala logarítmica)")
    ax2.set_ylabel("comparações")
    ax2.grid(alpha=.3)
    ax2.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    return True


def main():
    rapido = "--rapido" in sys.argv
    tamanhos = [100, 500, 1000] if rapido else [100, 500, 1000, 2000, 5000, 10000]
    os.makedirs(PASTA, exist_ok=True)

    print("Critério: cada nó visitado durante a busca conta como 1 comparação.")
    print(f"Tamanhos: {tamanhos}\n")
    t0 = time.perf_counter()
    linhas = rodar(tamanhos)

    for ordem in ("crescente", "decrescente", "aleatória"):
        imprimir_tabela(linhas, ordem)

    print("\n=== Buscas malsucedidas (chave inexistente) - sequência crescente ===")
    print(f"{'n':>6} | {'méd BST':>8} | {'méd AVL':>7} | {'máx BST':>7} | {'máx AVL':>7}")
    for l in linhas:
        if l["ordem"] == "crescente":
            print(f"{l['n']:>6} | {l['media_falha_bst']:>8} | {l['media_falha_avl']:>7} | "
                  f"{l['max_falha_bst']:>7} | {l['max_falha_avl']:>7}")

    ex = buscas_exemplo(1000)
    print("\n=== Buscas individuais - n = 1000, inserção crescente ===")
    print(f"{'chave':>6} | {'existe':>6} | {'comp BST':>8} | {'comp AVL':>8}")
    for e in ex:
        print(f"{e['chave']:>6} | {e['encontrada']:>6} | {e['comp_bst']:>8} | {e['comp_avl']:>8}")

    salvar_csv(os.path.join(PASTA, "resultados.csv"), linhas)
    salvar_csv(os.path.join(PASTA, "buscas_exemplo.csv"), ex)
    ok = gerar_grafico(linhas, os.path.join(PASTA, "grafico_comparacoes.png"))

    print(f"\nArquivos salvos em: {PASTA}")
    print("  - resultados.csv\n  - buscas_exemplo.csv" + ("\n  - grafico_comparacoes.png" if ok else ""))
    print(f"Tempo total: {time.perf_counter() - t0:.1f} s")


if __name__ == "__main__":
    main()
