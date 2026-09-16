"""
test_final.py
Testes do Projeto Final: validam a INTEGRACAO entre fila de
prioridade, historico (lista encadeada) e undo/redo (pilha).
"""

from sistema_triagem import SistemaTriagem

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


def testar_fluxo_completo():
    s = SistemaTriagem()

    ana = s.cadastrar_paciente("Ana", "verde")
    bruno = s.cadastrar_paciente("Bruno", "amarelo")
    carla = s.cadastrar_paciente("Carla", "azul")

    checar("3 pacientes aguardando apos cadastro", s.pacientes_aguardando(), 3)

    checar("atendimento sem reclassificacao segue prioridade (Bruno=amarelo primeiro)",
           s.atender_proximo().nome, "Bruno")

    checar("historico tem 1 paciente apos 1o atendimento", len(s.historico()), 1)
    checar("Ana (verde) e a proxima, antes de Carla (azul)",
           s.atender_proximo().nome, "Ana")
    checar("Carla e a ultima", s.atender_proximo().nome, "Carla")
    checar("fila vazia ao final", s.pacientes_aguardando(), 0)
    checar("historico completo com 3 pacientes", len(s.historico()), 3)


def testar_reclassificacao_integrada():
    s = SistemaTriagem()
    ana = s.cadastrar_paciente("Ana", "azul")       # pouco urgente
    bruno = s.cadastrar_paciente("Bruno", "verde")   # pouco urgente tambem

    # Emergencia descoberta: Ana na verdade e um caso vermelho.
    s.reclassificar_paciente(ana.id, "vermelho")
    checar("apos reclassificar, Ana e atendida primeiro (era a ultima)",
           s.atender_proximo().nome, "Ana")

    checar("Bruno continua na fila normalmente", s.atender_proximo().nome, "Bruno")


def testar_desfazer_reclassificacao_integrada():
    s = SistemaTriagem()
    carla = s.cadastrar_paciente("Carla", "verde")
    diego = s.cadastrar_paciente("Diego", "amarelo")

    s.reclassificar_paciente(carla.id, "vermelho")
    checar("apos reclassificar Carla para vermelho, ela e a proxima",
           s.posicao_na_fila(carla.id), 0)

    s.desfazer_reclassificacao(carla.id)
    checar("apos desfazer, Carla volta a ser verde (Diego, amarelo, vai primeiro)",
           s.atender_proximo().nome, "Diego")
    checar("Carla (verde novamente) e atendida por ultimo",
           s.atender_proximo().nome, "Carla")


def testar_busca_no_historico():
    s = SistemaTriagem()
    p1 = s.cadastrar_paciente("Eva", "amarelo")
    s.atender_proximo()
    encontrado = s.buscar_no_historico(p1.id)
    checar("busca no historico encontra paciente atendido", encontrado.nome, "Eva")
    checar("busca no historico nao encontra paciente inexistente",
           s.buscar_no_historico(9999), None)


def testar_sistema_vazio():
    s = SistemaTriagem()
    checar("atender_proximo em sistema vazio retorna None", s.atender_proximo(), None)
    checar("posicao na fila em sistema vazio retorna -1", s.posicao_na_fila(1), -1)


if __name__ == "__main__":
    testar_fluxo_completo()
    testar_reclassificacao_integrada()
    testar_desfazer_reclassificacao_integrada()
    testar_busca_no_historico()
    testar_sistema_vazio()

    print(f"\nResumo: {testes_ok} passaram, {testes_falha} falharam.")
    if testes_falha > 0:
        raise SystemExit(1)
