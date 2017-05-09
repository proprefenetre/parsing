import re
from collections import namedtuple

tokens = [
        # r"(?P<WORD>[^\"\'{}\[\](),\n ]+)",
        r"(?P<WORD>\w+)",
        r"(?P<COMMA>,)",
        r"(?P<LPAREN>\()",
        r"(?P<RPAREN>\))",
        r"(?P<WS>\s+)",
        ]

def lex(tokens):

    Token = namedtuple("Token", ["span", "type", "value"])
    pattern = re.compile("|".join(tokens))

    def tokenize(text):
        scanner = pattern.scanner(text)
        for m in iter(scanner.match, None):
            t = Token(m.span(), m.lastgroup, m.group())
            if t.type not in ('WS'):
                yield t

    return tokenize

if __name__ == "__main__":
    from pprint import pprint

    lexer = lex(tokens)
    test = "lex this"

    pprint([t for t in lexer(test)])

    
