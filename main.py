from login import realizar_login
from scanner import listar_aplicacoes
from checker import testar_aplicacao
from logger import log
from config import APP_PATH
from report import salvar_relatorio


def main():

    log("=" * 60)
    log("INICIANDO SCRIPTCASE MONITOR")
    log("=" * 60)

    # Login
    p, browser, context, page = realizar_login()

    try:

        # Descobre aplicações
        apps = listar_aplicacoes(APP_PATH)

        # Durante os testes, limite a quantidade abaixo
        # Depois basta remover esta linha
        apps = listar_aplicacoes(APP_PATH)

        total = len(apps)
        ok = 0
        erro = 0

        log(f"Foram encontradas {total} aplicações.\n")

        # Testa cada aplicação
        for app in apps:

            if testar_aplicacao(page, app):
                ok += 1
            else:
                erro += 1

        log("")
        log("=" * 60)
        log("RESUMO")
        log("=" * 60)
        log(f"Total : {total}")
        log(f"OK    : {ok}")
        log(f"Erro  : {erro}")
        salvar_relatorio()
        
    except Exception as e:

        log(f"ERRO: {e}")

    finally:

        browser.close()
        p.stop()

        log("Navegador encerrado.")


if __name__ == "__main__":
    main()