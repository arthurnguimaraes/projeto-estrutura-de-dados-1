# Relatório Técnico Final — Sistema de Triagem de Pronto-Socorro
**Linguagem:** Python 3

## 1. Visão geral do sistema

O sistema simula o fluxo de um pronto-socorro: chegada de pacientes,
classificação por gravidade (Protocolo de Manchester), atendimento por
prioridade e registro em histórico. Integra três estruturas de dados
estudadas ao longo da disciplina, cumprindo o requisito do Módulo 6 de
"combinar ao menos duas estruturas estudadas".

## 2. Estruturas integradas e por quê

| Estrutura | Módulo de origem | Por que essa estrutura resolve o problema |
|---|---|---|
| Fila de prioridade (5 filas FIFO por cor) | Módulo 5 | Modela exatamente a regra real de triagem: gravidade decide quem é atendido primeiro, mas dentro do mesmo nível de gravidade a ordem de chegada é justa |
| Lista encadeada | Módulo 3 | Histórico de atendimentos cresce de forma imprevisível ao longo do dia; inserção no início/fim é O(1), sem desperdício de memória com capacidade pré-alocada |
| Pilha (via undo/redo) | Módulo 4 | Corrigir uma classificação errada é uma ação "desfazer a última decisão" — mapeamento direto para LIFO |

## 3. Interface pública do `SistemaTriagem`

| Método | Parâmetros | Retorno | Complexidade |
|---|---|---|---|
| `cadastrar_paciente(nome, classificacao)` | `str`, `str` | `Paciente` | O(1) |
| `atender_proximo()` | — | `Paciente \| None` | O(k), k=5 (busca pela cor mais grave) + O(1) inserção no histórico |
| `reclassificar_paciente(id, nova_cor)` | `int`, `str` | `None` | O(n) — reconstrói a fila (ver seção 4) |
| `desfazer_reclassificacao(id)` | `int` | `None` | O(n) — mesma razão |
| `pacientes_aguardando()` | — | `int` | O(k) |
| `posicao_na_fila(id)` | `int` | `int` | O(n) |
| `historico()` | — | `list[Paciente]` | O(n) |
| `buscar_no_historico(id)` | `int` | `Paciente \| None` | O(n) — busca linear na lista encadeada |

## 4. Por que reclassificar custa O(n)

A `FilaPrioridade` organiza pacientes em 5 filas FIFO separadas (uma por
cor), cada uma uma `FilaEncadeada` própria. Quando um paciente muda de
cor, ele precisa "trocar de fila" — como uma fila encadeada FIFO não
suporta remoção eficiente de um elemento arbitrário no meio (só do
início), a solução adotada foi **reconstruir a fila inteira** a partir dos
pacientes ainda em espera (armazenados também em um dicionário
`_pacientes_em_espera`, para acesso O(1) por ID).

**Justificativa da escolha:** reclassificações são eventos raros
comparados a `atender_proximo`/`cadastrar_paciente` (que ocorrem a cada
paciente). Pagar O(n) ocasionalmente em troca de manter
`atender_proximo` simples e O(k) constante é um trade-off razoável para
o volume de pacientes de um pronto-socorro (dezenas a poucas centenas
por turno, não milhões).

## 5. Comparação: quando usar lista, pilha ou fila (síntese do Módulo 6)

| Estrutura | Quando usar | Custo típico |
|---|---|---|
| Lista (array ou encadeada) | Dados que precisam ser percorridos, buscados ou listados por completo, sem ordem de prioridade | O(n) na maioria das operações não-extremidade |
| Pilha (LIFO) | A última ação precisa poder ser desfeita antes de qualquer outra | O(1) em todas as operações |
| Fila (FIFO) | Ordem de chegada deve ser respeitada | O(1) com array circular ou lista encadeada |
| Fila de prioridade | Existe um critério de urgência que sobrepõe a ordem de chegada | O(1) a O(k) por nível, dependendo da implementação |

## 6. Testes de integração realizados

16 testes cobrindo o fluxo completo: cadastro → atendimento respeitando
prioridade → histórico atualizado; reclassificação alterando a ordem de
atendimento; desfazer reclassificação restaurando a ordem original;
busca no histórico; e comportamento do sistema vazio — ver
`test_final.py`.

## 7. Limitações e trabalhos futuros

- Sem reavaliação automática por tempo de espera (discutido no relatório
  do Módulo 5).
- Sem persistência em disco/banco de dados — os dados existem apenas
  durante a execução do programa.
- A reconstrução O(n) da fila ao reclassificar poderia ser otimizada
  com uma fila de prioridade baseada em heap indexado, caso o volume de
  reclassificações crescesse muito — não foi necessário neste escopo.
