# Generated from command.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .commandParser import commandParser
else:
    from commandParser import commandParser

# This class defines a complete listener for a parse tree produced by commandParser.
class commandListener(ParseTreeListener):

    # Enter a parse tree produced by commandParser#command_eof_nl.
    def enterCommand_eof_nl(self, ctx:commandParser.Command_eof_nlContext):
        pass

    # Exit a parse tree produced by commandParser#command_eof_nl.
    def exitCommand_eof_nl(self, ctx:commandParser.Command_eof_nlContext):
        pass


    # Enter a parse tree produced by commandParser#command.
    def enterCommand(self, ctx:commandParser.CommandContext):
        pass

    # Exit a parse tree produced by commandParser#command.
    def exitCommand(self, ctx:commandParser.CommandContext):
        pass


    # Enter a parse tree produced by commandParser#pipe.
    def enterPipe(self, ctx:commandParser.PipeContext):
        pass

    # Exit a parse tree produced by commandParser#pipe.
    def exitPipe(self, ctx:commandParser.PipeContext):
        pass


    # Enter a parse tree produced by commandParser#call.
    def enterCall(self, ctx:commandParser.CallContext):
        pass

    # Exit a parse tree produced by commandParser#call.
    def exitCall(self, ctx:commandParser.CallContext):
        pass


    # Enter a parse tree produced by commandParser#atom.
    def enterAtom(self, ctx:commandParser.AtomContext):
        pass

    # Exit a parse tree produced by commandParser#atom.
    def exitAtom(self, ctx:commandParser.AtomContext):
        pass


    # Enter a parse tree produced by commandParser#argument.
    def enterArgument(self, ctx:commandParser.ArgumentContext):
        pass

    # Exit a parse tree produced by commandParser#argument.
    def exitArgument(self, ctx:commandParser.ArgumentContext):
        pass


    # Enter a parse tree produced by commandParser#redirection.
    def enterRedirection(self, ctx:commandParser.RedirectionContext):
        pass

    # Exit a parse tree produced by commandParser#redirection.
    def exitRedirection(self, ctx:commandParser.RedirectionContext):
        pass


    # Enter a parse tree produced by commandParser#pipe_op.
    def enterPipe_op(self, ctx:commandParser.Pipe_opContext):
        pass

    # Exit a parse tree produced by commandParser#pipe_op.
    def exitPipe_op(self, ctx:commandParser.Pipe_opContext):
        pass


    # Enter a parse tree produced by commandParser#semicolon.
    def enterSemicolon(self, ctx:commandParser.SemicolonContext):
        pass

    # Exit a parse tree produced by commandParser#semicolon.
    def exitSemicolon(self, ctx:commandParser.SemicolonContext):
        pass


    # Enter a parse tree produced by commandParser#double_amphersand.
    def enterDouble_amphersand(self, ctx:commandParser.Double_amphersandContext):
        pass

    # Exit a parse tree produced by commandParser#double_amphersand.
    def exitDouble_amphersand(self, ctx:commandParser.Double_amphersandContext):
        pass


    # Enter a parse tree produced by commandParser#double_pipe.
    def enterDouble_pipe(self, ctx:commandParser.Double_pipeContext):
        pass

    # Exit a parse tree produced by commandParser#double_pipe.
    def exitDouble_pipe(self, ctx:commandParser.Double_pipeContext):
        pass


    # Enter a parse tree produced by commandParser#whitespace.
    def enterWhitespace(self, ctx:commandParser.WhitespaceContext):
        pass

    # Exit a parse tree produced by commandParser#whitespace.
    def exitWhitespace(self, ctx:commandParser.WhitespaceContext):
        pass


    # Enter a parse tree produced by commandParser#unquoted.
    def enterUnquoted(self, ctx:commandParser.UnquotedContext):
        pass

    # Exit a parse tree produced by commandParser#unquoted.
    def exitUnquoted(self, ctx:commandParser.UnquotedContext):
        pass


    # Enter a parse tree produced by commandParser#quoted.
    def enterQuoted(self, ctx:commandParser.QuotedContext):
        pass

    # Exit a parse tree produced by commandParser#quoted.
    def exitQuoted(self, ctx:commandParser.QuotedContext):
        pass


    # Enter a parse tree produced by commandParser#single_quoted.
    def enterSingle_quoted(self, ctx:commandParser.Single_quotedContext):
        pass

    # Exit a parse tree produced by commandParser#single_quoted.
    def exitSingle_quoted(self, ctx:commandParser.Single_quotedContext):
        pass


    # Enter a parse tree produced by commandParser#back_quoted.
    def enterBack_quoted(self, ctx:commandParser.Back_quotedContext):
        pass

    # Exit a parse tree produced by commandParser#back_quoted.
    def exitBack_quoted(self, ctx:commandParser.Back_quotedContext):
        pass


    # Enter a parse tree produced by commandParser#double_quoted.
    def enterDouble_quoted(self, ctx:commandParser.Double_quotedContext):
        pass

    # Exit a parse tree produced by commandParser#double_quoted.
    def exitDouble_quoted(self, ctx:commandParser.Double_quotedContext):
        pass



del commandParser