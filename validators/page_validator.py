ERROR_PATTERNS = [
    {
        "id": "PHP_FATAL",
        "nome": "PHP Fatal Error",
        "padrao": "Fatal error:",
        "categoria": "Erro de PHP",
    },
    {
        "id": "PHP_PARSE",
        "nome": "PHP Parse Error",
        "padrao": "Parse error:",
        "categoria": "Erro de PHP",
    },
    {
        "id": "ORACLE",
        "nome": "Oracle Error",
        "padrao": "ORA-",
        "categoria": "Erro no Oracle",
    },
    {
        "id": "SQL_SERVER",
        "nome": "SQL Server",
        "padrao": "SQLSTATE",
        "categoria": "Erro no SQL",
    },
    {
        "id": "HTTP_500",
        "nome": "HTTP 500",
        "padrao": "HTTP 500",
        "categoria": "Erro HTTP",
    },
]


def extrair_linha(texto: str, padrao: str) -> str | None:
    """
    Retorna a linha onde o padrão foi encontrado.
    """

    for linha in texto.splitlines():
        if padrao.lower() in linha.lower():
            return linha.strip()

    return None


def validar_pagina(texto: str) -> dict:
    """
    Analisa o texto da página procurando erros conhecidos.

    Retorno:
    {
        "ok": bool,
        "erro": dict | None
    }
    """

    texto_normalizado = texto.lower()

    for erro in ERROR_PATTERNS:

        if erro["padrao"].lower() in texto_normalizado:

            resultado = erro.copy()
            resultado["linha"] = extrair_linha(texto, erro["padrao"])

            return {
                "ok": False,
                "erro": resultado
            }

    return {
        "ok": True,
        "erro": None
    }