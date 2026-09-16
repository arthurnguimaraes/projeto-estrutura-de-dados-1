"""
pilha_encadeada.py
Semana 10 - Pilha (LIFO) implementada com lista encadeada.
"""


class _No:
    __slots__ = ("item", "proximo")

    def __init__(self, item):
        self.item = item
        self.proximo = None


class PilhaEncadeada:
    """TAD Pilha - implementacao com nos encadeados. LIFO."""

    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def empilhar(self, item):
        """Complexidade: O(1) - insere sempre como novo topo."""
        novo_no = _No(item)
        novo_no.proximo = self._topo
        self._topo = novo_no
        self._tamanho += 1

    def desempilhar(self):
        """Complexidade: O(1)."""
        if self.esta_vazia():
            raise IndexError("Pilha vazia: nao e possivel desempilhar")
        no_removido = self._topo
        self._topo = no_removido.proximo
        self._tamanho -= 1
        return no_removido.item

    def topo(self):
        """Complexidade: O(1)."""
        if self.esta_vazia():
            raise IndexError("Pilha vazia: nao ha topo")
        return self._topo.item

    def esta_vazia(self):
        return self._tamanho == 0

    def tamanho(self):
        return self._tamanho
