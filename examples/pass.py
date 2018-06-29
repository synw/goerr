from datetime import datetime
from goerr import Err


def run_func(funcname):
    i = 3
    while i > 0:
        print(funcname + "running")
        i -= 1


class Foo(Err):

    def run(self):
        self.func2()

    def func1(self):
        run_func("func1")
        self.err("An error message")
        run_func("func1")

    def func2(self):
        self.func1()
        run_func("func2")
        self.err()
        run_func("func2")


foo = Foo()
foo.run()
print("Run finished, checking:")
foo.trace()