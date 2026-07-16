"""
src/utils.py
Funciones auxiliares reutilizables para ToDo.
"""

from datetime import datetime
from uuid import uuid4
import re


DATE_FMT = "%Y-%m-%d"
DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


def today():
    return datetime.now().strftime(DATE_FMT)


def now():
    return datetime.now().strftime(DATETIME_FMT)


def generate_uuid():
    return str(uuid4())


def slugify(text):
    text = str(text).strip().lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9áéíóúüñ\-]", "", text)
    return text


def sanitize_text(text):
    if text is None:
        return ""
    return str(text).strip()


def progress_to_int(value):
    try:
        value = int(value)
    except Exception:
        value = 0

    return max(0, min(100, value))


def format_date(value, in_fmt=DATE_FMT, out_fmt="%d/%m/%Y"):
    if not value:
        return ""
    return datetime.strptime(value, in_fmt).strftime(out_fmt)


def parse_date(value, fmt=DATE_FMT):
    return datetime.strptime(value, fmt)


def is_empty(value):
    return value is None or str(value).strip() == ""


if __name__ == "__main__":
    print("Hoy:", today())
    print("Ahora:", now())
    print("UUID:", generate_uuid())
    print("Slug:", slugify("Mi Primera Tarea"))
