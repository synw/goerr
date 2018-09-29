import sys
import inspect
import traceback
import logging
from datetime import datetime
from typing import List
from .colors import colors
from .messages import Msg


class Err():
    """
    Errors manager
    """
    errors = []  # type: List[Err]
    trace_errs = False  # type: bool
    errs_traceback = True  # type: bool
    logger = None  # type: logging.Logger
    log_errs = False  # type: bool
    log_format = "csv"  # type: str
    log_path = "errors.log"  # type: str
    test_errs_mode = False  # type: bool

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
            
    def _err(self, errclass: str="error", *args) -> "Err":
        """
        Creates an error
        """
        error = self._new_err(errclass, *args)
        if self.log_errs is True:
            sep = " "
            if self.log_format == "csv":
                sep = ","
            msg = str(datetime.now()) + sep + \
                self._errmsg(error, msgformat=self.log_format)
            self.logger.error(msg)
        print(self._errmsg(error))
        self._add(error)
        return error
            
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
            # for el in st:
            #   print(el)
            function = st[3][3]
            if function == "<module>":
                function = None
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
            msg += " from " + colors.bold(error.function)
        if error.caller is not None:
            msg += " called from " + colors.bold(error.caller)
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

    def _errmsg(self, error: "Err", tb: bool=False, i: int=None,
                msgformat: str="terminal") -> str:
        """
        Get the error message
        """
        if msgformat == "terminal":
            msg = self._headline(error, i)
            if error.ex is not None:
                msg += "\n" + "line " + colors.bold(str(error.line))
                msg += ": " + colors.yellow(error.code)
                msg += "\n" + str(error.file)
                if self.errs_traceback is True or tb is True:
                    if error.tb is not None:
                        msg += "\n" + error.tb
        elif msgformat == "csv":
            sep = ","
            msg = error.msg + sep
            msg += str(error.line) + sep + error.code + sep
            msg += str(error.file)
        elif msgformat == "text":
            sep = ","
            msg = error.msg
            if error.ex is not None:
                msg += sep + str(error.line) + sep + error.code + sep
                msg += str(error.file) + sep         
                if self.errs_traceback is True or tb is True:
                    if error.tb is not None:
                        msg += sep + error.tb
        elif msgformat == "dict":
            msg = {"date": datetime.now()}
            if error.ex is not None:
                msg["msg"] = error.msg
                msg["line"] = error.line
                msg["code"] = error.code
                msg["file"] = error.file         
                if self.errs_traceback is True or tb is True:
                    if error.tb is not None:
                        msg["traceback"] = error.tb
        return msg
    
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
    

class Trace(Err):
    """
    Tracess manager
    """
    errors = []  # type: List[Err]
    trace_errs = True  # type: bool
    errs_traceback = False  # type: bool
    
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
        
    def via(self, *args):
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
    logger = None  # type: logging.Logger
    log_errs = True  # type: bool
    log_format = "csv"  # type: str
    log_path = "errors.log"  # type: str

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
            
