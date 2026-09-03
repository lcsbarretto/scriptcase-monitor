from services.login import realizar_login
from services.checker import testar_aplicacao
from services.logger import log
from services.report import salvar_relatorio

import importlib


def executar_monitor(progresso_callback=None):

    # ==========================================================
    # RECARREGA AS CONFIGURAÇÕES ATUAIS
    # ==========================================================

    import config.config
    import config.monitor_config
    import config.context_config
    import services.scanner
    import services.context_manager

    importlib.reload(
        config.config
    )

    importlib.reload(
        config.monitor_config
    )

    importlib.reload(
        config.context_config
    )

    # Os serviços que mantêm referências das configurações
    # precisam ser atualizados.
    importlib.reload(
        services.scanner
    )

    importlib.reload(
        services.context_manager
    )

    # Importa as configurações somente depois do reload
    from config.config import APP_PATH

    # Importa os serviços atualizados
    from services.scanner import listar_aplicacoes
    from services.context_manager import preparar_contexto

    # ==========================================================
    # INÍCIO DA EXECUÇÃO
    # ==========================================================

    log("=" * 60)
    log("INICIANDO SCRIPTCASE MONITOR")
    log("=" * 60)

    p, browser, context, page = realizar_login()

    try:

        # Prepara o contexto
        preparar_contexto(
            page,
            context
        )

        # Descobre as aplicações
        apps = listar_aplicacoes(
            APP_PATH
        )

        total = len(apps)

        ok = 0
        erro = 0

        log(
            f"Foram encontradas {total} aplicações.\n"
        )

        # Informa início do progresso
        if progresso_callback:

            progresso_callback(
                atual=0,
                total=total,
                aplicacao=None,
                ok=ok,
                erro=erro
            )

        # Testa cada aplicação
        for indice, app in enumerate(
            apps,
            start=1
        ):

            resultado = testar_aplicacao(
                page,
                app
            )

            if resultado:
                ok += 1
            else:
                erro += 1

            # Atualiza progresso
            if progresso_callback:

                progresso_callback(
                    atual=indice,
                    total=total,
                    aplicacao=app,
                    ok=ok,
                    erro=erro
                )

        log("")

        log("=" * 60)
        log("RESUMO")
        log("=" * 60)

        log(f"Total : {total}")
        log(f"OK    : {ok}")
        log(f"Erro  : {erro}")

        salvar_relatorio()

        return {
            "total": total,
            "ok": ok,
            "erro": erro
        }

    except Exception as e:

        log(f"ERRO: {e}")

        return {
            "total": 0,
            "ok": 0,
            "erro": 0,
            "exception": str(e)
        }

    finally:

        browser.close()
        p.stop()

        log("Navegador encerrado.")


if __name__ == "__main__":

    executar_monitor()