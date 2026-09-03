from pathlib import Path

import config.monitor_config as monitor_config


IGNORAR = {
    "_lib",
    "_libtmp",
    "tmp",
    "css",
    "img",
    "doc",
    "ico",
    "third"
}


PREFIXOS = (
    "frm",
    "cons",
    "cns"
)


def listar_aplicacoes(app_path):

    # Obtém os valores atuais da configuração.
    # Isso evita manter MAX_APPS, ONLY_ENABLED e
    # FILTROS congelados na memória.
    filtros = monitor_config.FILTROS
    max_apps = monitor_config.MAX_APPS
    only_enabled = monitor_config.ONLY_ENABLED
    order = monitor_config.ORDER

    print(f"[DEBUG] APP_PATH: {app_path}")
    print(f"[DEBUG] MAX_APPS: {max_apps}")
    print(f"[DEBUG] ONLY_ENABLED: {only_enabled}")
    print(f"[DEBUG] ORDER: {order}")
    print(f"[DEBUG] FILTROS: {filtros}")

    aplicacoes = []

    for pasta in Path(app_path).iterdir():

        if not pasta.is_dir():
            continue

        if pasta.name in IGNORAR:
            continue

        if not pasta.name.startswith(PREFIXOS):
            continue

        arquivo_principal = (
            pasta / f"{pasta.name}.php"
        )

        if not arquivo_principal.exists():
            continue

        # Se ONLY_ENABLED estiver desativado,
        # ignora completamente os filtros.
        if only_enabled:

            if not filtros.get(
                pasta.name,
                False
            ):
                continue

        aplicacoes.append(
            pasta.name
        )

    print(
        f"[DEBUG] Aplicações antes da ordenação: "
        f"{len(aplicacoes)}"
    )

    aplicacoes.sort()

    if order == "DESC":
        aplicacoes.reverse()


    if max_apps > 0:

        aplicacoes = aplicacoes[
            :max_apps
        ]


    return aplicacoes