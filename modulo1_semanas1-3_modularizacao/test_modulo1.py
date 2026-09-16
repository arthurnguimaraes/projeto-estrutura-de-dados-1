"""
test_modulo1.py
Casos de teste do Entregavel 1, exigidos pelas normas gerais de
entrega do roteiro (item 3: "Testes com casos de entrada e saida
esperada"). Nao depende de bibliotecas externas (sem pytest) -
basta rodar:  python3 test_modulo1.py
"""

from paciente import Paciente
from utils import gerar_id_paciente, resetar_contador_id, formatar_hora_chegada
from validacao import validar_classificacao, validar_nome, prioridade_numerica
from parametros_demo import reclassificar_paciente, tentar_alterar_string, trocar_valores
from recursao_demo import fatorial, fibonacci, busca_binaria_recursiva

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


def testar_utils():
    resetar_contador_id()
    checar("primeiro id gerado deve ser 1", gerar_id_paciente(), 1)
    checar("segundo id gerado deve ser 2", gerar_id_paciente(), 2)
    checar("terceiro id gerado deve ser 3", gerar_id_paciente(), 3)

    from datetime import datetime
    momento = datetime(2026, 8, 25, 14, 30, 0)
    checar("formatacao de data/hora fixa",
           formatar_hora_chegada(momento), "25/08/2026 14:30:00")


def testar_validacao():
    checar("vermelho e uma classificacao valida", validar_classificacao("vermelho"), True)
    checar("VERMELHO (maiusculo) tambem e valido", validar_classificacao("VERMELHO"), True)
    checar("roxo NAO e uma classificacao valida", validar_classificacao("roxo"), False)
    checar("numero nao e uma classificacao valida", validar_classificacao(123), False)

    checar("nome nao vazio e valido", validar_nome("Joao"), True)
    checar("nome vazio e invalido", validar_nome("   "), False)

    checar("prioridade numerica de vermelho", prioridade_numerica("vermelho"), 1)
    checar("prioridade numerica de azul", prioridade_numerica("azul"), 5)


def testar_parametros():
    p = Paciente(1, "Teste", "verde", "10:00:00")
    reclassificar_paciente(p, "laranja")
    checar("reclassificar_paciente altera o objeto (mutavel)",
           p.classificacao, "laranja")

    cor = "verde"
    tentar_alterar_string(cor)
    checar("string original nao muda fora da funcao (imutavel)", cor, "verde")

    checar("troca de valores (swap)", trocar_valores(1, 2), (2, 1))


def testar_recursao():
    checar("fatorial de 0", fatorial(0), 1)
    checar("fatorial de 5", fatorial(5), 120)
    checar("fibonacci de 0", fibonacci(0), 0)
    checar("fibonacci de 10", fibonacci(10), 55)

    pacientes = [Paciente(i, f"P{i}", "verde", "10:00:00") for i in [1, 3, 7, 9, 12]]
    checar("busca binaria encontra id=7", busca_binaria_recursiva(pacientes, 7), 2)
    checar("busca binaria encontra id=1 (primeiro)", busca_binaria_recursiva(pacientes, 1), 0)
    checar("busca binaria encontra id=12 (ultimo)", busca_binaria_recursiva(pacientes, 12), 4)
    checar("busca binaria nao encontra id=99", busca_binaria_recursiva(pacientes, 99), -1)


def testar_erros_esperados():
    try:
        fatorial(-1)
        checar("fatorial(-1) deveria levantar ValueError", False, True)
    except ValueError:
        checar("fatorial(-1) levanta ValueError corretamente", True, True)

    try:
        prioridade_numerica("cor_invalida")
        checar("prioridade_numerica invalida deveria levantar ValueError", False, True)
    except ValueError:
        checar("prioridade_numerica invalida levanta ValueError corretamente", True, True)


if __name__ == "__main__":
    testar_utils()
    testar_validacao()
    testar_parametros()
    testar_recursao()
    testar_erros_esperados()

    print(f"\nResumo: {testes_ok} passaram, {testes_falha} falharam.")
    if testes_falha > 0:
        raise SystemExit(1)
