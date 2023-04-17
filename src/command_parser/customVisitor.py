from command_parser.Grammar.commandVisitor import commandVisitor
from command_parser.Grammar.commandParser import commandParser


class customVisitor(commandVisitor):
    """
    <Class>
    -------

    Purpose
    -------
    Collect the tokens of a parsing command
    """

    def __init__(self):
        self.__sequence_order = []
        self.__command_tokens = [[]]
        self.__current_command = 0

    # Override
    def visitPipe_op(self, ctx: commandParser.Pipe_opContext):
        self.__command_tokens[self.__current_command].append("|")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by commandParser#argument.
    def visitArgument(self, ctx: commandParser.ArgumentContext):
        self.__command_tokens[self.__current_command].append("Argument")
        return self.visitChildren(ctx)

    # Override
    def visitRedirection(self, ctx: commandParser.RedirectionContext):
        self.__command_tokens[self.__current_command].append("Redirection")
        return self.visitChildren(ctx)

    # Override
    def visitSemicolon(self, ctx: commandParser.SemicolonContext):
        self.__sequence_order.append(";")
        new_command = []
        self.__command_tokens.append(new_command)
        self.__current_command += 1
        return self.visitChildren(ctx)

    # Visit a parse tree produced by commandParser#double_amphersand.
    def visitDouble_amphersand(
        self, ctx: commandParser.Double_amphersandContext
    ):
        self.__sequence_order.append("&&")
        new_command = []
        self.__command_tokens.append(new_command)
        self.__current_command += 1
        return self.visitChildren(ctx)

    # Visit a parse tree produced by commandParser#double_pipe.
    def visitDouble_pipe(self, ctx: commandParser.Double_pipeContext):
        self.__sequence_order.append("||")
        new_command = []
        self.__command_tokens.append(new_command)
        self.__current_command += 1
        return self.visitChildren(ctx)

    # Override
    def visitWhitespace(self, ctx: commandParser.WhitespaceContext):
        current_command_tokens = self.__command_tokens[self.__current_command]
        current_command_tokens.append(" ")
        return self.visitChildren(ctx)

    # Override
    def visitUnquoted(self, ctx: commandParser.UnquotedContext):
        # UNQUOTED CHARSET
        self.__command_tokens[self.__current_command].append("U")
        return self.visitChildren(ctx)

    # Override
    def visitSingle_quoted(self, ctx: commandParser.Single_quotedContext):
        self.__command_tokens[self.__current_command].append("SQ")
        return self.visitChildren(ctx)

    # Override
    def visitBack_quoted(self, ctx: commandParser.Back_quotedContext):
        current_command_tokens = self.__command_tokens[self.__current_command]
        current_command_tokens.append("BQ")
        return self.visitChildren(ctx)

    # Override
    def visitDouble_quoted(self, ctx: commandParser.Double_quotedContext):
        self.__command_tokens[self.__current_command].append("DQ")
        return self.visitChildren(ctx)

    def retrieve_command_tokens(self):
        return self.__command_tokens

    def retrieve_sequence_order(self):
        return self.__sequence_order
