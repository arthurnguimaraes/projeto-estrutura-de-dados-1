# Relatório Técnico — Módulo 1: Modularização
**Projeto:** Sistema de Triagem de Pronto-Socorro | **Linguagem:** Python 3

## 1. Funções implementadas (assinatura, parâmetros e retorno)

### `utils.py`
| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `gerar_id_paciente()` | nenhum | `int` | ID sequencial único, incrementado a cada chamada |
| `formatar_hora_chegada(momento=None)` | `momento: datetime \| None` | `str` | Data/hora no formato `DD/MM/AAAA HH:MM:SS` |

### `validacao.py`
| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `validar_classificacao(cor)` | `cor: str` | `bool` | Verifica se `cor` é uma das 5 cores do Protocolo de Manchester |
| `validar_nome(nome)` | `nome: str` | `bool` | Verifica se o nome não é vazio |
| `prioridade_numerica(cor)` | `cor: str` | `int` (1–5) | Converte a cor no peso numérico de prioridade; levanta `ValueError` se inválida |

### `parametros_demo.py`
| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `reclassificar_paciente(paciente, nova_cor)` | `paciente: Paciente`, `nova_cor: str` | `Paciente` | Altera a classificação diretamente no objeto (efeito por referência) |
| `tentar_alterar_string(classificacao)` | `classificacao: str` | `str` | Demonstra que a string original não é afetada (efeito por valor) |
| `trocar_valores(a, b)` | `a, b` | `tuple` | Swap clássico, retornado como tupla |

### `recursao_demo.py`
| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `fatorial(n)` | `n: int` | `int` | Fatorial recursivo; `ValueError` se `n < 0` |
| `fibonacci(n)` | `n: int` | `int` | N-ésimo termo de Fibonacci, recursivo |
| `busca_binaria_recursiva(lista, id, inicio, fim)` | lista ordenada de `Paciente`, `id: int` | `int` (índice ou -1) | Busca recursiva O(log n) |

## 2. Passagem de parâmetros em Python: por valor x por referência

Python não possui a dicotomia explícita "por valor / por referência" (com
`&`/`*`) que existe em C ou C++. O comportamento observado depende da
**mutabilidade do objeto**:

- **Objetos mutáveis** (instâncias de classes, listas, dicionários): a
  função recebe uma referência ao **mesmo objeto** na memória. Alterar um
  atributo dentro da função (`paciente.classificacao = nova_cor`) altera o
  objeto original, visível fora da função — comportamento equivalente a
  passagem por referência em C (`Paciente *paciente`).
- **Objetos imutáveis** (`int`, `float`, `str`, `tuple`): qualquer
  "alteração" dentro da função na verdade cria um **novo objeto local**,
  desvinculado da variável do chamador — comportamento equivalente a
  passagem por valor em C.

Isso foi demonstrado experimentalmente em `test_modulo1.py`:
`reclassificar_paciente` altera o paciente original, enquanto
`tentar_alterar_string` não altera a variável `cor` fora da função.

## 3. Nota sobre o Protocolo de Manchester (base do Módulo 5)

As 5 classificações que serão usadas na fila de prioridade hospitalar,
já centralizadas em `validacao.py`:

| Cor | Nome | Prioridade | Tempo máx. de espera |
|---|---|---|---|
| Vermelho | Emergência | 1 (mais urgente) | 0 min (imediato) |
| Laranja | Muito Urgente | 2 | 10 min |
| Amarelo | Urgente | 3 | 60 min |
| Verde | Pouco Urgente | 4 | 120 min |
| Azul | Não Urgente | 5 (menos urgente) | 240 min |

Essa tabela será a base direta da fila de prioridade implementada no
Módulo 5 — cada paciente será enfileirado com peso igual à coluna
"Prioridade", e o "Tempo máx. de espera" poderá alimentar, em versões
futuras do projeto, uma política de reavaliação (fora do escopo
obrigatório deste trabalho).

## 4. Observações sobre a linguagem escolhida (Python)

Conforme a tabela de observações do roteiro da disciplina, Python não
possui tipagem/alocação manual de memória. Isso impacta principalmente o
Módulo 2 (alocação estática x dinâmica), onde não existe `malloc`/`free`
explícitos — a "alocação estática" será simulada por uma estrutura de
capacidade fixa (lista pré-dimensionada), e a "alocação dinâmica" por uma
estrutura ligada por nós (sem limite de capacidade), com a gestão de
memória delegada ao *garbage collector* do Python. Essa adaptação será
detalhada no relatório do Módulo 2.

## 5. Estrutura planejada para os próximos módulos

- **Módulo 2:** TAD `FichaTriagem` (versões estática e dinâmica).
- **Módulo 3:** TAD Lista (pacientes aguardando triagem).
- **Módulo 4:** TAD Pilha (histórico de reclassificações — undo/redo).
- **Módulo 5:** TAD Fila de Prioridade (coração do sistema: atendimento
  por classificação de Manchester).
- **Módulo 6:** Integração completa — Sistema de Triagem de Pronto-Socorro.
