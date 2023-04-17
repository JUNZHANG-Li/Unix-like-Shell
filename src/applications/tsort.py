from applications.application import application
from applications.decorators import unsafe
from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.NoFileFoundError import NoFileFoundError
from Errors.InvalidGraphError import InvalidGraphError
from Errors.GraphInitialisationError import GraphInitialisationError
import networkx as nx


class tsort(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the tsort application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "tsort"
        super().__init__(args)

    def _execute(self) -> str:
        output = ""
        ts = list()
        edges = list()

        if len(self._args) != 1 and len(self._args) != 0:
            raise WrongNumberOfArgsError(
                self._app, "0", "1", str(len(self._args))
            )

        if len(self._args) == 0:
            # from stdin
            inp = self._stdin
            if not self._stdin_from_file and not self._stdin:
                inp = input()

            inp = inp.replace("\n", " ").replace("\t", " ")
            edge_list = inp.split(" ")
            self.__validate_graph_from_stdin(edge_list)
            ts = self.__get_ts_from_stdin(edge_list)

            for i in range(len(edge_list)):
                edge_list[i] = "> " + edge_list[i].replace("-", " ")

            edges = edge_list

        if len(self._args) == 1:
            # from file
            file = self._args[0]
            self.__validate_graph_from_file(file)

            ts = self.__get_ts_from_file(file)

            with open(file, "r") as f:
                for line in f:
                    edges.append(
                        "> " + line.replace("\n", "").replace("-", " ")
                    )

        for edge in edges:
            output += str(edge) + "\n"
        for node in ts:
            output += str(node) + "\n"

        return output

    def __get_ts_from_stdin(self, edge_list: list) -> list:
        ts = list()
        try:
            DG = nx.parse_edgelist(
                edge_list,
                comments=None,
                delimiter="-",
                create_using=nx.DiGraph,
            )
            ts = list(nx.topological_sort(DG))
        except nx.NetworkXUnfeasible:
            raise GraphInitialisationError(self._app, "stdin") from None
        return ts

    def __validate_graph_from_stdin(self, edge_list: list) -> None:
        all_edges_valid = True
        for edge in edge_list:
            nodes = [x for x in edge.split("-", 1) if x]
            if any(not x.isnumeric() for x in nodes):
                raise InvalidGraphError(self._app, str(nodes))
            all_edges_valid = all_edges_valid and len(nodes) == 2
        return all_edges_valid

    def __get_ts_from_file(self, filename: str) -> list:
        ts = list()
        try:
            DG = nx.read_edgelist(
                filename,
                comments=None,
                delimiter="-",
                create_using=nx.DiGraph,
            )
            TS = list(nx.topological_sort(DG))
            ts = TS
        except nx.NetworkXUnfeasible:
            raise GraphInitialisationError(self._app, filename) from None
        return ts

    def __validate_graph_from_file(self, file) -> None:
        try:
            with open(file, "r") as f:
                for line in f:
                    line = line.replace("\n", "")
                    self.__is_line_valid_format(line)
        except FileNotFoundError:
            raise NoFileFoundError(self._app, file)

    def __is_line_valid_format(self, line: str) -> bool:
        nodes = [x for x in line.split("-", 1) if x]
        if any(not x.isnumeric() for x in nodes):
            raise InvalidGraphError(self._app, str(nodes))
        return len(nodes) == 2


class _tsort(tsort):
    @unsafe
    def _execute(self):
        return super()._execute()
