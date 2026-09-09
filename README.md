# ScriptCase Tester

Ferramenta para automação de testes e validação de aplicações ScriptCase utilizando Python e Playwright.

O projeto realiza o login no ambiente, identifica as aplicações disponíveis, executa testes de abertura e valida o conteúdo das páginas procurando erros conhecidos.

O objetivo é facilitar a identificação de aplicações com problemas após atualizações, deploys ou manutenções, gerando logs, screenshots e um relatório consolidado dos erros encontrados.

---

## Funcionalidades

- Login automático no ScriptCase
- Descoberta automática das aplicações
- Abertura automática das aplicações
- Validação do conteúdo das páginas
- Identificação de erros conhecidos
- Extração de mensagens de erro
- Extração de mensagens de erros SQL
- Suporte a erros Oracle
- Captura de screenshots configurável
- Geração de logs
- Relatório consolidado de aplicações com erro
- Configuração através de arquivos `.ini`
- Contexto de execução configurável
- Injeção de variáveis de contexto através de parâmetros de URL
- Interface gráfica para configuração e execução dos testes
- Execução em modo Headless
- Separação de logs e screenshots por execução

---

## Como funciona

O ScriptCase Tester executa as aplicações seguindo o fluxo:

```text
Login
  ↓
Preparação do contexto
  ↓
Descoberta das aplicações
  ↓
Abertura das aplicações
  ↓
Validação da página
  ↓
Extração do erro
  ↓
Screenshot (quando configurado)
  ↓
Relatório
```

---

## Estrutura do Projeto

```text
scriptcase-monitor/
│
├── config/
│   ├── config.py
│   ├── monitor_config.py
│   ├── context_config.py
│   ├── config.ini
│   ├── monitor.ini
│   └── context.ini
│
├── services/
│   ├── artifacts.py
│   ├── checker.py
│   ├── context_manager.py
│   ├── logger.py
│   ├── login.py
│   ├── report.py
│   └── scanner.py
│
├── validators/
│   └── page_validator.py
│
├── utils/
│   └── paths.py
│
├── interface/
│   └── app.py
│
├── logs/
├── screenshots/
├── main.py
└── requirements.txt
```

---

## Organização

| Diretório/Arquivo | Responsabilidade |
|---|---|
| `config/` | Configurações da aplicação e carregamento dos arquivos `.ini`. |
| `services/` | Regras de negócio e serviços responsáveis pela execução dos testes. |
| `validators/` | Validações realizadas sobre o conteúdo das páginas. |
| `utils/` | Utilitários compartilhados pelo projeto. |
| `interface/` | Interface gráfica para configuração e execução dos testes. |
| `logs/` | Logs gerados durante cada execução. |
| `screenshots/` | Capturas de tela das aplicações, conforme configuração. |
| `main.py` | Ponto de entrada e orquestração da execução. |

### Principais serviços

| Serviço | Responsabilidade |
|---|---|
| `login.py` | Realiza o login e inicializa o navegador Playwright. |
| `scanner.py` | Identifica as aplicações disponíveis para teste. |
| `checker.py` | Abre e executa a validação de cada aplicação. |
| `context_manager.py` | Prepara o contexto de execução antes dos testes. |
| `page_validator.py` | Identifica padrões de erro e extrai suas mensagens. |
| `report.py` | Registra sucessos, erros e gera o relatório. |
| `logger.py` | Registra os eventos da execução. |
| `artifacts.py` | Gerencia screenshots e artefatos de cada execução. |

---

# Configuração

O projeto utiliza arquivos `.ini` para separar as configurações do ambiente, da execução e do contexto de testes.

## config.ini

Responsável pelas configurações principais do ambiente ScriptCase.

Exemplo:

```ini
[SCRIPTCASE]

URL=
APP_PATH=
BASE_URL=
USUARIO=
SENHA=
HEADLESS=True
TIMEOUT=10000
LOG_PATH=logs
SCREENSHOT_PATH=screenshots
SCREENSHOT_MODE=ERROR
```

> Não versionar credenciais reais no repositório.

### Principais configurações

| Configuração | Descrição |
|---|---|
| `URL` | URL utilizada para acesso ao ambiente. |
| `APP_PATH` | Caminho das aplicações que serão identificadas pelo scanner. |
| `BASE_URL` | URL base utilizada para abertura das aplicações. |
| `USUARIO` | Usuário utilizado no login. |
| `SENHA` | Senha utilizada no login. |
| `HEADLESS` | Define se o navegador será executado sem interface gráfica. |
| `TIMEOUT` | Tempo limite das operações do Playwright. |

