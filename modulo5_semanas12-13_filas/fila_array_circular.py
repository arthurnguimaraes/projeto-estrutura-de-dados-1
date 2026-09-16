"""
fila_array_circular.py
Semana 12 - Fila (FIFO) implementada com ARRAY CIRCULAR de capacidade
fixa. O array circular evita o custo O(n) de deslocar elementos a cada
'desenfileirar', reaproveitando os espacos liberados no inicio do
array atraves de aritmetica modular sobre os indices.
"""


class FilaArrayCircular:
    """TAD Fila - implementacao com array circular. FIFO: First In, First Out."""

    def __init__(self, capacidade):
        if capacidade <= 0:
            raise ValueError("Capacidade deve ser positiva")
        self._capacidade = capacidade
        self._dados = [None] * capacidade
        self._inicio = 0     # indice do primeiro elemento (frente da fila)
        self._quantidade = 0

    def enfileirar(self, item):
        """Complexidade: O(1). Insere na posicao logo apos o ultimo elemento."""
        if self.esta_cheia():
            raise OverflowError("Fila cheia: capacidade atingida")
        posicao_insercao = (self._inicio + self._quantidade) % self._capacidade
        self._dados[posicao_insercao] = item
        self._quantidade += 1

    def desenfileirar(self):
        """Complexidade: O(1). Remove e retorna o item da frente da fila."""
        if self.esta_vazia():
            raise IndexError("Fila vazia: nao e possivel desenfileirar")
        item = self._dados[self._inicio]
        self._dados[self._inicio] = None
        self._inicio = (self._inicio + 1) % self._capacidade
        self._quantidade -= 1
        return item

    def frente(self):
        """Complexidade: O(1)."""
        if self.esta_vazia():
            raise IndexError("Fila vazia: nao ha frente")
        return self._dados[self._inicio]

    def esta_vazia(self):
        return self._quantidade == 0

    def esta_cheia(self):
        return self._quantidade == self._capacidade

    def tamanho(self):
        return self._quantidade
