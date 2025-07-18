import locale
import json
from pathlib import Path

LANG_DIR = Path(__file__).parent
DEFAULT_LANG = "en"


def get_system_lang():
    lang, _ = locale.getdefaultlocale()
    return (lang or DEFAULT_LANG).split("_")[0]


def load_translations(lang=None):
    lang = lang or get_system_lang()
    filename = f"{lang}.json"
    path = LANG_DIR / filename

    if not path.exists():
        path = LANG_DIR / f"{DEFAULT_LANG}.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
