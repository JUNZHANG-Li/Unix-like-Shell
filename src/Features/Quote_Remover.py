from command.Call import Call
from command.Pipe import Pipe
from sub_shell import sub_shell
from Features.Feature import Feature


class Quote_Remover(Feature):
    """
    <Class>
    -------

    Purpose
    -------
    To remove the quotes that form the quoted
    terminals in the arguments in the command
    """

    def __init__(self) -> None:
        super().__init__()

    def remove_quotes_from_args(self, ss: sub_shell) -> int:
        """
        Functionality
        -------------
        Remove all quotes forming the quoted
        terminals that form the argument terminals
        part of the command in the subshell

        Parameters
        ----------
        ss : sub_shell
            the current sub shell running

        Returns
        -------
        Literal[0] : int
            Exit status
        """
        for cmd in ss.getCommandSequence():
            if isinstance(cmd, Call):
                self.__remove_quotes_from_args(cmd)

            if isinstance(cmd, Pipe):
                for call in cmd.getCalls():
                    self.__remove_quotes_from_args(call)
        return 0

    def __remove_quotes_from_args(self, c: Call):
        """
        Functionality
        -------------
        Helper for remove_quotes_from_args
        """

        args = c.getArgs()

        for i in range(len(args)):
            args[i] = self.__remove_quotes_from_arg(args[i])

    def __remove_quotes_from_arg(self, arg):
        """
        Functionality
        -------------
        Helper for __remove_quotes_from_args
        """

        current_quote = ""
        embedded_in_backquote = False
        i = 0
        while i < len(arg):
            if arg[i] == "`":
                embedded_in_backquote = not embedded_in_backquote
            if arg[i] == current_quote and not embedded_in_backquote:
                current_quote = ""
                arg = arg[:i] + arg[i + 1:]
                i -= 1
            elif (
                arg[i] in {"'", '"'}
                and not current_quote
                and not embedded_in_backquote
            ):
                current_quote = arg[i]
                arg = arg[:i] + arg[i + 1:]
                i -= 1

            i += 1
        return arg
