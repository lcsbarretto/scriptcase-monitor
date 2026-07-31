# ScriptCase Monitor

Monitor automatizado para validação de aplicações ScriptCase utilizando Playwright.

O projeto realiza o login no ambiente, identifica as aplicações disponíveis, executa testes de abertura e registra os resultados da execução, facilitando a identificação de aplicações com problemas após atualizações, deploys ou manutenções.

---

## ✨ Funcionalidades

- Login automático no ScriptCase
- Descoberta automática das aplicações
- Abertura de cada aplicação
- Validação da página carregada
- Captura de screenshots (configurável)
- Geração de logs
- Relatório de aplicações com erro
- Configuração através de arquivos `.ini`

---

## 📁 Estrutura do Projeto

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

### Organização

| Diretório | Responsabilidade |
|-----------|------------------|
| **config/** | Arquivos de configuração da aplicação e carregamento das configurações. |
| **services/** | Implementação das regras de negócio, incluindo login, descoberta das aplicações, validação, geração de relatórios, logs e gerenciamento dos artefatos da execução. |
| **validators/** | Regras responsáveis por validar se uma aplicação foi carregada corretamente. |
| **utils/** | Utilitários compartilhados entre os módulos, como gerenciamento de caminhos do projeto. |
| **logs/** | Logs gerados durante cada execução. |
| **screenshots/** | Capturas de tela geradas durante a validação das aplicações. |
| **main.py** | Ponto de entrada da aplicação e responsável por orquestrar toda a execução do monitor. |

---

## ⚙️ Configuração

### config.ini

Arquivo responsável pelas configurações de acesso ao ambiente ScriptCase.

Exemplo:

```ini
[LOGIN]
URL=
USERNAME=
PASSWORD=
```

---

### monitor.ini

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

### Modos de Screenshot

| Valor | Descrição |
|--------|-----------|
| `NONE` | Não gera screenshots. |
| `ERROR` | Gera screenshots apenas em aplicações com erro. |
| `ALL` | Gera screenshots de todas as aplicações. |

---

## 🚀 Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
```

Acesse a pasta do projeto:

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

## ▶️ Execução

Execute o monitor utilizando:

```bash
python main.py
```

---

## 📄 Saída da Execução

Ao término da execução serão gerados:

- Logs da execução
- Screenshots (conforme configuração)
- Relatório contendo as aplicações que apresentaram erro

---

## 🛠️ Tecnologias

- Python 3
- Playwright
- ConfigParser
- pathlib

---

## 📌 Roadmap

- [x] Login automático
- [x] Descoberta das aplicações
- [x] Validação automática
- [x] Captura de screenshots
- [x] Geração de logs
- [x] Relatório de erros
- [ ] Relatório HTML
- [ ] Exportação para JSON
- [ ] Execução paralela
- [ ] Dashboard de resultados

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT.