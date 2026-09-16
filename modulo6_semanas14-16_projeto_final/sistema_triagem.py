"""
sistema_triagem.py
Modulo 6 - Projeto Final (Semanas 14-16).

Sistema de Triagem de Pronto-Socorro completo, integrando AO MENOS
DUAS estruturas estudadas ao longo da disciplina (conforme exigido):

  1. FILA DE PRIORIDADE (Modulo 5) - fila de pacientes aguardando
     atendimento, respeitando o Protocolo de Manchester.
  2. LISTA ENCADEADA (Modulo 3) - historico/prontuario de pacientes
     ja atendidos no dia, permitindo busca e listagem.
  3. PILHA, via GerenciadorReclassificacao (Modulo 4) - permite
     desfazer/refazer uma reclassificacao feita por engano ANTES do
     paciente ser atendido (funcionalidade extra que enriquece o
     sistema, mantendo o escopo obrigatorio ja atendido pelos itens 1 e 2).
"""

from paciente import Paciente
from utils import gerar_id_paciente, formatar_hora_chegada
from validacao import validar_classificacao, validar_nome, CLASSIFICACOES
from fila_prioridade import FilaPrioridade
from lista_encadeada_simples import ListaEncadeadaSimples
from undo_redo_classificacao import GerenciadorReclassificacao


class SistemaTriagem:
    """
    Classe principal que integra a fila de prioridade (pacientes
    aguardando) com o historico de atendimentos (lista encadeada) e
    o controle de undo/redo de reclassificacao (pilha), por paciente.
    """

    def __init__(self):
        self._fila_espera = FilaPrioridade()
        self._historico_atendidos = ListaEncadeadaSimples()
        self._gerenciadores_reclassificacao = {}  # id_paciente -> GerenciadorReclassificacao
        self._pacientes_em_espera = {}  # id_paciente -> Paciente (para acesso rapido/reclassificacao)

    # ---------- Cadastro e triagem ----------

    def cadastrar_paciente(self, nome, classificacao):
        """
        Realiza a triagem inicial de um novo paciente: valida os
        dados, gera ID e horario de chegada, e o insere na fila de
        prioridade correspondente.
        """
        if not validar_nome(nome):
            raise ValueError("Nome invalido")
        if not validar_classificacao(classificacao):
            raise ValueError(f"Classificacao invalida: {classificacao!r}")

        paciente = Paciente(
            gerar_id_paciente(), nome, classificacao.lower(), formatar_hora_chegada()
        )
        self._fila_espera.enfileirar(paciente)
        self._pacientes_em_espera[paciente.id] = paciente
        self._gerenciadores_reclassificacao[paciente.id] = GerenciadorReclassificacao(paciente)
        return paciente

    def reclassificar_paciente(self, id_paciente, nova_classificacao):
        """
        Corrige a classificacao de um paciente que AINDA ESTA na fila
        de espera (usa a pilha de undo/redo por tras dos panos).
        Como a fila de prioridade e organizada por cor, o paciente e
        removido e reenfileirado na nova cor.
        """
        if not validar_classificacao(nova_classificacao):
            raise ValueError(f"Classificacao invalida: {nova_classificacao!r}")
        if id_paciente not in self._pacientes_em_espera:
            raise KeyError("Paciente nao encontrado na fila de espera")

        gerenciador = self._gerenciadores_reclassificacao[id_paciente]
        gerenciador.reclassificar(nova_classificacao.lower())
        self._reconstruir_fila_apos_reclassificacao()

    def desfazer_reclassificacao(self, id_paciente):
        """Desfaz a ultima reclassificacao de um paciente ainda em espera."""
        gerenciador = self._gerenciadores_reclassificacao[id_paciente]
        gerenciador.desfazer()
        self._reconstruir_fila_apos_reclassificacao()

    def _reconstruir_fila_apos_reclassificacao(self):
        """
        Como a FilaPrioridade organiza pacientes por cor em filas
        separadas, uma reclassificacao exige realocar o paciente na
        fila correta. Reconstruimos a fila de prioridade a partir dos
        pacientes ainda em espera (O(n), aceitavel pois so ocorre em
        reclassificacoes, que sao eventos raros comparados a
        enfileirar/desenfileirar).
        """
        nova_fila = FilaPrioridade()
        for paciente in self._pacientes_em_espera.values():
            nova_fila.enfileirar(paciente)
        self._fila_espera = nova_fila

    # ---------- Atendimento ----------

    def atender_proximo(self):
        """
        Chama o proximo paciente da fila de prioridade e o move para
        o historico de atendidos (lista encadeada).
        """
        if self._fila_espera.esta_vazia():
            return None
        paciente = self._fila_espera.desenfileirar()
        del self._pacientes_em_espera[paciente.id]
        del self._gerenciadores_reclassificacao[paciente.id]
        # Insere no INICIO (posicao=0), nao no fim: a lista encadeada tem
        # ponteiro de inicio, entao isso continua O(1) e faz `historico()`
        # retornar do mais recente para o mais antigo, como documentado.
        self._historico_atendidos.inserir(paciente, posicao=0)
        return paciente

    # ---------- Consultas ----------

    def pacientes_aguardando(self):
        return self._fila_espera.tamanho()

    def pacientes_por_cor(self):
        return self._fila_espera.tamanho_por_cor()

    def posicao_na_fila(self, id_paciente):
        return self._fila_espera.posicao_estimada(id_paciente)

    def historico(self):
        """Lista todos os pacientes ja atendidos, do mais recente ao mais antigo."""
        return self._historico_atendidos.percorrer()

    def buscar_no_historico(self, id_paciente):
        posicao = self._historico_atendidos.buscar(
            Paciente(id_paciente, "", "", ""), chave=lambda p: p.id
        )
        if posicao == -1:
            return None
        return self._historico_atendidos.percorrer()[posicao]
