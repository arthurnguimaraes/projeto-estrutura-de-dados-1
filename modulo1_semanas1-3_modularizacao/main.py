"""
main.py
Ponto de entrada do Entregavel 1 (Modulo 1 - Semanas 1 a 3).
Demonstra a biblioteca de funcoes utilitarias funcionando de forma
integrada: geracao de ID, validacao, passagem de parametros e
recursividade.
"""

from paciente import Paciente
from utils import gerar_id_paciente, formatar_hora_chegada
from validacao import validar_classificacao, validar_nome, prioridade_numerica
from parametros_demo import reclassificar_paciente
from recursao_demo import busca_binaria_recursiva


def cadastrar_paciente(nome, classificacao):
    """Cria um novo Paciente validando nome e classificacao antes."""
    if not validar_nome(nome):
        raise ValueError("Nome invalido")
    if not validar_classificacao(classificacao):
        raise ValueError(f"Classificacao invalida: {classificacao!r}")

    novo_id = gerar_id_paciente()
    hora = formatar_hora_chegada()
    return Paciente(novo_id, nome, classificacao.lower(), hora)


def main():
    print("=== Sistema de Triagem - Entregavel 1 (Modulo 1) ===\n")

    pacientes = [
        cadastrar_paciente("Ana Souza", "verde"),
        cadastrar_paciente("Bruno Lima", "amarelo"),
        cadastrar_paciente("Carla Dias", "vermelho"),
    ]

    for p in pacientes:
        print(p, "- prioridade numerica:", prioridade_numerica(p.classificacao))

    print("\nReclassificando paciente 1 para 'laranja' (por referencia):")
    reclassificar_paciente(pacientes[0], "laranja")
    print(pacientes[0])

    print("\nBuscando paciente de id=2 com busca binaria recursiva:")
    idx = busca_binaria_recursiva(pacientes, 2)
    print("Encontrado no indice:", idx, "->", pacientes[idx] if idx != -1 else None)


if __name__ == "__main__":
    main()
