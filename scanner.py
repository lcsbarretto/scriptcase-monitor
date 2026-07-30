from pathlib import Path

from monitor_config import (
    FILTROS,
    MAX_APPS,
    ONLY_ENABLED,
    ORDER
)

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

    aplicacoes = []

    for pasta in Path(app_path).iterdir():

        if not pasta.is_dir():
            continue

        if pasta.name in IGNORAR:
            continue

        if not pasta.name.startswith(PREFIXOS):
            continue

        arquivo_principal = pasta / f"{pasta.name}.php"

        if not arquivo_principal.exists():
            continue

        if ONLY_ENABLED:

            if not FILTROS.get(pasta.name, False):
                continue

        aplicacoes.append(pasta.name)

    aplicacoes.sort()

    if ORDER == "DESC":
        aplicacoes.reverse()

    if MAX_APPS > 0:
        aplicacoes = aplicacoes[:MAX_APPS]

    return aplicacoes