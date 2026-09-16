"""
simulacao_atendimento_hospitalar.py
Semana 13 - Simulacao de atendimento (aplicacao pratica pedida no
roteiro: "Simulacao de atendimento - banco, impressora, escalonamento
de processos", aqui adaptada para pronto-socorro).

Simula a chegada de varios pacientes ao longo do tempo e o atendimento
respeitando a fila de prioridade (Protocolo de Manchester).
"""

from fila_prioridade import FilaPrioridade
from paciente import Paciente
from utils import gerar_id_paciente, resetar_contador_id


def simular_chegada_pacientes(fila, lista_chegadas):
    """
    lista_chegadas: lista de tuplas (nome, classificacao).
    Cada paciente recebe um ID sequencial e e enfileirado na ordem
    dada (simulando a ordem real de chegada ao pronto-socorro).
    """
    pacientes_cadastrados = []
    for nome, classificacao in lista_chegadas:
        paciente = Paciente(gerar_id_paciente(), nome, classificacao, "chegada simulada")
        fila.enfileirar(paciente)
        pacientes_cadastrados.append(paciente)
    return pacientes_cadastrados


def simular_atendimento(fila, historico_atendimentos):
    """
    Atende UM paciente por vez (o de maior prioridade disponivel),
    registrando o atendimento na lista de historico (que sera
    formalizada como TAD Lista/Historico no Modulo 6).
    """
    if fila.esta_vazia():
        return None
    paciente_atendido = fila.desenfileirar()
    historico_atendimentos.append(paciente_atendido)
    return paciente_atendido


def relatorio_simulacao(historico_atendimentos):
    """Imprime um pequeno relatorio da ordem de atendimento realizada."""
    print("=== Relatorio da Simulacao de Atendimento ===")
    for posicao, paciente in enumerate(historico_atendimentos, start=1):
        print(f"{posicao:>2}. {paciente.nome:<10} - {paciente.classificacao}")


if __name__ == "__main__":
    resetar_contador_id()
    fila = FilaPrioridade()
    historico = []

    # Cenario: chegada de 8 pacientes em um horario de pico, em ordem
    # de chegada, com gravidades variadas.
    chegadas = [
        ("Ana",    "verde"),
        ("Bruno",  "amarelo"),
        ("Carla",  "azul"),
        ("Diego",  "laranja"),
        ("Elisa",  "amarelo"),
        ("Fabio",  "vermelho"),   # emergencia chega no meio do fluxo
        ("Gisele", "verde"),
        ("Hugo",   "laranja"),
    ]

    simular_chegada_pacientes(fila, chegadas)

    print("Pacientes aguardando por cor:", fila.tamanho_por_cor())
    print()

    while not fila.esta_vazia():
        atendido = simular_atendimento(fila, historico)
        print(f"Atendendo: {atendido.nome} ({atendido.classificacao})")

    print()
    relatorio_simulacao(historico)
