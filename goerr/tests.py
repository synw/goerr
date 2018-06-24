import unittest
from goerr import Trace
from goerr.colors import colors


class TestErr(Trace):

    def create(self):
        try:
            "a" > 1
        except Exception as e:
            self.err(e)
            return e

    def create_from_msg(self):
        return self.err("Error message")


class GoerrTest(unittest.TestCase):

    def setUp(self):
        self.err = TestErr()

    def test_err_from_ex(self):
        self.assertFalse(self.err.exists)
        ex = self.err.create()
        self.assertTrue(self.err.exists)
        self.assertEqual(len(self.err.errors), 1)
        err = self.err.errors[0]
        self.assertEqual(err.ex, ex)
        self.assertEqual(err.type, "<class 'TypeError'>")
        self.assertEqual(err.msg, "unorderable types: str() > int()")

    def test_err_from_msg(self):
        self.err.create_from_msg()
        self.assertEqual(len(self.err.errors), 2)
        self.assertEqual(self.err.errors[1].msg, "Error message")

    def test_reset(self):
        self.err.reset()
        self.assertEqual(len(self.err.errors), 0)

    def test_log(self):
        self.err.reset()
        self.err.create_from_msg()
        msg = self.err.log()
        self.assertEqual(msg, "Error message from create_from_msg")
        self.err.reset()
        self.err.create()
        msg = self.err.log()
        self.assertEqual(
            msg, 'unorderable types: str() > int() "a" > 1 from create')
        self.err.reset()
        msg = self.err.log()
        self.assertIsNone(msg)

    def test_stack(self):
        self.err.reset()
        self.err.stack()
        self.assertEqual(len(self.err.errors), 0)
        self.err.create_from_msg()
        self.err.stack()
        self.assertEqual(len(self.err.errors), 2)
        err = self.err.errors[1]
        """expected = "[" + colors.red("Error") + "] "
        expected += "from " + colors.bold("create_from_msg") + "\n"
        expected += "Error message"""
        self.assertIsNone(err.msg)
        self.assertEqual(err.function, "test_stack")

    def test_check(self):
        self.err.reset()
        self.err.check()
        self.assertEqual(len(self.err.errors), 0)
        self.err.create_from_msg()
        self.err.check()

    """def test_fatal(self):
        self.err.reset()
        self.err.create()
        try:
            "x" > 2
        except Exception as e:
            self.err.fatal(e)
        #self.assertEqual(len(self.err.errors), 1)
        self.assertRaises(TypeError)"""

    def test_display(self):
        self.err.reset()
        self.err.err("Error message", display=True)
        self.err.err("Error message", display=False)
        self.err.err("Error message")

    def test_get_args(self):
        self.err.reset()
        e = self.err.create()
        ex, _ = self.err._get_args(e)
        self.assertEqual(ex, e)
        _, msg = self.err._get_args("Error message")
        self.assertEqual(msg, "Error message")

    def test_err_msg_traceback(self):
        self.err.reset()
        self.err.create()
        err = self.err.errors[0]
        err._errmsg(True)
        self.assertIsNotNone(err.tb)
        self.err.reset()
        self.err.create_from_msg()
        err = self.err.errors[0]
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
        self.assertEqual(txt, res)


if __name__ == '__main__':
    unittest.main()
