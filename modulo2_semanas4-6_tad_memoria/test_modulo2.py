"""
test_modulo2.py
Testes do Entregavel 2: TAD Ficha de Triagem nas versoes estatica e
dinamica. Compara o comportamento das duas implementacoes por tras
da MESMA interface publica.
"""

from paciente import Paciente
from ficha_triagem_estatica import RepositorioFichasEstatico
from ficha_triagem_dinamica import RepositorioFichasDinamico

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


def testar_estatico():
    repo = RepositorioFichasEstatico(3)
    checar("repo estatico comeca vazio", repo.quantidade(), 0)
    checar("insere paciente 1", repo.inserir_ficha(Paciente(1, "A", "verde", "x")), True)
    checar("insere paciente 2", repo.inserir_ficha(Paciente(2, "B", "azul", "x")), True)
    checar("insere paciente 3", repo.inserir_ficha(Paciente(3, "C", "amarelo", "x")), True)
    checar("repo esta cheio (capacidade=3)", repo.esta_cheio(), True)
    checar("insercao alem da capacidade falha", repo.inserir_ficha(Paciente(4, "D", "verde", "x")), False)
    checar("busca paciente existente", repo.buscar_ficha(2).nome, "B")
    checar("busca paciente inexistente", repo.buscar_ficha(99), None)
    checar("remove paciente existente", repo.remover_ficha(2), True)
    checar("quantidade apos remocao", repo.quantidade(), 2)
    checar("apos remover, nao esta mais cheio", repo.esta_cheio(), False)
    checar("insere novamente apos abrir espaco", repo.inserir_ficha(Paciente(5, "E", "verde", "x")), True)


def testar_dinamico():
    repo = RepositorioFichasDinamico()
    checar("repo dinamico comeca vazio", repo.quantidade(), 0)
    checar("repo dinamico nunca fica cheio", repo.esta_cheio(), False)

    for i in range(1, 11):  # insere 10 - muito mais que a capacidade usada no estatico
        repo.inserir_ficha(Paciente(i, f"P{i}", "verde", "x"))
    checar("insere 10 pacientes sem limite de capacidade", repo.quantidade(), 10)
    checar("continua nao-cheio mesmo com 10 fichas", repo.esta_cheio(), False)

    checar("busca paciente existente", repo.buscar_ficha(7).nome, "P7")
    checar("remove paciente existente", repo.remover_ficha(7), True)
    checar("quantidade apos remocao", repo.quantidade(), 9)
    checar("busca apos remocao retorna None", repo.buscar_ficha(7), None)


if __name__ == "__main__":
    testar_estatico()
    testar_dinamico()
    print(f"\nResumo: {testes_ok} passaram, {testes_falha} falharam.")
    if testes_falha > 0:
        raise SystemExit(1)
