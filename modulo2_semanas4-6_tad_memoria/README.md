# Entregável 2 — Módulo 2 (Semanas 4–6): TAD e Memória
**Projeto:** Sistema de Triagem de Pronto-Socorro | **Linguagem:** Python 3

## Conteúdo

| Arquivo | Semana | Conteúdo |
|---|---|---|
| `tad_ficha_triagem_spec.md` | 4 | Especificação da interface do TAD (sem implementação) |
| `ficha_triagem_estatica.py` | 5 | Implementação com capacidade fixa (simula array estático) |
| `ficha_triagem_dinamica.py` | 6 | Implementação com lista ligada por nós (simula alocação dinâmica) |
| `test_modulo2.py` | — | Testes comparando as duas versões |
| `relatorio.md` | — | Relatório técnico comparativo |

`paciente.py`, `validacao.py` e `utils.py` foram copiados do Módulo 1
(reaproveitados sem alterações).

## Como executar

```bash
python3 test_modulo2.py
```

## Decisões de projeto

Python não possui alocação manual de memória (sem `malloc`/`free`), então:
- A versão **estática** foi simulada com uma lista Python de tamanho fixo,
  pré-preenchida com `None`, cuja capacidade é definida na criação do
  repositório e nunca cresce — o mais próximo do comportamento de um
  `array` de tamanho fixo declarado em C.
- A versão **dinâmica** foi simulada com uma lista ligada por nós
  (`_No`), criados sob demanda a cada inserção, sem limite de capacidade
  — analogia estrutural direta com `malloc(sizeof(No))` em C, mas com a
  liberação de memória (`free`) feita automaticamente pelo garbage
  collector do Python quando um nó deixa de ser referenciado.

Veja `relatorio.md` para a comparação completa entre as duas versões.
