"""
undo_redo_classificacao.py
Semana 11 - Aplicacao pratica de pilha: desfazer/refazer (undo/redo)
de reclassificacoes feitas na triagem.

Cenario real: um enfermeiro reclassifica um paciente por engano (ex.:
marca como 'verde' quando deveria ser 'amarelo') e precisa poder
desfazer a ultima acao rapidamente, sem perder a possibilidade de
refazer caso desista de desfazer.

Usa DUAS pilhas:
- pilha_desfazer: guarda o HISTORICO de classificacoes anteriores.
- pilha_refazer: guarda as classificacoes desfeitas, para poder
  reaplicar (redo) caso o usuario mude de ideia.
"""

from pilha_array import PilhaArray


class GerenciadorReclassificacao:
    """
    Controla o historico de classificacoes de UM paciente, permitindo
    desfazer (undo) e refazer (redo) reclassificacoes.
    """

    def __init__(self, paciente):
        self._paciente = paciente
        self._pilha_desfazer = PilhaArray()  # classificacoes anteriores
        self._pilha_refazer = PilhaArray()   # classificacoes desfeitas

    def reclassificar(self, nova_classificacao):
        """
        Aplica uma nova classificacao, empilhando a anterior no
        historico de undo. Qualquer 'redo' pendente e descartado,
        pois uma nova acao muda o rumo do historico (comportamento
        padrao em editores de texto, por exemplo).
        """
        classificacao_anterior = self._paciente.classificacao
        self._pilha_desfazer.empilhar(classificacao_anterior)
        self._paciente.classificacao = nova_classificacao

        # Uma nova acao invalida o "futuro" de redo anterior.
        self._pilha_refazer = PilhaArray()

    def desfazer(self):
        """
        Volta para a classificacao anterior. Levanta erro se nao
        houver nada para desfazer.
        """
        if self._pilha_desfazer.esta_vazia():
            raise IndexError("Nao ha reclassificacoes para desfazer")

        classificacao_atual = self._paciente.classificacao
        classificacao_anterior = self._pilha_desfazer.desempilhar()

        self._pilha_refazer.empilhar(classificacao_atual)
        self._paciente.classificacao = classificacao_anterior
        return classificacao_anterior

    def refazer(self):
        """
        Reaplica a ultima classificacao desfeita. Levanta erro se nao
        houver nada para refazer.
        """
        if self._pilha_refazer.esta_vazia():
            raise IndexError("Nao ha reclassificacoes para refazer")

        classificacao_atual = self._paciente.classificacao
        proxima_classificacao = self._pilha_refazer.desempilhar()

        self._pilha_desfazer.empilhar(classificacao_atual)
        self._paciente.classificacao = proxima_classificacao
        return proxima_classificacao

    def pode_desfazer(self):
        return not self._pilha_desfazer.esta_vazia()

    def pode_refazer(self):
        return not self._pilha_refazer.esta_vazia()
