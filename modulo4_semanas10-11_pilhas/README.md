# Entregável 4 — Módulo 4 (Semanas 10–11): Pilhas
**Projeto:** Sistema de Triagem de Pronto-Socorro | **Linguagem:** Python 3

## Conteúdo

| Arquivo | Semana | Conteúdo |
|---|---|---|
| `pilha_array.py` | 10 | TAD Pilha implementado com array (lista Python) |
| `pilha_encadeada.py` | 10 | TAD Pilha implementado com lista encadeada |
| `undo_redo_classificacao.py` | 11 | Aplicação prática: desfazer/refazer reclassificações |
| `test_modulo4.py` | — | Testes das pilhas e da aplicação de undo/redo |
| `relatorio.md` | — | Relatório técnico |

## Aplicação escolhida (Semana 11)

Entre as 3 opções do roteiro (avaliação de expressões pós-fixadas,
verificação de balanceamento de parênteses, ou undo/redo), foi escolhida
**undo/redo**, por ser diretamente aplicável ao problema real do
projeto: um enfermeiro pode reclassificar um paciente por engano
durante a triagem e precisa poder desfazer (e, se necessário, refazer)
essa ação rapidamente.

## Como executar

```bash
python3 test_modulo4.py
```

## Decisões de projeto

- Foram implementadas as duas versões de pilha (array e encadeada)
  pedidas no roteiro, com a mesma interface (`empilhar`, `desempilhar`,
  `topo`, `esta_vazia`, `tamanho`), para focar a comparação apenas na
  estrutura interna.
- A aplicação de undo/redo usa **duas pilhas** (`pilha_desfazer` e
  `pilha_refazer`), um padrão clássico: toda nova reclassificação
  invalida o "futuro" de redo, exatamente como em editores de texto.
