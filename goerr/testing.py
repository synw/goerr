import unittest
from io import StringIO
from contextlib import redirect_stdout


tc = unittest.TestCase()


def assert_err(err_type, func, *args, **kwargs):
    f = StringIO()
    with redirect_stdout(f):
        func(*args, **kwargs)
    displayed = f.getvalue()
    is_displayed = False
    err_label = "[\033[91merror\033[0m]"
    if err_label in displayed:
        if err_type is not None:
            if err_type in displayed:
                is_displayed = True
        else:
            is_displayed = True
    tc.assertTrue(is_displayed)
