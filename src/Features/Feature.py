from abc import ABCMeta


class Feature(metaclass=ABCMeta):
    """
    <Abstract class>
    ----------------

    Purpose
    -------
    Implements the shared functionalities of shell operations
    """

    def __init__(self) -> None:
        pass

    def _replace_arg_with_args(
        self, args: list, index_in_args: int, replacement_args: list
    ) -> int:
        """
        Functionality
        -------------
        Replaces the argument at index index_in_args
        with all arguments of replacement_args
        """
        del args[index_in_args]
        while len(replacement_args) != 0:
            args.insert(index_in_args, replacement_args.pop(0))
            index_in_args += 1
        return 0

    def _is_back_quoted(self, arg):
        if len(arg) < 2:
            return False
        return arg[0] == "`" and arg[len(arg) - 1] == "`"

    def _is_double_quoted(self, arg):
        if len(arg) < 2:
            return False
        return arg[0] == "`" and arg[len(arg) - 1] == "`"

    def _is_single_quoted(self, arg):
        if len(arg) < 2:
            return False
        return arg[0] == "`" and arg[len(arg) - 1] == "`"

    def _is_quoted(self, arg):
        return (
            self._is_back_quoted(arg)
            or self._is_single_quoted(arg)
            or self._is_double_quoted(arg)
        )
