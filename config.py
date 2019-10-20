import bleach

from mdparse.images import ImageExtension

POSTGRES_CONFIG = {
    "user": "root",
    "pass": "toor",
    "host": "localhost",
    "port": 5432,
    "database": "bettermemes",
}
SECRET_KEY = "a very secret string"
ALLOWED_HTML = (
    bleach.ALLOWED_TAGS
    + ["p", "pre", "br", "table", "thead", "tr", "th", "tbody", "td"]
    + ["h{}".format(n) for n in range(1, 7)]
)
MARKDOWN_EXTENSIONS = [
    "markdown.extensions.fenced_code",
    "markdown.extensions.tables",
    ImageExtension(),
]
