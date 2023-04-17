class InvalidRangeError(Exception):
    def __init__(
        self,
        app,
        range,
        arg,
        entered,
        *args: object,
    ) -> None:
        super().__init__(args)
        self._app = app
        self._range = range
        self._arg = arg
        self._entered = entered

    def __str__(self) -> str:
        return (
            f"Invalid Range Error -> application: {self._app} ; "
            f'range "{self._range}" in argument "{self._arg}" expects numbers '
            f'but "{self._entered}" was entered'
        )
