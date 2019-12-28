#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lexer import lexer


class BaseParser:
    def __init__(self, token_expressions, accepted_tokens=None):
        self.lex = lexer(token_expressions)
        self.stream = None
        self.current = None
        self.lookahead = None
        self.accepted_tokens = accepted_tokens

    def _consume(self):
        self.current, self.lookahead = self.lookahead, next(self.stream, None)

    def match(self, *ttype):
        if self.lookahead and self.lookahead.type in ttype:
            self._consume()
            return True
        else:
            msg = f"expecting {ttype}"
            if self.lookahead:
                msg = msg + f"; found {self.lookahead.type} at {self.lookahead.span}: '{self.lookahead.value}'"
            raise SyntaxError(msg)

    def parse(self, string):
        self.stream = self.lex(string)
        self._consume()
        return getattr(self, self.entry)()


class ListParser(BaseParser):

    """Python-like lists (with parentheses instead of brackets)"""

    # list := '(' elements ')'

    # elements := atom (',' atom )*

    # atom := ID
    #          | STR
    #          | NUM
    #          | list

    entry = "list"

    def list(self):
        self.match("LPAREN")
        val = self.elements()
        self.match("RPAREN")
        return val

    def elements(self):
        val = []
        val.append(self.atom())
        while self.lookahead.type == "COMMA":
            self.match("COMMA")
            val.append(self.atom())
        return val

    def atom(self):
        if self.lookahead.type in self.accepted_tokens:
            self.match(self.accepted_tokens)
            return self.current.value
        elif self.lookahead.type == "NUM":
            self.match("NUM")
            return int(self.current.value)
        elif self.lookahead.type == "LPAREN":
            return self.list()
        else:
            raise SyntaxError(f"expecting 'name' or 'list'; found {self.lookahead}")


class SexprParser(ListParser):

    """
    sexpr := '(' elements ')'

    elements := atom ( atom )*

    atom := ID | NUM

    """
    tokens = [
        r"(?P<ID>[a-zA-Z\-]+)",
        r"(?P<ADD>\+)",
        r"(?P<SUB>\-)",
        r"(?P<MUL>\*)",
        r"(?P<DIV>\\)",
        r"(?P<NUM>\d+)",
        r"(?P<LPAREN>\()",
        r"(?P<RPAREN>\))",
        r"(?P<WS>\s+)",
    ]

    ttypes = ("ID", "NUM", "ADD")

    entry = "sexpr"

    def __init__(self):
        super().__init__(self.tokens, self.ttypes)

    def sexpr(self):
        self.match("LPAREN")
        val = self.elements()
        self.match("RPAREN")
        return val

    def elements(self):
        val = [self.atom()]
        while self.lookahead and self.lookahead.type != "RPAREN":
            val.append(self.atom())
        return val

    def atom(self):
        if self.lookahead.type in self.accepted_tokens:
            self.match(*self.accepted_tokens)
            if self.current.type == "NUM":
                return int(self.current.value)
            else:
                return self.current.value
        elif self.match("LPAREN"):
            val = self.elements()
            self.match("RPAREN")
            return val


class StringParser(BaseParser):

    """
    string := DQUOTE | SQUOTE elements DQUOTE | SQUOTE

    elements := atom ( atom )*

    atom := WORD | PUNCT

    """

    tokens = [
        r"(?P<WORD>\w+)",
        r"(?P<DQUOTE>\")",
        r"(?P<SQUOTE>')",
        r"(?P<PUNCT>[[:punct:]])",
        r"(?P<WS>\s+)",
    ]

    ttypes = ["WORD", "PUNCT", "WS"]

    entry = "string"

    def __init__(self):
        super().__init__(self.tokens, self.ttypes)

    def string(self):
        self.match("DQUOTE", "SQUOTE")
        self.qtype = self.current.type
        val = self.elements()
        self.match(self.qtype)
        return val

    def elements(self):
        val = []
        val.append(self.atom())
        while self.lookahead.type not in ("DQUOTE", "SQUOTE"):
            val.append(self.atom())
        return val

    def atom(self):
        if self.lookahead.type in self.accepted_tokens:
            self.match(*self.accepted_tokens)
            return self.current.value
        elif self.lookahead.type == self.qtype:
            return self.string()
        else:
            raise SyntaxError(f"Invalid syntax")


if __name__ == "__main__":

    sexpr_tests = ["(this list)",
                   "(this list (of lists))",
                   "(this (nested (list of lists)))",
                   "(1 + 1)"]

    sexpr_parser = SexprParser()
    for test in sexpr_tests:
        print("Lists: ", sexpr_parser.parse(test))

    string_tests = ["\"Lorem ipsum dolor sit amet, consectetuer\"", "'Cum sociis natoque penatibus et magnis dis parturient montes'"]

    string_parser = StringParser()
    for test in string_tests:
        print("String: ", string_parser.parse(test))
