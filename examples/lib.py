import time
import pandas as pd
from goerr import Trace

err = Trace()


def run_func(funcname, i=3):
    while i > 0:
        print(funcname + " running")
        i -= 1
    time.sleep(0.5)


class Foo(Trace):
    trace_errs = True

    def run(self):
        run_func("run", 1)
        self.func3()

    def func1(self):
        df = None
        run_func("func1")
        try:
            df = pd.DataFrame("wrong")
        except Exception as e:
            err.new(e)
        run_func("func1")
        return df

    def func2(self):
        # df = self.func1()
        run_func("func2")
        try:
            df = self.func1()
            df2 = df.copy()
        except Exception as e:
            err.new(e, "Can not copy dataframe")
        run_func("func2")

    def func3(self):
        # df = self.func1()
        run_func("func3")
        self.func2()
        try:
            "a" > 1
        except Exception as e:
            err.new(e)
        run_func("func3")


foo = Foo()
foo.run()
print("Run finished, checking:")
err.trace()
