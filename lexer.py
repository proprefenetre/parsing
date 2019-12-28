import regex as re
from collections import namedtuple


Token = namedtuple("Token", ["span", "type", "value"])


def lexer(tokens):

    pattern = re.compile("|".join(tokens))

    def tokenize(text):
        scanner = pattern.scanner(text)
        for m in iter(scanner.match, None):
            t = Token(m.span(), m.lastgroup, m.group())
            if t.type not in ("WS"):
                yield t

    return tokenize


if __name__ == "__main__":

    tokens = [
        r"(?P<WORD>\w+)",
        r"(?P<DQUOTE>\")",
        r"(?P<SQUOTE>')",
        r"(?P<PUNCT>[[:punct:]])",
        r"(?P<WS>\s+)",
    ]

    lex = lexer(tokens)
    test = "lex this, and this! Also, this is 'quoted'."

    for i in lex(test):
        print(i)
