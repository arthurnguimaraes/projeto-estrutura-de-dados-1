# Relatório Técnico — Módulo 2: TAD e Memória
**Projeto:** Sistema de Triagem de Pronto-Socorro | **Linguagem:** Python 3

## 1. TAD implementado: Ficha de Triagem

Interface pública (idêntica nas duas versões — ver `tad_ficha_triagem_spec.md`):
`criar_repositorio`, `inserir_ficha`, `remover_ficha`, `buscar_ficha`,
`listar_fichas`, `esta_cheio`, `quantidade`.

O encapsulamento garante que o código cliente (ex.: o futuro
`sistema_triagem.py` do Módulo 6) nunca precise saber se, por trás da
interface, existe um array de tamanho fixo ou uma lista ligada.

## 2. Complexidade das operações

| Operação | Versão Estática (array fixo) | Versão Dinâmica (lista ligada) |
|---|---|---|
| Inserir | O(n) — procura primeira posição livre | O(1) — insere sempre no início |
| Remover por id | O(n) — busca linear na posição | O(n) — busca linear percorrendo nós |
| Buscar por id | O(n) — busca linear | O(n) — busca linear |
| Listar todas | O(n) | O(n) |
| Verificar se está cheio | O(1) | O(1) (sempre `False`) |

## 3. Comparação estática x dinâmica

| Critério | Estática | Dinâmica |
|---|---|---|
| Capacidade máxima | Fixa, definida na criação | Ilimitada (até a memória disponível) |
| Desperdício de memória | Pode reservar espaço não usado (posições `None`) | Aloca exatamente o necessário, nó a nó |
| Overhead por elemento | Nenhum (slot já existe no array) | Um ponteiro extra por nó (`proximo`) |
| Inserção no melhor caso | O(n) para achar slot livre | O(1) sempre |
| Previsibilidade | Alta — sem crescimento inesperado de memória | Cresce dinamicamente conforme a demanda |

**Conclusão:** para um sistema de triagem real, onde o número de pacientes
aguardando é imprevisível e pode variar bastante ao longo do dia, a
versão **dinâmica** é mais adequada — evita desperdiçar memória com uma
capacidade fixa superestimada e evita rejeitar pacientes por falta de
espaço quando a demanda ultrapassa o previsto. A versão estática seria
preferível apenas em cenários com limite físico real e conhecido (ex.:
número fixo de leitos de emergência).

## 4. Diferença em relação a uma implementação em C

Em C, a versão estática corresponderia a `Paciente fichas[N];` (array na
pilha ou de tamanho fixo global), e a versão dinâmica a uma lista ligada
com `malloc(sizeof(No))` a cada inserção e `free(no)` a cada remoção,
com risco de *memory leak* se o `free` for esquecido.

Em Python:
- Não há `malloc`/`free` explícitos — a criação de um objeto (`_No(paciente)`)
  aloca memória automaticamente, e a remoção de todas as referências a um
  nó (ex.: quando `anterior.proximo` passa a apontar para o nó seguinte)
  torna esse nó elegível para coleta pelo **garbage collector**, sem
  intervenção manual.
- Isso elimina a classe de bugs de vazamento de memória por `free`
  esquecido, mas também remove o controle fino que a linguagem C oferece
  sobre o momento exato da liberação de memória.

## 5. Testes realizados

20 casos cobrindo: inserção até a capacidade máxima (estática), rejeição
de inserção quando cheio, inserção sem limite (dinâmica), busca por id
existente/inexistente, remoção e atualização da contagem — ver
`test_modulo2.py`.
