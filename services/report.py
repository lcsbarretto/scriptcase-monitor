from services import artifacts


ERROS = []

SUCESSOS = []


def registrar_erro(aplicacao, erro):

    """
    Registra uma aplicação que apresentou erro.
    """

    ERROS.append({
        "aplicacao": aplicacao,
        "categoria": erro["categoria"],
        "tipo": erro["nome"],
        "mensagem": erro["mensagem"]
    })


def registrar_sucesso(aplicacao):

    """
    Registra uma aplicação validada com sucesso.
    """

    SUCESSOS.append(aplicacao)


def salvar_relatorio():

    """
    Gera um relatório contendo as aplicações testadas
    e os erros encontrados.
    """

    if artifacts.LOG_DIR is None:
        artifacts.iniciar_execucao()

    arquivo = artifacts.LOG_DIR / "erros.txt"

    total = len(SUCESSOS) + len(ERROS)

    with open(
        arquivo,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("=" * 60 + "\n")
        f.write("SCRIPTCASE TESTER\n")
        f.write("=" * 60 + "\n\n")

        f.write(
            f"Total de aplicações : {total}\n"
        )

        f.write(
            f"Sucesso             : {len(SUCESSOS)}\n"
        )

        f.write(
            f"Erros               : {len(ERROS)}\n\n"
        )

        if not ERROS:

            f.write(
                "Nenhum erro encontrado.\n"
            )

            return

        f.write("=" * 60 + "\n")
        f.write("APLICAÇÕES COM ERRO\n")
        f.write("=" * 60 + "\n\n")

        for item in ERROS:

            f.write(
                f"Aplicação : {item['aplicacao']}\n"
            )

            f.write(
                f"Categoria : {item['categoria']}\n"
            )

            f.write(
                f"Tipo      : {item['tipo']}\n"
            )

            f.write(
                f"Mensagem  : {item['mensagem']}\n"
            )

            f.write("-" * 60 + "\n")