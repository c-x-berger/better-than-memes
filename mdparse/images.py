from urllib.parse import urlparse

from markdown import Extension
from markdown.treeprocessors import Treeprocessor

"""
Flagrantly stolen from https://github.com/Python-Markdown/markdown/wiki/Tutorial-Altering-Markdown-Rendering
"""


class ImageCleaner(Treeprocessor):
    def run(self, root):
        for element in root.iter("img"):
            attrib = element.attrib
            if urlparse(attrib["src"]).netloc:
                tail = element.tail
                element.clear()
                element.tag = "a"
                element.set("href", attrib.pop("src"))
                element.text = attrib.pop("alt")
                element.tail = tail
                for k, v in attrib.items():
                    element.set(k, v)


class ImageExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(ImageCleaner(md), "inlineimageprocessor", 15)
