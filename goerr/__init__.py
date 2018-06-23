import inspect
import traceback
import sys
# import json
from datetime import datetime
from .colors import colors
"""
DJANGO = False
try:
    from django.core.mail import send_mail
    from django.conf import settings
    try:
        ADMINS = settings.ADMINS
        DJANGO = True
    except Exception:
        pass
except Exception:
    pass
"""


class Err():
    """
    Error object
    """

    def __init__(self, date, function, msg=None, errtype=None, line=None,
                 file=None, code=None, tb=None, ex=None):
        """
        Datastructure of an error
        """
        self.date = date  # datetime.datetime
        self.function = function  # string
        self.msg = msg  # string
        self.type = errtype  # string
        self.line = line  # int
        self.file = file  # string
        self.code = code  # string
        self.tb = tb  # string
        self.ex = ex  # Exception

    def __repr__(self):
        msg = "<goerror.Err object: '" + self.msg + "'>"
        return msg

    def __str__(self):
        return self._errmsg()

    def _print(self, tb=False, i=None):
        """
        Print the error message
        """
        print(self._errmsg(tb, i))

    def _trace(self, i=0):
        """
        Print the error message with stack trace
        """
        print(self._errmsg(True, i))

    def _headline(self, i):
        """
        Format the error message's headline
        """
        # number of the error
        errnum = "[" + colors.red("error") + "] "
        if i is not None:
            errnum = "[" + colors.red("error " + str(i)) + "] "
        msg = errnum
        # function name
        funcstr = ""
        if self.function is not None:
            funcstr = "from " + colors.bold(self.function)
            msg += str(funcstr)
        if self.type is not None or self.msg is not None:
            msg += "\n"
        if self.type is not None:
            msg += self.type + " : "
        if self.msg is not None:
            msg += str(self.msg)
        return msg

    def _errmsg(self, tb=False, i=None):
        """
        Get the error message
        """
        msg = self._headline(i)
        if self.ex is not None:
            msg += "\n" + "line " + colors.bold(str(self.line))
            msg += ": " + colors.yellow(self.code)
            msg += "\n" + str(self.file)
            if tb is True:
                if self.tb is not None:
                    msg += "\n" + self.tb
        return msg


class Trace():
    """
    Trace object
    """
    errors = []

    def __repr__(self):
        msg = "<goerror.Trace object: " + str(len(self.errors)) + " errors>"
        return msg

    @property
    def exists(self):
        """
        Check if the trace has at least one error
        """
        if len(self.errors) > 0:
            return True
        return False

    def err(self, *args, **kwargs):
        """
        Add an error to the trace
        """
        # check arguments
        self._check_args(args)
        ex, msg = self._get_args(args)
        # construct the error
        # handle exception
        errtype = None
        ftb = None
        function = None
        file = None
        line = None
        code = None
        ex_msg = None
        if ex is not None:
            # get info from exception
            errobj, ex_msg, tb = sys.exc_info()
            # if funcname is not None:
            file, line, function, code = traceback.extract_tb(tb)[-1]
            errtype = str(errobj)
            ftb = traceback.format_exc()
        if function is None:
            function = inspect.stack()[1][3]
        if ex_msg is not None:
            if msg:
                msg += " " + str(ex_msg)
            else:
                msg = str(ex_msg)
        # init error object
        date = datetime.now()
        error = Err(date, function, msg, errtype, line, file, code, ftb, ex)
        # append the error to the trace
        self.errors.append(error)
        # display the error
        display = True
        if "display" in kwargs:
            if kwargs["display"] is not False:
                display = True
        if display is True:
            print(error)

    def check(self, reset=True):
        if self.exists is True:
            caller = inspect.stack()[1][3]
            date = datetime.now()
            error = Err(date, caller)
            self.errors.append(error)
            self.trace()

    def log(self):
        if self.exists is True:
            error = self.errors[0]
            msg = error.msg
            if error.code is not None:
                msg += " " + error.code
            if error.function is not None:
                msg += " from " + error.function
            return msg

    def stack(self):
        if self.exists is True:
            caller = inspect.stack()[1][3]
            date = datetime.now()
            error = Err(date, caller)
            self.errors.append(error)

    def fatal(self, *args):
        self.err(*args, display=False)
        self.trace()
        ex = self.errors[0].ex
        self.reset()
        raise(ex)

    def trace(self):
        # errors = self.errors[::-1]
        i = 1
        for error in self.errors:
            error._print(True, i)
            i += 1

    def reset(self):
        self.errors = []

    # ------------- Serializers -------------

    # TODO : update seriializers

    """
    def to_json(self, indent=None, reset=False):
        errors = []
        for error in self.errors:
            newerror = error.copy()
            newerror["ex"] = str(newerror["ex"])
            newerror["date"] = self.format_date(newerror["date"])
            errors.append(newerror)
        if reset is True:
            self.reset()
        return json.dumps(errors, indent=indent)

    def format_date(self, date):
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def to_html(self, reset=False, reverse=False):
        msg = ""
        errors = self.errors
        if reverse is True:
            errors = reversed(self.errors)
        for error in errors:
            ex = str(error["ex"])
            date = error["date"].strftime('%Y-%m-%d %H:%M:%S')
            errormsg = error["msg"]
            func = error["function"]
            tb = error["error"]
            tb = tb.replace("[0m", "")
            tb = tb.replace("[1m", "")
            tb = tb.replace(" line ", " <b>line</b> ")
            tb = tb.replace("\n", "<br />")
            msg += '<p class="error"><em>' + errormsg + '</em>'
            if errormsg:
                if func:
                    msg += " from function <b>" + func + "</b>"
                msg += ' ' + date
            if ex != "None":
                msg += "<em>" + ex + "</em>"
            if tb:
                msg += '</p><p>' + tb
            msg += "</p>"
        if reset is True:
            self.reset()
        return msg

    def to_dict(self):
        return self.errors
    """
    """def report(self):
        global DJANGO, ADMINS
        mails = []
        if DJANGO is True:
            for admin in ADMINS:
                mails.append(admin[1])
            content = ""
            i = 0
            for error in self.errors:
                content = content + self._str(error, i)
                i += 1
            send_mail("error", content, "goerror@site.com", mails)
        else:
            self.trace()"""

    def _get_args(self, args):
        """
        Returns exception, message
        """
        exc = None
        msg = None
        for arg in args:
            if isinstance(arg, str):
                msg = arg
            elif isinstance(arg, Exception):
                exc = arg
        return exc, msg

    def _check_args(self, *args):
        """
        Check if the args for the constructor are correct
        """
        num_args = len(args[0])
        if num_args == 0:
            print("[" + colors.red("error") + "] "
                  "Goerr error: either a string or an Exception object"
                  " are required to create an error object")
            raise


err = Trace()
