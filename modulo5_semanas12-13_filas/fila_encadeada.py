"""
fila_encadeada.py
Semana 12 - Fila (FIFO) implementada com lista encadeada (sem limite
de capacidade).
"""


class _No:
    __slots__ = ("item", "proximo")

    def __init__(self, item):
        self.item = item
        self.proximo = None


class FilaEncadeada:
    """TAD Fila - implementacao com nos encadeados. FIFO, sem limite de capacidade."""

    def __init__(self):
        self._inicio = None
        self._fim = None
        self._quantidade = 0

    def enfileirar(self, item):
        """Complexidade: O(1) - insere no fim, com ponteiro _fim mantido."""
        novo_no = _No(item)
        if self.esta_vazia():
            self._inicio = novo_no
        else:
            self._fim.proximo = novo_no
        self._fim = novo_no
        self._quantidade += 1

    def desenfileirar(self):
        """Complexidade: O(1) - remove do inicio."""
        if self.esta_vazia():
            raise IndexError("Fila vazia: nao e possivel desenfileirar")
        no_removido = self._inicio
        self._inicio = no_removido.proximo
        if self._inicio is None:
            self._fim = None
        self._quantidade -= 1
        return no_removido.item

    def frente(self):
        """Complexidade: O(1)."""
        if self.esta_vazia():
            raise IndexError("Fila vazia: nao ha frente")
        return self._inicio.item

    def esta_vazia(self):
        return self._quantidade == 0

    def esta_cheia(self):
        return False  # sem limite de capacidade

    def tamanho(self):
        return self._quantidade

    def percorrer(self):
        """
        Retorna uma lista com os itens da fila, da frente para o fim,
        sem remove-los. Usado, por exemplo, pela FilaPrioridade para
        consultas de posicao. Complexidade: O(n).
        """
        resultado = []
        atual = self._inicio
        while atual is not None:
            resultado.append(atual.item)
            atual = atual.proximo
        return resultado
