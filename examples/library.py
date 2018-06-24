import pandas as pd
from goerr import Trace


class TestRun(Trace):

    def run0(self):
        self.err("Error run zero")

    def run1(self):
        self.run0()
        try:
            pd.DataFrame("err")
        except Exception as e:
            self.err(e, "Can no construct dataframe")

    def run(self):
        self.run1()
        try:
            "x" > 2
        except Exception as e:
            self.err(e)


err = TestRun()
err.reset()
err.run()
print("----------- End of the run, checking ------------")
err.check()
