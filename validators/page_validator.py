from validators.extractors import (
    extrair_http,
    extrair_oracle,
    extrair_php,
    extrair_sqlserver,
)

ERROR_PATTERNS = [
    {
        "id": "PHP_FATAL",
        "nome": "PHP Fatal Error",
        "padrao": "Fatal error:",
        "categoria": "Erro de PHP",
        "extractor": extrair_php,
    },
    {
        "id": "PHP_PARSE",
        "nome": "PHP Parse Error",
        "padrao": "Parse error:",
        "categoria": "Erro de PHP",
        "extractor": extrair_php,
    },
    {
        "id": "ORACLE",
        "nome": "Oracle Error",
        "padrao": "ORA-",
        "categoria": "Erro no Oracle",
        "extractor": extrair_oracle,
    },
    {
        "id": "SQL_SERVER",
        "nome": "SQL Server",
        "padrao": "SQLSTATE",
        "categoria": "Erro no SQL",
        "extractor": extrair_sqlserver,
    },
    {
        "id": "HTTP_500",
        "nome": "HTTP 500",
        "padrao": "HTTP 500",
        "categoria": "Erro HTTP",
        "extractor": extrair_http,
    },
]


def validar_pagina(texto: str) -> dict:
    """
    Analisa o texto visível da página procurando erros conhecidos.

    Retorno:

    {
        "ok": bool,
        "erro": dict | None
    }
    """

    texto_normalizado = texto.lower()

    for erro in ERROR_PATTERNS:

        if erro["padrao"].lower() in texto_normalizado:

            resultado = {
            "id": erro["id"],
            "nome": erro["nome"],
            "categoria": erro["categoria"],
            "mensagem": erro["extractor"](
                texto,
                erro["padrao"]
                )
            }

            resultado["mensagem"] = erro["extractor"](
                texto,
                erro["padrao"],
            )

            return {
                "ok": False,
                "erro": resultado,
            }

    return {
        "ok": True,
        "erro": None,
    }