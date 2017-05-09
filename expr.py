#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lexer import lex
from parser import ListParser, SexprParser
from pprint import pprint


tokens = [
    r"(?P<COMMENT>\<--)",
    r"(?P<NUM>[0-9]+)",
    r"(?P<ID>[a-zA-Z0-9_-]+)",
    r"(?P<COMMA>,)",
    r"(?P<SQUOTE>\')",
    r"(?P<DQUOTE>\")",
    r"(?P<LPAREN>\()",
    r"(?P<RPAREN>\))",
    # r"(?P<NL>\n)",
    r"(?P<WS>\s+)",]

S = SexprParser(tokens)

class Expr:

    def __init__(self, seq):
        self.head = seq[0]
        self.tail = seq[1:][0]

    def __repr__(self):
        return f"{self.head}: {self.tail}"
    

ast = []
with open('test.md', 'r') as tf:
    for x in tf.readlines():
        if x.startswith('('):
            e = L.parse(x)
            print(e)
            # e = Expr(S.parse(x))
            # ast.append(Expr(S.parse(x)))
            ast.append(e)


repl_table = {}
for a in ast:
    if a.head == 'replace':
        key, val = a.tail
        repl_table[key] = val

print(repl_table)

string = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At
vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren,
no sea takimata sanctus est Lorem ipsum dolor sit amet."""

# for k, v in repl_table.items():
#     string = string.replace(k, v)
#
# print(string)
