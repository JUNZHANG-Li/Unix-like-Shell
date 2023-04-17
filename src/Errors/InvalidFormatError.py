class InvalidFormatError(Exception):
    def __init__(
        self,
        app,
        expected,
        entered,
        *args: object,
    ) -> None:
        super().__init__(args)
        self._app = app
        self._expected = expected
        self._entered = entered

    def __str__(self) -> str:
        return (
            f"Invalid Format entered -> application: "
            f"{self._app} expects format "
            f'"{self._expected}" but "{self._entered}" was entered'
        )
