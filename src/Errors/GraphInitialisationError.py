class GraphInitialisationError(Exception):
    def __init__(
        self,
        app,
        src,
        *args: object,
    ) -> None:
        super().__init__(args)
        self._app = app
        self._src = src

    def __str__(self) -> str:
        return (
            f"Graph Initialisation Error -> application: {self._app} "
            f'cannot initialise a DAG from "{self._src}", '
            f"due to a cycle in the graph."
        )
