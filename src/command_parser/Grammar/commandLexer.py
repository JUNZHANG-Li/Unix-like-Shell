# Generated from command.g4 by ANTLR 4.11.1
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,16,74,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,
        7,13,2,14,7,14,2,15,7,15,1,0,1,0,1,1,1,1,1,2,1,2,1,2,1,3,1,3,1,3,
        1,4,1,4,1,5,1,5,1,6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,3,10,57,8,10,
        1,10,1,10,4,10,61,8,10,11,10,12,10,62,1,11,1,11,1,12,1,12,1,13,1,
        13,1,14,1,14,1,15,1,15,0,0,16,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,
        17,9,19,10,21,11,23,12,25,13,27,14,29,15,31,16,1,0,6,2,0,9,9,32,
        32,9,0,9,10,13,13,32,32,34,34,39,39,59,60,62,62,96,96,124,124,7,
        0,10,10,13,13,34,34,39,39,59,59,96,96,124,124,4,0,10,10,13,13,34,
        34,96,96,3,0,10,10,13,13,96,96,3,0,10,10,13,13,39,39,76,0,1,1,0,
        0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,
        0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,
        0,23,1,0,0,0,0,25,1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,
        1,33,1,0,0,0,3,35,1,0,0,0,5,37,1,0,0,0,7,40,1,0,0,0,9,43,1,0,0,0,
        11,45,1,0,0,0,13,47,1,0,0,0,15,49,1,0,0,0,17,51,1,0,0,0,19,53,1,
        0,0,0,21,60,1,0,0,0,23,64,1,0,0,0,25,66,1,0,0,0,27,68,1,0,0,0,29,
        70,1,0,0,0,31,72,1,0,0,0,33,34,5,60,0,0,34,2,1,0,0,0,35,36,5,62,
        0,0,36,4,1,0,0,0,37,38,5,38,0,0,38,39,5,38,0,0,39,6,1,0,0,0,40,41,
        5,124,0,0,41,42,5,124,0,0,42,8,1,0,0,0,43,44,5,59,0,0,44,10,1,0,
        0,0,45,46,5,124,0,0,46,12,1,0,0,0,47,48,5,39,0,0,48,14,1,0,0,0,49,
        50,5,34,0,0,50,16,1,0,0,0,51,52,5,96,0,0,52,18,1,0,0,0,53,54,7,0,
        0,0,54,20,1,0,0,0,55,57,5,13,0,0,56,55,1,0,0,0,56,57,1,0,0,0,57,
        58,1,0,0,0,58,61,5,10,0,0,59,61,5,13,0,0,60,56,1,0,0,0,60,59,1,0,
        0,0,61,62,1,0,0,0,62,60,1,0,0,0,62,63,1,0,0,0,63,22,1,0,0,0,64,65,
        8,1,0,0,65,24,1,0,0,0,66,67,8,2,0,0,67,26,1,0,0,0,68,69,8,3,0,0,
        69,28,1,0,0,0,70,71,8,4,0,0,71,30,1,0,0,0,72,73,8,5,0,0,73,32,1,
        0,0,0,4,0,56,60,62,0
    ]

class commandLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    LANGLE = 1
    RANGLE = 2
    DOUBLE_AMPHERSAND = 3
    DOUBLE_PIPE = 4
    SEMICOLON = 5
    PIPE = 6
    SINGLEQUOTE = 7
    DOUBLEQUOTE = 8
    BACKQUOTE = 9
    WHITESPACE = 10
    NEWLINE = 11
    UNQUOTED = 12
    NONKEYWORD = 13
    DQCONTENT = 14
    BQCONTENT = 15
    SQCONTENT = 16

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'<'", "'>'", "'&&'", "'||'", "';'", "'|'", "'''", "'\"'", "'`'" ]

    symbolicNames = [ "<INVALID>",
            "LANGLE", "RANGLE", "DOUBLE_AMPHERSAND", "DOUBLE_PIPE", "SEMICOLON", 
            "PIPE", "SINGLEQUOTE", "DOUBLEQUOTE", "BACKQUOTE", "WHITESPACE", 
            "NEWLINE", "UNQUOTED", "NONKEYWORD", "DQCONTENT", "BQCONTENT", 
            "SQCONTENT" ]

    ruleNames = [ "LANGLE", "RANGLE", "DOUBLE_AMPHERSAND", "DOUBLE_PIPE", 
                  "SEMICOLON", "PIPE", "SINGLEQUOTE", "DOUBLEQUOTE", "BACKQUOTE", 
                  "WHITESPACE", "NEWLINE", "UNQUOTED", "NONKEYWORD", "DQCONTENT", 
                  "BQCONTENT", "SQCONTENT" ]

    grammarFileName = "command.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


