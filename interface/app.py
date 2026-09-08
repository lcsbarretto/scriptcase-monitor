import configparser
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

# ==========================================================
# CAMINHO RAIZ DO PROJETO
# ==========================================================

if getattr(sys, "frozen", False):
    ROOT = Path(sys.executable).resolve().parent
else:
    ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CONFIG_DIR = ROOT / "config"


class MonitorInterface:

    BG = "#0a1020"
    CARD = "#111a2d"
    INPUT = "#0c1424"
    BORDER = "#243653"
    TEXT = "#e8f0ff"
    MUTED = "#8d9bb5"
    BLUE = "#1683ff"
    BLUE_HOVER = "#2a96ff"
    BLUE_PRESS = "#0d68cc"
    CYAN = "#39c9ff"
    SUCCESS = "#35d07f"
    ERROR = "#ff5f6d"

    def __init__(self, root):
        self.root = root

        self.root.title("ScriptCase Tester")
        self.root.geometry("900x780")
        self.root.minsize(760, 520)
        self.root.resizable(True, True)
        self.root.configure(bg=self.BG)

        # Permite que o conteúdo acompanhe o redimensionamento da janela.
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.logo_image = None

        self.config = configparser.ConfigParser()
        self.monitor_config = configparser.ConfigParser()
        self.context_config = configparser.ConfigParser()

        self.configurar_estilo()
        self.criar_interface()
        self.carregar_configuracoes()

    # ==========================================================
    # ESTILO
    # ==========================================================

    def configurar_estilo(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background=self.BG)
        style.configure("TLabel", background=self.BG, foreground=self.TEXT)

        style.configure(
            "Title.TLabel",
            background=self.BG,
            foreground=self.TEXT,
            font=("Segoe UI", 20, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background=self.BG,
            foreground=self.MUTED,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Section.TLabel",
            background=self.CARD,
            foreground=self.TEXT,
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "Muted.TLabel",
            background=self.CARD,
            foreground=self.MUTED,
            font=("Segoe UI", 9)
        )

        style.configure(
            "TNotebook",
            background=self.BG,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background=self.CARD,
            foreground=self.MUTED,
            padding=(22, 11),
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", self.INPUT),
                ("active", "#182640")
            ],
            foreground=[
                ("selected", self.CYAN),
                ("active", self.TEXT)
            ]
        )

        style.configure(
            "TEntry",
            fieldbackground=self.INPUT,
            foreground=self.TEXT,
            insertcolor=self.TEXT,
            bordercolor=self.BORDER,
            lightcolor=self.BORDER,
            darkcolor=self.BORDER,
            padding=8
        )

        style.map(
            "TEntry",
            bordercolor=[("focus", self.BLUE)],
            lightcolor=[("focus", self.BLUE)],
            darkcolor=[("focus", self.BLUE)]
        )

        style.configure(
            "TCombobox",
            fieldbackground=self.INPUT,
            foreground=self.TEXT,
            background=self.INPUT,
            arrowcolor=self.CYAN,
            bordercolor=self.BORDER,
            padding=7
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.INPUT)],
            foreground=[("readonly", self.TEXT)],
            bordercolor=[("focus", self.BLUE)]
        )

        style.configure(
            "TCheckbutton",
            background=self.CARD,
            foreground=self.TEXT,
            font=("Segoe UI", 10)
        )

        style.map(
            "TCheckbutton",
            background=[("active", self.CARD)],
            foreground=[("active", self.TEXT)]
        )

        style.configure(
            "Primary.TButton",
            background=self.BLUE,
            foreground="#ffffff",
            borderwidth=0,
            focusthickness=0,
            padding=(20, 10),
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Primary.TButton",
            background=[
                ("pressed", self.BLUE_PRESS),
                ("active", self.BLUE_HOVER),
                ("disabled", "#26344d")
            ],
            foreground=[
                ("disabled", "#71809a")
            ]
        )

        style.configure(
            "Secondary.TButton",
            background=self.CARD,
            foreground=self.TEXT,
            borderwidth=1,
            bordercolor=self.BORDER,
            lightcolor=self.BORDER,
            darkcolor=self.BORDER,
            padding=(16, 9),
            font=("Segoe UI", 10)
        )

        style.map(
            "Secondary.TButton",
            background=[
                ("pressed", self.BLUE_PRESS),
                ("active", "#182640")
            ],
            foreground=[
                ("pressed", "#ffffff"),
                ("active", self.CYAN)
            ],
            bordercolor=[
                ("pressed", self.BLUE),
                ("active", self.BLUE)
            ]
        )

        style.configure(
            "Horizontal.TProgressbar",
            background=self.BLUE,
            troughcolor=self.INPUT,
            bordercolor=self.BORDER,
            lightcolor=self.BLUE,
            darkcolor=self.BLUE,
            thickness=12
        )

        style.configure(
            "Vertical.TScrollbar",
            background=self.CARD,
            troughcolor=self.INPUT,
            bordercolor=self.BORDER,
            arrowcolor=self.MUTED,
            relief="flat",
            borderwidth=0
        )

        style.map(
            "Vertical.TScrollbar",
            background=[
                ("active", self.BLUE),
                ("pressed", self.BLUE_PRESS)
            ],
            arrowcolor=[
                ("active", self.CYAN)
            ]
        )

    # ==========================================================
    # INTERFACE PRINCIPAL
    # ==========================================================

    def criar_interface(self):

        # ------------------------------------------------------
        # ESTRUTURA PRINCIPAL
        # ------------------------------------------------------

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # ------------------------------------------------------
        # CABEÇALHO FIXO
        # ------------------------------------------------------

        header = tk.Frame(
            self.root,
            bg=self.BG
        )

        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=28,
            pady=(18, 8)
        )

        header.grid_columnconfigure(1, weight=1)

        self.carregar_logo(header)

        titulo = tk.Frame(
            header,
            bg=self.BG
        )

        titulo.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(12, 0)
        )

        tk.Label(
            titulo,
            text="ScriptCase Tester",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        tk.Label(
            titulo,
            text="Validação e testes de aplicações ScriptCase",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        self.status_label = tk.Label(
            header,
            text="● Pronto",
            bg=self.BG,
            fg=self.SUCCESS,
            font=("Segoe UI", 9, "bold")
        )

        self.status_label.grid(
            row=0,
            column=2,
            sticky="e",
            padx=(12, 0)
        )

        # ------------------------------------------------------
        # ÁREA PRINCIPAL COM SCROLL
        # ------------------------------------------------------

        self.main_canvas = tk.Canvas(
            self.root,
            bg=self.BG,
            bd=0,
            highlightthickness=0
        )

        self.main_canvas.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(28, 0),
            pady=(4, 0)
        )

        self.main_scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.main_canvas.yview
        )

        self.main_scrollbar.grid(
            row=1,
            column=1,
            sticky="ns",
            padx=(0, 12),
            pady=(4, 0)
        )

        self.main_canvas.configure(
            yscrollcommand=self.main_scrollbar.set
        )

        self.main_content = tk.Frame(
            self.main_canvas,
            bg=self.BG
        )

        self.main_window = self.main_canvas.create_window(
            (0, 0),
            window=self.main_content,
            anchor="nw"
        )

        self.main_content.bind(
            "<Configure>",
            self._atualizar_area_scroll
        )

        self.main_canvas.bind(
            "<Configure>",
            self._redimensionar_conteudo_scroll
        )

        # Roda do mouse em toda a interface.
        # Fora do editor, rola a janela principal; sobre o editor, rola
        # somente o conteúdo interno de aplicações.
        self.root.bind_all(
            "<MouseWheel>",
            self._scroll_mouse_global
        )
        self.root.bind_all(
            "<Button-4>",
            self._scroll_mouse_global
        )
        self.root.bind_all(
            "<Button-5>",
            self._scroll_mouse_global
        )

        # ------------------------------------------------------
        # ABAS
        # ------------------------------------------------------

        notebook = ttk.Notebook(
            self.main_content
        )

        notebook.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=0,
            pady=(0, 12)
        )

        self.main_content.grid_columnconfigure(
            0,
            weight=1
        )

        self.aba_ambiente = ttk.Frame(notebook)
        self.aba_monitor = ttk.Frame(notebook)
        self.aba_contexto = ttk.Frame(notebook)

        notebook.add(
            self.aba_ambiente,
            text="  Ambiente  "
        )

        notebook.add(
            self.aba_monitor,
            text="  Monitor  "
        )

        notebook.add(
            self.aba_contexto,
            text="  Contexto  "
        )

        self.criar_aba_ambiente()
        self.criar_aba_monitor()
        self.criar_aba_contexto()

        # ------------------------------------------------------
        # ÁREA DE PROGRESSO
        # ------------------------------------------------------

        self.progress_frame = tk.Frame(
            self.main_content,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        self.progress_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.progress_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.progress_frame.grid_columnconfigure(
            1,
            weight=0
        )

        task_logo_frame = tk.Frame(
            self.progress_frame,
            bg=self.CARD
        )

        task_logo_frame.grid(
            row=0,
            column=1,
            rowspan=3,
            sticky="e",
            padx=(8, 14),
            pady=8
        )

        self.criar_logo_tarefas(
            task_logo_frame
        )

        self.progress_label = tk.Label(
            self.progress_frame,
            text="Aguardando execução...",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI", 10)
        )

        self.progress_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(10, 3)
        )

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            style="Horizontal.TProgressbar"
        )

        self.progress_bar.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=16,
            pady=4
        )

        self.progress_info = tk.Label(
            self.progress_frame,
            text="0 / 0 aplicações",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.progress_info.grid(
            row=2,
            column=0,
            sticky="w",
            padx=16,
            pady=(3, 10)
        )

        # ------------------------------------------------------
        # BOTÕES
        # ------------------------------------------------------

        botoes = ttk.Frame(
            self.main_content
        )

        botoes.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 18)
        )

        ttk.Button(
            botoes,
            text="Salvar configurações",
            style="Secondary.TButton",
            command=self.salvar_configuracoes
        ).pack(
            side="left"
        )

        self.botao_iniciar = ttk.Button(
            botoes,
            text="▶  Iniciar teste",
            style="Primary.TButton",
            command=self.iniciar_teste
        )

        self.botao_iniciar.pack(
            side="right"
        )

    # ==========================================================
    # SCROLL DA JANELA PRINCIPAL
    # ==========================================================

    def _atualizar_area_scroll(self, event=None):

        self.main_canvas.configure(
            scrollregion=self.main_canvas.bbox("all")
        )

    def _redimensionar_conteudo_scroll(self, event):

        self.main_canvas.itemconfigure(
            self.main_window,
            width=event.width
        )

    def _scroll_mouse_global(self, event):

        if event.widget == self.applications_text:
            if getattr(event, "num", None) == 4:
                self.applications_text.yview_scroll(-3, "units")
            elif getattr(event, "num", None) == 5:
                self.applications_text.yview_scroll(3, "units")
            else:
                unidades = int(-1 * (event.delta / 120))
                if unidades:
                    self.applications_text.yview_scroll(unidades, "units")
            return "break"

        if getattr(event, "num", None) == 4:
            self.main_canvas.yview_scroll(-3, "units")
        elif getattr(event, "num", None) == 5:
            self.main_canvas.yview_scroll(3, "units")
        else:
            unidades = int(-1 * (event.delta / 120))
            if unidades:
                self.main_canvas.yview_scroll(unidades, "units")

        return "break"

    def _scroll_janela(self, event):

        self.main_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==========================================================
    # LOGO
    # ==========================================================

    def carregar_logo(self, parent):

        caminho = ROOT / "logo.png"

        if not caminho.exists():
            return

        try:
            imagem = tk.PhotoImage(file=str(caminho))

            # Logo principal do cabeçalho.
            self.logo_image = self.redimensionar_logo(
                imagem,
                72
            )

            tk.Label(
                parent,
                image=self.logo_image,
                bg=self.BG,
                bd=0
            ).grid(
                row=0,
                column=0,
                sticky="w"
            )

            # A mesma imagem também vira o ícone da janela.
            self.root.iconphoto(
                True,
                self.logo_image
            )

        except Exception:
            self.logo_image = None

    def redimensionar_logo(self, imagem, tamanho_maximo):

        largura = imagem.width()
        altura = imagem.height()

        fator = max(
            1,
            (largura + tamanho_maximo - 1) // tamanho_maximo,
            (altura + tamanho_maximo - 1) // tamanho_maximo
        )

        if fator > 1:
            return imagem.subsample(fator, fator)

        return imagem

    def criar_logo_tarefas(self, parent):

        caminho = ROOT / "logo.png"

        if not caminho.exists():
            return

        try:
            imagem = tk.PhotoImage(file=str(caminho))

            self.task_logo_image = self.redimensionar_logo(
                imagem,
                40
            )

            tk.Label(
                parent,
                image=self.task_logo_image,
                bg=self.CARD,
                bd=0
            ).pack()

        except Exception:
            self.task_logo_image = None

    # ==========================================================
    # ABA AMBIENTE
    # ==========================================================

    def criar_aba_ambiente(self):

        frame = tk.Frame(
            self.aba_ambiente,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.aba_ambiente.grid_rowconfigure(0, weight=1)
        self.aba_ambiente.grid_columnconfigure(0, weight=1)

        frame.grid_columnconfigure(1, weight=1)

        inner = tk.Frame(frame, bg=self.CARD)
        inner.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )
        inner.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        frame = inner

        self.url = self.criar_campo(
            frame,
            "URL:",
            0
        )

        self.app_path = self.criar_campo(
            frame,
            "App Path:",
            1
        )

        self.base_url = self.criar_campo(
            frame,
            "Base URL:",
            2
        )

        self.usuario = self.criar_campo(
            frame,
            "Usuário:",
            3
        )

        self.senha = self.criar_campo(
            frame,
            "Senha:",
            4,
            senha=True
        )

        self.headless = tk.BooleanVar()

        ttk.Checkbutton(
            frame,
            text="Executar em modo Headless",
            variable=self.headless
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w",
            pady=10
        )

        self.timeout = self.criar_campo(
            frame,
            "Timeout:",
            6
        )

    # ==========================================================
    # ABA MONITOR
    # ==========================================================

    def criar_aba_monitor(self):

        frame = tk.Frame(
            self.aba_monitor,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.aba_monitor.grid_rowconfigure(
            0,
            weight=1,
            minsize=470
        )
        self.aba_monitor.grid_columnconfigure(
            0,
            weight=1
        )

        inner = tk.Frame(frame, bg=self.CARD)
        inner.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )

        frame.grid_rowconfigure(
            0,
            weight=1,
            minsize=420
        )
        frame.grid_columnconfigure(
            0,
            weight=1
        )

        inner.grid_rowconfigure(
            6,
            weight=1,
            minsize=145
        )
        inner.grid_columnconfigure(
            1,
            weight=1
        )

        frame = inner

        self.max_apps = self.criar_campo(
            frame,
            "Máximo de aplicações:",
            0
        )

        ttk.Label(
            frame,
            text="Ordem:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=8
        )

        self.order = ttk.Combobox(
            frame,
            values=["ASC", "DESC"],
            state="readonly",
            width=30
        )

        self.order.grid(
            row=1,
            column=1,
            sticky="w",
            pady=8
        )

        self.only_enabled = tk.BooleanVar()

        ttk.Checkbutton(
            frame,
            text="Testar somente aplicações habilitadas",
            variable=self.only_enabled
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            pady=10
        )

        ttk.Label(
            frame,
            text="Screenshots:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=8
        )

        self.screenshot_mode = ttk.Combobox(
            frame,
            values=["NONE", "ERROR", "ALL"],
            state="readonly",
            width=30
        )

        self.screenshot_mode.grid(
            row=3,
            column=1,
            sticky="w",
            pady=8
        )

        ttk.Separator(
            frame,
            orient="horizontal"
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=15
        )

        ttk.Label(
            frame,
            text="Aplicações configuradas",
            style="Section.TLabel"
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w"
        )

        texto_frame = tk.Frame(
            frame,
            bg=self.CARD
        )

        texto_frame.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=10
        )

        texto_frame.grid_propagate(False)
        texto_frame.configure(
            height=145
        )

        texto_frame.grid_rowconfigure(
            0,
            weight=1
        )
        texto_frame.grid_columnconfigure(0, weight=1)

        self.applications_text = tk.Text(
            texto_frame,
            height=6,
            width=70,
            font=("Consolas", 10),
            bg=self.INPUT,
            fg=self.TEXT,
            insertbackground=self.CYAN,
            selectbackground=self.BLUE,
            selectforeground="#ffffff",
            relief="solid",
            bd=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.BLUE,
            highlightthickness=1,
            padx=10,
            pady=8,
            wrap="none"
        )

        self.applications_text.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Sem scrollbar visível: a rolagem continua disponível pela roda
        # do mouse e pelo teclado.
        # O scroll continua disponível pelo mouse/teclado, mas a barra
        # vertical fica oculta para manter o visual limpo.
        self.applications_text.configure(
            yscrollcommand=lambda first, last: None
        )

        ttk.Label(
            frame,
            text=(
                "Formato: nome_da_aplicacao=True/False\n"
                "Uma aplicação por linha. As alterações serão salvas "
                "em config/monitor.ini."
            ),
            style="Muted.TLabel",
            wraplength=600
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="w"
        )

        frame.columnconfigure(
            1,
            weight=1
        )

        frame.rowconfigure(
            6,
            weight=1
        )

    def _scroll_aplicacoes(self, event):
        self.applications_text.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )
        return "break"

    def _scroll_aplicacoes_linux(self, event):
        if event.num == 4:
            self.applications_text.yview_scroll(-3, "units")
        elif event.num == 5:
            self.applications_text.yview_scroll(3, "units")
        return "break"

    # ==========================================================
    # ABA CONTEXTO
    # ==========================================================

    def criar_aba_contexto(self):

        frame = tk.Frame(
            self.aba_contexto,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.aba_contexto.grid_rowconfigure(0, weight=1)
        self.aba_contexto.grid_columnconfigure(0, weight=1)

        inner = tk.Frame(frame, bg=self.CARD)
        inner.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        inner.grid_rowconfigure(6, weight=1)

        frame = inner

        ttk.Label(
            frame,
            text="Contexto de execução",
            style="Section.TLabel"
        ).pack(
            anchor="w"
        )

        self.context_enabled = tk.BooleanVar()

        ttk.Checkbutton(
            frame,
            text="Ativar contexto de execução",
            variable=self.context_enabled
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.context_status = ttk.Label(
            frame,
            text="Status: -"
        )

        self.context_status.pack(
            anchor="w",
            pady=5
        )

        self.context_mode_label = ttk.Label(
            frame,
            text="Modo: -"
        )

        self.context_mode_label.pack(
            anchor="w",
            pady=5
        )

        ttk.Separator(
            frame,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=15
        )

        ttk.Label(
            frame,
            text="Variáveis configuradas",
            style="Section.TLabel"
        ).pack(
            anchor="w"
        )

        self.context_variables = tk.Text(
            frame, height=12, width=70, font=("Consolas", 9),
            bg=self.INPUT, fg=self.MUTED,
            insertbackground=self.CYAN,
            selectbackground=self.BLUE,
            selectforeground="#ffffff",
            relief="solid", bd=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.BLUE,
            highlightthickness=1,
            padx=10, pady=8, state="disabled"
        )

        self.context_variables.pack(
            fill="both",
            expand=True,
            pady=10
        )

        ttk.Label(
            frame,
            text=(
                "As variáveis de contexto são armazenadas no arquivo "
                "config/context.ini.\n"
                "Você pode editar os valores acima e salvar pela interface."
            ),
            style="Muted.TLabel",
            wraplength=600
        ).pack(
            anchor="w"
        )

    # ==========================================================
    # CAMPOS
    # ==========================================================

    def criar_campo(
        self,
        frame,
        texto,
        linha,
        senha=False
    ):

        ttk.Label(
            frame,
            text=texto
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            pady=8
        )

        campo = ttk.Entry(
            frame,
            width=40,
            show="*" if senha else ""
        )

        campo.grid(
            row=linha,
            column=1,
            sticky="ew",
            pady=8,
            padx=(18, 0)
        )

        return campo

    # ==========================================================
    # CARREGAMENTO
    # ==========================================================

    def carregar_configuracoes(self):

        self.config.read(
            CONFIG_DIR / "config.ini",
            encoding="utf-8"
        )

        self.monitor_config.read(
            CONFIG_DIR / "monitor.ini",
            encoding="utf-8"
        )

        self.context_config.read(
            CONFIG_DIR / "context.ini",
            encoding="utf-8"
        )

        self.carregar_config()
        self.carregar_monitor_config()
        self.carregar_contexto()

    # ==========================================================
    # CONFIG.INI
    # ==========================================================

    def carregar_config(self):

        if not self.config.has_section("SCRIPTCASE"):
            return

        cfg = self.config["SCRIPTCASE"]

        self.url.insert(
            0,
            cfg.get("URL", "")
        )

        self.app_path.insert(
            0,
            cfg.get("APP_PATH", "")
        )

        self.base_url.insert(
            0,
            cfg.get("BASE_URL", "")
        )

        self.usuario.insert(
            0,
            cfg.get("USUARIO", "")
        )

        self.senha.insert(
            0,
            cfg.get("SENHA", "")
        )

        self.headless.set(
            cfg.getboolean(
                "HEADLESS",
                fallback=True
            )
        )

        self.timeout.insert(
            0,
            cfg.get(
                "TIMEOUT",
                "10000"
            )
        )

    # ==========================================================
    # MONITOR.INI
    # ==========================================================

    def carregar_monitor_config(self):

        if self.monitor_config.has_section("MONITOR"):

            monitor = self.monitor_config["MONITOR"]

            self.max_apps.insert(
                0,
                monitor.get(
                    "MAX_APPS",
                    "0"
                )
            )

            self.order.set(
                monitor.get(
                    "ORDER",
                    "ASC"
                )
            )

            self.only_enabled.set(
                monitor.getboolean(
                    "ONLY_ENABLED",
                    fallback=True
                )
            )

        if self.monitor_config.has_section("SCREENSHOT"):

            screenshot = self.monitor_config["SCREENSHOT"]

            self.screenshot_mode.set(
                screenshot.get(
                    "MODE",
                    "ERROR"
                )
            )

        # ==========================================
        # FILTROS
        # ==========================================

        self.applications_text.delete(
            "1.0",
            tk.END
        )

        if self.monitor_config.has_section("FILTROS"):

            filtros = self.monitor_config["FILTROS"]

            for nome, valor in filtros.items():

                self.applications_text.insert(
                    tk.END,
                    f"{nome}={valor}\n"
                )

        else:

            self.applications_text.insert(
                tk.END,
                "Nenhuma aplicação configurada.\n"
            )

    # ==========================================================
    # CONTEXT.INI
    # ==========================================================

    def carregar_contexto(self):

        if self.context_config.has_section("CONTEXT"):

            context = self.context_config["CONTEXT"]

            enabled = context.getboolean(
                "ENABLED",
                fallback=False
            )

            mode = context.get(
                "MODE",
                "URL"
            )

            self.context_enabled.set(
                enabled
            )

            self.context_status.config(
                text=(
                    "Status: "
                    + (
                        "Habilitado"
                        if enabled
                        else "Desabilitado"
                    )
                )
            )

            self.context_mode_label.config(
                text=f"Modo: {mode}"
            )

        self.context_variables.configure(state="normal")

        self.context_variables.delete(
            "1.0",
            tk.END
        )

        if self.context_config.has_section("VARIABLES"):

            variables = self.context_config["VARIABLES"]

            for nome, valor in variables.items():

                self.context_variables.insert(
                    tk.END,
                    f"{nome} = {valor}\n"
                )

        else:

            self.context_variables.insert(
                tk.END,
                "Nenhuma variável configurada.\n"
            )

    # ==========================================================
    # SALVAR CONFIG.INI
    # ==========================================================

    def salvar_config(self):

        if not self.config.has_section("SCRIPTCASE"):
            self.config["SCRIPTCASE"] = {}

        cfg = self.config["SCRIPTCASE"]

        cfg["URL"] = self.url.get()
        cfg["APP_PATH"] = self.app_path.get()
        cfg["BASE_URL"] = self.base_url.get()
        cfg["USUARIO"] = self.usuario.get()
        cfg["SENHA"] = self.senha.get()
        cfg["HEADLESS"] = str(
            self.headless.get()
        )
        cfg["TIMEOUT"] = self.timeout.get()

        with open(
            CONFIG_DIR / "config.ini",
            "w",
            encoding="utf-8"
        ) as arquivo:

            self.config.write(arquivo)

    # ==========================================================
    # SALVAR MONITOR.INI
    # ==========================================================

    def salvar_monitor_config(self):

        if not self.monitor_config.has_section("MONITOR"):
            self.monitor_config["MONITOR"] = {}

        monitor = self.monitor_config["MONITOR"]

        monitor["MAX_APPS"] = self.max_apps.get()
        monitor["ORDER"] = self.order.get()
        monitor["ONLY_ENABLED"] = str(
            self.only_enabled.get()
        )

        if not self.monitor_config.has_section("SCREENSHOT"):
            self.monitor_config["SCREENSHOT"] = {}

        self.monitor_config["SCREENSHOT"]["MODE"] = (
            self.screenshot_mode.get()
        )

        # ==========================================
        # FILTROS
        # ==========================================

        if not self.monitor_config.has_section("FILTROS"):
            self.monitor_config["FILTROS"] = {}

        filtros = self.monitor_config["FILTROS"]

        filtros.clear()

        texto = self.applications_text.get(
            "1.0",
            tk.END
        )

        for linha in texto.splitlines():

            linha = linha.strip()

            if not linha:
                continue

            if "=" not in linha:
                continue

            nome, valor = linha.split(
                "=",
                1
            )

            nome = nome.strip()
            valor = valor.strip()

            if not nome:
                continue

            filtros[nome] = valor

        with open(
            CONFIG_DIR / "monitor.ini",
            "w",
            encoding="utf-8"
        ) as arquivo:

            self.monitor_config.write(arquivo)

    # ==========================================================
    # SALVAR CONTEXT.INI
    # ==========================================================

    def salvar_contexto(self):

        if not self.context_config.has_section("CONTEXT"):
            self.context_config["CONTEXT"] = {}

        context = self.context_config["CONTEXT"]

        context["ENABLED"] = str(
            self.context_enabled.get()
        )

        if not context.get("MODE"):
            context["MODE"] = "URL"

        if not self.context_config.has_section("VARIABLES"):
            self.context_config["VARIABLES"] = {}

        variables = self.context_config["VARIABLES"]

        variables.clear()

        texto = self.context_variables.get(
            "1.0",
            tk.END
        )

        for linha in texto.splitlines():

            linha = linha.strip()

            if not linha:
                continue

            if "=" not in linha:
                continue

            nome, valor = linha.split(
                "=",
                1
            )

            nome = nome.strip()
            valor = valor.strip()

            if not nome:
                continue

            variables[nome] = valor

        with open(
            CONFIG_DIR / "context.ini",
            "w",
            encoding="utf-8"
        ) as arquivo:

            self.context_config.write(arquivo)

        # Atualiza o status exibido na aba Contexto após o salvamento.
        enabled = self.context_enabled.get()

        self.context_status.config(
            text=(
                "Status: "
                + (
                    "Habilitado"
                    if enabled
                    else "Desabilitado"
                )
            )
        )

    # ==========================================================
    # SALVAR TUDO
    # ==========================================================

    def salvar_configuracoes(self):

        try:

            self.salvar_config()
            self.salvar_monitor_config()
            self.salvar_contexto()

            messagebox.showinfo(
                "Configuração",
                "Configurações salvas com sucesso."
            )

        except Exception as e:

            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar as configurações.\n\n{e}"
            )

    # ==========================================================
    # EXECUTAR TESTE
    # ==========================================================
    def iniciar_teste(self):

        try:

            self.salvar_config()
            self.salvar_monitor_config()
            self.salvar_contexto()

        except Exception as e:

            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar as configurações.\n\n{e}"
            )

            return

        self.botao_iniciar.config(
            state="disabled"
        )

        self.progress_bar["value"] = 0

        self.progress_label.config(
            text="Iniciando monitor..."
        )

        self.progress_info.config(
            text="Aguardando aplicações..."
        )

        thread = threading.Thread(
            target=self.executar_teste_thread,
            daemon=True
        )

        thread.start()
        
    def executar_teste_thread(self):

        try:

            from main import executar_monitor

            resultado = executar_monitor(
                progresso_callback=self.atualizar_progresso
            )

            self.root.after(
                0,
                lambda: self.finalizar_teste(resultado)
            )

        except Exception as e:

            self.root.after(
                0,
                self.erro_teste,
                str(e)
            )

    def atualizar_progresso(
        self,
        atual,
        total,
        aplicacao,
        ok,
        erro
    ):

        self.root.after(
            0,
            lambda: self._atualizar_interface_progresso(
                atual,
                total,
                aplicacao,
                ok,
                erro
            )
        )

    def _atualizar_interface_progresso(
        self,
        atual,
        total,
        aplicacao,
        ok,
        erro
    ):

        if total <= 0:
            percentual = 0
        else:
            percentual = (
                atual / total
            ) * 100

        self.progress_bar["value"] = percentual

        if aplicacao:

            self.progress_label.config(
                text=f"Testando: {aplicacao}"
            )

        self.progress_info.config(
            text=(
                f"{atual} / {total} aplicações "
                f"| OK: {ok} "
                f"| Erros: {erro}"
            )
        )

    def finalizar_teste(self, resultado):

        self.progress_bar["value"] = 100

        self.progress_label.config(
            text="Teste concluído!"
        )

        self.progress_info.config(
            text=(
                f"Total: {resultado['total']} "
                f"| OK: {resultado['ok']} "
                f"| Erros: {resultado['erro']}"
            )
        )

        self.botao_iniciar.config(
            state="normal"
        )

        messagebox.showinfo(
            "Teste concluído",
            (
                "A execução foi concluída.\n\n"
                f"Total de aplicações: {resultado['total']}\n"
                f"Sucessos: {resultado['ok']}\n"
                f"Erros: {resultado['erro']}"
            )
        )


    def erro_teste(self, erro):

        self.botao_iniciar.config(
            state="normal"
        )

        self.progress_label.config(
            text="Erro durante a execução."
        )

        messagebox.showerror(
            "Erro",
            f"Ocorreu um erro durante a execução.\n\n{erro}"
        )





if __name__ == "__main__":

    root = tk.Tk()

    app = MonitorInterface(root)

    root.mainloop()