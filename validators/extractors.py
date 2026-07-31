def extrair_padrao(texto: str, padrao: str) -> str | None:
    """
    Extrator padrão.
    Retorna a primeira linha onde o padrão foi encontrado.
    """

    for linha in texto.splitlines():

        if padrao.lower() in linha.lower():
            return linha.strip()

    return None


def extrair_sqlserver(texto: str, padrao: str) -> str | None:
    """
    Extrator de erro SQL Server.

    Nesta primeira versão utiliza o extrator padrão.
    Será evoluído posteriormente.
    """

    return extrair_padrao(texto, padrao)


def extrair_oracle(texto: str, padrao: str) -> str | None:
    """
    Extrator de erro Oracle.

    Nesta primeira versão utiliza o extrator padrão.
    Será evoluído posteriormente.
    """

    return extrair_padrao(texto, padrao)


def extrair_php(texto: str, padrao: str) -> str | None:
    """
    Extrator para erros PHP.
    """

    return extrair_padrao(texto, padrao)


def extrair_http(texto: str, padrao: str) -> str | None:
    """
    Extrator para erros HTTP.
    """

    return extrair_padrao(texto, padrao)