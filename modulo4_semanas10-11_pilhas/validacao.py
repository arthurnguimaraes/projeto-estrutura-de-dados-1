"""
validacao.py
Modulo responsavel pela validacao de dados de entrada do sistema.
Semana 1: exemplo de separacao de responsabilidades em modulos
(a validacao nao se mistura com a geracao de IDs nem com a logica
principal do programa).
"""

# As 5 classificacoes do Protocolo de Manchester, que serao usadas
# como base da fila de prioridade a partir do Modulo 5.
CLASSIFICACOES = {
    "vermelho": {"nome": "Emergencia",      "prioridade": 1, "tempo_max_min": 0},
    "laranja":  {"nome": "Muito Urgente",    "prioridade": 2, "tempo_max_min": 10},
    "amarelo":  {"nome": "Urgente",          "prioridade": 3, "tempo_max_min": 60},
    "verde":    {"nome": "Pouco Urgente",    "prioridade": 4, "tempo_max_min": 120},
    "azul":     {"nome": "Nao Urgente",      "prioridade": 5, "tempo_max_min": 240},
}


def validar_classificacao(cor):
    """
    Retorna True se 'cor' for uma das 5 classificacoes validas do
    Protocolo de Manchester (case-insensitive), False caso contrario.
    """
    if not isinstance(cor, str):
        return False
    return cor.strip().lower() in CLASSIFICACOES


def validar_nome(nome):
    """Retorna True se o nome do paciente for uma string nao vazia."""
    return isinstance(nome, str) and len(nome.strip()) > 0


def prioridade_numerica(cor):
    """
    Converte a cor da classificacao no seu peso numerico de prioridade
    (1 = mais urgente, 5 = menos urgente). Levanta ValueError se a cor
    for invalida.
    """
    cor_normalizada = cor.strip().lower()
    if not validar_classificacao(cor_normalizada):
        raise ValueError(f"Classificacao invalida: {cor!r}")
    return CLASSIFICACOES[cor_normalizada]["prioridade"]
