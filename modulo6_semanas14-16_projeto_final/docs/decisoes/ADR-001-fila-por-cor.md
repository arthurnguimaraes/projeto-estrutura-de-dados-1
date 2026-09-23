# ADR-001: Fila de prioridade como 5 filas FIFO separadas por cor

**Status:** Aceito

## Contexto

O Protocolo de Manchester classifica cada paciente em uma de 5 cores
(vermelho, laranja, amarelo, verde, azul), da mais para a menos grave.
O sistema precisa sempre chamar o próximo paciente respeitando dois
critérios ao mesmo tempo: gravidade primeiro, e dentro da mesma
gravidade, ordem de chegada (FIFO).

Duas abordagens foram consideradas:

1. Uma única fila com comparação de prioridade a cada inserção (heap
   binário ou lista ordenada).
2. Cinco filas FIFO independentes, uma por cor, e ao atender sempre
   olhar a fila da cor mais grave que não está vazia.

## Decisão

Implementar a `FilaPrioridade` (`fila_prioridade.py`) como 5 filas FIFO
separadas (uma `FilaEncadeada` por cor), em vez de uma única estrutura
com comparação de prioridade por elemento.

## Consequências

- `atender_proximo` fica O(k), com k = 5 (número fixo de cores) — só
  precisa olhar qual das 5 filas não-vazias tem a cor mais grave.
- `cadastrar_paciente` é O(1) — só insere no fim da fila da cor
  correspondente, sem nenhuma comparação.
- A ordem de chegada dentro da mesma cor é garantida automaticamente
  pela própria fila FIFO, sem precisar guardar timestamp para
  desempate.
- Só funciona bem porque o número de níveis de prioridade é pequeno e
  fixo (5 cores). Com muitos níveis de prioridade diferentes, uma heap
  seria mais adequada.
- Reclassificar um paciente (mudar de cor) fica mais caro — ver
  [ADR-002](ADR-002-reclassificacao-o-n.md).
