from goerr import Err

"""
Print basic errors in a class
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


foo = Foo()
foo.func1()
print("Run finished")
