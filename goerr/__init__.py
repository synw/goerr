import sys
import inspect
import traceback
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Union
from .colors import colors
from .messages import Msg


class Err:
    """
    Errors manager
    """

    errors: List["Err"] = []
    trace_errs = False
    errs_traceback = True
    logger: logging.Logger
    log_errs = False
    log_format = "csv"
    log_path = "errors.log"
    test_errs_mode = False

    def __init__(
        self,
        function: str = "",
        date: datetime = datetime.now(),
        msg: str = "",
        errtype: str = "",
        errclass: str = "",
        line: int = 0,
        file: str = "",
        code: str = "",
        tb: str = "",
        ex: Union[Exception, None] = None,
        caller: str = "",
        caller_msg: str = "",
    ):
        """
        Datastructure of an error
        """
        self.date = date
        self.function = function
        self.msg = msg
        self.errtype = errtype
        self.errclass = errclass
        self.line = line
        self.file = file
        self.code = code
        self.tb = tb
        self.ex = ex
        self.caller = caller
        self.caller_msg = caller_msg
        self.new = self.err

    def __repr__(self):
        msg = "<goerror.Err object: " + str(self.errclass) + " error>"
        return msg

    def __str__(self):
        return self.msg

    def err(self, *args):
        """
        Creates an error
        """
        error = self._err("error", *args)
        return error

    def panic(self, *args):
        """
        Creates a fatal error and exit
        """
        self._err("fatal", *args)
        if self.test_errs_mode is False:  # pragma: no cover
            sys.exit(1)  # pragma: no cover

    def warning(self, *args) -> "Err":
        """
        Creates a warning message
        """
        error = self._create_err("warning", *args)
        print(self._errmsg(error))
        return error

    def info(self, *args) -> "Err":
        """
        Creates an info message
        """
        error = self._create_err("info", *args)
        print(self._errmsg(error))
        return error

    def debug(self, *args) -> "Err":
        """
        Creates a debug message
        """
        error = self._create_err("debug", *args)
        print(self._errmsg(error))
        return error

    def _create_err(self, errclass: str, *args) -> "Err":
        """
        Create an error
        """
        error = self._new_err(errclass, *args)
        self._add(error)
        return error

    def _err(self, errclass: str = "error", *args) -> "Err":
        """
        Creates an error
        """
        error = self._new_err(errclass, *args)
        if self.log_errs is True:
            sep = " "
            if self.log_format == "csv":
                sep = ","
            msg = (
                str(datetime.now())
                + sep
                + self._errmsg(error, msgformat=self.log_format)
            )
            self.logger.error(msg)
        print(self._errmsg(error))
        self._add(error)
        return error

    def _new_err(self, errclass: str, *args) -> "Err":
        """
        Error constructor
        """
        # get the message or exception
        ex, msg = self._get_args(*args)
        # construct the error
        # handle exception
        ftb: str = ""
        function: Union[str, None] = None
        errtype: str = ""
        file: str = ""
        line: int = 0
        code: str = ""
        ex_msg: str = ""
        caller: Union[str, None] = None
        caller_msg: Union[str, None] = None
        st = inspect.stack()

        if ex is not None:
            # get info from exception
            errobj, ex_msg, tb = sys.exc_info()  # type: ignore
            tb = traceback.extract_tb(tb)
            file, line, function, code = tb[-1]
            # if called from an external lib
            if len(tb) > 1:
                file, line, caller, code = tb[0]
            else:
                call_stack = []
                for c in st:
                    call_stack.append(c[3])
                caller = self._get_caller(call_stack, function or "")
            internals = [
                "err",
                "_new_err",
                "fatal",
                "warning",
                "debug",
                "info",
                "<module>",
            ]
            if caller == function or caller in internals:
                caller = None
            # handle messages
            if msg is not None:
                caller_msg = msg
                msg = str(ex_msg)
            else:
                msg = str(ex_msg)
            ftb = traceback.format_exc()
            errtype = errobj.__name__  # type: ignore
        if function is None:
            # for el in st:
            #   print(el)
            function = st[3][3]
            if function == "<module>":
                function = None
        # init error object
        date = datetime.now()
        error = Err(
            function or "",
            date,
            msg or "",
            errtype or "",
            errclass,
            line,
            file,
            code,
            ftb,
            ex,
            caller or "",
            caller_msg or "",
        )
        return error

    def _headline(self, error, i: int) -> str:
        """
        Format the error message's headline
        """
        msgs = Msg()
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
        if error.function is not None:
            msg += " from " + colors.bold(error.function)  # type: ignore
        if error.caller is not None:
            msg += " called from " + colors.bold(error.caller)  # type: ignore
        if error.caller_msg is not None:
            msg += "\n" + error.caller_msg
        if error.function is not None and error.msg is not None:
            msg += ": "
        else:
            msg = msg + " "
        if error.errtype is not None:
            msg += error.errtype + " : "
        if error.msg is not None:
            msg += error.msg
        return msg

    def _errmsg_dict(
        self, error: "Err", tb: bool = False
    ) -> Dict[str, Union[datetime, str, int]]:
        msg: Dict[str, Union[datetime, str, int]] = {"date": datetime.now()}
        if error.ex is not None:
            msg["msg"] = error.msg
            msg["line"] = error.line
            msg["code"] = error.code
            msg["file"] = error.file
            if self.errs_traceback is True or tb is True:
                if error.tb is not None:
                    msg["traceback"] = error.tb
        return msg

    def _errmsg(
        self, error: "Err", tb: bool = False, i: int = 0, msgformat: str = "terminal"
    ) -> str:
        """
        Get the error message
        """
        if msgformat == "terminal":
            msg_str = self._headline(error, i)
            if error.ex is not None:
                msg_str += "\n" + "line " + colors.bold(str(error.line))  # type: ignore
                msg_str += ": " + colors.yellow(error.code)  # type: ignore
                msg_str += "\n" + str(error.file)
                if self.errs_traceback is True or tb is True:
                    if error.tb is not None:
                        msg_str += "\n" + error.tb
            return msg_str
        elif msgformat == "csv":
            sep = ","
            msg_str = error.msg + sep
            msg_str += str(error.line) + sep + error.code + sep
            msg_str += str(error.file)
            return msg_str
        elif msgformat == "text":
            sep = ","
            msg_str = error.msg
            if error.ex is not None:
                msg_str += sep + str(error.line) + sep + error.code + sep
                msg_str += str(error.file) + sep
                if self.errs_traceback is True or tb is True:
                    if error.tb is not None:
                        msg_str += sep + error.tb
            return msg_str
        else:
            raise Exception(f"Unknown msg format {msgformat}")

    def to_dict(self):
        """
        Returns a dictionnary with the error elements
        """
        return self._errmsg(self, msgformat="dict")

    def _print_errs(self):
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

    def _add(self, error: "Err"):
        """
        Adds an error to the trace if required
        """
        if self.trace_errs is True:
            self.errors.append(error)

    def _get_caller(self, callers: List[str], function: str) -> Union[str, None]:
        """
        Get the caller function from the provided function
        """
        is_next = False
        for c in callers:
            if is_next is True:
                return c
            if function == c:
                is_next = True

    def _get_args(self, *args) -> Tuple[Union[Exception, None], Union[str, None]]:
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


