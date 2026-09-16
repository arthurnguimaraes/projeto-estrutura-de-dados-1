# Relatório Técnico — Módulo 3: Listas
**Projeto:** Sistema de Triagem de Pronto-Socorro | **Linguagem:** Python 3

## 1. TAD Lista — interface pública

`inserir(item, posicao=None)`, `remover(posicao)`, `buscar(item, chave)`,
`percorrer()`, `tamanho()`, `esta_vazia()` — implementados de forma
equivalente nas 4 variações (array, encadeada simples, dupla, circular).

## 2. Complexidade das operações (comparação array x encadeada)

| Operação | Array (`ListaArray`) | Encadeada Simples | Dupla (não circular) |
|---|---|---|---|
| Inserir no início | O(n) — desloca todos os elementos | O(1) | O(1) |
| Inserir no final | O(1) amortizado | O(1) — ponteiro `_fim` mantido | O(1) — ponteiro `_fim` mantido |
| Inserir no meio (posição k) | O(n) — desloca elementos após k | O(n) — percorre até a posição | O(n) — percorre até a posição |
| Remover do início | O(n) — desloca elementos restantes | O(1) | O(1) |
| Remover do final | O(1) | O(n) — não há ponteiro reverso p/ achar o penúltimo | O(1) — ponteiro `anterior` disponível |
| Buscar por valor | O(n) — busca linear | O(n) — busca linear | O(n) — busca linear |
| Percorrer do fim para o início | O(n), mas requer iterar do índice 0 se não houver acesso reverso nativo* | Não suportado diretamente (só há `proximo`) | O(n) — suportado nativamente via `anterior` |

*Em Python, `list` suporta indexação reversa nativamente (O(1) por
acesso), mas percorrer todos os elementos de trás para frente ainda é O(n).

## 3. Comparação array x encadeada — quando usar cada uma

- **Array (`ListaArray`)**: melhor quando o acesso por índice é frequente
  e as inserções/remoções concentram-se no final da lista (baixo custo
  de deslocamento). Em Python, `list.append` é O(1) amortizado.
- **Encadeada simples**: melhor quando inserções/remoções no início são
  frequentes (ex.: uma pilha de reclassificações recentes) e não há
  necessidade de acesso aleatório por índice.
- **Duplamente encadeada**: adequada quando é preciso navegar em ambas
  as direções (ex.: revisar o prontuário do paciente mais recente para
  o mais antigo e vice-versa) — custo extra de memória (um ponteiro
  `anterior` a mais por nó) compensado pela flexibilidade de navegação.
- **Circular**: útil para revezamento cíclico, como escalas de plantão
  de médicos/enfermeiros, onde depois do último elemento se volta ao
  primeiro automaticamente.

## 4. Testes realizados

18 casos cobrindo: lista vazia, inserção em posição arbitrária, busca
por chave (existente e inexistente), remoção do início/meio, percurso
em ambos os sentidos (lista dupla) e verificação estrutural dos
ponteiros de encadeamento circular — ver `test_modulo3.py`.
