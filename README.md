# Sistema de Triagem de Pronto-Socorro

**Disciplina:** Algoritmos e Estrutura de Dados I (Engenharia de Software) | **Linguagem:** Python 3, sem dependências externas

Todo pronto-socorro enfrenta o mesmo problema: em um dado momento há
mais pacientes esperando do que profissionais para atender, e a ordem
de chegada sozinha não é justa quando alguém chega em estado grave
depois de quem chegou primeiro com um caso leve. Este projeto resolve
isso simulando uma triagem baseada no **Protocolo de Manchester** (5
níveis de gravidade — vermelho, laranja, amarelo, verde, azul), e serve
como projeto integrador de uma disciplina de Estrutura de Dados: cada
módulo do repositório corresponde a um entregável do semestre, e o
projeto final (Módulo 6) combina as estruturas estudadas em um sistema
único e funcional.

## Estrutura do repositório

```
triagem-pronto-socorro/
├── modulo1_semanas1-3_modularizacao/     # Entregável 1 — funções, parâmetros, recursão
├── modulo2_semanas4-6_tad_memoria/       # Entregável 2 — TAD com alocação estática x dinâmica
├── modulo3_semanas7-9_listas/            # Entregável 3 — lista em array, encadeada simples, dupla e circular
├── modulo4_semanas10-11_pilhas/          # Entregável 4 — pilha + undo/redo de classificação
├── modulo5_semanas12-13_filas/           # Entregável 5 — fila circular/encadeada + fila de prioridade
└── modulo6_semanas14-16_projeto_final/   # Projeto final — integra as estruturas acima
```

Cada pasta é **autocontida**: tem seu próprio código-fonte comentado,
`README.md`, testes e `relatorio.md` técnico (1–2 páginas), seguindo as
normas de entrega da disciplina. Por isso alguns arquivos-base
(`paciente.py`, `validacao.py`, `utils.py`) aparecem copiados em mais
de uma pasta — é proposital: cada entrega podia ser corrigida
isoladamente, na data correspondente do cronograma.

## Como rodar

Não há dependências externas — só Python 3 padrão.

```bash
# Rodar os testes de um módulo específico (exemplo: Módulo 5)
cd modulo5_semanas12-13_filas
python3 test_modulo5.py

# Rodar o sistema de triagem final, interativo, no terminal
cd modulo6_semanas14-16_projeto_final
python3 interface_cli.py

# Rodar os testes de TODOS os módulos de uma vez, a partir da raiz
for d in modulo*/; do echo "== $d =="; (cd "$d" && python3 test_*.py); done
```

**Resultado atual: 123 testes passando em 6 módulos, 0 falhas.**

## Resumo por módulo

| Módulo | Semanas | Estrutura central | Testes |
|---|---|---|---|
| 1 — Modularização | 1–3 | Funções, parâmetros, recursão | 25 |
| 2 — TAD e Memória | 4–6 | TAD estático x dinâmico | 20 |
| 3 — Listas | 7–9 | Array, encadeada simples, dupla e circular | 18 |
| 4 — Pilhas | 10–11 | Pilha + undo/redo de classificação | 21 |
| 5 — Filas | 12–13 | Fila circular/encadeada + **fila de prioridade** | 23 |
| 6 — Projeto Final | 14–16 | Integração: fila de prioridade + lista + pilha | 16 |

Cada pasta tem um `README.md` com instruções específicas de execução e
um `relatorio.md` com a análise técnica exigida (interface pública,
complexidade das operações, comparações entre implementações).

## Decisões de projeto

- **A fila de prioridade (Módulo 5, coração do Módulo 6) não usa
  nenhuma estrutura pronta do Python** — nem `heapq`, nem
  `collections.deque` diretamente. Ela é composta por 5 instâncias da
  `FilaEncadeada` (a fila FIFO com nós encadeados implementada na
  Semana 12), uma por cor do Protocolo de Manchester, respeitando FIFO
  dentro do mesmo nível de gravidade. Um heap binário resolveria o
  mesmo problema em O(log n), mas com apenas 5 níveis discretos essa
  abordagem é mais simples de auditar e roda em O(1) por operação —
  ver a justificativa completa em `modulo5.../relatorio.md`.
- **O histórico de atendimentos (Módulo 3/6) é uma lista encadeada
  simples**, não um array: o volume de pacientes atendidos por turno é
  imprevisível, e inserir no início (mantendo o mais recente primeiro)
  é O(1) com um ponteiro de início, sem desperdiçar memória com
  capacidade pré-alocada.
- **Reclassificar um paciente custa O(n)** (reconstrói a fila de
  prioridade a partir de quem ainda está esperando), uma troca
  consciente: reclassificações são raras comparadas a
  atender/enfileirar, então vale manter essas duas operações simples e
  O(1)/O(k).

## Limitações conhecidas

- Sem reavaliação automática de prioridade por tempo de espera (fica
  registrado como trabalho futuro nos relatórios dos Módulos 5 e 6).
- Sem persistência em disco — os dados existem apenas durante a
  execução do programa.

## Licença

Distribuído sob a licença MIT — veja [`LICENSE`](LICENSE).

---

Projeto desenvolvido para a disciplina de Algoritmos e Estrutura de
Dados I, com o roteiro de trabalho adaptado para Python 3.
