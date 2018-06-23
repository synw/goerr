from goerr import Trace


def msg(mesg):
    print("------------------------------------------------")
    print(mesg)
    print("------------------------------------------------")


class TestErr(Trace):

    def func1(self):
        msg("Function 1 running")
        self.output("function 1")
        try:
            "a" > 1
        except Exception as e:
            self.err(e)

    def func2(self):
        msg("Function 2 running")
        self.output("function 2")
        try:
            int({})
        except Exception as e:
            self.err(e, "Error message")

    def func3(self):
        msg("Function 3 running")
        self.output("function 3")
        self.err("An error has occured")

    def run(self):
        self.func1()
        self.func2()
        self.func3()
        self.stack()

    def output(self, msg, i=3):
        while i > 0:
            print(msg)
            i -= 1


te = TestErr()
te.run()
msg("### Log msg:")
log_msg = te.log()
print(log_msg)
msg("### Full trace:")
te.check()
