"""
interface_grafica.py
Modulo 6 - Interface grafica (GUI) em Tkinter para o Sistema de
Triagem de Pronto-Socorro.

Ao contrario de interface_cli.py (menu em texto, no terminal), este
arquivo abre uma JANELA de verdade - e um programa executavel com
tela, como pedido pela disciplina. A logica de dominio continua 100%
em sistema_triagem.py: esta interface so CHAMA os metodos publicos de
SistemaTriagem (cadastrar_paciente, atender_proximo, reclassificar
_paciente, desfazer/refazer_reclassificacao, fila_detalhada,
historico...) e desenha o resultado na tela. Nenhuma regra de negocio
e duplicada aqui.

Requisitos: apenas a biblioteca padrao do Python (tkinter ja vem
junto do CPython na maioria dos sistemas). Em algumas distros Linux
o tkinter fica em um pacote separado do sistema operacional; se a
janela nao abrir com "ModuleNotFoundError: No module named 'tkinter'",
instale com:
    sudo apt install python3-tk        # Debian/Ubuntu
    sudo dnf install python3-tkinter   # Fedora

Como executar:
    cd modulo6_semanas14-16_projeto_final
    python3 interface_grafica.py
"""

import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from sistema_triagem import SistemaTriagem
from validacao import CLASSIFICACOES

# Mesma paleta de cores do Protocolo de Manchester usada no prototipo
# web (interface_web_prototipo.html), para manter a identidade visual
# entre as duas interfaces do projeto.
CORES_HEX = {
    "vermelho": "#DC2626",
    "laranja": "#EA580C",
    "amarelo": "#B45309",
    "verde": "#15803D",
    "azul": "#1D4ED8",
}

# Cores ordenadas da mais grave para a menos grave (mesma ordem usada
# na fila de prioridade).
ORDEM_CORES = sorted(CLASSIFICACOES, key=lambda cor: CLASSIFICACOES[cor]["prioridade"])

# Mesmo conjunto de pacientes de exemplo do prototipo web, para que
# quem for demonstrar o projeto tenha os dois "Carregar exemplo"
# consistentes entre si.
PACIENTES_EXEMPLO = [
    ("Marcos Ferreira", "vermelho"),
    ("Julia Nascimento", "laranja"),
    ("Heitor Almeida", "laranja"),
    ("Bruna Castro", "amarelo"),
    ("Elisa Ramos", "amarelo"),
    ("Ana Beatriz Souza", "verde"),
    ("Gisele Prado", "verde"),
    ("Carla Menezes", "azul"),
]

BG = "#F2F5F6"
SURFACE = "#FFFFFF"
LINE = "#D7E0E1"
INK = "#111A1C"
INK_SOFT = "#5A6B6E"
ACCENT = "#0F6E63"


