import unittest

from shell import shell
from sub_shell import sub_shell
from Features.Quote_Remover import Quote_Remover
from Features.Globber import Globber
from Features.Command_Substituter import Command_Substituter
from Features.Application_Setter import Application_Setter
from Features.Pipeline import Pipeline

from applications.echo import echo
from applications.cut import cut

from collections import deque


class TestQuoteRemover(unittest.TestCase):
    def test_remove_quotes_from_arg(self):
        out = deque()
        q = Quote_Remover()
        testDict = {
            '"aaa"': "aaa",
            'a"a"a': "aaa",
            '"a"a': "aa",
            'a"a"': "aa",
            "a\"'a'\"a": "a'a'a",
            "a'\"a\"'a": 'a"a"a',
            'a"\'"a"\'"a': "a'a'a",
            "a'\"'a'\"'a": 'a"a"a',
            '"a"\'a\'"a"': "aaa",
        }
        for testcase, answer in testDict.items():
            ss = sub_shell(testcase, out)
            ss.parse()
            q.remove_quotes_from_args(ss)
            call = ss.getCommandSequence()[0]
            self.assertEqual(call.getArgs()[0], answer)

    def test_remove_quotes_from_call(self):
        out = deque()
        q = Quote_Remover()
        testCase = "echo `echo hello` 'world'"
        answer = ["echo", "`echo hello`", "world"]

        ss = sub_shell(testCase, out)
        ss.parse()
        q.remove_quotes_from_args(ss)
        call = ss.getCommandSequence()[0]
        self.assertEqual(call.getArgs(), answer)

    def test_remove_quotes_from_pipe(self):
        out = deque()
        q = Quote_Remover()
        testCase = "echo 'hello' | echo 'world'"
        answer = [["echo", "hello"], ["echo", "world"]]

        ss = sub_shell(testCase, out)
        ss.parse()
        q.remove_quotes_from_args(ss)
        pipe = ss.getCommandSequence()
        for pipe_index in range(len(pipe)):
            calls = pipe[pipe_index].getCalls()
            for call_index in range(len(calls)):
                # print(calls[call_index].getArgs(), answer[call_index])
                self.assertEqual(
                    calls[call_index].getArgs(), answer[call_index]
                )


class TestGlobe(unittest.TestCase):
    def test_globe_with_call(self):
        out = deque()
        g = Globber()
        testDict = {
            "*.txt": ["dummy.txt", "requirements.txt"],
            "req*.txt": ["requirements.txt"],
            "thisFileDoesNotExist*.txt": ["thisFileDoesNotExist*.txt"],
            "echo '*.txt'": ["echo", "'*.txt'"],
            "echo": ["echo"],
            # "echo *.txt | cat": [['echo', 'requirements.txt'], ['cat']],
        }
        for testcase, answer in testDict.items():
            ss = sub_shell(testcase, out)
            ss.parse()
            g.globe(ss)
            call = ss.getCommandSequence()[0]
            self.assertEqual(call.getArgs(), answer)

    def test_globe_with_pipe(self):
        out = deque()
        g = Globber()
        testDict = {
            "echo *.txt | cat": [
                ["echo", "dummy.txt", "requirements.txt"],
                ["cat"],
            ],
        }
        for testcase, answer in testDict.items():
            ss = sub_shell(testcase, out)
            ss.parse()
            g.globe(ss)
            pipe = ss.getCommandSequence()
            for pipe_index in range(len(pipe)):
                calls = pipe[pipe_index].getCalls()
                for call_index in range(len(calls)):
                    self.assertEqual(
                        calls[call_index].getArgs(), answer[call_index]
                    )


class TestCommandSubstituter(unittest.TestCase):
    def test_command_substituter_with_call(self):
        out = deque()
        cs = Command_Substituter()
        s = shell()
        testDict = {
            "echo `echo hello world`": ["echo", "hello", "world"],
            "`echo echo` hello world": ["echo", "hello", "world"],
            "`echo echo hello` world": ["echo", "hello", "world"],
            "echo a`echo b`c": ["echo", "abc"],
            "echo `echo hello ;echo world`": ["echo", "hello", "world"],
            'echo "`echo hello world`"': ["echo", '"hello world"'],
        }
        for testcase, answer in testDict.items():
            ss = sub_shell(testcase, out)
            ss.parse()
            cs.command_substitute(ss, s)
            call = ss.getCommandSequence()[0]
            self.assertEqual(call.getArgs(), answer)

    def test_command_substituter_with_pipe(self):
        out = deque()
        cs = Command_Substituter()
        s = shell()
        testDict = {
            "echo hello | echo world": [["echo", "hello"], ["echo", "world"]]
        }
        for testcase, answer in testDict.items():
            ss = sub_shell(testcase, out)
            ss.parse()
            cs.command_substitute(ss, s)
            pipe = ss.getCommandSequence()
            for pipe_index in range(len(pipe)):
                calls = pipe[pipe_index].getCalls()
                for call_index in range(len(calls)):
                    self.assertEqual(
                        calls[call_index].getArgs(), answer[call_index]
                    )


class TestApplicationSetter(unittest.TestCase):
    def test_application_setter_with_call(self):
        out = deque()
        a = Application_Setter()
        testDict = {
            "pwd": ["pwd"],
            "echo hello world": ["echo"],
            "echo hello ; echo world": ["echo", "echo"],
            # "echo abc | cut -b 1": ['echo', 'cut'],
            "cat input.txt < input2.txt > output.txt": ["cat"],
            "<input.txt cat input2.txt": ["cat"],
            ">output.txt cat input.txt": ["cat"],
        }
        for testcase, answer in testDict.items():
            ss = sub_shell(testcase, out)
            ss.parse()
            a.set_applications(ss)
            calls = ss.getCommandSequence()
            for call_index in range(len(calls)):
                # call = calls[call_index].getApp()
                self.assertEqual(
                    calls[call_index].getApp(), answer[call_index]
                )

    def test_application_setter_with_pipe(self):
        out = deque()
        a = Application_Setter()
        testDict = {
            # "pwd": ['pwd'],
            # "echo hello world": ['echo'],
            # "echo hello ; echo world": ['echo', 'echo'],
            "echo abc | cut -b 1": ["echo", "cut"],
            # "cat input.txt < input2.txt > output.txt": ['cat'],
            # "<input.txt cat input2.txt": ['cat'],
            # ">output.txt cat input.txt": ['cat'],
        }
        for testcase, answer in testDict.items():
            ss = sub_shell(testcase, out)
            ss.parse()
            a.set_applications(ss)
            pipe = ss.getCommandSequence()
            for pipe_index in range(len(pipe)):
                calls = pipe[pipe_index].getCalls()
                for call_index in range(len(calls)):
                    # print(calls[call_index].getApp())
                    self.assertEqual(
                        calls[call_index].getApp(), answer[call_index]
                    )


class TestPipeline(unittest.TestCase):
    def test_pipeline(self):
        app_1 = echo(["ABCDE"])
        app_1.run()
        app_2 = cut(["-b", "1-3,5"])
        testResult = Pipeline().pipe(app_1, app_2, deque())
        self.assertEqual(testResult, "ABCE\n")

    def test_pipeline_exception_crash(self):
        out = deque()
        new_shell = shell()
        with self.assertRaises(SystemExit):
            new_shell.eval("ls nowhere | echo world", out)
