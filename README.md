# TED 01 – Implementação e Comparação de Árvores de Busca (BST × AVL)

**Disciplina:** Estrutura de Dados – UNIBALSAS
**Dupla:** Pedro paulo e Matheus Brito
**Linguagem:** Python 3.8 

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `bst.py` | Árvore Binária de Busca: inserção, busca com contagem de comparações, altura, percursos em-ordem / pré-ordem / por níveis e desenho em texto |
| `avl.py` | Árvore AVL: inserção, altura e fator de balanceamento, detecção dos casos LL/RR/LR/RL, as 4 rotações, busca com contagem, percursos, desenho com FB e `verificar()` |
| `experimento.py` | Script das medições: insere a mesma sequência (crescente, decrescente e aleatória) nas duas árvores, faz as buscas e conta as comparações |
| `testes.py` | 12 testes automáticos (cada rotação isolada, rotações com subárvores, 30 sequências aleatórias verificadas após cada inserção) |
| `resultados/` | Saídas geradas pelo experimento (`resultados.csv`, `buscas_exemplo.csv`, `grafico_comparacoes.png`) |
| `Relatorio_TED01_BST_AVL.pdf` | Relatório com resultados e análise |

## Como executar

Abra um terminal **dentro desta pasta** e rode:

```bash
# 1) Demonstrações rápidas (mostram as árvores desenhadas no terminal)
python bst.py
python avl.py          # mostra as 4 rotações (LL, RR, LR, RL) acontecendo

# 2) Testes automáticos
python testes.py

# 3) Experimento completo (n = 100 ... 10.000; leva ~20 s)
python experimento.py

#    versão rápida (n = 100, 500, 1000; ~1 s)
python experimento.py --rapido
```

No Windows, se `python` não funcionar, use `py`.

## Critério de contagem de comparações

Cada nó visitado durante a busca conta como **1 comparação** (em cada nó a chave procurada é comparada com a chave do nó para decidir entre achou / esquerda / direita). O mesmo critério é usado na BST e na AVL, e as duas usam exatamente o mesmo código de busca, então a única diferença medida é a **forma** da árvore.

## Observação

A BST foi implementada de forma **iterativa** porque, com inserção ordenada, ela vira uma lista de altura *n*; com n = 10.000 uma versão recursiva estouraria o limite de recursão do Python. A AVL pode ser recursiva, pois sua altura fica em torno de 14 para n = 10.000.
