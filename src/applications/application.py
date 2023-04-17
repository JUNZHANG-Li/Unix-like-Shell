import sys
from collections import deque
from Features.Pipeline import Pipeline
from Errors.IncorrectNumberOfRedirections import (
    IncorrectNumberOfRedirections,
)
from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.InvalidFlagsError import InvalidFlagsError
from Errors.NotANumberError import NotANumberError
from Errors.InvalidRangeError import InvalidRangeError
from Errors.NoFileFoundError import NoFileFoundError
from Errors.DirectoryNotFoundError import DirectoryNotFoundError
from Errors.GraphInitialisationError import GraphInitialisationError
from Errors.InvalidGraphError import InvalidGraphError
from Errors.InvalidFormatError import InvalidFormatError

from abc import ABCMeta, abstractmethod


class application(metaclass=ABCMeta):
    """
    <Abstract class>
    ----------------

    Purpose
    -------
    Implements the shared functionalities between all applications

    Functionalities
    ---------------
    run : function
        initialises io_redirections and executes the application

    _execute : function
        executes the application according
        to arguments and returns an output : str

    _IO_redirection : function
        help initialise the io_redirections for applications

    _connect_to_pipeline : function
        connect the stdout of the current application
        to the stdin of the next application via the pipeline object
    """

    def __init__(
        self,
        args: list = list(),
        stdin=None,
        stdout: str = "",
        app_sequence: deque = deque(),
    ) -> None:
        self._args = args
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = True
        self._app_sequence = app_sequence
        self._stdin_from_file = False
        self._stdout_to_file = False

    """
    SETTER
    """

    def set_stdin(self, stdout: str):
        if not self._stdin_from_file:
            self._stdin = stdout

    def set_app_sequence(self, app_sequence):
        self._app_sequence = app_sequence

    """
    GETTER
    """

    def get_stdout(self):
        return self._stdout

    def get_stderr(self):
        return self._stderr

    """
    RUNNING APP
    """

    def run(self) -> str:
        """
        Functionality
        -------------
        Runs the current application and returns the stdout of the application

        Returns
        -------
        self._stdout : str
            the current application's stdout
        """
        redirection_status = self._initiate_IO_redirection()
        if redirection_status < 0:
            return redirection_status

        if self._stdin_from_file:
            self._stdin = self._stdin.read()

        output = ""
        output = self._try_execute_app()

        if self._stdout_to_file:
            self._stdout.write(output)
            self._stdout.close()
            output = ""

        self._stdout = output
        if self._app_sequence:
            self._stdout = self._connect_to_pipeline(Pipeline())
        return self._stdout

    def _try_execute_app(self):
        """
        Functionality
        -------------
        Try execute application

        On any exception, print the error message and
        return to error code to crash current shell

        Returns
        -------
        output : str
            the output of application's execution
        """
        try:
            output = self._execute()
            return output
        except WrongNumberOfArgsError as wna:
            self.__handle_error(wna)
            return self._stdout
        except InvalidFlagsError as ife:
            self.__handle_error(ife)
            return self._stdout
        except NotANumberError as na:
            self.__handle_error(na)
            return self._stdout
        except InvalidRangeError as ir:
            self.__handle_error(ir)
            return self._stdout
        except NoFileFoundError as nff:
            self.__handle_error(nff)
            return self._stdout
        except DirectoryNotFoundError as dnf:
            self.__handle_error(dnf)
            return self._stdout
        except GraphInitialisationError as gi:
            self.__handle_error(gi)
            return self._stdout
        except InvalidGraphError as ig:
            self.__handle_error(ig)
            return self._stdout
        except InvalidFormatError as ift:
            self.__handle_error(ift)
            return self._stdout

    def __handle_error(self, exception):
        print(exception, file=sys.stderr)
        self._stderr = False

    @abstractmethod
    def _execute(self) -> str:
        pass

    """
    PIPELINING
    """

    def _connect_to_pipeline(self, p: Pipeline) -> str:
        """
        Functionality
        -------------
        To connect the current application's
        stdout with the stdin of the next application in the app_sequence
        (abstractly : pipeline of applications)

        Parameters
        ----------
        p : Pipeline
            an instance of Pipeline to connect the current application
            to the next application in the app_sequence
            (abstractly : pipeline of applications)

        Returns
        -------
        next_app_stdout : str
            the stdout of the next connected application
        """
        next_app_stdout = p.pipe(
            self, self._app_sequence.popleft(), self._app_sequence
        )

        return next_app_stdout

    """
    IO REDIRECTION
    """

    def _initiate_IO_redirection(self):
        """
        Functionality
        -------------
        Try Initiate the IO redirection for the application

        Returns
        -------
        Literals[0], Literals[-1] : int

        exit status of self._IO_redirection
        """
        try:
            self._IO_redirection()
            return 0
        except IncorrectNumberOfRedirections as ir:
            print(ir)
            return -1

    def _IO_redirection(self) -> int:
        """
        Functionality
        -------------
        Helper for self._initiate_IO_redirection
        """
        if not self._has_correct_amount_of_redirections():
            raise IncorrectNumberOfRedirections(self)

        input = self._get_input_redirection_file()
        if input:
            self._stdin = input
            self._stdin_from_file = True

        output = self._get_output_redirection_file()
        if output:
            self._stdout = output
            self._stdout_to_file = True
        return 0

    """
    IO REDIRECTION HELPERS
    """

    def _has_correct_amount_of_redirections(self):
        input_redirection_counter = 0
        output_redirection_counter = 0
        if not self._args:
            return True

        for arg in self._args:
            if len(arg) != 0 and arg[0] == "<":
                input_redirection_counter += 1
            if len(arg) != 0 and arg[0] == ">":
                output_redirection_counter += 1

        return (
            input_redirection_counter <= 1 and output_redirection_counter <= 1
        )

    def _get_input_redirection_file(self):
        if not self._args:
            return self._args
        for arg in self._args:
            if len(arg) != 0 and arg[0] == "<":
                self._args.remove(arg)
                return open(arg[1: len(arg)], "r")
        return None

    def _get_output_redirection_file(self):
        if not self._args:
            return self._args
        for arg in self._args:
            if len(arg) != 0 and arg[0] == ">":
                self._args.remove(arg)
                return open(arg[1: len(arg)], "w")
        return None

    """
    CLASS INFORMATION FUNCTION
    """

    def __str__(self) -> str:
        return (
            f"application: {self._app} has {len(self._args)} arguments, "
            f"{len([x for x in self._args if x[0] in {'<'}])} "
            f"input redirections "
            f"and {len([x for x in self._args if x[0] in {'>'}])} "
            f"output redirections"
        )