class Trace(Err):
    """
    Traces manager
    """

    errors: List[Err] = []
    trace_errs = True
    errs_traceback = False

    def __repr__(self):
        s = "s"
        numerrs = len(self.errors)
        if numerrs == 1:
            s = ""
        msg = "<goerror.Trace object: " + str(numerrs) + " error" + s + ">"
        return msg

    def trace(self):
        """
        Print the errors trace if there are some errors
        """
        if len(self.errors) > 0:
            numerrs = len(self.errors)
            print("========= Trace (" + str(numerrs) + ") =========")
        self._print_errs()
        self.errors = []

    def via(self, *args) -> Union[Err, None]:
        """
        Creates an empty error to record in the stack
        trace
        """
        error = None
        if len(self.errors) > 0:
            error = self._err("via", *args)
        return error

    def panic(self, *args):
        """
        Creates a fatal error and exit
        """
        self._err(*args)
        self.trace()
        if self.test_errs_mode is False:  # pragma: no cover
            sys.exit(1)


class Log(Err):
    """
    Errors manager with logging
    """

    logger: logging.Logger
    log_errs = True
    log_format = "csv"
    log_path = "errors.log"

    def __init__(self, log_path=None):
        """
        Init Err with logger
        """
        if log_path is not None:
            self.log_path = log_path
        self.logger = logging.getLogger(__name__)
        f_handler = logging.FileHandler(self.log_path)
        f_handler.setLevel(logging.ERROR)
        self.logger.addHandler(f_handler)
        super(Log, self).__init__()
