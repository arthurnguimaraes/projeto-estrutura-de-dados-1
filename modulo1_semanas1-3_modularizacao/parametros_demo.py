"""
parametros_demo.py
Semana 2 - Passagem de parametros por valor e por referencia.

Em Python nao existe a distincao explicita "por valor / por referencia"
como em C ou C++ (com & e *). O que existe e:
  - Objetos MUTAVEIS (listas, dicionarios, instancias de classes) se
    comportam como passagem por referencia: a funcao recebe uma
    referencia ao MESMO objeto, e alteracoes nos seus atributos
    persistem fora da funcao.
  - Objetos IMUTAVEIS (int, float, str, tuple) se comportam, na
    pratica, como passagem por valor: qualquer "alteracao" dentro da
    funcao na verdade cria um novo objeto local, e o valor original
    fora da funcao nao muda.

Este modulo demonstra essa diferenca usando o TAD Paciente.
"""

from paciente import Paciente


def reclassificar_paciente(paciente, nova_cor):
    """
    Simula passagem "por referencia": Paciente e um objeto mutavel,
    entao a alteracao do atributo 'classificacao' PERSISTE fora da
    funcao, pois estamos alterando o mesmo objeto na memoria.
    """
    paciente.classificacao = nova_cor
    return paciente


def tentar_alterar_string(classificacao):
    """
    Simula passagem "por valor": strings sao imutaveis em Python.
    Reatribuir 'classificacao' dentro da funcao cria uma nova string
    LOCAL; a variavel original do chamador nao e afetada.
    """
    classificacao = "alterado_localmente"
    return classificacao


def trocar_valores(a, b):
    """
    Equivalente a um 'swap' classico. Como inteiros sao imutaveis,
    a troca so e visivel atraves do retorno (tupla), nao por efeito
    colateral nos parametros originais.
    """
    return b, a


if __name__ == "__main__":
    # Demonstracao rapida em execucao direta do arquivo.
    p = Paciente(1, "Joao Silva", "verde", "25/08/2026 10:00:00")
    print("Antes:", p)
    reclassificar_paciente(p, "laranja")
    print("Depois (mudou, pois Paciente e mutavel):", p)

    cor_original = "verde"
    tentar_alterar_string(cor_original)
    print("cor_original continua:", cor_original, "(nao mudou, str e imutavel)")

    x, y = 10, 20
    x, y = trocar_valores(x, y)
    print("Apos troca:", x, y)
