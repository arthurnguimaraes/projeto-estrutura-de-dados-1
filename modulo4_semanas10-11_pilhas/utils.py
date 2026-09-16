"""
utils.py
Funcoes utilitarias gerais do sistema: geracao de IDs e formatacao
de data/hora. Mantidas separadas de validacao.py e de paciente.py
para reforcar a modularizacao pedida na Semana 1.
"""

from datetime import datetime

# Contador interno usado para gerar IDs sequenciais e unicos.
_proximo_id = 1


def gerar_id_paciente():
    """
    Gera um ID sequencial unico para cada novo paciente cadastrado.
    Cada chamada retorna um numero maior que o anterior.
    """
    global _proximo_id
    id_gerado = _proximo_id
    _proximo_id += 1
    return id_gerado


def resetar_contador_id():
    """Reseta o contador de IDs. Usado apenas nos testes automatizados."""
    global _proximo_id
    _proximo_id = 1


def formatar_hora_chegada(momento=None):
    """
    Retorna a data/hora formatada como string 'DD/MM/AAAA HH:MM:SS'.
    Se 'momento' nao for informado, usa o instante atual.
    """
    if momento is None:
        momento = datetime.now()
    return momento.strftime("%d/%m/%Y %H:%M:%S")
