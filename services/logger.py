from datetime import datetime

from services import artifacts


def log(texto):

    agora = datetime.now().strftime("%H:%M:%S")

    linha = f"[{agora}] {texto}"

    print(linha)

    if artifacts.LOG_DIR is None:
        artifacts.iniciar_execucao()

    log_file = artifacts.LOG_DIR / "tester.log"

    with open(
        log_file,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(linha + "\n")