"""
ficha_triagem_estatica.py
Semana 5 - Alocacao ESTATICA de memoria.

Em C, alocacao estatica seria um array de tamanho fixo definido em
tempo de compilacao (ex.: Paciente fichas[100];). Python nao tem essa
nocao em tempo de compilacao, entao simulamos o conceito reservando
uma lista de tamanho FIXO no momento da criacao (capacidade maxima
definida na criacao do repositorio e nunca alterada), preenchida com
None nas posicoes vazias - o mais proximo que se pode chegar do
comportamento de um array estatico dentro de uma linguagem gerenciada.
"""

from paciente import Paciente


class RepositorioFichasEstatico:
    """TAD Ficha de Triagem - implementacao com capacidade fixa (like array estatico)."""

    def __init__(self, capacidade):
        if capacidade <= 0:
            raise ValueError("Capacidade deve ser positiva")
        self._capacidade = capacidade
        # Lista pre-dimensionada, simulando um array estatico de tamanho fixo.
        self._fichas = [None] * capacidade
        self._quantidade = 0

    def esta_cheio(self):
        return self._quantidade >= self._capacidade

    def quantidade(self):
        return self._quantidade

    def inserir_ficha(self, paciente):
        """O(n) no pior caso (procura primeira posicao livre)."""
        if self.esta_cheio():
            return False
        for i in range(self._capacidade):
            if self._fichas[i] is None:
                self._fichas[i] = paciente
                self._quantidade += 1
                return True
        return False

    def remover_ficha(self, id_paciente):
        """O(n): precisa varrer o array procurando o id."""
        for i in range(self._capacidade):
            if self._fichas[i] is not None and self._fichas[i].id == id_paciente:
                self._fichas[i] = None
                self._quantidade -= 1
                return True
        return False

    def buscar_ficha(self, id_paciente):
        """O(n): busca linear, pois o array nao esta ordenado por id."""
        for ficha in self._fichas:
            if ficha is not None and ficha.id == id_paciente:
                return ficha
        return None

    def listar_fichas(self):
        """O(n): retorna apenas as posicoes preenchidas."""
        return [f for f in self._fichas if f is not None]
