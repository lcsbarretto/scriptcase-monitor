from datetime import datetime

from services.artifacts import LOG_DIR

LOG_FILE = LOG_DIR / "monitor.log"


def log(texto):

    agora = datetime.now().strftime("%H:%M:%S")

    linha = f"[{agora}] {texto}"

    print(linha)

    with open(LOG_FILE, "a", encoding="utf8") as f:

        f.write(linha + "\n")