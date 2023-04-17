from command.Call import Call
from command.Pipe import Pipe
from sub_shell import sub_shell
from Features.Feature import Feature


class Application_Setter(Feature):
    """
    <Class>
    -------

    Purpose
    -------
    To set the application of subcommands
    """

    def __init__(self) -> None:
        super().__init__()

    def set_applications(self, ss: sub_shell):
        """
        Functionality
        -------------
        To set the first argument of each subcommand
        in the current running sub_shell as the
        application of said subcommand

        Parameters
        ----------
        ss : sub_shell
            the current instance of subshell running

        Returns
        -------
        Literal[0] : int
            Exit Status
        """
        for cmd in ss.getCommandSequence():
            if isinstance(cmd, Call):
                self.__set_application(cmd)

            if isinstance(cmd, Pipe):
                for call in cmd.getCalls():
                    self.__set_application(call)
        return 0

    def __set_application(self, call: Call):
        args = call.getArgs()
        for i in range(len(args)):
            s = args[i]
            if not s[0] in {"<", ">"}:
                call.set_app(s)
                del args[i]
                return 0
