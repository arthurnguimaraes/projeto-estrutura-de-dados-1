"""
paciente.py
Representa a entidade Paciente usada em todo o sistema de triagem.
Nesta fase (Modulo 1) e apenas uma estrutura simples de dados;
no Modulo 2 ela sera formalizada como um TAD (Tipo Abstrato de Dados).
"""


class Paciente:
    """Estrutura basica que representa a ficha de um paciente na triagem."""

    def __init__(self, id_paciente, nome, classificacao, hora_chegada):
        self.id = id_paciente
        self.nome = nome
        self.classificacao = classificacao  # cor do Protocolo de Manchester
        self.hora_chegada = hora_chegada

    def __repr__(self):
        return (f"Paciente(id={self.id}, nome={self.nome!r}, "
                f"classificacao={self.classificacao!r}, "
                f"hora_chegada={self.hora_chegada!r})")

    def __eq__(self, other):
        if not isinstance(other, Paciente):
            return NotImplemented
        return self.id == other.id
