POSTGRES_CONFIG = {
    "user": "root",
    "pass": "toor",
    "host": "localhost",
    "port": 5432,
    "database": "bettermemes",
}
SECRET_KEY = "a very secret string"
MARKDOWN_EXTENSIONS = [
    "markdown.extensions.fenced_code",
    "markdown.extensions.tables",
    ImageExtension(),
]
