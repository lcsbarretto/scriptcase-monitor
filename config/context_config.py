from configparser import ConfigParser
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

config = ConfigParser()
config.read(BASE_DIR / "context.ini", encoding="utf-8")


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