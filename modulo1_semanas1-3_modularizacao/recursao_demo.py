"""
recursao_demo.py
Semana 3 - Recursividade como tecnica de modularizacao.

Contem os 3 exercicios pedidos no roteiro (fatorial, Fibonacci e
busca binaria recursiva), com a busca binaria ja adaptada para
buscar um Paciente por ID em uma lista ordenada - uma previa util
do que sera reaproveitado no modulo de historico/prontuario.
"""


def fatorial(n):
    """Calcula n! recursivamente. Levanta ValueError para n negativo."""
    if n < 0:
        raise ValueError("Fatorial nao definido para numeros negativos")
    if n in (0, 1):
        return 1
    return n * fatorial(n - 1)


def fibonacci(n):
    """Retorna o n-esimo termo da sequencia de Fibonacci (0-indexado)."""
    if n < 0:
        raise ValueError("Fibonacci nao definido para indices negativos")
    if n in (0, 1):
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def busca_binaria_recursiva(lista_pacientes_ordenada, id_procurado,
                             inicio=0, fim=None):
    """
    Busca recursiva por um paciente com o ID informado, dentro de uma
    lista de objetos Paciente ORDENADA por id crescente.
    Retorna o indice do paciente encontrado, ou -1 se nao existir.

    Complexidade: O(log n), pois a cada chamada o espaco de busca
    e dividido pela metade.
    """
    if fim is None:
        fim = len(lista_pacientes_ordenada) - 1

    if inicio > fim:
        return -1

    meio = (inicio + fim) // 2
    paciente_meio = lista_pacientes_ordenada[meio]

    if paciente_meio.id == id_procurado:
        return meio
    elif paciente_meio.id < id_procurado:
        return busca_binaria_recursiva(lista_pacientes_ordenada, id_procurado,
                                        meio + 1, fim)
    else:
        return busca_binaria_recursiva(lista_pacientes_ordenada, id_procurado,
                                        inicio, meio - 1)


if __name__ == "__main__":
    print("5! =", fatorial(5))
    print("Fibonacci(10) =", fibonacci(10))

    from paciente import Paciente
    pacientes = [
        Paciente(1, "Ana", "verde", "10:00:00"),
        Paciente(3, "Bruno", "amarelo", "10:05:00"),
        Paciente(7, "Carla", "laranja", "10:10:00"),
        Paciente(9, "Diego", "vermelho", "10:12:00"),
    ]
    print("Busca id=7 ->", busca_binaria_recursiva(pacientes, 7))
    print("Busca id=2 ->", busca_binaria_recursiva(pacientes, 2))
