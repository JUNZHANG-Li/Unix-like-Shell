from antlr4 import InputStream, CommonTokenStream
from command_parser.Grammar.commandLexer import commandLexer
from command_parser.Grammar.commandParser import commandParser
from command_parser.customVisitor import customVisitor
from command_parser.Parser_Error_Handlers.customErrorStrategy import (
    customErrorStrategy,
)


class Parser:
    def __init__(self) -> None:
        self._visitor = None

    def parse(self, cmdline):
        lexer = commandLexer(InputStream(cmdline))
        stream = CommonTokenStream(lexer)
        parser = commandParser(stream)
        parser.removeErrorListeners()
        parser._errHandler = customErrorStrategy()
        tree = parser.command()

        self._visitor = customVisitor()
        self._visitor.visit(tree)

    def getTokens(self):
        return self._visitor.retrieve_command_tokens()

    def getSequenceOrder(self):
        return self._visitor.retrieve_sequence_order()
