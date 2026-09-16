# Entregável 1 — Módulo 1 (Semanas 1–3): Modularização
**Projeto:** Sistema de Triagem de Pronto-Socorro
**Linguagem:** Python 3

## O que este entregável contém

Biblioteca de funções utilitárias modularizada, que servirá de base para o
sistema de triagem construído nos módulos seguintes.

| Arquivo | Semana | Conteúdo |
|---|---|---|
| `paciente.py` | — | Estrutura básica `Paciente` (será formalizada como TAD no Módulo 2) |
| `utils.py` | 1 | Geração de ID sequencial e formatação de data/hora |
| `validacao.py` | 1 | Validação de nome e classificação (Protocolo de Manchester) |
| `parametros_demo.py` | 2 | Demonstração de passagem por valor x por referência |
| `recursao_demo.py` | 3 | Fatorial, Fibonacci e busca binária recursiva |
| `main.py` | — | Integra tudo em um fluxo de demonstração |
| `test_modulo1.py` | — | Testes automatizados (25 casos) |

## Como executar

Requer apenas Python 3.8+ (sem dependências externas).

```bash
# Rodar a demonstração principal
python3 main.py

# Rodar os testes
python3 test_modulo1.py
```

## Decisões de projeto

- **Separação em módulos:** cada arquivo tem uma única responsabilidade
  (geração de dados, validação, demonstração de parâmetros, recursão),
  evitando um único `main.py` monolítico.
- **Sem dependências externas:** os testes usam apenas `assert`/comparação
  manual (função `checar`), dispensando `pytest`, para manter o projeto
  simples de rodar em qualquer ambiente.
- **Classificação de Manchester definida desde já:** embora a fila de
  prioridade só seja implementada no Módulo 5, as 5 cores e seus pesos
  numéricos já ficam centralizados em `validacao.py`, para serem
  reaproveitados sem alterações nos módulos seguintes.
- **Linguagem:** Python foi escolhido pela agilidade de desenvolvimento.
  Isso implica adaptações em relação a linguagens como C (ver
  `relatorio.md`, seção "Observações sobre a linguagem").
