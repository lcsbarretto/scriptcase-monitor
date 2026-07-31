import time
from services.artifacts import salvar_screenshot
from config.config import BASE_URL
from config.monitor_config import SCREENSHOT_MODE
from services.logger import log
from services.report import registrar_erro, registrar_sucesso
from validators.page_validator import validar_pagina


def testar_aplicacao(page, app):

    url = f"{BASE_URL}/{app}/{app}.php"

    log(f"Abrindo: {url}")

    inicio = time.perf_counter()

    try:

        page.goto(url, wait_until="networkidle")

        tempo = time.perf_counter() - inicio


        texto =  page.locator("body").inner_text()

        resultado = validar_pagina(texto)
        erro = resultado["erro"]

        if not resultado["ok"]:

            # Sempre registra o erro
            registrar_erro(
                app,
                resultado["erro"]
            )

            # Screenshot conforme configuração
            if SCREENSHOT_MODE in ("ERROR", "ALL"):
                salvar_screenshot(page, app)
                log(f"[ERRO] {app} ({tempo:.2f}s)")
                log(f"Categoria : {erro['categoria']}")
                log(f"Mensagem  : {erro['mensagem']}")

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