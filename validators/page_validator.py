ERROR_PATTERNS = [
    {
        "nome": "PHP Fatal Error",
        "padrao": "Fatal error:",
        "categoria": "Erro de PHP"
    },
    {
        "nome": "PHP Parse Error",
        "padrao": "Parse error:",
        "categoria": "Erro de PHP"
    },
    {
        "nome": "Oracle Error",
        "padrao": "ORA-",
        "categoria": "Erro no Oracle"

    },
    {
        "nome": "SQL Server",
        "padrao": "SQLSTATE",
        "categoria": "Erro no SQL"
    },
    {
        "nome": "HTTP 500",
        "padrao": "HTTP 500",
        "categoria": "Erro HTTP"
    },
]


def validar_html(html: str):

    html = html.lower()

    for erro in ERROR_PATTERNS:

        if erro["padrao"].lower() in html:
            return False, erro["nome"]

    return True, None