"""
test_modulo5.py
Testes do Entregavel 5: TAD Fila (array circular e encadeada) + Fila
de Prioridade (Manchester) + simulacao de atendimento.
"""

from paciente import Paciente
from fila_array_circular import FilaArrayCircular
from fila_encadeada import FilaEncadeada
from fila_prioridade import FilaPrioridade

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


def testar_fila_array_circular():
    f = FilaArrayCircular(3)
    checar("fila circular comeca vazia", f.esta_vazia(), True)
    f.enfileirar("a")
    f.enfileirar("b")
    f.enfileirar("c")
    checar("fila circular fica cheia com 3 (capacidade=3)", f.esta_cheia(), True)

    try:
        f.enfileirar("d")
        checar("enfileirar alem da capacidade deveria falhar", False, True)
    except OverflowError:
        checar("enfileirar alem da capacidade levanta OverflowError", True, True)

    checar("frente e FIFO (primeiro inserido)", f.frente(), "a")
    checar("desenfileira em ordem FIFO", f.desenfileirar(), "a")
    f.enfileirar("d")  # reaproveita espaco circular liberado
    checar("apos reaproveitar espaco, ainda tem 3 itens", f.tamanho(), 3)
    checar("ordem apos reaproveitar espaco (b, c, d)",
           [f.desenfileirar() for _ in range(3)], ["b", "c", "d"])


def testar_fila_encadeada():
    f = FilaEncadeada()
    checar("fila encadeada comeca vazia", f.esta_vazia(), True)
    checar("fila encadeada nunca fica cheia", f.esta_cheia(), False)
    for x in [1, 2, 3]:
        f.enfileirar(x)
    checar("frente FIFO", f.frente(), 1)
    checar("desenfileira em ordem", [f.desenfileirar() for _ in range(3)], [1, 2, 3])


def testar_fila_prioridade():
    fp = FilaPrioridade()
    checar("fila de prioridade comeca vazia", fp.esta_vazia(), True)

    fp.enfileirar(Paciente(1, "Ana", "verde", "t1"))
    fp.enfileirar(Paciente(2, "Bruno", "amarelo", "t2"))
    fp.enfileirar(Paciente(3, "Carla", "vermelho", "t3"))
    fp.enfileirar(Paciente(4, "Diego", "amarelo", "t4"))

    checar("total de pacientes na fila", fp.tamanho(), 4)
    checar("emergencia (vermelho) e atendida primeiro mesmo chegando por ultimo",
           fp.desenfileirar().nome, "Carla")
    checar("dentro do mesmo nivel (amarelo), respeita FIFO: Bruno antes de Diego",
           fp.desenfileirar().nome, "Bruno")
    checar("Diego (amarelo, chegou depois) vem antes de Ana (verde)",
           fp.desenfileirar().nome, "Diego")
    checar("por ultimo, Ana (verde)", fp.desenfileirar().nome, "Ana")
    checar("fila vazia ao final", fp.esta_vazia(), True)

    try:
        fp.enfileirar(Paciente(5, "Erro", "roxo", "t5"))
        checar("classificacao invalida deveria falhar", False, True)
    except ValueError:
        checar("classificacao invalida levanta ValueError", True, True)


def testar_posicao_estimada():
    fp = FilaPrioridade()
    fp.enfileirar(Paciente(1, "Ana", "verde", "t1"))
    fp.enfileirar(Paciente(2, "Bruno", "amarelo", "t2"))
    fp.enfileirar(Paciente(3, "Carla", "amarelo", "t3"))
    checar("posicao do Bruno (1o amarelo)", fp.posicao_estimada(2), 0)
    checar("posicao da Carla (2o amarelo, apos Bruno)", fp.posicao_estimada(3), 1)
    checar("posicao da Ana (verde, apos os 2 amarelos)", fp.posicao_estimada(1), 2)
    checar("posicao de paciente inexistente", fp.posicao_estimada(99), -1)


if __name__ == "__main__":
    testar_fila_array_circular()
    testar_fila_encadeada()
    testar_fila_prioridade()
    testar_posicao_estimada()
    print(f"\nResumo: {testes_ok} passaram, {testes_falha} falharam.")
    if testes_falha > 0:
        raise SystemExit(1)
