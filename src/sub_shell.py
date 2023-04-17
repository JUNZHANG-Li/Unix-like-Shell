from command.Command_Sequence import Command_Sequence
from abc import ABCMeta


class sub_shell(metaclass=ABCMeta):
    """
    <Abstract class>
    ----------------

    Purpose
    -------
    Implements the functionalities of shell

    Functionalities
    ---------------
    parse : function
        parses the input command

    execute : function
        execute all command in the command sequence
    """

    def __init__(
        self,
        cmdline: str = "",
        stdOut: list = None,
    ) -> None:

        self._cmdline = cmdline
        self._shell_stdOut = stdOut
        self._command_sequence = None

    def parse(self):
        self._command_sequence = Command_Sequence(
            self._cmdline, self._shell_stdOut
        )

    def _call_command_substituter(self, cs, ss, new_shell) -> int:
        """
        Functionality
        -------------
        Subsitutes any backquoted terminals in the
        command currently being ran by subshell with
        a command substituter object

        Parameters
        ----------
        cs : Command_Substituter
            an instance of Command_Substituter to perform substitution
        ss : sub_shell
            the current instance of subshell running
        new_shell : sub_shell
            a new instance of subshell for performing command substitution

        Returns
        -------
        exit_status : int
            Exit Status of cs.command_substitute(ss, new_shell)
        """
        exit_status = cs.command_substitute(ss, new_shell)
        return exit_status

    def _call_quote_remover(self, qr, ss) -> int:
        """
        Functionality
        -------------
        To remove the quotes that form the
        quoted terminals in the argument in the command
        that is currently being run by the sub_shell

        Parameters
        ----------
        qr : Quote_Remover
            an instance of Quote_Remover that perform the quote removal
        ss : sub_shell
            the current instance of subshell running

        Returns
        -------
        exit_status : int
            Exit Status of qr.remove_quotes_from_args(ss)
        """
        exit_status = qr.remove_quotes_from_args(ss)
        return exit_status

    def _call_glober(self, gb, ss) -> int:
        """
        Functionality
        -------------
        To globe all unquoted asterisks (*) in argument
        in command currently being run by sub shell

        Parameters
        ----------
        gb : Globber
            an instance of Globber that perform
            the globbing on all unquoted asterisks
        ss : sub_shell
            the current instance of subshell running

        Returns
        -------
        exit_status : int
            Exit Status of gb.globe(ss)
        """
        exit_status = gb.globe(ss)
        return exit_status

    def _call_application_setter(self, ap, ss) -> int:
        """
        Functionality
        -------------
        To set the first argument of each subcommand
        in the sub_shell as the application of said
        subcommand

        Parameters
        ----------
        ap : Application_Setter
            an instance of Application_Setter that
            sets the application of the subcommand
        ss : sub_shell
            the current instance of subshell running

        Returns
        -------
        exit_status : int
            Exit Status of ap.set_applications(ss)
        """
        exit_status = ap.set_applications(ss)
        return exit_status

    def getCommandSequence(self):
        return self._command_sequence.getCommandSequence()

    def execute(self):
        self._command_sequence.execute()
