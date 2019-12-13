import bleach

from mdparse.extra_markdown import StrikeoutExtension
from mdparse.images import ImageExtension

ID_LENGTH = 7
POSTGRES_CONFIG = {
    "user": "root",
    "pass": "toor",
    "host": "localhost",
    "port": 5432,
    "database": "bettermemes",
}
SECRET_KEY = "a very secret string"
ALLOWED_HTML = bleach.ALLOWED_TAGS
ALLOWED_HTML.extend(
    ["del", "p", "pre", "br", "table", "thead", "tr", "th", "tbody", "td"]
)
ALLOWED_HTML.extend(["h{}".format(n) for n in range(1, 7)])
MARKDOWN_EXTENSIONS = [
    "markdown.extensions.fenced_code",
    "markdown.extensions.tables",
    StrikeoutExtension(),
    ImageExtension(),
]
