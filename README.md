# ScriptCase Monitor

Ferramenta automatizada para testes e validação de aplicações ScriptCase utilizando Python, Playwright e uma interface gráfica.

O projeto realiza o login no ambiente, prepara o contexto de execução, identifica as aplicações disponíveis, executa testes de abertura e valida o conteúdo das páginas procurando erros conhecidos.

O objetivo é facilitar a identificação de aplicações com problemas após atualizações, deploys ou manutenções, gerando logs, screenshots e um relatório consolidado dos erros encontrados. A aplicação também possui uma interface gráfica para centralizar a configuração e acompanhar a execução dos testes.

---

## Funcionalidades

- Login automático no ScriptCase

- Descoberta automática das aplicações

- Abertura automática das aplicações

- Validação do conteúdo das páginas

- Identificação de erros conhecidos

- Extração da mensagem de erro

- Extração de mensagens de erros SQL

- Suporte a erros Oracle

- Captura de screenshots configurável

- Geração de logs

- Relatório consolidado de aplicações com erro

- Configuração através de arquivos `.ini`

- Contexto de execução configurável

- Injeção de variáveis de contexto através de parâmetros de URL

---

## Como funciona

O monitor executa as aplicações seguindo o fluxo:

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

│   ├── config.py

│   ├── monitor_config.py

│   ├── context_config.py

│   ├── config.ini

│   ├── monitor.ini

│   └── context.ini

│

├── services/

│   ├── artifacts.py

│   ├── checker.py

│   ├── context_manager.py

│   ├── logger.py

│   ├── login.py

│   ├── report.py

│   └── scanner.py

│

├── validators/

│   └── page_validator.py

│

├── utils/

│   └── paths.py

│

├── logs/

├── screenshots/

│

├── main.py

└── requirements.txt

```

---

## Organização

| Diretório/Arquivo | Responsabilidade |

|---|---|

| **config/** | Configurações da aplicação e carregamento dos arquivos `.ini`. |

| **services/** | Regras de negócio e serviços responsáveis pela execução do monitor. |

| **validators/** | Validações realizadas sobre o conteúdo das páginas. |

| **utils/** | Utilitários compartilhados pelo projeto. |

| **logs/** | Logs gerados durante cada execução. |

| **screenshots/** | Capturas de tela das aplicações, conforme configuração. |

| **main.py** | Ponto de entrada e orquestração da execução. |

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

| `artifacts.py` | Gerencia screenshots e artefatos da execução. |

---

# Configuração

O projeto utiliza arquivos `.ini` para separar as configurações do ambiente, da execução e do contexto de testes.

---

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

---

## monitor.ini

Responsável pelas configurações da execução do monitor.

Exemplo:

```ini

[MONITOR]

MAX_APPS=0

ORDER=ASC

ONLY_ENABLED=True

[SCREENSHOT]

MODE=ERROR

```

### Configurações

| Configuração | Descrição |

|---|---|

| `MAX_APPS=0` | Testa todas as aplicações. |

| `MAX_APPS=N` | Limita a execução às primeiras `N` aplicações. |

| `ORDER=ASC` | Ordena as aplicações de forma crescente. |

| `ONLY_ENABLED=True` | Considera somente aplicações habilitadas. |

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

Para esses casos, o monitor possui um contexto de execução configurável.

O contexto permite definir variáveis que serão adicionadas à URL antes da abertura da aplicação.

---

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

As variáveis são configuráveis e não ficam fixas no código do monitor.

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

Isso permite preparar o ambiente de teste sem alterar o código-fonte.

---

# Validação de Erros

O monitor possui uma lista de padrões de erro conhecidos.

Exemplos:

```text

PHP Fatal Error

PHP Parse Error

Oracle Error

SQL Server

HTTP 500

```

A validação identifica o padrão encontrado e tenta extrair a mensagem correspondente.

Para erros SQL, o extrator pode recuperar mensagens mais completas, por exemplo:

```text

SQLState: 42000

Error Code: 102

Message: [Microsoft][ODBC Driver 17 for SQL Server]

[SQL Server]Incorrect syntax near ')'.

```

O objetivo é fornecer informações suficientes para facilitar a investigação sem precisar analisar manualmente cada aplicação.

---

# Relatório

Ao final da execução, o monitor gera um relatório contendo:

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

Tipo      : SQL Server

Mensagem  : SQLState: 42000 Error Code: 102 Message:

[Microsoft][ODBC Driver 17 for SQL Server][SQL Server]

Incorrect syntax near ')'.

```

---

# Logs

Cada execução possui seu próprio diretório de artefatos.

Exemplo:

```text

logs/

└── 2026-08-24_14-30-00-123456/

    ├── tester.log

    └── erros.txt

```

Isso permite manter os resultados de diferentes execuções separados.

---

# Screenshots

Quando habilitados, os screenshots também são separados por execução:

```text

screenshots/

└── 2026-08-24_14-30-00/

    ├── aplicacao1.png

    ├── aplicacao2.png

    └── aplicacao3.png

```

---

# Instalação

Clone o repositório:

```bash

git clone <url-do-repositorio>

```

Acesse a pasta:

```bash

cd scriptcase-monitor

```

Crie um ambiente virtual:

```bash

python -m venv .venv

```

Ative o ambiente virtual.

### Windows

```powershell

.venv\Scripts\activate

```

### Linux/macOS

```bash

source .venv/bin/activate

```

Instale as dependências:

```bash

pip install -r requirements.txt

```

Instale os navegadores do Playwright:

```bash

playwright install

```

Configure os arquivos:

```text

config/config.ini

config/monitor.ini

config/context.ini

```

---

# Execução

Execute o ScriptCase Tester:

```bash

python interface/app.py

```

---

# Saída da Execução

Ao término da execução serão gerados:

- Logs da execução

- Screenshots, conforme configuração

- Relatório de aplicações com erro

- Mensagens detalhadas dos erros encontrados

---

# Tecnologias

- Python 3

- Playwright

- ConfigParser

- pathlib

Tkinter

PyInstaller

---

# Roadmap

## Monitoramento

- [x] Login automático

- [x] Descoberta das aplicações

- [x] Validação automática

- [x] Identificação de erros conhecidos

- [x] Extração de mensagens de erro

- [x] Extração de erros SQL

- [x] Captura de screenshots

- [x] Geração de logs

- [x] Relatório de erros

- [x] Contexto de execução configurável

- [x] Variáveis de contexto por URL

## Melhorias futuras

- [ ] Interface gráfica para execução dos testes

- [ ] Interface para edição dos arquivos `.ini`

- [ ] Seleção das aplicações que serão testadas pela interface

- [ ] Configuração visual das variáveis de contexto

- [ ] Visualização dos resultados da execução na interface

- [ ] Relatório HTML

- [ ] Exportação para JSON

- [ ] Execução paralela

- [ ] Dashboard de resultados

---

# Interface Gráfica

Uma das próximas evoluções do projeto será a criação de uma interface gráfica para facilitar a utilização do monitor.

A interface deverá permitir, sem necessidade de editar arquivos manualmente:

- Iniciar uma execução

- Configurar parâmetros do monitor

- Alterar configurações de screenshot

- Ativar/desativar o contexto

- Cadastrar variáveis de contexto

- Alterar valores das variáveis

- Selecionar aplicações para teste

- Acompanhar o progresso da execução

- Visualizar os resultados

- Consultar os erros encontrados

A ideia é manter os arquivos `.ini` como mecanismo de configuração interno, enquanto a interface funcionará como uma camada visual sobre essas configurações.

---

# Licença

Este projeto está licenciado sob a licença MIT.