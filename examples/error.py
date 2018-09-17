import pprint
from datetime import datetime
from goerr import Err

"""
Print basic errors
"""


def run_func(funcname):
    i = 3
    while i > 0:
        print(funcname + "running")
        i -= 1


class Foo(Err):

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
            error = self.err(e, "Now is not later!")
            print("Dictionnary with the error elements:")
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(self.errdict(error))
        run_func("func2")


foo = Foo()
foo.func1()
foo.func2()
print("Run finished")
