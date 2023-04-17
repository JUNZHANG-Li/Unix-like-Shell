import unittest
import os

from unittest import mock

from command.Call import Call

from applications.pwd import pwd, _pwd
from applications.cd import cd, _cd
from applications.ls import ls, _ls
from applications.cat import cat, _cat
from applications.echo import echo, _echo
from applications.head import head, _head
from applications.tail import tail, _tail
from applications.grep import grep, _grep
from applications.cut import cut, _cut
from applications.find import find, _find
from applications.uniq import uniq, _uniq
from applications.sort import sort, _sort
from applications.mkdir import mkdir, _mkdir
from applications.sed import sed, _sed
from applications.wc import wc, _wc
from applications.mv import mv, _mv
from applications.tsort import tsort, _tsort

from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.InvalidFlagsError import InvalidFlagsError
from Errors.NotANumberError import NotANumberError
from Errors.NoFileFoundError import NoFileFoundError
from Errors.InvalidRangeError import InvalidRangeError
from Errors.DirectoryNotFoundError import DirectoryNotFoundError
from Errors.InvalidFormatError import InvalidFormatError
from Errors.GraphInitialisationError import GraphInitialisationError
from Errors.InvalidGraphError import InvalidGraphError


class Test_IO_redirection(unittest.TestCase):
    def test_input_redirection(self):
        writefile = [
            "cat",
            ["</comp0010/test/input.txt", ">/comp0010/test/output.txt"],
        ]
        readInput = ["cat", ["</comp0010/test/input.txt"]]
        readOutput = ["cat", ["</comp0010/test/output.txt"]]

        c = Call()
        app, args = writefile[0], writefile[1]
        c.set_app(app)
        c.set_args(args)
        c.execute()

        c1 = Call()
        app, args = readInput[0], readInput[1]
        c1.set_app(app)
        c1.set_args(args)
        inp = c1.execute().get_stdout()

        c2 = Call()
        app, args = readOutput[0], readOutput[1]
        c2.set_app(app)
        c2.set_args(args)
        out = c2.execute().get_stdout()

        self.assertEqual(inp, out)

    def test_two_indirection(self):
        testCase = [
            "cat",
            ["</comp0010/test/input.txt", ">/comp0010/test/output.txt"],
        ]
        c = Call()
        app, args = testCase[0], testCase[1]
        c.set_app(app)
        c.set_args(args)
        out = c.execute().get_stdout()
        self.assertEqual(out, "")


