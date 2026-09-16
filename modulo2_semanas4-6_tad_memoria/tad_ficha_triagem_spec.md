# Especificação do TAD "Ficha de Triagem" (Semana 4)

Conforme pedido no roteiro, esta semana apenas **especifica** o TAD,
sem implementá-lo (a implementação vem nas Semanas 5 e 6).

## Interface pública (operações)

| Operação | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `criar_repositorio(capacidade)` | `capacidade: int` | repositório vazio | Cria o repositório de fichas |
| `inserir_ficha(repo, paciente)` | repositório, `Paciente` | `bool` (sucesso) | Insere uma nova ficha de triagem |
| `remover_ficha(repo, id_paciente)` | repositório, `int` | `bool` (sucesso) | Remove a ficha pelo ID |
| `buscar_ficha(repo, id_paciente)` | repositório, `int` | `Paciente \| None` | Busca uma ficha pelo ID |
| `listar_fichas(repo)` | repositório | `list[Paciente]` | Retorna todas as fichas cadastradas |
| `esta_cheio(repo)` | repositório | `bool` | Indica se atingiu a capacidade máxima (relevante na versão estática) |
| `quantidade(repo)` | repositório | `int` | Número de fichas atualmente armazenadas |

## Encapsulamento

A interface acima **não expõe** como as fichas são armazenadas
internamente (array de tamanho fixo ou estrutura ligada por nós) —
esse é exatamente o ponto que será comparado nas Semanas 5 e 6: duas
implementações diferentes por trás da mesma interface pública.
