import unittest
# import pandas as pd
from datetime import datetime
from goerr import Err
from goerr.messages import Msgs
from goerr.colors import colors
from goerr.testing import assert_err

errs = Err()
errs.trace_errs = True
errs.test_errs_mode = True


class ErrTest(unittest.TestCase):

    def test_repr(self):
        errs.errors = []
        errs.err("An error message")
        msg = "<goerror.Err object: 1 error>"
        self.assertEqual(errs.__repr__(), msg)
        errs.err("An error message")
        msg = "<goerror.Err object: 2 errors>"
        self.assertEqual(errs.__repr__(), msg)

    def test_str(self):
        errs.errors = []
        errs.err("An error message")
        msg = "[\033[91merror\033[0m] from \033[1mtest_str\033[0m\n" \
            "An error message"
        self.assertEqual(errs.__str__(), msg)

    def test_err_msg(self):
        errs.errors = []
        errs.errs_traceback = True
        try:
            "a" > 1
        except Exception as e:
            errs.err(e)
        errs.err("Another error")
        self.assertEqual(len(errs.errors), 2)
        errs.errs_traceback = False

    def test_caller(self):
        errs.errors = []

        class Foo():

            def func1(self):
                try:
                    1 > "bar"
                except Exception as e:
                    errs.err(e)

            def func2(self):
                self.func1()
                try:
                    now = datetime.later()
                except Exception as e:
                    errs.err(e, "Now is not later!")

        foo = Foo()
        foo.func2()
        self.assertEqual(errs.errors[0].caller, "func2")
        self.assertEqual(errs.errors[0].function, "func1")
        self.assertEqual(errs.errors[1].caller, "test_caller")
        self.assertEqual(errs.errors[1].function, "func2")

        caller = errs._get_caller(["one", "two"], "one")
        self.assertEqual(caller, "two")

    def test_get_args(self):
        try:
            "a" > 1
        except Exception as e:
            ex, msg = errs._get_args(e, "msg")
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
        errs.errors = []
        errs.errs_traceback = False
        try:
            "a" > 1
        except Exception as e:
            errs.err(e)
        errs.err("Another error")
        errs.trace()
        errs.errs_traceback = True

    def test_no_trace(self):
        errs.errors = []
        errs.trace_errs = False
        try:
            "a" > 1
        except Exception as e:
            errs.err(e)
        errs.err("Another error")
        self.assertEqual(len(errs.errors), 0)
        errs.trace_errs = True

    def test_trace(self):
        errs.errors = []
        errs.trace_errs = True
        try:
            "a" > 1
        except Exception as e:
            errs.err(e)
        errs.err("Another error")
        self.assertEqual(len(errs.errors), 2)

    def test_panic(self):
        try:
            "a" > 1
        except Exception as e:
            errs.panic(e)

    def test_warning(self):
        errs.errors = []
        msg = "A warning message"
        errs.warning(msg)
        self.assertEqual(errs.errors[0].msg, msg)
        errs.warning(msg)
        self.assertEqual(len(errs.errors), 2)

    def test_info(self):
        errs.errors = []
        msg = "An info message"
        errs.info(msg)
        self.assertEqual(errs.errors[0].msg, msg)
        errs.info(msg)
        self.assertEqual(len(errs.errors), 2)

    def test_debug(self):
        errs.errors = []
        msg = "A debug message"
        errs.debug(msg)
        self.assertEqual(errs.errors[0].msg, msg)
        errs.debug(msg)
        self.assertEqual(len(errs.errors), 2)

    def test_via(self):
        errs.errors = []
        msg = "A message"
        errs.err(msg)
        errs.err()
        self.assertEqual(len(errs.errors), 2)
        errs.trace()

    def test_colors(self):
        color = '\033[94m'
        msg = "color"
        txt = colors.blue(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = '\033[92m'
        txt = colors.green(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = '\033[93m'
        txt = colors.yellow(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = '\033[95m'
        txt = colors.purple(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = '\033[1m'
        txt = colors.bold(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)
        color = '\033[4m'
        txt = colors.underline(msg)
        res = color + msg + "\033[0m"
        self.assertEqual(txt, res)


msgs = Msgs()


class TestMsgs(unittest.TestCase):

    def setUp(self):
        self.msg = "A message"

    def test_msgs(self):
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


if __name__ == '__main__':
    unittest.main()
