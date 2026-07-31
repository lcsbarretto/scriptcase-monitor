from playwright.sync_api import sync_playwright
from config.config import URL, USUARIO, SENHA, HEADLESS, TIMEOUT
from services.logger import log


def validar_login(page):
    """
    Valida se o login foi realizado com sucesso.
    Retorna True quando autenticado.
    """

    # Ainda existe o campo de login?
    if page.get_by_placeholder("login").count() > 0:
        return False

    # Ainda existe o campo de senha?
    if page.get_by_placeholder("Senha").count() > 0:
        return False

    return True


def realizar_login():

    p = sync_playwright().start()

    browser = p.chromium.launch(
        headless=HEADLESS
    )

    context = browser.new_context(
        ignore_https_errors=True
    )

    page = context.new_page()
    page.set_default_timeout(TIMEOUT)

    log(f"Acessando {URL}")

    page.goto(URL)

    page.get_by_placeholder("login").fill(USUARIO)
    page.get_by_placeholder("Senha").fill(SENHA)

    page.get_by_role("button", name="ENTRAR").click()

    page.wait_for_load_state("networkidle")

    if not validar_login(page):
        log("ERRO - Falha na autenticação.")
        browser.close()
        p.stop()
        raise Exception("Usuário ou senha inválidos.")

    log("Login realizado com sucesso.")

    return p, browser, context, page