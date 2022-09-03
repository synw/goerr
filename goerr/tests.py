# flake8: noqa: E501
import unittest

# import pandas as pd
from datetime import datetime
from goerr import Err, Trace
from goerr.messages import Msg
from goerr.colors import colors


def newerr():
    err = Err()
    err.test_errs_mode = True
    return err


def newtr():
    tr = Trace()
    tr.test_errs_mode = True
    tr.errors = []
    return tr


class ErrTest(unittest.TestCase):
    def test_repr(self):
        err = newtr()
        err.new("An error message")
        msg = "<goerror.Trace object: 1 error>"
        self.assertEqual(err.__repr__(), msg)
        err.new("An error message")
        msg = "<goerror.Trace object: 2 errors>"
        self.assertEqual(err.__repr__(), msg)

    def test_str(self):
        err = newerr()
        msg = "An error message"
        error = err.new(msg)
        self.assertEqual(error.__str__(), msg)

    def test_err_msg(self):
        err = newtr()
        try:
            "a" > 1  # type: ignore
        except Exception as e:
            err.new(e)
        err.new("Another error")
        self.assertEqual(len(err.errors), 2)

    def test_caller(self):
        err = newtr()

        class Foo:
            def func1(self):
                try:
                    1 > "bar"  # type: ignore
                except Exception as e:
                    err.new(e)

            def func2(self):
                self.func1()
                try:
                    now = datetime.later()  # type: ignore
                except Exception as e:
                    err.new(e, "Now is not later!")

        foo = Foo()
        foo.func2()
        self.assertEqual(err.errors[0].caller, "func2")
        self.assertEqual(err.errors[0].function, "func1")
        self.assertEqual(err.errors[1].caller, "test_caller")
        self.assertEqual(err.errors[1].function, "func2")

        caller = err._get_caller(["one", "two"], "one")
        self.assertEqual(caller, "two")

    def test_get_args(self):
        err = newerr()
        try:
            "a" > 1  # type: ignore
        except Exception as e:
            ex, msg = err._get_args(e, "msg")
            self.assertEqual(ex, e)
            self.assertEqual(msg, "msg")

    """def test_caller_from_lib(self):
        print("---------------------------- ccccccccccccccc")

        class Bar(Err):

            def run(self):
                self.func3()

            def func1(self):
                df = None
                try:
                    df = pd.DataFrame("wrong")
                except Exception as e:
                    self.err(e)
                    print("ERR 1", self.errors[0])
                return df

            def func2(self):
                try:
                    df = self.func1()
                    df2 = df.copy()
                except Exception as e:
                    self.err(e, "Can not copy dataframe")

            def func3(self):
                #df = self.func1()
                self.func2()
                try:
                    "a" > 1
                except Exception as e:
                    self.err(e)

        foo = Bar()
        foo.run()
        i = 0
        print("ERRS: ", foo.errors)
        for el in foo.errors:
            print(i, el.caller, el.function)
            i += 1
        self.assertEqual(foo.errors[0].function, "__init__")
        self.assertEqual(foo.errors[0].caller, "func1")"""

    def test_no_traceback(self):
        err = newtr()
        err.errs_traceback = False
        try:
            "a" > 1  # type: ignore
        except Exception as e:
            err.new(e)
        err.new("Another error")
        err.trace()
        err.errs_traceback = True

    def test_no_trace(self):
        err = newerr()
        try:
            "a" > 1  # type: ignore
        except Exception as e:
            err.new(e)
        err.new("Another error")
        self.assertEqual(len(err.errors), 0)

    def test_trace(self):
        err = newtr()
        try:
            "a" > 1  # type: ignore
        except Exception as e:
            err.new(e)
        err.new("Another error")
        self.assertEqual(len(err.errors), 2)

    def test_panic(self):
        err = newerr()
        try:
            "a" > 1  # type: ignore
        except Exception as e:
            err.panic(e)

    def test_warning(self):
        err = newtr()
        msg = "A warning message"
        err.warning(msg)
        self.assertEqual(err.errors[0].msg, "A warning message")
        err.warning(msg)
        self.assertEqual(len(err.errors), 2)

    def test_info(self):
        err = newerr()
        msg = "An info message"
        error = err.info(msg)
        self.assertEqual(error.msg, msg)

    def test_debug(self):
        err = newtr()
        msg = "A debug message"
        err.debug(msg)
        self.assertEqual(err.errors[0].msg, msg)
        err.debug(msg)
        self.assertEqual(len(err.errors), 2)

    def test_via(self):
        err = newtr()
        msg = "A message"
        err.new(msg)
        err.via()
        self.assertEqual(len(err.errors), 2)

    """def test_to_dict(self):
        err = newerr()
        try:
            "a" > 1  # type: ignore
        except Exception as e:
            error = err.new(e)
            d = {
                "line": 195,
                "traceback": 'Traceback (most recent call last):\n  File "tests.py", line 195, in test_to_dict\n    "a" > 1\nTypeError: unorderable types: str() > int()\n',
                "file": "tests.py",
                "msg": "unorderable types: str() > int()",
                "code": '"a" > 1',
            }
            d2 = error.to_dict()
            del d2["date"]
            self.assertEqual(d, d2)"""

    def test_colors(self):
        color = "\033[94m"
        msg = "color"
        txt = colors.blue(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = "\033[92m"
        txt = colors.green(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = "\033[93m"
        txt = colors.yellow(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = "\033[95m"
        txt = colors.purple(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = "\033[1m"
        txt = colors.bold(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = "\033[4m"
        txt = colors.underline(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)


class TestMsgs(unittest.TestCase):
    def setUp(self):
        self.msg = "A message"

    def test_msgs(self):
        msgs = Msg()
        fatal = msgs.fatal()
        error = msgs.error()
        warning = msgs.warning()
        info = msgs.info()
        via = msgs.via()
        debug = msgs.debug()
        endmsg = "[\033[91m\033[1mfatal error\033[0m]"
        self.assertEqual(fatal, endmsg)
        endmsg = "[\033[91merror\033[0m]"
        self.assertEqual(error, endmsg)
        endmsg = "[\033[95m\033[1mwarning\033[0m]"
        self.assertEqual(warning, endmsg)
        endmsg = "[\033[94minfo\033[0m]"
        self.assertEqual(info, endmsg)
        endmsg = "[\033[93mdebug\033[0m]"
        self.assertEqual(debug, endmsg)
        endmsg = "[\033[92mvia\033[0m]"
        self.assertEqual(via, endmsg)

    def test_msgs_with_numbers(self):
        msgs = Msg()
        fatal = msgs.fatal(1)
        error = msgs.error(1)
        warning = msgs.warning(1)
        info = msgs.info(1)
        debug = msgs.debug(1)
        via = msgs.via(1)
        endmsg = "1 [\033[91m\033[1mfatal error\033[0m]"
        self.assertEqual(fatal, endmsg)
        endmsg = "1 [\033[91merror\033[0m]"
        self.assertEqual(error, endmsg)
        endmsg = "1 [\033[95m\033[1mwarning\033[0m]"
        self.assertEqual(warning, endmsg)
        endmsg = "1 [\033[94minfo\033[0m]"
        self.assertEqual(info, endmsg)
        endmsg = "1 [\033[93mdebug\033[0m]"
        self.assertEqual(debug, endmsg)
        endmsg = "1 [\033[92mvia\033[0m]"
        self.assertEqual(via, endmsg)


if __name__ == "__main__":
    unittest.main()
