import unittest
from shell import shell
from collections import deque


class TestShell(unittest.TestCase):

    """
    Test for Shell
    """

    def test_shell(self):
        out = deque()
        shell().eval("echo foo", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    def test_shell_prime(self):
        out = deque()
        new_shell = shell()
        new_shell.eval("`echo echo foo`", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)
