import unittest

from command.Call import Call
from command.Pipe import Pipe
from command.App_Factory import App_Factory
from shell import shell
from collections import deque
from applications.echo import echo, _echo

from Errors.UnsupportedApplicationError import UnsupportedApplicationError


class TestCall(unittest.TestCase):
    def test_call_setter_getter(self):
        testApp = "echo"
        testArgs = ["list", "of", "test", "cases"]
        testRequiresCommandSubstitution = ["hello", "`echo world`"]
        c = Call()
        c.set_app(testApp)
        c.set_args(testArgs)

        # testing set_app & getApp
        self.assertEqual(c.getApp(), testApp)

        # testing set_args & getArgs
        self.assertEqual(c.getArgs(), testArgs)

        c = Call()
        # test requires command substitution (no argument)
        requiresCommandSubstitution = c.requires_command_substitution()
        self.assertFalse(requiresCommandSubstitution)

        # test requires command substitution (there is no command substitution)
        c.set_args(testArgs)
        self.assertFalse(c.requires_command_substitution())

        # test requires command substitution (there is command substitution)
        c.set_args(testRequiresCommandSubstitution)
        self.assertTrue(c.requires_command_substitution())

    def test_call_try_create_application(self):
        testCases = [
            ["echo", ["list", "of", "test", "cases"], echo],
            ["_echo", ["list", "of", "test", "cases"], _echo],
            ["echo", ["``"], echo],
            # ['invalidApp', [], None]
        ]
        c = Call()
        for testCase in testCases:
            app, args, appType = testCase[0], testCase[1], testCase[2]
            c.set_app(app)
            c.set_args(args)
            app = c.try_create_application()

            # test application type
            self.assertTrue(isinstance(app, appType))

            # test application args
            self.assertEqual(app._args, args)

    def test_call_execute(self):
        validTestCase = [
            "echo",
            ["list", "of", "test", "cases"],
            "list of test cases\n",
        ]

        c = Call()
        app, args, answer = (
            validTestCase[0],
            validTestCase[1],
            validTestCase[2],
        )
        c.set_app(app)
        c.set_args(args)
        output = c.execute().get_stdout()

        # print('output: ', output)
        self.assertEqual(output, answer)

        invalidTestCase = ["catt", ["/comp0010/test/input.txt"]]

        c = Call()
        app, args = invalidTestCase[0], invalidTestCase[1]
        c.set_app(app)
        c.set_args(args)
        with self.assertRaises(SystemExit):
            c.execute()

    def test_call_unsupported_app(self):
        testCase = ["unsupportedApp", ["list", "of", "test", "cases"]]
        app, args = testCase[0], testCase[1]
        c = Call()
        c.set_app(app)
        c.set_args(args)
        with self.assertRaises(SystemExit):
            c.execute()


class TestPipe(unittest.TestCase):
    def test_addCall(self):
        testCase = ["echo", ["list", "of", "test", "cases"]]
        testCaseWithSubstitution = ["echo", ["hello", "`echo world`"]]
        app, args = testCase[0], testCase[1]
        app1, args1 = testCaseWithSubstitution[0], testCaseWithSubstitution[1]

        c, c1 = Call(), Call()
        c.set_app(app)
        c.set_args(args)
        c1.set_app(app1)
        c1.set_args(args1)
        p = Pipe()

        # test requires command substitution (no argument)
        requiresCommandSubstitution = p.requires_command_substitution()
        self.assertFalse(requiresCommandSubstitution)

        # test requires command substitution (there is no command substitution)
        p.addCall(c)
        requiresCommandSubstitution = p.requires_command_substitution()
        self.assertFalse(requiresCommandSubstitution)

        # testing addCall & getCalls
        self.assertEqual(len(p.getCalls()), 1)
        self.assertEqual(p.getCalls()[0], c)

        p.addCall(c1)
        # test requires command substitution (there is command substitution)
        requiresCommandSubstitution = p.requires_command_substitution()
        self.assertTrue(requiresCommandSubstitution)

    def test_pipe_print(self):
        testCase = ["echo", ["list", "of", "test", "cases"]]
        testCase1 = ["echo", ["hello", "`echo world`"]]
        app, args = testCase[0], testCase[1]
        app1, args1 = testCase1[0], testCase1[1]
        c, c1, p = Call(), Call(), Pipe()
        c.set_app(app)
        c.set_args(args)
        c1.set_app(app1)
        c1.set_args(args1)
        p.addCall(c)
        p.addCall(c1)
        p.print()

    def test_pipe_execute(self):
        testCase = ["echo", ["list", "of", "test", "cases"]]
        testCase1 = ["cut", ["-b", "1-3"]]
        app, args = testCase[0], testCase[1]
        app1, args1 = testCase1[0], testCase1[1]
        c, c1, p = Call(), Call(), Pipe()
        c.set_app(app)
        c.set_args(args)
        c1.set_app(app1)
        c1.set_args(args1)
        p.addCall(c)
        p.addCall(c1)

        self.assertEqual(p.execute().get_stdout(), "lis\n")

    def test_App_Factory(self):
        appFactory = App_Factory()

        appType = echo
        testCase = ["echo", ["hello", "world"]]
        app, args = testCase[0], testCase[1]
        self.assertTrue(
            isinstance(appFactory.create_application(app, args), appType)
        )

        testCase1 = ["_echo", ["hello", "world"]]
        app1, args1 = testCase1[0], testCase1[1]
        self.assertTrue(
            isinstance(appFactory.create_application(app1, args1), appType)
        )

        testCase2 = ["unsupportedApp", ["hello", "world"]]
        app2, args2 = testCase2[0], testCase2[1]
        with self.assertRaises(UnsupportedApplicationError) as ctx:
            appFactory.create_application(app2, args2)
        exceptionMessage = (
            "Unsupported Application -> application: "
            '"unsupportedApp" is not supported'
        )
        self.assertEqual(exceptionMessage, str(ctx.exception))

    def test_double_amp_stderr_0(self):
        out = deque()
        new_shell = shell()
        new_shell.eval("ls nowhere && echo world", out)
        self.assertEqual(out.popleft(), "")
        self.assertEqual(len(out), 0)

    def test_double_amp_stderr_1(self):
        out = deque()
        new_shell = shell()
        new_shell.eval("echo hello && echo world", out)
        self.assertEqual(out.popleft(), "hello\n ")
        self.assertEqual(out.popleft(), "world\n")
        self.assertEqual(len(out), 0)

    def test_double_pipe_stderr_0(self):
        out = deque()
        new_shell = shell()
        new_shell.eval("ls nowhere || echo world", out)
        self.assertEqual(out.popleft(), " ")
        self.assertEqual(out.popleft(), "world\n")
        self.assertEqual(len(out), 0)

    def test_double_pipe_stderr_1(self):
        out = deque()
        new_shell = shell()
        new_shell.eval("echo hello || echo world", out)
        self.assertEqual(out.popleft(), "hello\n")
        self.assertEqual(len(out), 0)
