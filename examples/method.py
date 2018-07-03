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
        try:
            1 > "bar"
        except Exception as e:
            self.err(e)
        run_func("func1")

    def func2(self):
        self.func1()
        run_func("func2")
        try:
            now = datetime.later()
        except Exception as e:
            self.err(e, "Now is not later!")
        run_func("func2")


foo = Foo()
foo.run()
print("Run finished")
