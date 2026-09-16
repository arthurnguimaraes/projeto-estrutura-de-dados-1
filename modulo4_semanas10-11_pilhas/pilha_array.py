"""
pilha_array.py
Semana 10 - Pilha (LIFO) implementada com array (lista Python).
"""


class PilhaArray:
    """TAD Pilha - implementacao com array. LIFO: Last In, First Out."""

    def __init__(self):
        self._dados = []

    def empilhar(self, item):
        """Insere no topo. Complexidade: O(1) amortizado."""
        self._dados.append(item)

    def desempilhar(self):
        """Remove e retorna o item do topo. Complexidade: O(1)."""
        if self.esta_vazia():
            raise IndexError("Pilha vazia: nao e possivel desempilhar")
        return self._dados.pop()

    def topo(self):
        """Retorna (sem remover) o item do topo. Complexidade: O(1)."""
        if self.esta_vazia():
            raise IndexError("Pilha vazia: nao ha topo")
        return self._dados[-1]

    def esta_vazia(self):
        return len(self._dados) == 0

    def tamanho(self):
        return len(self._dados)
