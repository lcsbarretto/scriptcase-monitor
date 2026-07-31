def extrair_padrao(texto: str, padrao: str) -> str | None:
    """
    Extrator padrão.
    Retorna a primeira linha onde o padrão foi encontrado.
    """

    for linha in texto.splitlines():

        if padrao.lower() in linha.lower():
            return linha.strip()

    return None


def _extrair_bloco(texto: str, inicio: str) -> str:
    """
    Captura todas as linhas a partir do marcador informado.
    Utilizado para erros de banco de dados.
    """

    linhas = texto.splitlines()

    capturando = False
    resultado = []

    for linha in linhas:

        linha = linha.strip()

        if not capturando:

            if inicio.lower() in linha.lower():
                capturando = True
            else:
                continue

        resultado.append(linha)

    mensagem = "\n".join(resultado).strip()

    # Remove linhas em branco repetidas
    while "\n\n\n" in mensagem:
        mensagem = mensagem.replace("\n\n\n", "\n\n")

    return mensagem


def extrair_sqlserver(texto: str, padrao: str) -> str:
    """
    Extrai toda a mensagem de erro do SQL Server.
    """

    return _extrair_bloco(texto, "SQLState")


def extrair_oracle(texto: str, padrao: str) -> str:
    """
    Extrai toda a mensagem de erro do Oracle.
    """

    return _extrair_bloco(texto, "ORA-")


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