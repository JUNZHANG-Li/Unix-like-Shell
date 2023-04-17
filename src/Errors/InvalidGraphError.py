class InvalidGraphError(Exception):
    def __init__(
        self,
        app,
        nodes,
        *args: object,
    ) -> None:
        super().__init__(args)
        self._app = app
        self._nodes = nodes

    def __str__(self) -> str:
        return (
            f"Invalid Graph Error -> application: {self._app} "
            f"expects a graph with edge relations "
            f'defined: "x-y" meaning "x to y" but '
            f"received a graph with undefined edge relation(s): {self._nodes}"
        )
