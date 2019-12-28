#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser import SexprParser


class Expr:
    def __init__(self, seq):
        self.head = seq[0]
        self.tail = seq[1:][0]

    def __repr__(self):
        return f"{self.head}: {self.tail}"


class AST:
    def __init__(self, parser):
        self.expressions = {}
        self.text = ""
        self.parser = parser

    def process(self, fname):
        with open(fname, "r") as tf:
            for line in tf.readlines():
                try:
                    e = self.parser.parse(line)
                    self.expressions[e[0]] = e[1:][0]
                except:
                    self.text += line


if __name__ == "__main__":

    string = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
    nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
    voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita
    kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."""

    tokens = [
        r"(?P<ID>[a-zA-Z0-9_-]+)",
        r"(?P<NUM>\d+)",
        r"(?P<LPAREN>\()",
        r"(?P<RPAREN>\))",
        r"(?P<WS>\s+)",
    ]

    S = SexprParser(tokens, ("ID", "NUM"))
    ast = AST(S)

    ast.process("test.md")

    print(ast.text)
    print(ast.expressions)

    # repl_table = {}
    # for a in ast:
    #     if a.head == 'replace':
    #         key, val = a.tail
    #         repl_table[key] = val
    #
    # print(repl_table)
    #
    # for k, v in repl_table.items():
    #     string = string.replace(k, v)
    #
    # print(string)
