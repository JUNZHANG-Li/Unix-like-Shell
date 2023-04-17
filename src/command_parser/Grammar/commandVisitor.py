# Generated from command.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .commandParser import commandParser
else:
    from commandParser import commandParser

# This class defines a complete generic visitor for a parse tree produced by commandParser.

class commandVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by commandParser#command_eof_nl.
    def visitCommand_eof_nl(self, ctx:commandParser.Command_eof_nlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#command.
    def visitCommand(self, ctx:commandParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#pipe.
    def visitPipe(self, ctx:commandParser.PipeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#call.
    def visitCall(self, ctx:commandParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#atom.
    def visitAtom(self, ctx:commandParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#argument.
    def visitArgument(self, ctx:commandParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#redirection.
    def visitRedirection(self, ctx:commandParser.RedirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#pipe_op.
    def visitPipe_op(self, ctx:commandParser.Pipe_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#semicolon.
    def visitSemicolon(self, ctx:commandParser.SemicolonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#double_amphersand.
    def visitDouble_amphersand(self, ctx:commandParser.Double_amphersandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#double_pipe.
    def visitDouble_pipe(self, ctx:commandParser.Double_pipeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#whitespace.
    def visitWhitespace(self, ctx:commandParser.WhitespaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#unquoted.
    def visitUnquoted(self, ctx:commandParser.UnquotedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#quoted.
    def visitQuoted(self, ctx:commandParser.QuotedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#single_quoted.
    def visitSingle_quoted(self, ctx:commandParser.Single_quotedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#back_quoted.
    def visitBack_quoted(self, ctx:commandParser.Back_quotedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#double_quoted.
    def visitDouble_quoted(self, ctx:commandParser.Double_quotedContext):
        return self.visitChildren(ctx)



del commandParser