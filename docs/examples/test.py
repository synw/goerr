from goerr import Err
from goerr.testing import assert_err

err = Err()


class Foo():

    def func1(self, param1, param2):
        print("Func 1 running")
        try:
            param1 > param2
        except Exception as e:
            err.new(e)


foo = Foo()
assert_err("TypeError", foo.func1, 1, "bar")
print("No test error")


def func2(param1, param2):
    print("Func 2 running")
    try:
        param1 > param2
    except Exception as e:
        err.new(e)

        
print("Assertion error: no error is fired:")
assert_err("TypeError", func2, 1, 0)
