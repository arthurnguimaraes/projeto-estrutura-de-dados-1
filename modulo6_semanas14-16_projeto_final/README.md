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
| `interface_cli.py` | Menu interativo de linha de comando (texto) |
| `interface_grafica.py` | Interface gráfica (janela, Tkinter) — ver seção abaixo |
| `interface_web_prototipo.html` | Protótipo de front-end web (HTML/CSS/JS), espelha a mesma lógica |
| `test_final.py` | 28 testes de integração |
| `relatorio.md` | Relatório técnico final |
| `apresentacao_roteiro.md` | Roteiro para a apresentação (10–15 min) |
| `paciente.py`, `validacao.py`, `utils.py` | Base (Módulo 1) |
| `pilha_array.py`, `undo_redo_classificacao.py` | Base (Módulo 4) |
| `fila_prioridade.py`, `fila_encadeada.py` | Base (Módulo 5) |
| `lista_encadeada_simples.py` | Base (Módulo 3) |

## Como executar

```bash
# Rodar o sistema com JANELA (Tkinter) - programa executavel com tela
python3 interface_grafica.py

# Rodar o sistema interativo por menu (texto, no terminal)
python3 interface_cli.py

# Rodar os testes de integração
python3 test_final.py
```

### Sobre `interface_grafica.py`

Programa executável com interface gráfica de verdade (janela, não
terminal), construído com **Tkinter** (biblioteca padrão do Python —
nenhuma dependência externa). Ele **não duplica nenhuma regra de
negócio**: chama diretamente os métodos públicos de `SistemaTriagem`
(o mesmo `sistema_triagem.py` usado por `interface_cli.py` e pelos
testes) e só desenha o resultado na tela. A janela mostra a fila de
espera agrupada por cor, permite cadastrar/atender pacientes, e
expõe undo **e redo** de reclassificação (usando a pilha dupla de
`undo_redo_classificacao.py` — o `interface_cli.py` só expõe o undo).

Requisitos: apenas Python 3 com Tkinter. Na maioria dos sistemas
(Windows, macOS, e a maior parte das distros Linux) já vem incluído.
Se aparecer `ModuleNotFoundError: No module named 'tkinter'` em
alguma distro Linux, instale o pacote do sistema operacional:

```bash
sudo apt install python3-tk        # Debian/Ubuntu
sudo dnf install python3-tkinter   # Fedora
```

Há também um protótipo de front-end **web** (`interface_web_prototipo.html`,
HTML/CSS/JS puro, sem instalação — basta abrir no navegador), que
espelha a mesma lógica de fila/histórico/undo em JavaScript, para
quem quiser uma demonstração rápida sem precisar rodar Python.

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
