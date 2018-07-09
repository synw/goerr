import inspect
import traceback
import sys
# import json
from datetime import datetime
from .colors import colors
from .messages import Msgs
from typing import List

msgs = Msgs()


class Err():
    """
    Errors manager
    """
    errors = []  # type: List[Err]
    trace_errs = False  # type: bool
    errs_traceback = True  # type: bool

    def __init__(self, function: str=None, date: datetime=datetime.now(),
                 msg: str=None, errtype: str=None, errclass: str=None,
                 line: int=None, file: str=None, code: str=None, tb: str=None,
                 ex: Exception=None, caller: str=None, caller_msg: str=None):
        """
        Datastructure of an error
        """
        self.date = date  # type: datetime.datetime
        self.function = function  # type: str
        self.msg = msg  # type: str
        self.errtype = errtype  # type: str
        self.errclass = errclass  # type: str
        self.line = line  # type: int
        self.file = file  # type: str
        self.code = code  # type: str
        self.tb = tb  # type: str
        self.ex = ex  # type: Exception
        self.caller = caller  # type: str
        self.caller_msg = caller_msg  # type: str

    def __repr__(self):
        s = "s"
        numerrs = len(self.errors)
        if numerrs == 1:
            s = ""
        msg = "<goerror.Err object: " + str(numerrs) + " error" + s + ">"
        return msg

    def __str__(self):
        msg = ""
        for error in self.errors:
            msg = msg + self._errmsg(error)
        return msg

    def fatal(self, *args, **kwargs):
        err = self._new_err("fatal", *args)
        self.errors.append(err)
        self.trace()
        if "test" not in kwargs:  # pragma: no cover
            sys.exit(1)  # pragma: no cover

    def error(self, *args):
        """
        Creates a single error and print it
        """
        if len(args) == 0:
            print("Error from goerr.Err.error: either an exception"
                  " or a message has to be provided as argument")
            return
        err = self._new_err("error", *args)
        print(self._errmsg(err))

    def err(self, *args):
        """
        Creates an error, record it in the trace and print it
        """
        err = self._new_err("error", *args)
        if len(args) > 0:
            print(self._errmsg(err))
        else:
            err.errclass = "via"
        if self.trace_errs is True:
            self.errors.append(err)

    def warning(self, *args):
        """
        Creates a warning message and record it in the trace
        """
        err = self._new_err("warning", *args)
        print(self._errmsg(err))
        if self.trace_errs is True:
            self.errors.append(err)

    def info(self, *args):
        """
        Creates an info message and record it in the trace
        """
        err = self._new_err("info", *args)
        print(self._errmsg(err))
        if self.trace_errs is True:
            self.errors.append(err)

    def debug(self, *args):
        """
        Creates a debug message and record it in the trace
        """
        err = self._new_err("debug", *args)
        print(self._errmsg(err))
        if self.trace_errs is True:
            self.errors.append(err)

    # main constructor

    def _new_err(self, errclass: str, *args) -> 'Err':
        """
        Error constructor
        """
        # get the message or exception
        ex, msg = self._get_args(*args)
        # construct the error
        # handle exception
        ftb = None  # type: str
        function = None  # type: str
        errtype = None  # type: str
        file = None  # type: str
        line = None  # type: int
        code = None  # type: str
        ex_msg = None  # type: str
        caller = None  # type: str
        caller_msg = None  # type: str

        st = inspect.stack()

        if ex is not None:
            # get info from exception
            errobj, ex_msg, tb = sys.exc_info()
            tb = traceback.extract_tb(tb)
            file, line, function, code = tb[-1]
            # if called from an external lib
            if len(tb) > 1:
                file, line, caller, code = tb[0]
            else:
                call_stack = []
                for c in st:
                    call_stack.append(c[3])
                caller = self._get_caller(call_stack, function)

            internals = [
                "err",
                "_new_err",
                "fatal",
                "warning",
                "debug",
                "info",
                "<module>"]
            if caller == function or caller in internals:
                caller = None
            # handle messages
            if msg is not None:
                caller_msg = msg
                msg = str(ex_msg)
            else:
                msg = str(ex_msg)
            ftb = traceback.format_exc()
            errtype = errobj.__name__
        if function is None:
            function = st[2][3]
        # init error object
        date = datetime.now()
        error = Err(
            function,
            date,
            msg,
            errtype,
            errclass,
            line,
            file,
            code,
            ftb,
            ex,
            caller,
            caller_msg)
        return error

    # display

    def print_errs(self):
        """
        Prints the errors trace with tracebacks
        """
        i = 0
        for error in self.errors:
            print(self._errmsg(error, tb=True, i=i))
            # for spacing
            if self.errs_traceback is False:
                print()
            i += 1

    def trace(self):
        """
        Print the errors trace if there are some errors
        """
        if len(self.errors) > 0:
            numerrs = len(self.errors)
            print("========= Trace (" + str(numerrs) + ") =========")
        self.print_errs()
        self.errors = []

    def _headline(self, error, i: int) -> str:
        """
        Format the error message's headline
        """
        # get the error title
        if error.errclass == "fatal":
            msg = msgs.fatal(i)
        elif error.errclass == "warning":
            msg = msgs.warning(i)
        elif error.errclass == "info":
            msg = msgs.info(i)
        elif error.errclass == "debug":
            msg = msgs.debug(i)
        elif error.errclass == "via":
            msg = msgs.via(i)
        else:
            msg = msgs.error(i)
        # function name
        msg += " from " + colors.bold(error.function)
        if error.caller is not None:
            msg += " called from " + colors.bold(error.caller)
        if error.caller_msg is not None:
            msg += "\n" + error.caller_msg
        if error.errtype is not None or error.msg is not None:
            msg += "\n"
        if error.errtype is not None:
            msg += error.errtype + " : "
        if error.msg is not None:
            msg += str(error.msg)
        return msg

    def _errmsg(self, error: "Err", tb: bool=False, i: int=None) -> str:
        """
        Get the error message
        """
        msg = self._headline(error, i)
        if error.ex is not None:
            msg += "\n" + "line " + colors.bold(str(error.line))
            msg += ": " + colors.yellow(error.code)
            msg += "\n" + str(error.file)
            if self.errs_traceback is True or tb is True:
                if error.tb is not None:
                    msg += "\n" + error.tb
        return msg

    # internal method

    def _get_caller(self, callers: List[str], function: str) -> str:
        """
        Get the caller function from the provided function
        """
        is_next = False
        for c in callers:
            if is_next is True:
                return c
            if function == c:
                is_next = True

    def _get_args(self, *args) -> (Exception, str):
        """
        Returns exception and message from the provided arguments
        """
        ex = None
        msg = None
        for arg in args:
            if isinstance(arg, str):
                msg = arg
            elif isinstance(arg, Exception):
                ex = arg
        return ex, msg
