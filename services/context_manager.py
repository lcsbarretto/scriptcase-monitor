from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse

from config.context_config import (
    CONTEXT_ENABLED,
    CONTEXT_MODE,
    CONTEXT_VARIABLES,
)

from services.logger import log


def preparar_url(url: str) -> str:
    """
    Adiciona as variáveis de contexto configuradas à URL.
    """

    if not CONTEXT_ENABLED:
        return url

    if CONTEXT_MODE != "URL":
        return url

    if not CONTEXT_VARIABLES:
        return url

    partes = urlparse(url)

    parametros = dict(parse_qsl(partes.query))

    parametros.update(CONTEXT_VARIABLES)

    nova_query = urlencode(parametros)

    nova_url = urlunparse(
        (
            partes.scheme,
            partes.netloc,
            partes.path,
            partes.params,
            nova_query,
            partes.fragment,
        )
    )

    return nova_url


def preparar_contexto(page, context):
    """
    Prepara o contexto da execução.

    Nesta etapa, o contexto é configurado através
    de parâmetros de URL.
    """

    if not CONTEXT_ENABLED:
        log("Contexto de execução desabilitado.")
        return

    log(f"Preparando contexto: {CONTEXT_MODE}")

    if not CONTEXT_VARIABLES:
        log("Nenhuma variável de contexto configurada.")
        return

    for nome, valor in CONTEXT_VARIABLES.items():
        log(f"Variável de contexto: {nome} = {valor}")