from datetime import datetime
from goerr import Err

'''
Print an errors trace after the execution
'''


def run_func(funcname):
    i = 3
    while i > 0:
        print(funcname + "running")
        i -= 1


class Foo(Err):
    # activate the tracing
    trace_errs = True

    def func1(self):
        run_func("func1")
        try:
            1 > "bar"
        except Exception as e:
            self.err(e)
        run_func("func1")

    def func2(self):
        run_func("func2")
        try:
            now = datetime.later()
        except Exception as e:
            self.err(e, "Now is not later!")
        run_func("func2")


foo = Foo()
foo.func1()
foo.func2()
print("Run finished, checking:")
foo.trace()