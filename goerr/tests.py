import unittest
from datetime import datetime
from goerr import Err
from goerr.messages import Msgs
from goerr.colors import colors


tr = Err()
tr.trace_errs = True


class ErrTest(unittest.TestCase):

    def test_repr(self):
        tr.errors = []
        tr.err("An error message")
        msg = "<goerror.Err object: 1 error>"
        self.assertEqual(tr.__repr__(), msg)
        tr.err("An error message")
        msg = "<goerror.Err object: 2 errors>"
        self.assertEqual(tr.__repr__(), msg)

    def test_str(self):
        tr.errors = []
        tr.err("An error message")
        msg = "[\033[91merror\033[0m] from \033[1mtest_str\033[0m\nAn error message"
        self.assertEqual(tr.__str__(), msg)

    def test_error(self):
        tr.errors = []
        try:
            "a" > 1
        except Exception as e:
            tr.err(e)
        tr.err("Another error")
        tr.trace()

    def test_caller(self):
        class Foo():
            def func1(self):
                try:
                    1 > "bar"
                except Exception as e:
                    tr.err(e)

            def func2(self):
                self.func1()
                try:
                    now = datetime.later()
                except Exception as e:
                    tr.err(e, "Now is not later!")

        Foo().func2()
        self.assertEqual(tr.errors[0].caller, "func2")
        self.assertEqual(tr.errors[0].function, "func1")
        self.assertEqual(tr.errors[1].caller, "test_caller")
        self.assertEqual(tr.errors[1].function, "func2")

    """def test_caller_from_lib(self):

        class Bar(Err):

            def run(self):
                self.func3()

            def func1(self):
                df = None
                try:
                    df = pd.DataFrame("wrong")
                except Exception as e:
                    self.err(e)
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
        print("ERRS -----------------")
        i = 0
        for el in foo.errors:
            print(i, el.caller, el.function)
            i += 1
        print("********************************")
        tr.trace()
        print("********************************")
        self.assertEqual(foo.errors[0].function, "__init__")
        self.assertEqual(foo.errors[0].caller, "func1")"""

    def test_no_traceback(self):
        tr.errors = []
        tr.errs_traceback = False
        try:
            "a" > 1
        except Exception as e:
            tr.err(e)
        tr.err("Another error")
        tr.trace()
        tr.errs_traceback = True

    def test_no_trace(self):
        tr.errors = []
        tr.trace_errs = False
        try:
            "a" > 1
        except Exception as e:
            tr.err(e)
        tr.err("Another error")
        self.assertEqual(len(tr.errors), 0)
        tr.trace_errs = True

    def test_fatal(self):
        try:
            "a" > 1
        except Exception as e:
            tr.fatal(e, test=True)

    def test_warning(self):
        tr.errors = []
        msg = "A warning message"
        tr.warning(msg)
        self.assertEqual(tr.errors[0].msg, msg)

    def test_info(self):
        tr.errors = []
        msg = "An info message"
        tr.info(msg)
        self.assertEqual(tr.errors[0].msg, msg)

    def test_debug(self):
        tr.errors = []
        msg = "A debug message"
        tr.debug(msg)
        self.assertEqual(tr.errors[0].msg, msg)

    def test_single_error(self):
        tr.errors = []
        msg = "A message"
        tr.error(msg)
        self.assertEqual(len(tr.errors), 0)
        tr.error()

    def test_via(self):
        tr.errors = []
        msg = "A message"
        tr.err(msg)
        tr.err()
        self.assertEqual(len(tr.errors), 2)
        tr.trace()

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
