from collections import deque
from Features.Feature import Feature


class Pipeline(Feature):
    """
    <Class>
    -------

    Purpose
    -------
    To bridge an application's stdout to another
    application's stdin
    """

    def pipe(self, app_1, app_2, app_sequence: deque):
        """
        Functionality
        -------------
        Set next application's standard input as the
        current application's standard output

        Set next application's app_sequence as app_sequence

        Run the next application

        Parameters
        ----------
        app_1 : application

        app_2 : application

        app_sequence : deque[application]

        Returns
        -------
        app_2.run() : str
            The standard output of the next application
        """
        if not app_1.get_stderr():
            exit()
        app_2.set_stdin(app_1.get_stdout())
        app_2.set_app_sequence(app_sequence)
        return app_2.run()
