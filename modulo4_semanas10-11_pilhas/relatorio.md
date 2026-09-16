# Relatório Técnico — Módulo 4: Pilhas
**Projeto:** Sistema de Triagem de Pronto-Socorro | **Linguagem:** Python 3

## 1. TAD Pilha — interface pública

`empilhar(item)`, `desempilhar()`, `topo()`, `esta_vazia()`, `tamanho()`
— implementada de forma idêntica nas duas versões (array e encadeada).

## 2. Complexidade das operações

| Operação | Pilha com Array | Pilha Encadeada |
|---|---|---|
| Empilhar (`push`) | O(1) amortizado (`list.append`) | O(1) (novo nó vira o topo) |
| Desempilhar (`pop`) | O(1) (`list.pop()` no final) | O(1) (remove o nó do topo) |
| Consultar topo | O(1) | O(1) |
| Verificar vazia | O(1) | O(1) |

**Observação:** diferente da lista genérica (Módulo 3), a pilha só opera
em uma extremidade, então tanto o array (removendo do final, não do
início) quanto a versão encadeada atingem O(1) em todas as operações —
não há motivo estrutural para preferir uma sobre a outra em termos de
desempenho puro; a escolha costuma depender de linguagem/ambiente
(em Python, `list.append`/`pop()` já é altamente otimizado).

## 3. Aplicação prática: undo/redo de reclassificação

**Problema real resolvido:** durante a correria de um pronto-socorro,
classificações incorretas acontecem. O sistema permite reverter (e
reaplicar) a última decisão sem precisar re-triagem completa do
paciente.

**Como funciona:**
- Toda chamada a `reclassificar()` empilha a classificação **anterior**
  em `pilha_desfazer` antes de aplicar a nova.
- `desfazer()` retira o topo de `pilha_desfazer`, aplica-o ao paciente,
  e empilha a classificação que estava em vigor em `pilha_refazer`
  (para permitir reverter o próprio desfazer).
- `refazer()` faz o caminho inverso.
- Uma nova chamada a `reclassificar()` **descarta** qualquer conteúdo
  pendente em `pilha_refazer` — comportamento padrão em qualquer editor
  com undo/redo (uma nova ação sempre invalida o "futuro" anterior).

**Complexidade:** todas as operações (`reclassificar`, `desfazer`,
`refazer`) são O(1), pois usam apenas empilhar/desempilhar.

## 4. Testes realizados

21 casos cobrindo: pilha vazia, ordem LIFO de desempilhamento, erro ao
desempilhar pilha vazia (nas duas implementações), e o fluxo completo de
reclassificar → desfazer → desfazer → refazer → nova reclassificação
(verificando o descarte do redo) — ver `test_modulo4.py`.
