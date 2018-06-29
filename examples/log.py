from datetime import datetime
from goerr import Err


class Foo(Err):

    def run(self):
        self.func2()

    def func2(self):
        try:
            now = datetime.later()
        except Exception as e:
            self.err(e, "Now is not later!")


foo = Foo()
foo.run()
print("------------- Log message:")
print(foo.log())
