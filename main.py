from services.logger import log
from services.report import salvar_relatorio
import importlib


def executar_monitor(progresso_callback=None):

    # ==========================================================
    # INICIA UMA NOVA EXECUÇÃO
    # ==========================================================

    from services.artifacts import iniciar_execucao
    from services import report

    iniciar_execucao()
    report.ERROS.clear()
    report.SUCESSOS.clear()
    # ==========================================================
    # RECARREGA AS CONFIGURAÇÕES ATUAIS
    # ==========================================================

    import config.config
    import config.monitor_config
    import config.context_config

    import services.login
    import services.scanner
    import services.context_manager
    import services.checker

    importlib.reload(
        config.config
    )

    importlib.reload(
        config.monitor_config
    )

    importlib.reload(
        config.context_config
    )

    # ==========================================================
    # RECARREGA OS SERVIÇOS
    # ==========================================================

    importlib.reload(
        services.login
    )

    importlib.reload(
        services.scanner
    )

    importlib.reload(
        services.context_manager
    )

    importlib.reload(
        services.checker
    )

    # ==========================================================
    # IMPORTA AS CONFIGURAÇÕES ATUALIZADAS
    # ==========================================================

    from config.config import APP_PATH

    # ==========================================================
    # IMPORTA OS SERVIÇOS ATUALIZADOS
    # ==========================================================

    from services.login import realizar_login
    from services.scanner import listar_aplicacoes
    from services.context_manager import preparar_contexto
    from services.checker import testar_aplicacao

    # ==========================================================
    # INÍCIO DA EXECUÇÃO
    # ==========================================================

    log("=" * 60)
    log("INICIANDO SCRIPTCASE TESTER")
    log("=" * 60)

    p, browser, context, page = realizar_login()

    try:

        # ======================================================
        # PREPARA O CONTEXTO
        # ======================================================

        preparar_contexto(
            page,
            context
        )

        # ======================================================
        # DESCOBRE AS APLICAÇÕES
        # ======================================================

        apps = listar_aplicacoes(
            APP_PATH
        )

        total = len(apps)

        ok = 0
        erro = 0

        log(
            f"Foram encontradas {total} aplicações."
        )

        # ======================================================
        # INFORMA INÍCIO DO PROGRESSO
        # ======================================================

        if progresso_callback:

            progresso_callback(
                atual=0,
                total=total,
                aplicacao=None,
                ok=ok,
                erro=erro
            )

        # ======================================================
        # TESTA CADA APLICAÇÃO
        # ======================================================

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

            # ==================================================
            # ATUALIZA PROGRESSO
            # ==================================================

            if progresso_callback:

                progresso_callback(
                    atual=indice,
                    total=total,
                    aplicacao=app,
                    ok=ok,
                    erro=erro
                )

        # ======================================================
        # RESUMO
        # ======================================================

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

        log(
            f"ERRO: {e}"
        )

        return {
            "total": 0,
            "ok": 0,
            "erro": 0,
            "exception": str(e)
        }

    finally:

        browser.close()
        p.stop()

        log(
            "Navegador encerrado."
        )


if __name__ == "__main__":

    executar_monitor()