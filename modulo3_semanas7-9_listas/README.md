# Entregável 3 — Módulo 3 (Semanas 7–9): Listas
**Projeto:** Sistema de Triagem de Pronto-Socorro | **Linguagem:** Python 3

## Conteúdo

| Arquivo | Semana | Conteúdo |
|---|---|---|
| `lista_array.py` | 7 | Lista sequencial (array dinâmico) |
| `lista_encadeada_simples.py` | 8 | Lista encadeada simples (um ponteiro `proximo`) |
| `lista_dupla_circular.py` | 9 | Lista duplamente encadeada, com modo circular opcional |
| `test_modulo3.py` | — | Testes das 4 variações |
| `relatorio.md` | — | Análise de complexidade comparada |

## Contexto de uso no sistema de triagem

Estas listas representam, por exemplo, os pacientes que já passaram
pela triagem e aguardam atendimento em ordem de chegada (antes da
priorização por gravidade, que só entra no Módulo 5), ou o prontuário
de pacientes já atendidos no dia.

## Como executar

```bash
python3 test_modulo3.py
```

## Decisões de projeto

- Todas as implementações compartilham a mesma interface conceitual
  (`inserir`, `remover`, `buscar`, `percorrer`, `tamanho`, `esta_vazia`),
  facilitando a comparação de desempenho pedida no roteiro.
- A lista duplamente encadeada e a lista circular foram implementadas
  na mesma classe (`ListaDuplamenteEncadeada`), com um parâmetro
  `circular` no construtor, para reaproveitar o código de navegação
  bidirecional sem duplicação.
- No modo circular, `percorrer()` é limitado ao tamanho conhecido da
  lista para evitar loop infinito (já que, por definição, um percurso
  circular nunca "termina" sozinho).
