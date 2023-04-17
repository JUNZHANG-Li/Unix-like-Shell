import unittest
from collections import deque

from shell import shell

from applications.cat import cat
from applications.cut import cut
from applications.head import head
from applications.tail import tail
from applications.cd import cd
from applications.tsort import tsort
from applications.sed import sed


class TestErrors(unittest.TestCase):
    def test_incorrect_number_of_redirections(self):
        app = cat(["input.txt", "<input_1.txt", "<input_2.txt"])
        output = app.run()
        self.assertEqual(output, -1)

    def test_wrong_number_of_args_error(self):
        app = cut(["-b", "1-3", "4-6", "/comp0010/test/input.txt"])
        output = app.run()
        self.assertEqual(output, "")

        app = cd(["path1", "path2"])
        output = app.run()
        self.assertEqual(output, "")

    def test_invalid_flag_error(self):
        app = head(["-b", "3", "/comp0010/test/input.txt"])
        output = app.run()
        self.assertEqual(output, "")

    def test_not_a_number_error(self):
        app = tail(["-n", "a", "/comp0010/test/input.txt"])
        output = app.run()
        self.assertEqual(output, "")

    def test_invalid_range_error(self):
        app = cut(["-b", "1-a", "/comp0010/test/input.txt"])
        output = app.run()
        self.assertEqual(output, "")

    def test_no_file_found_error(self):
        app = cat(["noSuchFileExist.txt"])
        output = app.run()
        self.assertEqual(output, "")

    def test_directory_not_found(self):
        app = cd(["notAValidDirectoryPath"])
        output = app.run()
        self.assertEqual(output, "")

    def test_invalid_graph(self):
        app = tsort(["/comp0010/test/bad_syntax_graph.txt"])
        output = app.run()
        self.assertEqual(output, "")

    def test_graph_initialisation(self):
        app = tsort(["/comp0010/test/cyclic_graph.txt"])
        output = app.run()
        self.assertEqual(output, "")

    def test_invalid_format(self):
        app = sed(["invalid_flag", "/comp0010/test/input.txt"])
        output = app.run()
        self.assertEqual(output, "")

    def test_invalid_command_error(self):
        with self.assertRaises(SystemExit):
            shell().eval(" ", deque())
