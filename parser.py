#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lexer import lex
from collections import Iterable
from pprint import pprint

class BaseParser:

    def __init__(self, tokens):
        self.lex = lex(tokens)
        self.stream = None
        self.current = None
        self.lookahead = None
        
    def _consume(self):
        self.current, self.lookahead = self.lookahead, next(self.stream, None)

    def match(self, *ttype):
        if self.lookahead.type in ttype:
            self._consume()
            return True
        else:
            raise SyntaxError(f"expecting {ttype}; found {self.lookahead.type}")
    
    def parse(self, string):
        self.stream = self.lex(string)
        self._consume()
        return getattr(self, self.top)()
            
#  ListParser {{{1 # 
class ListParser(BaseParser):

    """Python-like lists (with parentheses instead of brackets)"""

    # list := '(' elements ')'
    
    # elements := atom (',' atom )*

    # atom := ID
    #          | STR
    #          | NUM
    #          | list

    top = 'list'

    def list(self):
        self.match('LPAREN')
        val = self.elements()
        self.match('RPAREN')
        return val

    def elements(self):
        val = []
        val.append(self.atom())
        while self.lookahead.type == 'COMMA':
            self.match('COMMA')
            val.append(self.atom())
        return val
        
    def atom(self):
        if self.lookahead.type in ('ID', 'STR'):
            self.match('ID', 'STR')
            return self.current.value
        elif self.lookahead.type == 'NUM':
            self.match('NUM')
            return int(self.current.value)
        elif self.lookahead.type == 'LPAREN':
            return self.list()
        else:
            raise SyntaxError(f"expecting 'name' or 'list'; found {self.lookahead}")
#  1}}} # 

#  sexprparser {{{1 # 
class SexprParser(ListParser):

    """ doesn't need the comma in between elements """

    # elements := atom ( atom )*

    def elements(self):
        val = self.atom()
        while self.lookahead.type != 'RPAREN':
            val = val, self.atom()
        return val
        
    def atom(self):
        accepted_types = ('ID', 'STR', 'NUM', 'ADD', 'SUB', 'MUL', 'DIV')

        if self.lookahead.type in accepted_types:
            self.match(*accepted_types)
            return self.current.value
        elif self.lookahead.type == 'LPAREN':
            return self.list()
        else:
            raise SyntaxError(f"expecting 'elements' or 'atom'; found {self.lookahead}")
#  1}}} # 
#  stringparser {{{1 # 
class StringParser(BaseParser):
    """ parses everything between quotes """

    top = 'string'

    def d_quoted_string(self):
        self.match('DQUOTE')
        self.quote_t = 'SQUOTE'
        val = self.elements()
        self.match('DQUOTE')
        return val
    
    def s_quoted_string(self):
        self.match('SQUOTE')
        self.quote_t = 'DQUOTE'
        val = self.elements()
        self.match('SQUOTE')
        return val

    def elements(self):
        val = []
        val.append(self.atom())
        while self.lookahead.type not in ('DQUOTE', 'SQUOTE'):
            val.append(self.atom())
        return val
        
    def atom(self):
        if self.current.type != 'EOS':
            self._consume()
            return self.current.value
        # ze statement; it does nozing!
        elif (self.quote_t == 'SQUOTE' and self.lookahead.type == 'DQUOTE') or (self.quote_t == 'DQUOTE' and self.lookahead.type == 'SQUOTE'):
            return self.list()
        else:
            raise SyntaxError(f"expecting '{self.quote_t}'; found {self.lookahead}")
#  }}} # 


if __name__ == "__main__":
    
    tokens = [
        # r"(?P<STR>\"(\\.|[^\"])*\")",
        r"(?P<ID>[a-zA-Z\-]+)",
        # r"(?P<ADD>\+)",
        # r"(?P<SUB>\-)",
        # r"(?P<MUL>\*)",
        # r"(?P<DIV>\\)",
        r"(?P<NUM>\d+)",
        # r"(?P<COMMA>,)",
        r"(?P<LPAREN>\()",
        r"(?P<RPAREN>\))",
        r"(?P<WS>\s+)",
    ]

    F = Fexpreffionf(tokens)
    S = SexprParser(tokens)

    test = "(this (list (of lists)))"

    for t in S.lex(test):
        print(t)

    print(F.parse(test))