def _segundos_desde(hora_chegada_str):
    """Converte a string 'DD/MM/AAAA HH:MM:SS' (ver utils.py) em segundos decorridos."""
    try:
        chegada = datetime.strptime(hora_chegada_str, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        return 0
    return max(0, int((datetime.now() - chegada).total_seconds()))


def _formatar_segundos(total_segundos):
    minutos, segundos = divmod(int(total_segundos), 60)
    return f"{minutos}min {segundos}s" if minutos else f"{segundos}s"


class JanelaTriagem(tk.Tk):
    """Janela principal do prototipo grafico do sistema de triagem."""

    def __init__(self):
        super().__init__()
        self.title("Sistema de Triagem — Pronto-Socorro")
        self.geometry("1260x700")
        self.minsize(1040, 580)
        self.configure(bg=BG)

        self.sistema = SistemaTriagem()
        self._id_selecionado = None
        self._toast_job = None

        self._montar_estilo()
        self._montar_layout()
        self._atualizar_tudo()
        self.after(1000, self._tick_cronometro)

    # ------------------------------------------------------------ estilo
    def _montar_estilo(self):
        style = ttk.Style(self)
        for tema in ("clam", "alt", "default"):
            try:
                style.theme_use(tema)
                break
            except tk.TclError:
                continue

        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=INK)
        style.configure("Panel.TLabel", background=SURFACE, foreground=INK)
        style.configure("Header.TLabel", background=SURFACE, foreground=INK,
                         font=("Segoe UI", 11, "bold"))
        style.configure("Sub.TLabel", background=BG, foreground=INK_SOFT,
                         font=("Segoe UI", 9))
        style.configure("Stat.TLabel", background=SURFACE, foreground=INK,
                         font=("Segoe UI", 17, "bold"))
        style.configure("StatCaption.TLabel", background=SURFACE, foreground=INK_SOFT,
                         font=("Segoe UI", 8))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=27, font=("Segoe UI", 10),
                         background=SURFACE, fieldbackground=SURFACE)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#DCEEEA")],
                  foreground=[("selected", INK)])

    # ------------------------------------------------------------ layout
    def _montar_layout(self):
        header = ttk.Frame(self, padding=(18, 14, 18, 10))
        header.pack(fill="x")

        titulo = ttk.Frame(header)
        titulo.pack(side="left")
        ttk.Label(titulo, text="✚  Sistema de Triagem — Pronto-Socorro",
                  font=("Segoe UI", 14, "bold"), background=BG).pack(anchor="w")
        ttk.Label(titulo, text="Protocolo de Manchester · Algoritmos e Estrutura de Dados I",
                  style="Sub.TLabel").pack(anchor="w")

        stats = ttk.Frame(header)
        stats.pack(side="right")
        self.lbl_aguardando = self._criar_stat(stats, "Aguardando")
        self.lbl_atendidos = self._criar_stat(stats, "Atendidos")
        self.lbl_espera = self._criar_stat(stats, "Maior espera")

        corpo = ttk.Frame(self, padding=(18, 0, 18, 6))
        corpo.pack(fill="both", expand=True)

        # Larguras fixas para as colunas das pontas (cadastro/historico) e a
        # coluna central (fila) elastica, preenchendo o espaco restante -
        # mais previsivel do que grid com pesos quando o conteudo interno
        # (Treeview, Combobox) tem largura minima propria.
        painel_cadastro = tk.Frame(corpo, bg=SURFACE, highlightbackground=LINE,
                                    highlightthickness=1, width=320)
        painel_cadastro.pack(side="left", fill="y", padx=(0, 14))
        painel_cadastro.pack_propagate(False)

        painel_fila = tk.Frame(corpo, bg=SURFACE, highlightbackground=LINE,
                                highlightthickness=1)
        painel_fila.pack(side="left", fill="both", expand=True, padx=(0, 14))

        painel_historico = tk.Frame(corpo, bg=SURFACE, highlightbackground=LINE,
                                     highlightthickness=1, width=340)
        painel_historico.pack(side="left", fill="y")
        painel_historico.pack_propagate(False)

        self._montar_painel_cadastro(painel_cadastro)
        self._montar_painel_fila(painel_fila)
        self._montar_painel_historico(painel_historico)

        self.status_var = tk.StringVar(value="Bem-vindo(a). Cadastre um paciente ou carregue o exemplo.")
        ttk.Label(self, textvariable=self.status_var, anchor="center",
                  style="Sub.TLabel", padding=(0, 4, 0, 8)).pack(fill="x")

    def _criar_stat(self, parent, legenda):
        caixa = tk.Frame(parent, bg=SURFACE, highlightbackground=LINE, highlightthickness=1)
        caixa.pack(side="left", padx=4)
        valor = ttk.Label(caixa, text="0", style="Stat.TLabel")
        valor.pack(padx=16, pady=(6, 0))
        ttk.Label(caixa, text=legenda.upper(), style="StatCaption.TLabel").pack(padx=16, pady=(0, 6))
        return valor

    # -------------------------------------------------- painel: cadastro
    def _montar_painel_cadastro(self, painel):
        ttk.Label(painel, text="🩺 Nova triagem", style="Header.TLabel").pack(
            anchor="w", padx=18, pady=(18, 12))

        ttk.Label(painel, text="Nome do paciente", style="Panel.TLabel").pack(anchor="w", padx=18)
        self.entry_nome = tk.Entry(painel, font=("Segoe UI", 10), relief="solid",
                                    bd=1, highlightthickness=0)
        self.entry_nome.pack(fill="x", padx=18, pady=(3, 14), ipady=4)
        self.entry_nome.bind("<Return>", lambda evento: self._registrar_paciente())

        ttk.Label(painel, text="Classificação (Protocolo de Manchester)",
                  style="Panel.TLabel", wraplength=280).pack(anchor="w", padx=18)

        self.cor_var = tk.StringVar(value="amarelo")
        cores_frame = tk.Frame(painel, bg=SURFACE)
        cores_frame.pack(fill="x", padx=18, pady=(6, 16))
        for cor in ORDEM_CORES:
            linha = tk.Frame(cores_frame, bg=SURFACE)
            linha.pack(fill="x", pady=2)
            tk.Label(linha, text="●", fg=CORES_HEX[cor], bg=SURFACE,
                     font=("Segoe UI", 13)).pack(side="left")
            tk.Radiobutton(
                linha, text=f"{cor.capitalize()} — {CLASSIFICACOES[cor]['nome']}",
                variable=self.cor_var, value=cor, bg=SURFACE, activebackground=SURFACE,
                selectcolor=SURFACE, anchor="w", font=("Segoe UI", 9), bd=0,
                highlightthickness=0,
            ).pack(side="left", padx=(6, 0))

        tk.Button(painel, text="Registrar paciente", command=self._registrar_paciente,
                   bg=ACCENT, fg="white", activebackground=ACCENT, relief="flat",
                   font=("Segoe UI", 10, "bold"), pady=8, cursor="hand2"
                   ).pack(fill="x", padx=18, pady=(2, 10))

        linha_acoes = tk.Frame(painel, bg=SURFACE)
        linha_acoes.pack(fill="x", padx=18, pady=(0, 18))
        ttk.Button(linha_acoes, text="Carregar exemplo",
                   command=self._carregar_exemplo).pack(side="left", expand=True,
                                                          fill="x", padx=(0, 4))
        ttk.Button(linha_acoes, text="Reiniciar tudo",
                   command=self._reiniciar).pack(side="left", expand=True,
                                                   fill="x", padx=(4, 0))

    # ------------------------------------------------------- painel: fila
    def _montar_painel_fila(self, painel):
        painel.rowconfigure(1, weight=1)
        painel.columnconfigure(0, weight=1)

        cabecalho = tk.Frame(painel, bg=SURFACE)
        cabecalho.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))
        ttk.Label(cabecalho, text="⏳ Fila de espera", style="Header.TLabel").pack(side="left")
        self.lbl_fila_count = ttk.Label(cabecalho, text="0 pacientes", style="Panel.TLabel",
                                         foreground=INK_SOFT)
        self.lbl_fila_count.pack(side="right")

        colunas = ("cor", "id", "chegada", "espera")
        self.tree_fila = ttk.Treeview(painel, columns=colunas, show="tree headings",
                                       selectmode="browse")
        self.tree_fila.heading("#0", text="Paciente")
        self.tree_fila.heading("cor", text="Cor")
        self.tree_fila.heading("id", text="ID")
        self.tree_fila.heading("chegada", text="Chegada")
        self.tree_fila.heading("espera", text="Espera")
        self.tree_fila.column("#0", width=170, anchor="w")
        self.tree_fila.column("cor", width=80, anchor="center")
        self.tree_fila.column("id", width=40, anchor="center")
        self.tree_fila.column("chegada", width=80, anchor="center")
        self.tree_fila.column("espera", width=80, anchor="center")
        self.tree_fila.grid(row=1, column=0, sticky="nsew", padx=18)
        self.tree_fila.bind("<<TreeviewSelect>>", self._ao_selecionar_paciente)

        for cor in ORDEM_CORES:
            self.tree_fila.tag_configure(f"grupo_{cor}", foreground=CORES_HEX[cor],
                                          font=("Segoe UI", 9, "bold"))
            self.tree_fila.tag_configure(f"paciente_{cor}", foreground=INK)
        self.tree_fila.tag_configure("vazio", foreground="#8B999B")

        # painel de reclassificacao - so aparece com um paciente selecionado
        self.frame_reclass = tk.Frame(painel, bg=SURFACE)
        self.frame_reclass.grid(row=2, column=0, sticky="ew", padx=18, pady=(12, 0))
        self.reclass_label_var = tk.StringVar(value="Reclassificar:")
        ttk.Label(self.frame_reclass, textvariable=self.reclass_label_var,
                  style="Panel.TLabel").pack(side="left")
        self.combo_reclass = ttk.Combobox(
            self.frame_reclass, state="readonly", width=13,
            values=[f"{cor} — {CLASSIFICACOES[cor]['nome']}" for cor in ORDEM_CORES])
        self.combo_reclass.pack(side="left", padx=6)
        ttk.Button(self.frame_reclass, text="Aplicar", width=8,
                   command=self._aplicar_reclassificacao).pack(side="left")
        self.frame_reclass.grid_remove()

        acoes = tk.Frame(painel, bg=SURFACE)
        acoes.grid(row=3, column=0, sticky="ew", padx=18, pady=18)
        self.btn_atender = tk.Button(
            acoes, text="Atender próximo paciente", command=self._atender_proximo,
            bg=ACCENT, fg="white", activebackground=ACCENT, relief="flat",
            font=("Segoe UI", 10, "bold"), pady=8, cursor="hand2")
        self.btn_atender.pack(side="left", expand=True, fill="x", padx=(0, 4))
        self.btn_desfazer = ttk.Button(acoes, text="↩ Desfazer", command=self._desfazer,
                                        state="disabled")
        self.btn_desfazer.pack(side="left", padx=4)
        self.btn_refazer = ttk.Button(acoes, text="↪ Refazer", command=self._refazer,
                                       state="disabled")
        self.btn_refazer.pack(side="left", padx=(4, 0))

    # --------------------------------------------------- painel: historico
    def _montar_painel_historico(self, painel):
        painel.rowconfigure(1, weight=1)
        painel.columnconfigure(0, weight=1)

        cabecalho = tk.Frame(painel, bg=SURFACE)
        cabecalho.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))
        ttk.Label(cabecalho, text="📋 Histórico", style="Header.TLabel").pack(side="left")
        self.lbl_hist_count = ttk.Label(cabecalho, text="0", style="Panel.TLabel",
                                         foreground=INK_SOFT)
        self.lbl_hist_count.pack(side="right")

        colunas = ("id", "cor", "chegada")
        self.tree_hist = ttk.Treeview(painel, columns=colunas, show="tree headings")
        self.tree_hist.heading("#0", text="Paciente")
        self.tree_hist.heading("id", text="ID")
        self.tree_hist.heading("cor", text="Cor")
        self.tree_hist.heading("chegada", text="Chegada")
        self.tree_hist.column("#0", width=120)
        self.tree_hist.column("id", width=36, anchor="center")
        self.tree_hist.column("cor", width=70, anchor="center")
        self.tree_hist.column("chegada", width=80, anchor="center")
        self.tree_hist.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        for cor in ORDEM_CORES:
            self.tree_hist.tag_configure(f"hist_{cor}", foreground=CORES_HEX[cor])

    # ---------------------------------------------------------- acoes UI
    def _mostrar_status(self, mensagem):
        self.status_var.set(mensagem)

    def _registrar_paciente(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            self._mostrar_status("Digite o nome do paciente.")
            self.entry_nome.focus_set()
            return
        try:
            paciente = self.sistema.cadastrar_paciente(nome, self.cor_var.get())
        except ValueError as erro:
            messagebox.showerror("Erro ao cadastrar", str(erro))
            return
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.focus_set()
        self._mostrar_status(f"{paciente.nome} cadastrado(a) — {paciente.classificacao.capitalize()}.")
        self._atualizar_tudo()

    def _atender_proximo(self):
        paciente = self.sistema.atender_proximo()
        if paciente is None:
            self._mostrar_status("Não há pacientes aguardando.")
            return
        self._id_selecionado = None
        self._mostrar_status(f"Atendendo agora: {paciente.nome} ({paciente.classificacao.capitalize()}).")
        self._atualizar_tudo()

    def _buscar_paciente_na_fila(self, id_paciente):
        for pacientes in self.sistema.fila_detalhada().values():
            for paciente in pacientes:
                if paciente.id == id_paciente:
                    return paciente
        return None

    def _ao_selecionar_paciente(self, evento=None):
        selecao = self.tree_fila.selection()
        if not selecao or not selecao[0].startswith("p:"):
            self._id_selecionado = None
            self.frame_reclass.grid_remove()
            self._atualizar_botoes_undo()
            return
        self._id_selecionado = int(selecao[0].split(":", 1)[1])
        paciente = self._buscar_paciente_na_fila(self._id_selecionado)
        if paciente is None:
            self._id_selecionado = None
            self.frame_reclass.grid_remove()
            self._atualizar_botoes_undo()
            return
        nome_curto = paciente.nome if len(paciente.nome) <= 16 else paciente.nome[:15] + "…"
        self.reclass_label_var.set(f"Reclassificar {nome_curto}:")
        self.combo_reclass.set(f"{paciente.classificacao} — {CLASSIFICACOES[paciente.classificacao]['nome']}")
        self.frame_reclass.grid()
        self._atualizar_botoes_undo()

    def _aplicar_reclassificacao(self):
        if self._id_selecionado is None:
            return
        valor = self.combo_reclass.get()
        if not valor:
            self._mostrar_status("Escolha uma cor para reclassificar.")
            return
        nova_cor = valor.split(" — ")[0]
        try:
            self.sistema.reclassificar_paciente(self._id_selecionado, nova_cor)
        except (ValueError, KeyError) as erro:
            messagebox.showerror("Erro ao reclassificar", str(erro))
            return
        self._mostrar_status("Paciente reclassificado.")
        self._atualizar_tudo(manter_selecao=self._id_selecionado)

    def _desfazer(self):
        if self._id_selecionado is None:
            return
        try:
            self.sistema.desfazer_reclassificacao(self._id_selecionado)
        except (KeyError, IndexError) as erro:
            messagebox.showerror("Erro ao desfazer", str(erro))
            return
        self._mostrar_status("Última reclassificação desfeita.")
        self._atualizar_tudo(manter_selecao=self._id_selecionado)

    def _refazer(self):
        if self._id_selecionado is None:
            return
        try:
            self.sistema.refazer_reclassificacao(self._id_selecionado)
        except (KeyError, IndexError) as erro:
            messagebox.showerror("Erro ao refazer", str(erro))
            return
        self._mostrar_status("Reclassificação refeita.")
        self._atualizar_tudo(manter_selecao=self._id_selecionado)

    def _carregar_exemplo(self):
        self._reiniciar(silencioso=True)
        for nome, cor in PACIENTES_EXEMPLO:
            self.sistema.cadastrar_paciente(nome, cor)
        self._mostrar_status(f"Exemplo carregado — {len(PACIENTES_EXEMPLO)} pacientes na fila.")
        self._atualizar_tudo()

    def _reiniciar(self, silencioso=False):
        self.sistema = SistemaTriagem()
        self._id_selecionado = None
        if not silencioso:
            self._mostrar_status("Sistema reiniciado.")
        self._atualizar_tudo()

    # -------------------------------------------------------- atualizacao
    def _atualizar_tudo(self, manter_selecao=None):
        self._atualizar_fila(manter_selecao)
        self._atualizar_historico()
        self._atualizar_stats()
        self._atualizar_botoes_undo()

    def _atualizar_stats(self):
        aguardando = self.sistema.pacientes_aguardando()
        self.lbl_aguardando.configure(text=str(aguardando))
        self.lbl_atendidos.configure(text=str(len(self.sistema.historico())))
        maior_espera = 0
        for pacientes in self.sistema.fila_detalhada().values():
            for paciente in pacientes:
                maior_espera = max(maior_espera, _segundos_desde(paciente.hora_chegada))
        self.lbl_espera.configure(text=_formatar_segundos(maior_espera) if aguardando else "—")

    def _atualizar_fila(self, manter_selecao=None):
        self.tree_fila.delete(*self.tree_fila.get_children())
        detalhado = self.sistema.fila_detalhada()
        total = 0
        item_para_selecionar = None

        for cor in ORDEM_CORES:
            pacientes = detalhado[cor]
            total += len(pacientes)
            grupo_id = f"g:{cor}"
            texto_grupo = f"{cor.capitalize()} ({len(pacientes)})"
            self.tree_fila.insert("", "end", iid=grupo_id, text=texto_grupo, open=True,
                                   tags=(f"grupo_{cor}",))
            if not pacientes:
                self.tree_fila.insert(grupo_id, "end", text="— ninguém aguardando —",
                                       tags=("vazio",))
            for paciente in pacientes:
                item_id = f"p:{paciente.id}"
                hora = paciente.hora_chegada.split(" ")[-1]
                espera = _formatar_segundos(_segundos_desde(paciente.hora_chegada))
                self.tree_fila.insert(
                    grupo_id, "end", iid=item_id, text=paciente.nome,
                    values=(cor.capitalize(), paciente.id, hora, espera),
                    tags=(f"paciente_{cor}",))
                if manter_selecao is not None and paciente.id == manter_selecao:
                    item_para_selecionar = item_id

        self.lbl_fila_count.configure(text=f"{total} paciente{'s' if total != 1 else ''}")
        self.btn_atender.configure(state=("normal" if total else "disabled"))

        if item_para_selecionar:
            self.tree_fila.selection_set(item_para_selecionar)
            self.tree_fila.see(item_para_selecionar)
        else:
            self._id_selecionado = None
            self.frame_reclass.grid_remove()

    def _atualizar_historico(self):
        self.tree_hist.delete(*self.tree_hist.get_children())
        historico = self.sistema.historico()
        self.lbl_hist_count.configure(text=str(len(historico)))
        if not historico:
            self.tree_hist.insert("", "end", text="Nenhum paciente atendido ainda.")
            return
        for paciente in historico:
            cor = paciente.classificacao
            hora = paciente.hora_chegada.split(" ")[-1]
            self.tree_hist.insert(
                "", "end", text=paciente.nome,
                values=(paciente.id, cor.capitalize(), hora),
                tags=(f"hist_{cor}",))

    def _atualizar_botoes_undo(self):
        if self._id_selecionado is None:
            self.btn_desfazer.configure(state="disabled")
            self.btn_refazer.configure(state="disabled")
            return
        pode_desfazer = self.sistema.pode_desfazer_reclassificacao(self._id_selecionado)
        pode_refazer = self.sistema.pode_refazer_reclassificacao(self._id_selecionado)
        self.btn_desfazer.configure(state=("normal" if pode_desfazer else "disabled"))
        self.btn_refazer.configure(state=("normal" if pode_refazer else "disabled"))

    def _tick_cronometro(self):
        # Atualiza so os numeros de tempo de espera a cada segundo, sem
        # reconstruir a arvore inteira (evita perder selecao/scroll).
        self._atualizar_stats()
        detalhado = self.sistema.fila_detalhada()
        for cor in ORDEM_CORES:
            for paciente in detalhado[cor]:
                item_id = f"p:{paciente.id}"
                if self.tree_fila.exists(item_id):
                    valores = list(self.tree_fila.item(item_id, "values"))
                    valores[3] = _formatar_segundos(_segundos_desde(paciente.hora_chegada))
                    self.tree_fila.item(item_id, values=valores)
        self.after(1000, self._tick_cronometro)


def main():
    app = JanelaTriagem()
    app.mainloop()


if __name__ == "__main__":
    main()
