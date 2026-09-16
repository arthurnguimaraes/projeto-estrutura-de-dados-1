# Projeto Final — Módulo 6 (Semanas 14–16): Sistema de Triagem de Pronto-Socorro
**Linguagem:** Python 3 (sem dependências externas)

## Sobre o projeto

Sistema completo de triagem hospitalar baseado no **Protocolo de
Manchester**, integrando três estruturas de dados estudadas na
disciplina:

| Estrutura | Papel no sistema |
|---|---|
| **Fila de prioridade** (Módulo 5) | Organiza pacientes aguardando atendimento por gravidade (obrigatório) |
| **Lista encadeada** (Módulo 3) | Histórico/prontuário de pacientes já atendidos (obrigatório) |
| **Pilha** (Módulo 4, via undo/redo) | Permite corrigir uma classificação errada antes do atendimento (extra) |

## Arquivos

| Arquivo | Descrição |
|---|---|
| `sistema_triagem.py` | Classe `SistemaTriagem` — integra as 3 estruturas |
| `interface_cli.py` | Menu interativo de linha de comando |
| `test_final.py` | 16 testes de integração |
| `relatorio.md` | Relatório técnico final |
| `apresentacao_roteiro.md` | Roteiro para a apresentação (10–15 min) |
| `paciente.py`, `validacao.py`, `utils.py` | Base (Módulo 1) |
| `pilha_array.py`, `undo_redo_classificacao.py` | Base (Módulo 4) |
| `fila_prioridade.py`, `fila_encadeada.py` | Base (Módulo 5) |
| `lista_encadeada_simples.py` | Base (Módulo 3) |

## Como executar

```bash
# Rodar o sistema interativo (menu no terminal)
python3 interface_cli.py

# Rodar os testes de integração
python3 test_final.py
```

## Fluxo principal do sistema

1. **Cadastro/triagem:** paciente chega, é classificado (vermelho a
   azul) e entra na fila de prioridade.
2. **Atendimento:** o profissional chama sempre o próximo paciente de
   maior gravidade (respeitando FIFO dentro da mesma cor); o paciente
   atendido é movido da fila para o histórico (lista encadeada).
3. **Correção (extra):** se a classificação inicial estava errada, o
   sistema permite reclassificar o paciente (e desfazer, se necessário)
   enquanto ele ainda está na fila de espera.

## Decisões de projeto

- A reclassificação exige **reconstruir a fila de prioridade** (O(n)),
  pois a estrutura organiza pacientes em filas separadas por cor — essa
  escolha foi feita conscientemente, já que reclassificações são raras
  comparadas a atender/enfileirar (ver `relatorio.md`).
- Reavaliação automática por tempo de espera **não foi implementada**
  (ver discussão de escopo no relatório do Módulo 5) — mantida fora do
  projeto final para preservar o cronograma de 16 semanas.
