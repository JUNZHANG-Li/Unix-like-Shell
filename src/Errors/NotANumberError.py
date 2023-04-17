class NotANumberError(Exception):
    def __init__(
        self,
        app,
        arg_index,
        arg,
        entered,
        *args: object,
    ) -> None:
        super().__init__(args)
        self._app = app
        self._arg_index = arg_index
        self._arg = arg
        self._entered = entered

    def __str__(self) -> str:
        num_to_string = {"1": "1st", "2": "2nd", "3": "3rd"}
        # if self._arg_index in num_to_string:
        return (
            f"Not a number error -> application: {self._app} ; "
            f"{num_to_string[self._arg_index]} argument in "
            f"arguments {self._arg} expects numbers but "
            f'"{self._entered}" was entered'
        )
        # return (
        #     f"Not a number error -> application: {self._app} ; "
        #     f"{self._arg_index}th argument in arguments {self._arg} "
        #     f'expects numbers but "{self._entered}" was entered'
        # )
