#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser import SexprParser
import re


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
                    # what's the point of "define" as a keyword?
                    if e[0] == "define":
                        self.expressions[e[1][0]] = e[1][1]
                    self.expressions[e[0]] = e[1:][0]
                except:
                    self.text += line


if __name__ == "__main__":

    S = SexprParser()
    ast = AST(S)

    ast.process("test.md")

    for k, v in ast.expressions.items():
        ast.text = re.sub(f"{k}", f"{v}", ast.text)

    print(ast.text)
