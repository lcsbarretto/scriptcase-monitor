from config.context_config import (
    CONTEXT_ENABLED,
    CONTEXT_MODE,
    CONTEXT_VARIABLES,
)

from services.logger import log


def preparar_contexto(page, context):
    """
    Prepara o contexto da execução antes dos testes.

    Nesta etapa estamos apenas investigando como o ambiente
    mantém as informações de sessão.
    """

    if not CONTEXT_ENABLED:
        log("Contexto de execução desabilitado.")
        return

    log(f"Preparando contexto: {CONTEXT_MODE}")

    if CONTEXT_MODE == "VARIABLES":

        if not CONTEXT_VARIABLES:
            log("Nenhuma variável de contexto configurada.")
            return

        for nome, valor in CONTEXT_VARIABLES.items():
            log(f"Variável de contexto: {nome} = {valor}")
