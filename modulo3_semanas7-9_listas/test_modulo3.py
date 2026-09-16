"""
test_modulo3.py
Testes do Entregavel 3: TAD Lista completo (array, encadeada simples,
duplamente encadeada e circular), com verificacao de insercao,
remocao, busca e percurso.
"""

from paciente import Paciente
from lista_array import ListaArray
from lista_encadeada_simples import ListaEncadeadaSimples
from lista_dupla_circular import ListaDuplamenteEncadeada

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


def ids(lista_de_pacientes):
    return [p.id for p in lista_de_pacientes]


def testar_lista_array():
    l = ListaArray()
    checar("lista array comeca vazia", l.esta_vazia(), True)
    l.inserir(Paciente(1, "A", "verde", "x"))
    l.inserir(Paciente(2, "B", "azul", "x"))
    l.inserir(Paciente(3, "C", "amarelo", "x"), posicao=1)
    checar("insercao em posicao especifica (array)", ids(l.percorrer()), [1, 3, 2])
    checar("busca por chave (array)", l.buscar(Paciente(2, "", "", ""), chave=lambda p: p.id), 2)
    checar("busca inexistente (array)", l.buscar(Paciente(99, "", "", ""), chave=lambda p: p.id), -1)
    removido = l.remover(0)
    checar("remocao retorna o item certo (array)", removido.id, 1)
    checar("tamanho apos remocao (array)", l.tamanho(), 2)


def testar_lista_encadeada_simples():
    l = ListaEncadeadaSimples()
    checar("lista encadeada comeca vazia", l.esta_vazia(), True)
    l.inserir(Paciente(1, "A", "verde", "x"))
    l.inserir(Paciente(2, "B", "azul", "x"))
    l.inserir(Paciente(3, "C", "amarelo", "x"), posicao=1)
    checar("insercao em posicao especifica (encadeada)", ids(l.percorrer()), [1, 3, 2])
    checar("busca por chave (encadeada)", l.buscar(Paciente(3, "", "", ""), chave=lambda p: p.id), 1)
    removido = l.remover(0)
    checar("remocao do inicio (encadeada)", removido.id, 1)
    checar("percurso apos remocao (encadeada)", ids(l.percorrer()), [3, 2])
    checar("tamanho apos remocao (encadeada)", l.tamanho(), 2)


def testar_lista_dupla():
    l = ListaDuplamenteEncadeada(circular=False)
    for i in [1, 2, 3]:
        l.inserir(Paciente(i, f"P{i}", "verde", "x"))
    checar("percurso frente->tras (dupla)", ids(l.percorrer()), [1, 2, 3])
    checar("percurso tras->frente (dupla)", ids(l.percorrer(a_partir_do_fim=True)), [3, 2, 1])
    l.remover(1)
    checar("apos remover elemento do meio (dupla)", ids(l.percorrer()), [1, 3])


def testar_lista_circular():
    l = ListaDuplamenteEncadeada(circular=True)
    for i in [10, 20, 30]:
        l.inserir(Paciente(i, f"P{i}", "verde", "x"))
    checar("percurso circular tem tamanho fixo (nao trava)", ids(l.percorrer()), [10, 20, 30])
    checar("ultimo no aponta de volta para o primeiro", l._fim.proximo is l._inicio, True)
    checar("primeiro no aponta de volta para o ultimo", l._inicio.anterior is l._fim, True)


if __name__ == "__main__":
    testar_lista_array()
    testar_lista_encadeada_simples()
    testar_lista_dupla()
    testar_lista_circular()
    print(f"\nResumo: {testes_ok} passaram, {testes_falha} falharam.")
    if testes_falha > 0:
        raise SystemExit(1)
