"""
ficha_triagem_dinamica.py
Semana 6 - Alocacao DINAMICA de memoria.

Em C, isto corresponderia a uma lista encadeada com malloc()/free()
para cada no. Python nao possui malloc/free explicitos (a alocacao e
liberacao de memoria e feita automaticamente pelo interpretador via
contagem de referencias + garbage collector), entao aqui simulamos a
alocacao dinamica atraves de uma estrutura ligada por NOS (Node),
criados sob demanda (sem limite de capacidade pre-definido), que e o
analogo estrutural mais proximo do que se faria em C.
"""

from paciente import Paciente


class _No:
    """Representa um no alocado dinamicamente (equivalente a malloc de 1 struct)."""
    __slots__ = ("paciente", "proximo")

    def __init__(self, paciente):
        self.paciente = paciente
        self.proximo = None  # em C seria um ponteiro Node*


class RepositorioFichasDinamico:
    """TAD Ficha de Triagem - implementacao com alocacao dinamica (lista ligada)."""

    def __init__(self):
        self._inicio = None   # equivalente a um ponteiro Node* head, iniciado como NULL
        self._quantidade = 0

    def esta_cheio(self):
        # Nao ha limite de capacidade na alocacao dinamica.
        return False

    def quantidade(self):
        return self._quantidade

    def inserir_ficha(self, paciente):
        """
        O(1): insercao no inicio da lista.
        Equivale, em C, a: no = malloc(sizeof(No)); no->proximo = inicio; inicio = no;
        """
        novo_no = _No(paciente)
        novo_no.proximo = self._inicio
        self._inicio = novo_no
        self._quantidade += 1
        return True

    def remover_ficha(self, id_paciente):
        """
        O(n): precisa percorrer a lista ate encontrar o no com o id.
        Em C, o no removido precisaria de free(no) explicito; em Python,
        basta remover todas as referencias a ele que o garbage collector
        libera a memoria automaticamente.
        """
        anterior = None
        atual = self._inicio
        while atual is not None:
            if atual.paciente.id == id_paciente:
                if anterior is None:
                    self._inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                self._quantidade -= 1
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def buscar_ficha(self, id_paciente):
        """O(n): busca linear percorrendo os ponteiros 'proximo'."""
        atual = self._inicio
        while atual is not None:
            if atual.paciente.id == id_paciente:
                return atual.paciente
            atual = atual.proximo
        return None

    def listar_fichas(self):
        """O(n): percorre todos os nos coletando os pacientes."""
        resultado = []
        atual = self._inicio
        while atual is not None:
            resultado.append(atual.paciente)
            atual = atual.proximo
        return resultado
