from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

DEL_RE = r"(~~)(.*?)~~"


class StrikeoutExtension(Extension):
    def extendMarkdown(self, md: Markdown):
        del_tag = SimpleTagPattern(DEL_RE, "del")
        md.inlinePatterns.add("del", del_tag, ">not_strong")
