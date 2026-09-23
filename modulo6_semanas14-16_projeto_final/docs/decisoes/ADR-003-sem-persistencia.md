# ADR-003: Sem persistência em disco ou banco de dados

**Status:** Aceito

## Contexto

O projeto poderia salvar pacientes, fila e histórico em um arquivo ou
banco de dados, para que os dados sobrevivessem ao fechar o programa.
O foco do Módulo 6, porém, é demonstrar o uso combinado de estruturas
de dados (fila de prioridade, lista encadeada, pilha) — não construir
uma camada de persistência.

## Decisão

Todos os dados (fila de espera, histórico, pilhas de undo/redo)
existem apenas em memória, durante a execução do programa. Não há
arquivo, banco de dados nem qualquer forma de salvar/carregar estado
entre execuções.

## Consequências

- Simplifica bastante o escopo do projeto: nenhuma dependência
  externa (nenhum driver de banco, nenhum ORM), o que também mantém a
  promessa do README de "sem dependências externas".
- Os testes (`test_final.py`) não precisam de setup/teardown de banco
  — cada teste cria um `SistemaTriagem` novo em memória.
- Limitação clara: ao fechar o programa (CLI ou janela), todo o estado
  é perdido. Isso é aceitável para o escopo acadêmico do projeto, mas
  seria o primeiro ponto a resolver antes de qualquer uso real em um
  pronto-socorro.
- Caminho natural de evolução, se necessário no futuro: serializar o
  estado (por exemplo em JSON) ao fechar e recarregar ao abrir, sem
  precisar mudar nenhuma das estruturas de dados internas.
