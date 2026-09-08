from configparser import ConfigParser

from utils.paths import CONFIG_DIR


CONFIG_FILE = CONFIG_DIR / "context.ini"

config = ConfigParser()
config.read(CONFIG_FILE, encoding="utf-8")


CONTEXT_ENABLED = config.getboolean(
    "CONTEXT",
    "ENABLED",
    fallback=False
)

CONTEXT_MODE = config.get(
    "CONTEXT",
    "MODE",
    fallback="VARIABLES"
).upper()


CONTEXT_VARIABLES = {}

if config.has_section("VARIABLES"):
    for nome, valor in config.items("VARIABLES"):
        CONTEXT_VARIABLES[nome] = valor