"""
lista_array.py
Semana 7 - Lista sequencial (baseada em array).
TAD Lista implementado sobre uma lista Python usada como array
dinamico (equivalente conceitual a um vetor redimensionavel, tipo
std::vector em C++ ou ArrayList em Java).
"""


class ListaArray:
    """TAD Lista - implementacao sequencial (array)."""

    def __init__(self):
        self._dados = []

    def inserir(self, item, posicao=None):
        """
        Insere 'item' na posicao dada (ou no final, se omitida).
        Complexidade: O(1) amortizado se no final; O(n) se no meio/inicio
        (pois os elementos seguintes precisam ser deslocados).
        """
        if posicao is None:
            self._dados.append(item)
        else:
            if posicao < 0 or posicao > len(self._dados):
                raise IndexError("Posicao invalida")
            self._dados.insert(posicao, item)

    def remover(self, posicao):
        """
        Remove e retorna o item na posicao dada.
        Complexidade: O(n) - elementos seguintes precisam ser deslocados.
        """
        if posicao < 0 or posicao >= len(self._dados):
            raise IndexError("Posicao invalida")
        return self._dados.pop(posicao)

    def buscar(self, item, chave=lambda x: x):
        """
        Busca linear por 'item' (compara usando 'chave').
        Complexidade: O(n).
        Retorna a posicao encontrada ou -1.
        """
        for i, atual in enumerate(self._dados):
            if chave(atual) == chave(item):
                return i
        return -1

    def percorrer(self):
        """Retorna uma copia da lista de itens, na ordem de armazenamento. O(n)."""
        return list(self._dados)

    def tamanho(self):
        return len(self._dados)

    def esta_vazia(self):
        return len(self._dados) == 0
