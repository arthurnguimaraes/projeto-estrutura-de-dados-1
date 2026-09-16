"""
lista_dupla_circular.py
Semana 9 - Lista duplamente encadeada e lista circular.

Implementa uma lista duplamente encadeada (nos com 'anterior' e
'proximo') e, na mesma estrutura, oferece o modo circular (o 'proximo'
do ultimo no aponta de volta para o primeiro, e o 'anterior' do
primeiro aponta para o ultimo) - controlado pelo parametro 'circular'
no construtor.
"""


class _NoDuplo:
    __slots__ = ("item", "anterior", "proximo")

    def __init__(self, item):
        self.item = item
        self.anterior = None
        self.proximo = None


class ListaDuplamenteEncadeada:
    """
    TAD Lista - implementacao com encadeamento duplo, com suporte
    opcional a circularidade (percurso infinito util para, por
    exemplo, revezamento de plantoes de atendimento).
    """

    def __init__(self, circular=False):
        self._inicio = None
        self._fim = None
        self._tamanho = 0
        self._circular = circular

    def inserir(self, item, posicao=None):
        """
        Insercao no inicio ou fim: O(1). Em posicao arbitraria: O(n).
        """
        novo_no = _NoDuplo(item)

        if posicao is None:
            posicao = self._tamanho
        if posicao < 0 or posicao > self._tamanho:
            raise IndexError("Posicao invalida")

        if self._tamanho == 0:
            self._inicio = self._fim = novo_no
        elif posicao == 0:
            novo_no.proximo = self._inicio
            self._inicio.anterior = novo_no
            self._inicio = novo_no
        elif posicao == self._tamanho:
            novo_no.anterior = self._fim
            self._fim.proximo = novo_no
            self._fim = novo_no
        else:
            atual = self._no_na_posicao(posicao)
            anterior = atual.anterior
            anterior.proximo = novo_no
            novo_no.anterior = anterior
            novo_no.proximo = atual
            atual.anterior = novo_no

        self._tamanho += 1
        self._ajustar_circularidade()

    def remover(self, posicao):
        """O(n) no caso geral; O(1) se remover do inicio ou fim com no ja localizado."""
        if posicao < 0 or posicao >= self._tamanho:
            raise IndexError("Posicao invalida")

        no_removido = self._no_na_posicao(posicao)

        if no_removido.anterior is not None and not self._eh_extremidade(no_removido, "anterior"):
            no_removido.anterior.proximo = no_removido.proximo
        elif no_removido is self._inicio:
            self._inicio = no_removido.proximo if self._tamanho > 1 else None

        if no_removido.proximo is not None and not self._eh_extremidade(no_removido, "proximo"):
            no_removido.proximo.anterior = no_removido.anterior
        elif no_removido is self._fim:
            self._fim = no_removido.anterior if self._tamanho > 1 else None

        self._tamanho -= 1
        self._ajustar_circularidade()
        return no_removido.item

    def _eh_extremidade(self, no, lado):
        # Auxilia a nao "vazar" o laco circular ao remover extremidades.
        if lado == "anterior":
            return no is self._inicio
        return no is self._fim

    def _no_na_posicao(self, posicao):
        atual = self._inicio
        for _ in range(posicao):
            atual = atual.proximo
        return atual

    def _ajustar_circularidade(self):
        if self._tamanho == 0:
            return
        if self._circular:
            self._fim.proximo = self._inicio
            self._inicio.anterior = self._fim
        else:
            self._fim.proximo = None
            self._inicio.anterior = None

    def percorrer(self, a_partir_do_fim=False):
        """
        Percorre a lista. Se circular, percorre exatamente 'tamanho'
        elementos (evitando loop infinito).
        """
        resultado = []
        if self._tamanho == 0:
            return resultado

        if not a_partir_do_fim:
            atual = self._inicio
            for _ in range(self._tamanho):
                resultado.append(atual.item)
                atual = atual.proximo
        else:
            atual = self._fim
            for _ in range(self._tamanho):
                resultado.append(atual.item)
                atual = atual.anterior

        return resultado

    def tamanho(self):
        return self._tamanho

    def esta_vazia(self):
        return self._tamanho == 0
