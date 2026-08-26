import configparser
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"


class MonitorInterface:

    def __init__(self, root):
        self.root = root

        self.root.title("ScriptCase Monitor")
        self.root.geometry("700x650")
        self.root.resizable(False, False)

        self.config = configparser.ConfigParser()
        self.monitor_config = configparser.ConfigParser()
        self.context_config = configparser.ConfigParser()

        self.criar_interface()
        self.carregar_configuracoes()

    # ==========================================================
    # INTERFACE PRINCIPAL
    # ==========================================================

    def criar_interface(self):

        notebook = ttk.Notebook(self.root)
        notebook.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.aba_ambiente = ttk.Frame(notebook)
        self.aba_monitor = ttk.Frame(notebook)
        self.aba_contexto = ttk.Frame(notebook)

        notebook.add(
            self.aba_ambiente,
            text="Ambiente"
        )

        notebook.add(
            self.aba_monitor,
            text="Monitor"
        )

        notebook.add(
            self.aba_contexto,
            text="Contexto"
        )

        self.criar_aba_ambiente()
        self.criar_aba_monitor()
        self.criar_aba_contexto()

        botoes = ttk.Frame(self.root)
        botoes.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        ttk.Button(
            botoes,
            text="Salvar configurações",
            command=self.salvar_configuracoes
        ).pack(
            side="left"
        )

        ttk.Button(
            botoes,
            text="Iniciar teste",
            command=self.iniciar_teste
        ).pack(
            side="right"
        )

    # ==========================================================
    # ABA AMBIENTE
    # ==========================================================

    def criar_aba_ambiente(self):

        frame = ttk.Frame(
            self.aba_ambiente,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

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

        frame = ttk.Frame(
            self.aba_monitor,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

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
            font=("Arial", 10, "bold")
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w"
        )

        self.applications_text = tk.Text(
            frame,
            height=12,
            width=70
        )

        self.applications_text.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=10
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.applications_text.yview
        )

        scrollbar.grid(
            row=6,
            column=2,
            sticky="ns",
            pady=10
        )

        self.applications_text.configure(
            yscrollcommand=scrollbar.set
        )

        ttk.Label(
            frame,
            text=(
                "Formato: nome_da_aplicacao=True/False\n"
                "Uma aplicação por linha. As alterações serão salvas "
                "em config/monitor.ini."
            ),
            foreground="gray",
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

    # ==========================================================
    # ABA CONTEXTO
    # ==========================================================

    def criar_aba_contexto(self):

        frame = ttk.Frame(
            self.aba_contexto,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            frame,
            text="Contexto de execução",
            font=("Arial", 11, "bold")
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
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.context_variables = tk.Text(
            frame,
            height=12,
            width=70
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
            foreground="gray",
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
            sticky="w",
            pady=8
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
    # EXECUÇÃO
    # ==========================================================

    def iniciar_teste(self):

        self.salvar_configuracoes()

        messagebox.showinfo(
            "Teste",
            "A execução do monitor será conectada nesta etapa."
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = MonitorInterface(root)

    root.mainloop()