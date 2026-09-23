# ADR-002: Reclassificação reconstrói a fila inteira (O(n))

**Status:** Aceito

## Contexto

Às vezes a classificação inicial de um paciente está errada e precisa
ser corrigida (por exemplo, um paciente entrou como "amarelo" mas na
verdade é "vermelho"). Como a `FilaPrioridade` guarda os pacientes em
5 filas FIFO separadas por cor ([ADR-001](ADR-001-fila-por-cor.md)),
reclassificar significa "mover" o paciente de uma fila para outra.

O problema: uma fila FIFO encadeada (`FilaEncadeada`) só permite
remover eficientemente do início — não existe remoção O(1) de um
elemento arbitrário no meio da fila.

## Decisão

Ao reclassificar, `SistemaTriagem` reconstrói a `FilaPrioridade`
inteira a partir da lista de pacientes ainda em espera (mantida à
parte, em um dicionário `_pacientes_em_espera`, para permitir achar
qualquer paciente em O(1) por id). O mesmo vale para desfazer uma
reclassificação (undo/redo).

## Consequências

- `reclassificar_paciente` e `desfazer_reclassificacao` custam O(n),
  onde n é o número de pacientes aguardando.
- Isso é aceitável porque reclassificação é um evento raro comparado a
  `cadastrar_paciente`/`atender_proximo` (que acontecem a cada
  paciente) — e o volume de pacientes em um pronto-socorro por turno é
  de dezenas a poucas centenas, não milhões.
- Em troca, `atender_proximo` e `cadastrar_paciente` continuam simples
  e O(1)/O(k) — não pagam nenhum custo extra por causa da
  reclassificação existir.
- Se o volume de reclassificações crescesse muito, a estrutura poderia
  evoluir para uma fila de prioridade baseada em heap indexado (com
  suporte a `decrease-key`), que permitiria mudar a prioridade de um
  elemento sem reconstruir tudo. Não foi necessário nesse escopo.