---

## monitor.ini

Responsável pelas configurações da execução dos testes.

Exemplo:

```ini
[MONITOR]

MAX_APPS=0
ORDER=ASC
ONLY_ENABLED=True

[FILTROS]

cnsEmpresas=True
cnsColaboradores=True
frmCadastro=False

[SCREENSHOT]

MODE=ERROR
```

### Configurações

| Configuração | Descrição |
|---|---|
| `MAX_APPS=0` | Testa todas as aplicações encontradas. |
| `MAX_APPS=N` | Limita a execução às primeiras `N` aplicações. |
| `ORDER=ASC` | Ordena as aplicações de forma crescente. |
| `ORDER=DESC` | Ordena as aplicações de forma decrescente. |
| `ONLY_ENABLED=True` | Considera somente aplicações habilitadas nos filtros. |

### Filtros

Os filtros ficam na seção `[FILTROS]`.

Formato:

```ini
nome_da_aplicacao=True
```

ou:

```ini
nome_da_aplicacao=False
```

Isso permite controlar quais aplicações serão consideradas sem alterar o código-fonte.

### Modos de Screenshot

| Valor | Descrição |
|---|---|
| `NONE` | Não gera screenshots. |
| `ERROR` | Gera screenshots apenas para aplicações com erro. |
| `ALL` | Gera screenshots de todas as aplicações. |

---

# Contexto de Execução

Algumas aplicações podem depender de informações previamente carregadas na sessão ou de parâmetros utilizados durante a navegação normal do sistema.

Quando uma aplicação é acessada diretamente, esses valores podem não estar disponíveis, causando erros de execução ou consultas SQL inválidas.

Para esses casos, o ScriptCase Tester possui um contexto de execução configurável.

O contexto permite definir variáveis que serão adicionadas à URL antes da abertura da aplicação.

## context.ini

Exemplo:

```ini
[CONTEXT]

ENABLED=True
MODE=URL

[VARIABLES]

var_codiempr=1
var_codibene=1
var_codicolab=1
```

### Configurações

| Configuração | Descrição |
|---|---|
| `ENABLED=False` | Desativa a preparação do contexto. |
| `ENABLED=True` | Ativa a preparação do contexto. |
| `MODE=URL` | Adiciona as variáveis como parâmetros da URL. |

As variáveis permanecem configuráveis no arquivo `context.ini` e não ficam fixas no código do projeto.

Por exemplo:

```ini
[VARIABLES]

var_codiempr=15
var_codibene=8
var_codicolab=25
```

pode resultar em uma URL semelhante a:

```text
https://servidor/app/tela/tela.php?var_codiempr=15&var_codibene=8&var_codicolab=25
```

---

# Interface Gráfica

O projeto possui uma interface gráfica desenvolvida com Tkinter para facilitar a configuração e execução dos testes.

A interface está dividida em três áreas principais:

### Ambiente

Permite configurar:

- URL
- App Path
- Base URL
- Usuário
- Senha
- Modo Headless
- Timeout

### Monitor

Permite configurar:

- Quantidade máxima de aplicações
- Ordem de execução
- Aplicações habilitadas
- Modo de screenshots
- Filtros das aplicações

### Contexto

Permite:

- Ativar ou desativar o contexto
- Visualizar o modo configurado
- Visualizar as variáveis configuradas

As variáveis de contexto continuam armazenadas no `context.ini`; a interface não exige que cada variável seja cadastrada individualmente.

A interface também apresenta o progresso da execução e o resultado consolidado dos testes.

---

# Validação de Erros

O ScriptCase Tester possui uma lista de padrões de erro conhecidos.

Exemplos:

```text
PHP Fatal Error
PHP Parse Error
Oracle Error
SQL Server
HTTP 500
```

A validação identifica o padrão encontrado e tenta extrair a mensagem correspondente.

Para erros SQL Server, o extrator pode recuperar mensagens mais completas, por exemplo:

```text
SQLState: 42000
Error Code: 102
Message: [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Incorrect syntax near ')'.
```

O objetivo é fornecer informações suficientes para facilitar a investigação sem precisar analisar manualmente cada aplicação.

---

# Relatório

Ao final da execução, o ScriptCase Tester gera um relatório contendo:

```text
Total de aplicações
Sucesso
Erros
```

Para cada aplicação com erro:

