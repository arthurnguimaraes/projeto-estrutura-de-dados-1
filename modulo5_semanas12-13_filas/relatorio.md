# Relatório Técnico — Módulo 5: Filas
**Projeto:** Sistema de Triagem de Pronto-Socorro | **Linguagem:** Python 3

## 1. TAD Fila — interface pública

`enfileirar(item)`, `desenfileirar()`, `frente()`, `esta_vazia()`,
`tamanho()` (`esta_cheia()` adicional na versão com capacidade fixa).

## 2. Complexidade — array circular x lista encadeada

| Operação | Array Circular (capacidade fixa) | Lista Encadeada (sem limite) |
|---|---|---|
| Enfileirar | O(1) — usa aritmética modular, sem deslocar elementos | O(1) — insere no fim, com ponteiro `_fim` mantido |
| Desenfileirar | O(1) — avança o índice de início (`% capacidade`) | O(1) — remove do início |
| Consultar frente | O(1) | O(1) |
| Verificar cheia | O(1) | O(1) (sempre `False`) |

**Por que array *circular* e não um array comum?** Um array comum
exigiria O(n) para desenfileirar (deslocar todos os elementos após
remover o primeiro). O array circular resolve isso reaproveitando os
espaços liberados através de índices calculados com módulo (`%
capacidade`), atingindo O(1) — ao custo de ter uma capacidade máxima
fixa, definida na criação.

**Trade-off real:** a versão circular é ideal quando há um limite físico
conhecido (ex.: número de leitos de espera); a encadeada é preferível
quando a demanda é imprevisível, como tende a ser o caso real de um
pronto-socorro em dias de pico.

## 3. Fila de Prioridade (Protocolo de Manchester)

### Estrutura escolhida
Um dicionário de 5 filas FIFO — cada uma uma instância da própria
`FilaEncadeada` implementada nesta semana, sem recorrer a estruturas
prontas do Python —, uma por cor, ordenadas por prioridade na hora de
decidir quem atender.

### Complexidade
| Operação | Complexidade | Justificativa |
|---|---|---|
| `enfileirar` | O(1) | Insere direto na fila da cor correspondente |
| `desenfileirar` | O(k), k=5 (constante) | Percorre as cores da mais grave à menos grave até achar uma fila não vazia |
| `proximo` (consulta) | O(k) | Mesma lógica, sem remover |
| `posicao_estimada` | O(n) | Precisa contar quantos pacientes de prioridade igual/maior estão à frente |

Como k=5 é uma constante pequena e fixa (não cresce com o número de
pacientes), na prática `desenfileirar` se comporta como O(1).

**Por que não um heap binário?** Um heap ofereceria O(log n) para
inserir/remover com prioridades arbitrárias e contínuas. Como o
Protocolo de Manchester define apenas 5 níveis discretos, a abordagem
de "uma fila por nível" é mais simples de implementar, mais fácil de
auditar (importante em um sistema de saúde) e mais rápida na prática
(O(1) real por nível, sem custo logarítmico), sem abrir mão do
FIFO dentro do mesmo nível de gravidade — algo que um heap comum não
garante automaticamente sem lógica adicional.

## 4. Discussão da política anti-*starvation*

**Risco identificado:** um paciente "verde" ou "azul" poderia, em teoria,
esperar indefinidamente se chegarem pacientes mais graves continuamente.

**Decisão adotada neste projeto (mantendo o escopo enxuto):** a
reavaliação automática por tempo de espera (ex.: "promover" um paciente
verde para amarelo após X minutos) **não foi implementada** — ela fica
registrada aqui como *trabalho futuro*, pois exigiria um mecanismo de
tempo real (ou simulação de tempo) fora do escopo do roteiro da
disciplina. Na prática hospitalar real, esse problema é mitigado com
reavaliação periódica por um profissional de enfermagem, não por um
algoritmo automático — o que é coerente com o sistema atender fielmente
o Protocolo de Manchester tal como especificado, sem inventar regras
extras não pedidas.

## 5. Testes e simulação realizados

23 testes cobrindo: capacidade máxima da fila circular (com erro
esperado ao exceder), reaproveitamento de espaço circular, FIFO na fila
encadeada, e — o mais importante — a fila de prioridade: emergência
(vermelho) atendida antes de pacientes que chegaram primeiro, ordem FIFO
preservada dentro do mesmo nível de gravidade, e cálculo de posição
estimada na fila. Ver `test_modulo5.py` e a simulação completa em
`simulacao_atendimento_hospitalar.py` (8 pacientes, ordem de atendimento
verificada manualmente).
