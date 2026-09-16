"""
interface_cli.py
Modulo 6 - Interface de linha de comando (menu) para o Sistema de
Triagem de Pronto-Socorro. Ponto de entrada para uso interativo
(demonstracao na apresentacao final).
"""

from sistema_triagem import SistemaTriagem
from validacao import CLASSIFICACOES


def exibir_menu():
    print("\n===== SISTEMA DE TRIAGEM - PRONTO-SOCORRO =====")
    print("1. Cadastrar novo paciente (triagem)")
    print("2. Atender proximo paciente")
    print("3. Ver fila de espera (quantidade por cor)")
    print("4. Consultar posicao de um paciente na fila")
    print("5. Reclassificar paciente (corrigir triagem)")
    print("6. Desfazer ultima reclassificacao de um paciente")
    print("7. Ver historico de atendimentos")
    print("0. Sair")


def solicitar_classificacao():
    print("Classificacoes disponiveis:", ", ".join(CLASSIFICACOES.keys()))
    return input("Classificacao: ").strip().lower()


def main():
    sistema = SistemaTriagem()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opcao: ").strip()

        try:
            if opcao == "1":
                nome = input("Nome do paciente: ").strip()
                cor = solicitar_classificacao()
                paciente = sistema.cadastrar_paciente(nome, cor)
                print(f"Paciente cadastrado: {paciente}")

            elif opcao == "2":
                paciente = sistema.atender_proximo()
                if paciente is None:
                    print("Nao ha pacientes aguardando.")
                else:
                    print(f"Atendendo agora: {paciente}")

            elif opcao == "3":
                print("Pacientes aguardando por cor:", sistema.pacientes_por_cor())
                print("Total aguardando:", sistema.pacientes_aguardando())

            elif opcao == "4":
                id_paciente = int(input("ID do paciente: ").strip())
                posicao = sistema.posicao_na_fila(id_paciente)
                if posicao == -1:
                    print("Paciente nao encontrado na fila de espera.")
                else:
                    print(f"Posicao estimada na fila: {posicao}")

            elif opcao == "5":
                id_paciente = int(input("ID do paciente: ").strip())
                nova_cor = solicitar_classificacao()
                sistema.reclassificar_paciente(id_paciente, nova_cor)
                print("Reclassificacao aplicada com sucesso.")

            elif opcao == "6":
                id_paciente = int(input("ID do paciente: ").strip())
                sistema.desfazer_reclassificacao(id_paciente)
                print("Ultima reclassificacao desfeita.")

            elif opcao == "7":
                historico = sistema.historico()
                if not historico:
                    print("Nenhum paciente atendido ainda.")
                for p in historico:
                    print(f"  {p}")

            elif opcao == "0":
                print("Encerrando o sistema.")
                break

            else:
                print("Opcao invalida.")

        except (ValueError, KeyError, IndexError) as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