```text
Aplicação
Categoria
Tipo
Mensagem
```

Exemplo:

```text
Aplicação : cnsCodinsGrupoRep
Categoria : Erro no SQL
Tipo      : SQL Server
Mensagem  : SQLState: 42000 Error Code: 102 Message: [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Incorrect syntax near ')'.
```

---

# Logs

Cada execução possui seu próprio diretório de artefatos.

Exemplo:

```text
logs/
└── 2026-09-09_11-30-00-123456/
    └── tester.log
```

O relatório de erros também é salvo no diretório da execução:

```text
logs/
└── 2026-09-09_11-30-00-123456/
    ├── tester.log
    └── erros.txt
```

Isso permite manter os resultados de diferentes execuções separados, inclusive quando várias execuções são realizadas durante o mesmo uso da interface.

---

# Screenshots

Quando habilitados, os screenshots também são separados por execução:

```text
screenshots/
└── 2026-09-09_11-30-00-123456/
    ├── aplicacao1.png
    ├── aplicacao2.png
    └── aplicacao3.png
```

---

# Instalação

## Ambiente de desenvolvimento

Em uma máquina nova, após clonar o repositório, recomenda-se criar um ambiente virtual próprio para o projeto.

### Windows

```powershell
git clone <URL_DO_REPOSITORIO>
cd scriptcase-monitor

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python -m playwright install chromium

python interface/app.py
```

### Linux/macOS

```bash
git clone <URL_DO_REPOSITORIO>
cd scriptcase-monitor

python -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
python -m playwright install chromium

python interface/app.py
```

> **Importante:** o `requirements.txt` instala a biblioteca Python do Playwright, mas o navegador Chromium precisa ser instalado separadamente com `python -m playwright install chromium`.

> Recomenda-se utilizar `python -m pip` e `python -m playwright` para garantir que os comandos sejam executados pelo Python do ambiente virtual `.venv`.

Após a instalação, configure:

```text
config/config.ini
config/monitor.ini
config/context.ini
```

---

# Execução

Para executar a interface gráfica:

```bash
python interface/app.py
```

A execução também pode ser iniciada diretamente pelo código principal:

```bash
python main.py
```

---

# Execução como aplicativo

O projeto pode ser distribuído como executável utilizando PyInstaller.

A distribuição recomendada é no formato `onedir`, mantendo os arquivos de configuração externos e editáveis.

Estrutura esperada:

```text
ScriptCaseTester/
├── ScriptCaseTester.exe
├── config/
│   ├── config.ini
│   ├── monitor.ini
│   └── context.ini
└── _internal/
    └── ...
```

Os arquivos `.ini` devem permanecer externos ao executável para que as configurações possam ser alteradas sem recompilar a aplicação.

Os artefatos gerados durante a execução permanecem separados:

```text
ScriptCaseTester/
├── logs/
└── screenshots/
```

O navegador Chromium utilizado pelo Playwright também precisa estar presente na distribuição gerada pelo processo de build.

---

# Controle de versão

Arquivos gerados durante o desenvolvimento ou pela compilação não devem ser versionados.

Exemplos:

```gitignore
.venv/
__pycache__/
*.py[cod]
logs/
screenshots/
.vscode/
dist/
build/
*.spec
```

O diretório `dist/`, o diretório `build/` e arquivos `.spec` são utilizados no processo de build/distribuição e não fazem parte do código-fonte necessário para executar o projeto em modo de desenvolvimento.

---

# Tecnologias

- Python 3
- Playwright
- Tkinter
- ConfigParser
- pathlib
- PyInstaller

---

# Status do Projeto

O projeto encontra-se **funcionalmente concluído**.

As principais funcionalidades planejadas foram implementadas:

- [x] Login automático
- [x] Descoberta das aplicações
- [x] Validação automática
- [x] Identificação de erros conhecidos
- [x] Extração de mensagens de erro
- [x] Extração de erros SQL
- [x] Suporte a erros Oracle
- [x] Captura de screenshots
- [x] Geração de logs
- [x] Relatório de erros
- [x] Contexto de execução configurável
- [x] Variáveis de contexto por URL
- [x] Interface gráfica
- [x] Configuração através da interface
- [x] Execução em modo Headless
- [x] Separação de artefatos por execução
- [x] Distribuição como executável

A partir deste ponto, novas alterações tendem a ser voltadas principalmente para **correção de bugs, manutenção e ajustes pontuais**.

---

# Licença

Este projeto está licenciado sob a licença MIT.
