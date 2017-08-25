import traceback
from goerr.colors import cols


class Trace():
    errs = []
    first_ex = None

    def __repr__(self):
        msg = "<goerr.Trace object: " + \
            str(len(self.errs)) + " errors>"
        return msg

    def new(self, msg, isfrom=None, ex=None):
        err = self._new(msg, isfrom, ex)
        self.errs.append(err)
        return self

    def get(self):
        return self.errs

    def trace(self):
        i = 0
        for err in self.errs:
            print(self._str(err, i))
            if err["error"] is not None:
                print(err["error"])
            i += 1

    def throw(self):
        self.trace()
        if self.first_ex is not None:
            raise self.first_ex
        else:
            print("No exception to raise")

    def _str(self, err, i):
        msg = err["msg"]
        if err["isfrom"] is not None:
            msg = cols.FAIL + "Error " + str(i) + cols.ENDC + " from " + cols.BOLD + \
                err["isfrom"] + cols.ENDC + " : " + msg
        return msg

    def _new(self, msg, isfrom=None, ex=None):
        err = {}
        err["msg"] = msg
        err["isfrom"] = isfrom
        err["error"] = traceback.format_exc()
        print("NEW", ex, self.first_ex)
        if ex is not None and self.first_ex is None:
            self.first_ex = ex
        return err


error = Trace()
