"""
lista_encadeada_simples.py
Semana 8 - Lista encadeada simples (nos com um unico ponteiro 'proximo').
"""


class _No:
    __slots__ = ("item", "proximo")

    def __init__(self, item):
        self.item = item
        self.proximo = None


class ListaEncadeadaSimples:
    """TAD Lista - implementacao com encadeamento simples."""

    def __init__(self):
        self._inicio = None
        self._fim = None
        self._tamanho = 0

    def inserir(self, item, posicao=None):
        """
        posicao=None ou posicao==tamanho -> insere no final: O(1), pois
        mantemos um ponteiro para o ultimo no (_fim).
        Qualquer outra posicao -> O(n), pois e preciso percorrer os nos.
        """
        novo_no = _No(item)

        if posicao is None:
            posicao = self._tamanho

        if posicao < 0 or posicao > self._tamanho:
            raise IndexError("Posicao invalida")

        if posicao == 0:
            novo_no.proximo = self._inicio
            self._inicio = novo_no
            if self._tamanho == 0:
                self._fim = novo_no
        elif posicao == self._tamanho:
            if self._fim is not None:
                self._fim.proximo = novo_no
            self._fim = novo_no
            if self._inicio is None:
                self._inicio = novo_no
        else:
            atual = self._inicio
            for _ in range(posicao - 1):
                atual = atual.proximo
            novo_no.proximo = atual.proximo
            atual.proximo = novo_no

        self._tamanho += 1

    def remover(self, posicao):
        """O(n): mesmo removendo do inicio (O(1)), o caso geral exige percurso."""
        if posicao < 0 or posicao >= self._tamanho:
            raise IndexError("Posicao invalida")

        if posicao == 0:
            no_removido = self._inicio
            self._inicio = self._inicio.proximo
            if self._inicio is None:
                self._fim = None
        else:
            anterior = self._inicio
            for _ in range(posicao - 1):
                anterior = anterior.proximo
            no_removido = anterior.proximo
            anterior.proximo = no_removido.proximo
            if no_removido is self._fim:
                self._fim = anterior

        self._tamanho -= 1
        return no_removido.item

    def buscar(self, item, chave=lambda x: x):
        """O(n): busca linear percorrendo os ponteiros."""
        atual = self._inicio
        posicao = 0
        while atual is not None:
            if chave(atual.item) == chave(item):
                return posicao
            atual = atual.proximo
            posicao += 1
        return -1

    def percorrer(self):
        """O(n): percorre do inicio ao fim seguindo os ponteiros 'proximo'."""
        resultado = []
        atual = self._inicio
        while atual is not None:
            resultado.append(atual.item)
            atual = atual.proximo
        return resultado

    def tamanho(self):
        return self._tamanho

    def esta_vazia(self):
        return self._tamanho == 0
