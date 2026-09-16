# Entregável 5 — Módulo 5 (Semanas 12–13): Filas
**Projeto:** Sistema de Triagem de Pronto-Socorro | **Linguagem:** Python 3

Este é o módulo mais importante do projeto: a **fila de prioridade** é
o componente central de todo o sistema de triagem.

## Conteúdo

| Arquivo | Semana | Conteúdo |
|---|---|---|
| `fila_array_circular.py` | 12 | Fila FIFO com array circular, capacidade fixa |
| `fila_encadeada.py` | 12 | Fila FIFO com lista encadeada, sem limite |
| `fila_prioridade.py` | 13 | **Fila de prioridade Manchester (5 níveis)**, composta a partir de 5 `FilaEncadeada` |
| `simulacao_atendimento_hospitalar.py` | 13 | Simulação de um fluxo real de chegada/atendimento |
| `test_modulo5.py` | — | Testes das 3 filas |
| `relatorio.md` | — | Relatório técnico |

## Como executar

```bash
python3 simulacao_atendimento_hospitalar.py   # roda a simulação
python3 test_modulo5.py                       # roda os testes
```

## Como a fila de prioridade funciona

Em vez de um heap binário, foi usada uma abordagem mais simples e
transparente: **uma `FilaEncadeada` (a própria fila FIFO implementada
nesta semana) separada para cada uma das 5 cores** do Protocolo de
Manchester. Isso garante duas propriedades ao mesmo tempo:

1. Entre cores diferentes, quem tem cor mais grave é sempre atendido
   primeiro (mesmo que tenha chegado depois).
2. Dentro da mesma cor, a ordem de chegada é respeitada (FIFO) — dois
   pacientes "amarelo" são atendidos na ordem em que chegaram.

Veja `relatorio.md` para a análise de complexidade completa e a
discussão sobre a política adotada para evitar *starvation*.
