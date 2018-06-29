import unittest
from datetime import datetime
from goerr import Err
from goerr.messages import Msgs
from goerr.colors import colors


tr = Err()


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

    def test_log(self):
        tr.errors = []
        tr.err("Another error")
        print("ERRORS", tr.errors)
        self.assertEqual(tr.log(), "Another error")

    """def test_caller(self):
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
        self.assertEqual(tr.errors[0].function, "func1")"""

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


"""
class TestErr(Trace):

    def create(self):
        try:
            "a" > 1
        except Exception as e:
            tr.err(e)
            return e

    def create_from_msg(self):
        return tr.err("Error message")


class GoerrTest(unittest.TestCase):

    def setUp(self):
        tr.err = TestErr()

    def test_err_from_ex(self):
        self.assertFalse(len (tr.errors) > 0)
        ex = tr.err.create()
        self.assertTrue(len (tr.errors) > 0)
        self.assertEqual(len(tr.errs), 1)
        err = tr.errs[0]
        self.assertEqual(err.ex, ex)
        self.assertEqual(err.type, "<class 'TypeError'>")
        self.assertEqual(err.msg, "unorderable types: str() > int()")

    def test_err_from_msg(self):
        tr.err.create_from_msg()
        self.assertEqual(len(tr.errs), 2)
        self.assertEqual(tr.errs[1].msg, "Error message")

    def test_reset(self):
        tr.errors = []
        self.assertEqual(len(tr.errs), 0)

    def test_log(self):
        tr.errors = []
        tr.err.create_from_msg()
        msg = tr.err.log()
        self.assertEqual(msg, "Error message from create_from_msg")
        tr.errors = []
        tr.err.create()
        msg = tr.err.log()
        self.assertEqual(
            msg, 'unorderable types: str() > int() "a" > 1 from create')
        tr.errors = []
        msg = tr.err.log()
        self.assertIsNone(msg)

    def test_stack(self):
        tr.errors = []
        tr.err.stack()
        self.assertEqual(len(tr.errs), 0)
        tr.err.create_from_msg()
        tr.err.stack()
        self.assertEqual(len(tr.errs), 2)
        err = tr.errs[1]
        # expected = "[" + colors.red("Error") + "] "
        # expected += "from " + colors.bold("create_from_msg") + "\n"
        # expected += "Error message
        self.assertIsNone(err.msg)
        self.assertEqual(err.function, "test_stack")

    def test_check(self):
        tr.errors = []
        self.trace()
        self.assertEqual(len(tr.errs), 0)
        tr.err.create_from_msg()
        self.trace()

    "def test_fatal(self):
        tr.errors = []
        tr.err.create()
        try:
            "x" > 2
        except Exception as e:
            tr.err.fatal(e)
        #self.assertEqual(len(tr.errs), 1)
        self.assertRaises(TypeError)""

    def test_display(self):
        tr.errors = []
        tr.err("Error message", display=True)
        tr.err("Error message", display=False)
        tr.err("Error message")

    def test_get_args(self):
        tr.errors = []
        e = tr.err.create()
        ex, _ = tr.err._get_args(e)
        self.assertEqual(ex, e)
        _, msg = tr.err._get_args("Error message")
        self.assertEqual(msg, "Error message")

    def test_err_msg_traceback(self):
        tr.errors = []
        tr.err.create()
        err = tr.errs[0]
        err._errmsg(True)
        self.assertIsNotNone(err.tb)
        tr.errors = []
        tr.err.create_from_msg()
        err = tr.errs[0]
        err._errmsg(True)
        self.assertIsNone(err.tb)

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
        self.assertEqual(txt, res)"""


msgs = Msgs()


class TestMsgs(unittest.TestCase):

    def setUp(self):
        self.msg = "A message"

    def test_msgs(self):
        fatal = msgs.fatal()
        error = msgs.error()
        warning = msgs.warning()
        info = msgs.info()
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

    def test_msgs_with_numbers(self):
        fatal = msgs.fatal(1)
        error = msgs.error(1)
        warning = msgs.warning(1)
        info = msgs.info(1)
        debug = msgs.debug(1)
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


if __name__ == '__main__':
    unittest.main()