class Test_pwd(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        return super().setUp()

    def test_pwd_in_root(self):
        new_pwd = pwd([])
        out = new_pwd._execute()
        self.assertEqual(out, "/comp0010\n")

    def test_pwd_with_args(self):
        new_pwd = pwd(["test"])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_pwd._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "pwd requires 0 argument(s), "
            "but 1 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_pwd(self):
        new_pwd = _pwd([])
        out = new_pwd._execute()
        self.assertEqual(out, "/comp0010\n")


class Test_cd(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        return super().setUp()

    def test_cd(self):
        new_cd = cd(["tools"])
        out = new_cd._execute()
        self.assertEqual(out, "")
        self.assertEqual(os.getcwd(), "/comp0010/tools")

        new_cd = cd([".."])
        out = new_cd._execute()
        self.assertEqual(out, "")
        self.assertEqual(os.getcwd(), "/comp0010")

    def test_cd_with_no_args(self):
        new_cd = cd([])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_cd._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "cd requires 1 argument(s), "
            "but 0 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_cd_with_invalid_dir(self):
        new_cd = cd(["invalid_dir"])
        with self.assertRaises(DirectoryNotFoundError) as error:
            new_cd._execute()
        exceptionMessage = (
            "Directory Not Found Error -> application: "
            'cd cannot locate "invalid_dir"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_cd(self):
        new_cd = _cd(["tools"])
        out = new_cd._execute()
        self.assertEqual(out, "")
        self.assertEqual(os.getcwd(), "/comp0010/tools")

        new_cd = _cd([".."])
        out = new_cd._execute()
        self.assertEqual(out, "")
        self.assertEqual(os.getcwd(), "/comp0010")


class Test_ls(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        return super().setUp()

    def test_ls_with_no_arguments(self):
        os.chdir("test_directory")
        new_ls = ls([])
        out = new_ls._execute()
        self.assertEqual(out, "aaa.txt\tdir1\n")

    def test_ls_with_one_argument(self):
        new_ls = ls(["test_directory/dir1"])
        out = new_ls._execute()
        self.assertEqual(out, "bbb.txt\tccc.txt\n")

    def test_ls_with_two_arguments(self):
        new_ls = ls(["test_directory/dir1", "test_directory"])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_ls._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "ls requires 0 to 1 arguments, but 2 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_ls(self):
        new_ls = _ls(["test_directory/dir1"])
        out = new_ls._execute()
        self.assertEqual(out, "bbb.txt\tccc.txt\n")


class Test_cat(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        return super().setUp()

    @mock.patch("applications.cat.input", create=True)
    def test_cat_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["/comp0010/test/input.txt"]
        new_cat = cat([])
        actual_output = new_cat._execute()
        expected_output = "/comp0010/test/input.txt"
        self.assertEqual(actual_output, expected_output)

    def test_cat_file(self):
        new_cat = cat(["test_directory/aaa.txt"])
        out = new_cat._execute()
        self.assertEqual(out, "i am text xd")

    def test_cat_invalid_file(self):
        new_cat = cat(["invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_cat._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'cat cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_cat(self):
        new_cat = _cat(["test_directory/aaa.txt"])
        out = new_cat._execute()
        self.assertEqual(out, "i am text xd")


class Test_echo(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        return super().setUp()

    def test_echo_with_one_arg(self):
        new_echo = echo(["hello world"])
        out = new_echo._execute()
        self.assertEqual(out, "hello world\n")

    def test_echo_with_multiple_args(self):
        new_echo = echo(["hello", "world"])
        out = new_echo._execute()
        self.assertEqual(out, "hello world\n")

    def test_unsafe_echo(self):
        new_echo = _echo(["hello world"])
        out = new_echo._execute()
        self.assertEqual(out, "hello world\n")


class Test_head(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    @mock.patch("applications.head.input", create=True)
    def test_head_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["test\n" * 20]
        new_head = head([])
        actual_output = new_head._execute()
        expected_output = "test\n" * 10
        self.assertEqual(actual_output, expected_output)

    def test_head_with_file(self):
        new_head = head(["bbb.txt"])
        out = new_head._execute()
        self.assertEqual(out, "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n")

    @mock.patch("applications.head.input", create=True)
    def test_head_with_user_input_and_zero_lines(self, mocked_input):
        mocked_input.side_effect = ["test\n" * 20]
        new_head = head(["-n", "0"])
        actual_output = new_head._execute()
        expected_output = ""
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.head.input", create=True)
    def test_head_with_user_input_and_option(self, mocked_input):
        mocked_input.side_effect = ["test\n" * 20]
        new_head = head(["-n", "17"])
        actual_output = new_head._execute()
        expected_output = "test\n" * 17
        self.assertEqual(actual_output, expected_output)

    def test_head_with_file_and_option(self):
        new_head = head(["-n", "17", "bbb.txt"])
        out = new_head._execute()
        self.assertEqual(
            out, "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n"
        )

    def test_head_with_invalid_flag(self):
        new_head = head(["-w", "12"])
        with self.assertRaises(InvalidFlagsError) as error:
            new_head._execute()
        exceptionMessage = (
            "Invalid Flags entered -> application: "
            'head expects flag(s) "-n" but "-w" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_head_with_valid_flag_but_not_a_number(self):
        new_head = head(["-n", "twelve"])
        with self.assertRaises(NotANumberError) as error:
            new_head._execute()
        exceptionMessage = (
            "Not a number error -> application: head ; "
            "2nd argument in arguments ['-n', 'twelve'] "
            'expects numbers but "twelve" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_head_with_invalid_file(self):
        new_head = head(["invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_head._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'head cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_head_with_wrong_num_of_args(self):
        new_head = head(["-n", "17", "bbb.txt", "ccc.txt"])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_head._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "head requires 0 to 3 arguments, but 4 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_head(self):
        new_head = _head(["-n", "17", "bbb.txt"])
        out = new_head._execute()
        self.assertEqual(
            out, "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n"
        )


class Test_tail(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    @mock.patch("applications.tail.input", create=True)
    def test_tail_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["test\n" * 20]
        new_tail = tail([])
        actual_output = new_tail._execute()
        expected_output = "test\n" * 10
        self.assertEqual(actual_output, expected_output)

    def test_tail_with_file(self):
        new_tail = tail(["bbb.txt"])
        out = new_tail._execute()
        self.assertEqual(out, "11\n12\n13\n14\n15\n16\n17\n18\n19\n20")

    @mock.patch("applications.tail.input", create=True)
    def test_tail_with_user_input_and_zero_lines(self, mocked_input):
        mocked_input.side_effect = ["test\n" * 20]
        new_tail = tail(["-n", "0"])
        actual_output = new_tail._execute()
        expected_output = ""
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.tail.input", create=True)
    def test_tail_with_user_input_and_option(self, mocked_input):
        mocked_input.side_effect = ["test\n" * 20]
        new_tail = tail(["-n", "17"])
        actual_output = new_tail._execute()
        expected_output = "test\n" * 17
        self.assertEqual(actual_output, expected_output)

    def test_tail_with_file_and_option(self):
        new_tail = tail(["-n", "17", "bbb.txt"])
        out = new_tail._execute()
        self.assertEqual(
            out, "4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20"
        )

    def test_tail_with_invalid_flag(self):
        new_tail = tail(["-w", "12"])
        with self.assertRaises(InvalidFlagsError) as error:
            new_tail._execute()
        exceptionMessage = (
            "Invalid Flags entered -> application: "
            'tail expects flag(s) "-n" but "-w" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_tail_with_valid_flag_but_not_a_number(self):
        new_tail = tail(["-n", "twelve"])
        with self.assertRaises(NotANumberError) as error:
            new_tail._execute()
        exceptionMessage = (
            "Not a number error -> application: tail ; "
            "2nd argument in arguments ['-n', 'twelve'] "
            'expects numbers but "twelve" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_tail_with_invalid_file(self):
        new_tail = tail(["invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_tail._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'tail cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_tail_with_wrong_num_of_args(self):
        new_tail = tail(["-n", "17", "bbb.txt", "ccc.txt"])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_tail._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "tail requires 0 to 3 arguments, but 4 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_tail(self):
        new_tail = _tail(["-n", "17", "bbb.txt"])
        out = new_tail._execute()
        self.assertEqual(
            out, "4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20"
        )


class Test_grep(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    @mock.patch("applications.grep.input", create=True)
    def test_grep_with_user_input(self, mocked_input):
        mocked_input.side_effect = [
            "foo\nbar\nfoobar\nbarfoo\nfoofoo\nbarbar\n"
        ]
        new_grep = grep(["foo"])
        actual_output = new_grep._execute()
        expected_output = "foo\nfoobar\nbarfoo\nfoofoo\n"
        self.assertEqual(actual_output, expected_output)

    def test_grep_with_file(self):
        new_grep = grep(["python", "ccc.txt"])
        out = new_grep._execute()
        self.assertEqual(out, "python\npython is a snake\n")

    def test_grep_with_files(self):
        new_grep = grep(["python", "ccc.txt", "bbb.txt"])
        out = new_grep._execute()
        self.assertEqual(out, "ccc.txt:python\nccc.txt:python is a snake\n")

    def test_grep_with_invalid_files(self):
        new_grep = grep(["python", "invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_grep._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'grep cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_grep_with_wrong_num_of_args(self):
        new_grep = grep([])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_grep._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "grep requires 1 to * arguments, "
            "but 0 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_grep(self):
        new_grep = _grep(["python", "ccc.txt"])
        out = new_grep._execute()
        self.assertEqual(out, "python\npython is a snake\n")


class Test_cut(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    @mock.patch("applications.cut.input", create=True)
    def test_cut_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["python\npython\njava\nc\n"]
        new_cut = cut(["-b", "-2,4-"])
        actual_output = new_cut._execute()
        expected_output = "pyhon\npyhon\njaa\nc\n"
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.cut.input", create=True)
    def test_cut_with_user_input_and_invalid_flag(self, mocked_input):
        mocked_input.side_effect = ["python\npython\njava\nc\n"]
        new_cut = cut(["-n", "0"])
        with self.assertRaises(InvalidFlagsError) as error:
            new_cut._execute()
        exceptionMessage = (
            "Invalid Flags entered -> application: "
            'cut expects flag(s) "-b" but "-n" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_cut_with_file(self):
        new_cut = cut(["-b", "1,3,5", "ccc.txt"])
        out = new_cut._execute()
        self.assertEqual(out, "pto\nc\njv\r\npto\nci \nci \njv \nJv \n")

    def test_cut_with_file_and_invalid_flag(self):
        new_cut = cut(["-w", "1,3,5", "ccc.txt"])
        with self.assertRaises(InvalidFlagsError) as error:
            new_cut._execute()
        exceptionMessage = (
            "Invalid Flags entered -> application: "
            'cut expects flag(s) "-b" but "-w" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    @mock.patch("applications.cut.input", create=True)
    def test_cut_with_valid_range(self, mocked_input):
        mocked_input.side_effect = ["python\npython\njava\nc\n"]
        new_cut = cut(["-b", "1-2,4"])
        actual_output = new_cut._execute()
        expected_output = "pyh\npyh\njaa\nc\n"
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.cut.input", create=True)
    def test_cut_with_invalid_range(self, mocked_input):
        mocked_input.side_effect = ["python\npython\njava\nc\n"]
        new_cut = cut(["-b", "1-2-3,4-5"])
        with self.assertRaises(InvalidRangeError) as error:
            new_cut._execute()
        exceptionMessage = (
            "Invalid Range Error -> application: cut ; "
            'range "1-2-3" in argument "1-2-3,4-5" '
            'expects numbers but "2-3" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_cut_with_invalid_file(self):
        new_cut = cut(["-b", "1,3,5", "invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_cut._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'cut cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_cut_with_wrong_num_of_args(self):
        new_cut = cut(["-w", "1,3,5", "ccc.txt", "bbb.txt"])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_cut._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "cut requires 2 to 3 arguments, but 4 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_cut(self):
        new_cut = _cut(["-b", "1,3,5", "ccc.txt"])
        out = new_cut._execute()
        self.assertEqual(out, "pto\nc\njv\r\npto\nci \nci \njv \nJv \n")


class Test_find(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        return super().setUp()

    def test_find_without_specified_path(self):
        new_find = find(["-name", "bbb.txt"])
        out = new_find._execute()
        self.assertEqual(out, "./test_directory/dir1/bbb.txt\n")

    def test_find_without_specified_path_and_invalid_flag(self):
        new_find = find(["-wrong", "bbb.txt"])
        with self.assertRaises(InvalidFlagsError) as error:
            new_find._execute()
        exceptionMessage = (
            "Invalid Flags entered -> application: "
            'find expects flag(s) "-name" but "-wrong" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_find_with_specified_path(self):
        new_find = find(["test_directory", "-name", "bbb.txt"])
        out = new_find._execute()
        self.assertEqual(out, "test_directory/dir1/bbb.txt\n")

    def test_find_with_specified_path_and_invalid_flag(self):
        new_find = find(["/test_directory", "-wrong", "bbb.txt"])
        with self.assertRaises(InvalidFlagsError) as error:
            new_find._execute()
        exceptionMessage = (
            "Invalid Flags entered -> application: "
            'find expects flag(s) "-name" but "-wrong" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_find_with_wrong_num_of_args(self):
        new_find = find(["/test_directory", "-name", "bbb.txt", "ccc.txt"])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_find._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "find requires 2 to 3 arguments, but 4 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_find(self):
        new_find = _find(["test_directory", "-name", "bbb.txt"])
        out = new_find._execute()
        self.assertEqual(out, "test_directory/dir1/bbb.txt\n")


class Test_uniq(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    @mock.patch("applications.uniq.input", create=True)
    def test_uniq_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["python\npython\njava\nJava\nc\nR\n"]
        new_uniq = uniq([])
        actual_output = new_uniq._execute()
        expected_output = "python\njava\nJava\nc\nR\n"
        self.assertEqual(actual_output, expected_output)

    def test_uniq_with_file(self):
        new_uniq = uniq(["ccc.txt"])
        out = new_uniq._execute()
        self.assertEqual(
            out,
            "python\nc\njava\npython is a snake\n"
            "c is a letter\njava is an island\n"
            "Java Is An Island\n",
        )

    @mock.patch("applications.uniq.input", create=True)
    def test_uniq_with_user_input_and_case_insensitive(self, mocked_input):
        mocked_input.side_effect = ["python\npython\njava\nJava\nc\nR\n"]
        new_uniq = uniq(["-i"])
        actual_output = new_uniq._execute()
        expected_output = "python\njava\nc\nR\n"
        self.assertEqual(actual_output, expected_output)

    def test_uniq_with_file_and_case_insensitive(self):
        new_uniq = uniq(["-i", "ccc.txt"])
        out = new_uniq._execute()
        self.assertEqual(
            out,
            "python\nc\njava\npython is a snake"
            "\nc is a letter\njava is an island\n",
        )

    def test_uniq_with_invalid_flag(self):
        new_uniq = uniq(["-w", "ccc.txt"])
        with self.assertRaises(InvalidFlagsError) as error:
            new_uniq._execute()
        exceptionMessage = (
            "Invalid Flags entered -> application: "
            'uniq expects flag(s) "-i" but "-w" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_uniq_with_invalid_file(self):
        new_uniq = uniq(["invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_uniq._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'uniq cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_uniq_with_wrong_num_of_args(self):
        new_uniq = uniq(["-i", "ccc.txt", "bbb.txt"])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_uniq._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "uniq requires 0 to 2 arguments, "
            "but 3 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_uniq(self):
        new_uniq = _uniq(["ccc.txt"])
        out = new_uniq._execute()
        self.assertEqual(
            out,
            "python\nc\njava\npython is a snake\n"
            "c is a letter\njava is an island\n"
            "Java Is An Island\n",
        )


class Test_sort(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    @mock.patch("applications.sort.input", create=True)
    def test_sort_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["foo\nbar\nfoobar\nbarfoo\n"]
        new_sort = sort([])
        actual_output = new_sort._execute()
        expected_output = "bar\nbarfoo\nfoo\nfoobar\n"
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.sort.input", create=True)
    def test_sort_with_user_input_in_reverse(self, mocked_input):
        mocked_input.side_effect = ["foo\nbar\nfoobar\nbarfoo\n"]
        new_sort = sort(["-r"])
        actual_output = new_sort._execute()
        expected_output = "foobar\nfoo\nbarfoo\nbar\n"
        self.assertEqual(actual_output, expected_output)

    def test_sort_with_file(self):
        new_sort = sort(["ccc.txt"])
        out = new_sort._execute()
        self.assertEqual(
            out,
            "Java Is An Island\nc\nc is a letter\n"
            "c is a letter\njava\njava is an island\n"
            "python\npython is a snake\n",
        )

    def test_sort_with_file_in_reverse(self):
        new_sort = sort(["-r", "ccc.txt"])
        out = new_sort._execute()
        self.assertEqual(
            out,
            "python is a snake\npython\n"
            "java is an island\njava\nc is a letter"
            "\nc is a letter\nc\nJava Is An Island\n",
        )

    def test_sort_with_invalid_flag(self):
        new_sort = sort(["-w", "ccc.txt"])
        with self.assertRaises(InvalidFlagsError) as error:
            new_sort._execute()
        exceptionMessage = (
            "Invalid Flags entered -> application: "
            'sort expects flag(s) "-r" but "-w" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_sort_with_invalid_file(self):
        new_sort = sort(["invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_sort._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'sort cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_uniq_with_wrong_num_of_args(self):
        new_sort = sort(["-r", "ccc.txt", "bbb.txt"])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_sort._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "sort requires 0 to 2 arguments, "
            "but 3 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_sort(self):
        new_sort = _sort(["ccc.txt"])
        out = new_sort._execute()
        self.assertEqual(
            out,
            "Java Is An Island\nc\nc is a letter\n"
            "c is a letter\njava\njava is an island\n"
            "python\npython is a snake\n",
        )


class Test_mkdir(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        return super().setUp()

    def test_mkdir(self):
        new_mkdir = mkdir(["tempDir"])
        out = new_mkdir._execute()
        self.assertEqual(out, "")
        self.assertTrue(os.path.exists("/comp0010/tempDir"))

    def test_mkdir_with_no_args(self):
        new_mkdir = mkdir([])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_mkdir._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "mkdir requires 1 argument(s), but 0 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_mkdir(self):
        new_mkdir = _mkdir(["tempDir"])
        out = new_mkdir._execute()
        self.assertEqual(out, "")
        self.assertTrue(os.path.exists("/comp0010/tempDir"))


class Test_sed(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    @mock.patch("applications.sed.input", create=True)
    def test_sed_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["AAA\nccc\nAAA\n"]
        new_sed = sed(["s/A/D/g"])
        actual_output = new_sed._execute()
        expected_output = "DDD\nccc\nDDD\n"
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.sed.input", create=True)
    def test_sed_with_user_input_and_invalid_flag(self, mocked_input):
        mocked_input.side_effect = ["AAA\nccc\nAAA\n"]
        new_sed = sed(["invalid_flag"])
        with self.assertRaises(InvalidFormatError) as error:
            new_sed._execute()
        exceptionMessage = (
            "Invalid Format entered -> application: "
            'sed expects format ""s/regexp/replacement/g"" '
            'but "invalid_flag" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_sed_with_file(self):
        new_sed = sed(["s/C/E/", "/comp0010/test/input.txt"])
        out = new_sed._execute()
        self.assertEqual(out, "AAA\nBBB\nECC\n")

        new_sed = sed(["s/C/E/g", "/comp0010/test/input.txt"])
        out = new_sed._execute()
        self.assertEqual(out, "AAA\nBBB\nEEE\n")

        new_sed = sed(["s|C|E|g", "/comp0010/test/input.txt"])
        out = new_sed._execute()
        self.assertEqual(out, "AAA\nBBB\nEEE\n")

    def test_inconsistent_delimiter(self):
        new_sed = sed(["s/C|E/g]", "/comp0010/test/input.txt"])
        with self.assertRaises(ValueError) as error:
            new_sed._execute()
        exceptionMessage = "Inconsistent delimiter used"
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_sed_with_file_and_invalid_flag(self):
        new_sed = sed(["invalid_flag", "/comp0010/test/input.txt"])
        with self.assertRaises(InvalidFormatError) as error:
            new_sed._execute()
        exceptionMessage = (
            "Invalid Format entered -> application: "
            'sed expects format ""s/regexp/replacement/g"" '
            'but "invalid_flag" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_sed_with_invalid_file(self):
        new_sed = sed(["s/C/E/g", "invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_sed._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'sed cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_sed_with_invalid_format(self):
        new_sed = sed(["/C/E/g", "/comp0010/test/input.txt"])
        with self.assertRaises(InvalidFormatError) as error:
            new_sed._execute()
        exceptionMessage = (
            "Invalid Format entered -> application: "
            'sed expects format ""s/regexp/replacement/g"" '
            'but "/C/E/g" was entered'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    @mock.patch("applications.sed.input", create=True)
    def test_sed_with_invalid_format_from_sdtin(self, mocked_input):
        mocked_input.side_effect = ["AAA\nccc\nAAA\n"]
        new_sed = sed(["s/A/E/"])
        actual_output = new_sed._execute()
        expected_output = "EAA\nccc\nEAA\n"
        self.assertEqual(actual_output, expected_output)

    def test_sed_with_wrong_num_of_args(self):
        new_sed = sed(["-w", "1,3,5", "ccc.txt", "bbb.txt"])
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_sed._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "sed requires 1 to 2 arguments, "
            "but 4 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_sed(self):
        new_sed = _sed(["s/C/E/", "/comp0010/test/input.txt"])
        out = new_sed._execute()
        self.assertEqual(out, "AAA\nBBB\nECC\n")


class Test_wc(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    @mock.patch("applications.wc.input", create=True)
    def test_all_counts_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["AAA\nBBB\nCCC"]
        new_wc = wc([])
        actual_output = new_wc._execute()
        expected_output = "3\t3\t11\n"
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.wc.input", create=True)
    def test_line_count_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["AAA\nBBB\nCCC"]
        new_wc = wc(["-l"])
        actual_output = new_wc._execute()
        expected_output = "3\n"
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.wc.input", create=True)
    def test_character_count_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["AAA\nBBB\nCCC"]
        new_wc = wc(["-m"])
        actual_output = new_wc._execute()
        expected_output = "11\n"
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.wc.input", create=True)
    def test_word_count_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["AAA\nBBB CCC\nDDD"]
        new_wc = wc(["-w"])
        actual_output = new_wc._execute()
        expected_output = "4\n"
        self.assertEqual(actual_output, expected_output)

    def test_all_counts_with_file(self):
        new_wc = wc(["/comp0010/test/input.txt"])
        actual_output = new_wc._execute()
        expected_output = "3\t3\t12\n"
        self.assertEqual(actual_output, expected_output)

    def test_all_counts_with_multiple_file(self):
        new_wc = wc(["/comp0010/test/input.txt", "/comp0010/test/input.txt"])
        actual_output = new_wc._execute()
        expected_output = (
            "3\t3\t12\t/comp0010/test/input.txt\n"
            "3\t3\t12\t/comp0010/test/input.txt\n"
        )
        self.assertEqual(actual_output, expected_output)

    def test_line_count_with_file(self):
        new_wc = wc(["-l", "/comp0010/test/input.txt"])
        actual_output = new_wc._execute()
        expected_output = "3\n"
        self.assertEqual(actual_output, expected_output)

    def test_character_count_with_file(self):
        new_wc = wc(["-m", "/comp0010/test/input.txt"])
        actual_output = new_wc._execute()
        expected_output = "12\n"
        self.assertEqual(actual_output, expected_output)

    def test_word_count_with_file(self):
        new_wc = wc(["-w", "/comp0010/test/input.txt"])
        actual_output = new_wc._execute()
        expected_output = "3\n"
        self.assertEqual(actual_output, expected_output)

    def test_line_count_with_invalid_file(self):
        new_wc = wc(["-l", "invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_wc._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'wc cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_character_count_with_invalid_file(self):
        new_wc = wc(["-m", "invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_wc._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'wc cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_word_count_with_invalid_file(self):
        new_wc = wc(["-w", "invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_wc._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'wc cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_all_counts_with_invalid_file(self):
        new_wc = wc(["invalid_file.txt"])
        with self.assertRaises(NoFileFoundError) as error:
            new_wc._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'wc cannot locate "invalid_file.txt"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_wc_with_file(self):
        new_wc = wc(["/comp0010/test/input.txt"])
        out = new_wc._execute()
        self.assertEqual(out, "3\t3\t12\n")

    def test_unsafe_wc(self):
        new_wc = _wc(["/comp0010/test/input.txt"])
        out = new_wc._execute()
        self.assertEqual(out, "3\t3\t12\n")


class Test_mv(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    def test_mv_with_files(self):
        new_mv = mv(
            [
                "/comp0010/test_directory/aaa.txt",
                "/comp0010/test_directory/dir2",
            ]
        )
        out = new_mv._execute()
        self.assertEqual(out, "")

    def test_mv_with_invalid_file(self):
        new_mv = mv(["invalid_file.txt", "/comp0010/test_directory/dir1"])
        with self.assertRaises(NoFileFoundError) as error:
            new_mv._execute()
        exceptionMessage = (
            "No File Found Error -> application: "
            'mv cannot locate "[invalid_file.txt], '
            '[/comp0010/test_directory/dir1]"'
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_mv_with_wrong_num_of_args(self):
        new_mv = mv(
            [
                "/comp0010/test_directory/aaa.txt",
                "/comp0010/test_directory/dir1",
                "/comp0010/test_directory/dir2",
            ]
        )
        with self.assertRaises(WrongNumberOfArgsError) as error:
            new_mv._execute()
        exceptionMessage = (
            "Wrong number of arguments -> application: "
            "mv requires 2 argument(s), but 3 argument(s) was entered"
        )
        self.assertEqual(exceptionMessage, str(error.exception))

    def test_unsafe_mv(self):
        new_mv = _mv(
            [
                "/comp0010/test_directory/aaa.txt",
                "/comp0010/test_directory/dir2",
            ]
        )
        out = new_mv._execute()
        self.assertEqual(out, "")


class Test_tsort(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010/test_directory/dir1")
        return super().setUp()

    @mock.patch("applications.tsort.input", create=True)
    def test_tsort_with_user_input(self, mocked_input):
        mocked_input.side_effect = ["9-12 6-8"]
        new_tsort = tsort([])
        actual_output = new_tsort._execute()
        expected_output = "> 9 12\n> 6 8\n9\n6\n12\n8\n"
        self.assertEqual(actual_output, expected_output)

    @mock.patch("applications.tsort.input", create=True)
    def test_tsort_with_user_input_dag_error(self, mocked_input):
        mocked_input.side_effect = ["8-6 6-8"]
        new_tsort = tsort([])
        with self.assertRaises(GraphInitialisationError) as error:
            new_tsort._execute()
        exceptionmessage = (
            "Graph Initialisation Error -> application: tsort "
            'cannot initialise a DAG from "stdin", '
            "due to a cycle in the graph."
        )
        self.assertEqual(exceptionmessage, str(error.exception))

    @mock.patch("applications.tsort.input", create=True)
    def test_tsort_with_user_input_2(self, mocked_input):
        mocked_input.side_effect = ["9-12"]
        new_tsort = tsort([])
        actual_output = new_tsort._execute()
        expected_output = "> 9 12\n9\n12\n"
        self.assertEqual(actual_output, expected_output)

    def test_tsort_with_file_cyclic_graph(self):
        new_tsort = tsort(["/comp0010/test/cyclic_graph.txt"])
        with self.assertRaises(GraphInitialisationError) as error:
            new_tsort._execute()
        exceptionmessage = (
            "Graph Initialisation Error -> application: tsort "
            'cannot initialise a DAG from "/comp0010/test/cyclic_graph.txt", '
            "due to a cycle in the graph."
        )
        self.assertEqual(exceptionmessage, str(error.exception))

    def test_tsort_with_file(self):
        new_tsort = tsort(["/comp0010/test/DAG.txt"])
        out = new_tsort.run()
        self.assertEqual(
            out,
            "> 3 8\n> 3 10\n> 5 11\n> 7 8\n> 7 11\n> 8 9\n> 11 2\n"
            "> 11 9\n> 11 10\n3\n5\n7\n8\n11\n2\n9\n10\n",
        )

    def test_tsort_with_IO(self):
        new_tsort = tsort(["</comp0010/test/DAG.txt"])
        out = new_tsort.run()
        self.assertEqual(
            out,
            "> 3 8\n> 3 10\n> 5 11\n> 7 8\n> 7 11\n> 8 9\n> 11 2\n"
            "> 11 9\n> 11 10\n3\n5\n7\n8\n11\n2\n9\n10\n",
        )

    def test_tsort_with_unlocatable_file(self):
        new_tsort = tsort(["nowhere"])
        with self.assertRaises(NoFileFoundError) as error:
            new_tsort._execute()
        exceptionmessage = (
            "No File Found Error -> application: tsort "
            'cannot locate "nowhere"'
        )
        self.assertEqual(exceptionmessage, str(error.exception))

    def test_tsort_with_file_bad_syntax(self):
        new_tsort = tsort(["/comp0010/test/bad_syntax_graph.txt"])
        with self.assertRaises(InvalidGraphError) as error:
            new_tsort._execute()
        exceptionmessage = (
            "Invalid Graph Error -> application: tsort "
            "expects a graph with edge relations defined:"
            ' "x-y" meaning "x to y" but '
            "received a graph with undefined edge relation(s): ['2&5']"
        )
        self.assertEqual(exceptionmessage, str(error.exception))

    @mock.patch("applications.tsort.input", create=True)
    def test_tsort_with_user_input_bad_syntax(self, mocked_input):
        mocked_input.side_effect = ["6@8"]
        new_tsort = tsort([])
        with self.assertRaises(InvalidGraphError) as error:
            new_tsort._execute()
        exceptionmessage = (
            "Invalid Graph Error -> application: tsort "
            "expects a graph with edge relations defined:"
            ' "x-y" meaning "x to y" but '
            "received a graph with undefined edge relation(s): ['6@8']"
        )
        self.assertEqual(exceptionmessage, str(error.exception))

    def test_tsort_with_wrong_number_of_args(self):
        new_tsort = tsort(["1", "2"])
        with self.assertRaises(WrongNumberOfArgsError):
            new_tsort._execute()

    def test_unsafe_tsort(self):
        new_sed = _tsort(["/comp0010/test/input.txt"])
        out = new_sed._execute()
        self.assertEqual(out, "")
