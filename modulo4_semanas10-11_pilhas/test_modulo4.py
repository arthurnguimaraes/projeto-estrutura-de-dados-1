"""
test_modulo4.py
Testes do Entregavel 4: TAD Pilha (array e encadeada) + aplicacao
de undo/redo de reclassificacoes de triagem.
"""

from paciente import Paciente
from pilha_array import PilhaArray
from pilha_encadeada import PilhaEncadeada
from undo_redo_classificacao import GerenciadorReclassificacao

testes_ok = 0
testes_falha = 0


def checar(descricao, obtido, esperado):
    global testes_ok, testes_falha
    if obtido == esperado:
        testes_ok += 1
        print(f"[OK]    {descricao}")
    else:
        testes_falha += 1
        print(f"[FALHA] {descricao} -> esperado={esperado!r}, obtido={obtido!r}")


def testar_pilha(Pilha):
    nome = Pilha.__name__
    p = Pilha()
    checar(f"{nome}: comeca vazia", p.esta_vazia(), True)
    p.empilhar(1)
    p.empilhar(2)
    p.empilhar(3)
    checar(f"{nome}: topo apos 3 empilhamentos (LIFO)", p.topo(), 3)
    checar(f"{nome}: tamanho apos 3 empilhamentos", p.tamanho(), 3)
    checar(f"{nome}: desempilha na ordem LIFO", p.desempilhar(), 3)
    checar(f"{nome}: novo topo apos pop", p.topo(), 2)
    p.desempilhar()
    p.desempilhar()
    checar(f"{nome}: vazia apos remover tudo", p.esta_vazia(), True)

    try:
        p.desempilhar()
        checar(f"{nome}: desempilhar vazia deveria falhar", False, True)
    except IndexError:
        checar(f"{nome}: desempilhar vazia levanta IndexError", True, True)


def testar_undo_redo():
    paciente = Paciente(1, "Maria", "verde", "x")
    g = GerenciadorReclassificacao(paciente)

    g.reclassificar("amarelo")
    checar("apos 1a reclassificacao", paciente.classificacao, "amarelo")

    g.reclassificar("laranja")
    checar("apos 2a reclassificacao", paciente.classificacao, "laranja")

    g.desfazer()
    checar("apos 1o undo, volta para amarelo", paciente.classificacao, "amarelo")

    g.desfazer()
    checar("apos 2o undo, volta para verde (original)", paciente.classificacao, "verde")

    checar("nao pode desfazer alem do inicio", g.pode_desfazer(), False)

    g.refazer()
    checar("apos 1o redo, volta para amarelo", paciente.classificacao, "amarelo")

    g.reclassificar("vermelho")
    checar("nova acao descarta redo pendente", g.pode_refazer(), False)


if __name__ == "__main__":
    testar_pilha(PilhaArray)
    testar_pilha(PilhaEncadeada)
    testar_undo_redo()
    print(f"\nResumo: {testes_ok} passaram, {testes_falha} falharam.")
    if testes_falha > 0:
        raise SystemExit(1)
