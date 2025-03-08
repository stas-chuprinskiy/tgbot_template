from enum import Enum


class BotParseMode(str, Enum):
    HTML = "HTML"
    MARKDOWN = "MARKDOWN"
    MARKDOWNV2 = "MARKDOWNV2"
