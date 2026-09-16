"""
fila_prioridade.py
Semana 13 - Fila de prioridade, adaptada ao Protocolo de Manchester
(5 niveis de gravidade). E o COMPONENTE CENTRAL do sistema de triagem:
paciente com prioridade numerica menor (mais grave) e sempre atendido
antes de um paciente com prioridade maior (menos grave).

Implementacao: uma fila (FIFO) separada PARA CADA cor de classificacao,
usando a FilaEncadeada (Semana 12) ja implementada nesta disciplina -
sem recorrer a estruturas prontas do Python. Isso garante duas
propriedades importantes ao mesmo tempo:
  1. Entre cores diferentes, quem tem cor mais grave e atendido primeiro.
  2. Dentro da MESMA cor, a ordem de chegada e respeitada (FIFO) -
     ou seja, dois pacientes 'amarelo' sao atendidos na ordem em que
     chegaram, o que evita injustica entre pacientes de mesma gravidade.

Esta abordagem e mais simples e mais transparente para fins didaticos
que um heap binario, e tem complexidade O(1) para enfileirar/desenfileirar
dado um numero fixo (5) de niveis de prioridade.
"""

from fila_encadeada import FilaEncadeada
from validacao import CLASSIFICACOES, validar_classificacao


class FilaPrioridade:
    """
    Fila de prioridade baseada no Protocolo de Manchester.
    Internamente usa uma FilaEncadeada (fila FIFO propria, sem uso de
    bibliotecas prontas) por cor de classificacao.
    """

    def __init__(self):
        # Uma fila FIFO independente para cada cor -> preserva ordem de
        # chegada dentro do mesmo nivel de gravidade.
        self._filas_por_cor = {cor: FilaEncadeada() for cor in CLASSIFICACOES}

    def enfileirar(self, paciente):
        """
        Insere o paciente na fila correspondente a sua classificacao.
        Complexidade: O(1) - insere no fim da fila daquela cor.
        """
        cor = paciente.classificacao.lower()
        if not validar_classificacao(cor):
            raise ValueError(f"Classificacao invalida: {cor!r}")
        self._filas_por_cor[cor].enfileirar(paciente)

    def desenfileirar(self):
        """
        Remove e retorna o paciente de MAIOR prioridade (cor mais
        grave) que estiver aguardando ha mais tempo dentro dessa cor.

        Complexidade: O(k), onde k = numero de niveis de prioridade
        (aqui, k=5, uma constante pequena) - percorre as cores da mais
        grave para a menos grave ate achar uma fila nao vazia.
        """
        for cor in self._cores_ordenadas_por_prioridade():
            fila_da_cor = self._filas_por_cor[cor]
            if not fila_da_cor.esta_vazia():
                return fila_da_cor.desenfileirar()
        raise IndexError("Fila de prioridade vazia: nenhum paciente aguardando")

    def proximo(self):
        """Consulta (sem remover) o proximo paciente a ser atendido. Complexidade: O(k)."""
        for cor in self._cores_ordenadas_por_prioridade():
            fila_da_cor = self._filas_por_cor[cor]
            if not fila_da_cor.esta_vazia():
                return fila_da_cor.frente()
        return None

    def esta_vazia(self):
        return all(fila.esta_vazia() for fila in self._filas_por_cor.values())

    def tamanho(self):
        return sum(fila.tamanho() for fila in self._filas_por_cor.values())

    def tamanho_por_cor(self):
        """Retorna um dicionario {cor: quantidade_aguardando}, util para paineis/relatorios."""
        return {cor: fila.tamanho() for cor, fila in self._filas_por_cor.items()}

    def posicao_estimada(self, id_paciente):
        """
        Retorna a posicao estimada do paciente na fila de atendimento
        (0 = proximo a ser chamado), contando quantos pacientes com
        prioridade igual ou maior estao a frente dele.
        Retorna -1 se o paciente nao for encontrado.
        """
        posicao = 0
        for cor in self._cores_ordenadas_por_prioridade():
            fila_da_cor = self._filas_por_cor[cor]
            for paciente in fila_da_cor.percorrer():
                if paciente.id == id_paciente:
                    return posicao
                posicao += 1
        return -1

    @staticmethod
    def _cores_ordenadas_por_prioridade():
        # Ordena as cores da mais urgente (prioridade=1) para a menos
        # urgente (prioridade=5). Calculado uma vez por chamada, mas
        # como sao apenas 5 elementos, o custo e desprezivel O(1) na pratica.
        return sorted(CLASSIFICACOES, key=lambda cor: CLASSIFICACOES[cor]["prioridade"])
