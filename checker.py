import time

from artifacts import salvar_screenshot
from config import BASE_URL
from monitor_config import SCREENSHOT_MODE

from logger import log
from report import registrar_erro, registrar_sucesso
from validators.page_validator import validar_html


def testar_aplicacao(page, app):

    url = f"{BASE_URL}/{app}/{app}.php"

    log(f"Abrindo: {url}")

    inicio = time.perf_counter()

    try:

        page.goto(url, wait_until="networkidle")

        tempo = time.perf_counter() - inicio

        html = page.content()

        ok, erro = validar_html(html)

        if not ok:

            # Sempre registra o erro
            registrar_erro(app, erro)

            # Screenshot conforme configuração
            if SCREENSHOT_MODE in ("ERROR", "ALL"):
                salvar_screenshot(page, app)
                registrar_sucesso(app)
            log(f"[ERRO] {app} ({tempo:.2f}s) -> {erro}")

            return False

        # Sempre registra sucesso
        registrar_sucesso(app)

        # Screenshot apenas se configurado
        if SCREENSHOT_MODE == "ALL":
            salvar_screenshot(page, app)
            registrar_sucesso(app)
        log(f"[ OK ] {app} ({tempo:.2f}s)")

        return True

    except Exception as e:

        # Sempre registra a exceção
        registrar_erro(app, str(e))

        # Screenshot conforme configuração
        if SCREENSHOT_MODE in ("ERROR", "ALL"):
            salvar_screenshot(page, app)

        log(f"[EXCEPTION] {app} -> {e}")

        return False