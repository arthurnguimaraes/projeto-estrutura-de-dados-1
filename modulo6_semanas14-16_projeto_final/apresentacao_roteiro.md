# Roteiro de Apresentação (10–15 min)
**Sistema de Triagem de Pronto-Socorro**

## Sugestão de tempo por seção

1. **Problema real (1–2 min)** — todo pronto-socorro precisa decidir
   quem atender primeiro; ordem de chegada sozinha não é justa quando
   há casos graves.

2. **Estruturas usadas e por quê (3–4 min)**
   - Fila de prioridade (Manchester) → decide quem é atendido primeiro
   - Lista encadeada → histórico de atendimentos
   - Pilha (undo/redo) → corrigir erro de classificação

3. **Demonstração ao vivo (5–6 min)** — rodar `interface_cli.py`:
   - Cadastrar 4–5 pacientes com cores variadas
   - Mostrar a fila por cor (opção 3)
   - Atender alguns pacientes, mostrando que gravidade vence ordem de chegada
   - Reclassificar um paciente e mostrar que ele muda de posição
   - Desfazer a reclassificação
   - Mostrar o histórico final

4. **Análise de complexidade (2 min)** — tabela do relatório: por que
   cada estrutura escolhida é O(1)/O(k) nas operações mais frequentes.

5. **Limitações e trabalhos futuros (1 min)** — sem reavaliação
   automática por tempo, sem persistência em disco.

## Perguntas que a banca pode fazer (para se preparar)

- "Por que não usar um heap binário para a fila de prioridade?"
  → Resposta no relatório do Módulo 5, seção 3.
- "O que acontece se dois pacientes tiverem a mesma cor?"
  → FIFO dentro da mesma cor, demonstrado na simulação.
- "Como você evita que um paciente 'verde' espere para sempre?"
  → Discussão de anti-starvation no relatório do Módulo 5, seção 4
  (assumido como trabalho futuro, com justificativa).
