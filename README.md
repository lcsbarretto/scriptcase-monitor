# ScriptCase Monitor

Monitor automatizado para validação de aplicações ScriptCase utilizando Playwright.

O projeto realiza o login no ambiente, identifica automaticamente as aplicações disponíveis, executa testes de abertura e validação das telas, identifica erros conhecidos e gera um relatório técnico da execução, facilitando a validação do sistema após atualizações, deploys e manutenções.

---

# Funcionalidades

- Login automático no ScriptCase
- Descoberta automática das aplicações
- Abertura automática das aplicações
- Validação do conteúdo carregado
- Identificação automática de erros conhecidos
- Extração inteligente das mensagens de erro
- Captura de screenshots (configurável)
- Geração de logs da execução
- Relatório técnico das aplicações com erro
- Configuração através de arquivos `.ini`

---

# Estrutura do Projeto

```text
scriptcase-monitor/
│
├── config/
│   ├── config.py
│   ├── monitor_config.py
│   ├── config.ini
│   └── monitor.ini
│
├── services/
│   ├── artifacts.py
│   ├── checker.py
│   ├── logger.py
│   ├── login.py
│   ├── report.py
│   └── scanner.py
│
├── validators/
│   ├── extractors.py
│   └── page_validator.py
│
├── utils/
│   └── paths.py
│
├── logs/
├── screenshots/
│
├── main.py
└── requirements.txt
```

---

# Organização

| Diretório | Responsabilidade |
|-----------|------------------|
| **config/** | Arquivos de configuração da aplicação e carregamento das configurações. |
| **services/** | Implementação das regras de negócio, incluindo login, descoberta das aplicações, abertura das telas, geração de relatórios, logs e gerenciamento dos artefatos da execução. |
| **validators/** | Responsável por validar as páginas abertas, identificar erros conhecidos e extrair mensagens detalhadas para o relatório técnico. |
| **utils/** | Utilitários compartilhados entre os módulos, como gerenciamento dos caminhos da aplicação. |
| **logs/** | Logs e relatórios gerados durante cada execução. |
| **screenshots/** | Capturas de tela geradas conforme configuração da execução. |
| **main.py** | Ponto de entrada responsável por orquestrar toda a execução do monitor. |

---

# Arquitetura da Validação

O monitor foi desenvolvido utilizando responsabilidades bem definidas, facilitando sua manutenção e evolução.

```text
Scanner
    │
    ▼
Checker
    │
    ▼
Page Validator
    │
    ▼
Extractors
    │
    ▼
Report
```

Cada módulo possui uma responsabilidade específica:

- **Scanner** → Descobre automaticamente as aplicações do ScriptCase.
- **Checker** → Abre cada aplicação utilizando o Playwright.
- **Page Validator** → Identifica padrões de erro conhecidos.
- **Extractors** → Extrai mensagens detalhadas para cada categoria de erro.
- **Report** → Consolida os resultados e gera o relatório técnico da execução.

---

# Configuração

## config.ini

Arquivo responsável pelas configurações de acesso ao ambiente ScriptCase.

Exemplo:

```ini
[SCRIPTCASE]
URL=https://localhost/scriptcase
BASE_URL=https://localhost/scriptcase/app
APP_PATH=C:\NetMake\v9-php81\wwwroot\scriptcase\app

USUARIO=admin
SENHA=admin

HEADLESS=True
TIMEOUT=10000
```

---

## monitor.ini

Arquivo responsável pelas configurações da execução.

Exemplo:

```ini
[MONITOR]
MAX_APPS=0
ORDER=ASC
ONLY_ENABLED=True

[SCREENSHOT]
MODE=ERROR
```

---

## Configurações disponíveis

### MONITOR

| Configuração | Descrição |
|--------------|-----------|
| MAX_APPS | Limita a quantidade de aplicações testadas. `0` testa todas. |
| ORDER | Ordem da execução (`ASC` ou `DESC`). |
| ONLY_ENABLED | Executa apenas aplicações habilitadas. |

---

### SCREENSHOT

| Valor | Descrição |
|--------|-----------|
| NONE | Não gera screenshots. |
| ERROR | Gera screenshots apenas para aplicações com erro. |
| ALL | Gera screenshots de todas as aplicações. |

---

# Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
```

Entre na pasta do projeto:

```bash
cd scriptcase-monitor
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

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

---

# Execução

Execute o monitor utilizando:

```bash
python main.py
```

---

# Saída da Execução

Ao término da execução são gerados:

- Log completo da execução
- Screenshots (conforme configuração)
- Relatório técnico (`erros.txt`)

Exemplo:

```text
============================================================
SCRIPTCASE MONITOR
============================================================

Total de aplicações : 320
Sucesso             : 318
Erros               : 2

============================================================
APLICAÇÕES COM ERRO
============================================================

Aplicação : cnsEmpresa

Categoria : Erro no SQL

Tipo      : SQL Server

Mensagem:
Incorrect syntax near ')'.

select *
from TBEMPRESA
where (CODIEMPR =)

------------------------------------------------------------
```

---

# Erros Identificados

Atualmente o monitor identifica automaticamente:

- PHP Fatal Error
- PHP Parse Error
- Oracle Error
- SQL Server
- HTTP 500

A arquitetura permite adicionar facilmente novos validadores e extratores de erro.

---

# Tecnologias

- Python 3
- Playwright
- ConfigParser
- pathlib
- Git

---

# Roadmap

## Concluído

- [x] Login automático
- [x] Descoberta automática das aplicações
- [x] Abertura automática das telas
- [x] Validação das aplicações
- [x] Captura de screenshots
- [x] Geração de logs
- [x] Relatório técnico de erros
- [x] Arquitetura de extratores de erro
- [x] Organização do projeto em módulos

## Próximas evoluções

- [ ] Melhorar extração de mensagens SQL Server
- [ ] Melhorar extração de mensagens Oracle
- [ ] Extratores específicos para erros PHP
- [ ] Dashboard de resultados
- [ ] Comparação entre execuções
- [ ] Histórico de validações

---

# Licença

Este projeto está licenciado sob a licença MIT.