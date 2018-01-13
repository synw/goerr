# -*- coding: utf-8 -*-
from __future__ import print_function
import traceback
import sys
import json
from datetime import datetime
from .colors import colors
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


class Trace():
    errs = []
    first_ex = None

    def __repr__(self):
        msg = "<goerr.Trace object: " + \
            str(len(self.errs)) + " errors>"
        return msg

    @property
    def exists(self):
        if len(self.errs) > 0:
            return True
        return False

    @property
    def num(self):
        return len(self.errs)

    def new(self, *args):
        err = self._new(args)
        self.errs.append(err)
        return self

    def check(self):
        if self.exists:
            self.trace()

    def fatal(self):
        if self.exists:
            self.throw()

    def trace(self, reverse=False):
        errs = self.errs
        if reverse is True:
            errs = errs[::-1]
        i = len(self.errs) - 1
        for err in errs:
            print(self._str(err, i))
            print(err["error"])
            i -= 1
        self.reset()

    def throw(self, reverse=False):
        self.trace(reverse)
        if self.first_ex is not None:
            raise self.first_ex

    def report(self):
        global DJANGO, ADMINS
        mails = []
        if DJANGO is True:
            for admin in ADMINS:
                mails.append(admin[1])
            content = ""
            i = 0
            for err in self.errs:
                content = content + self._str(err, i)
                i += 1
            send_mail("Error", content, "goerr@site.com", mails)
        else:
            self.throw()

    def reset(self):
        self.errs = []
        self.first_ex = None

    def to_json(self, indent=None, reset=False):
        errs = []
        for error in self.errs:
            newerr = error.copy()
            newerr["ex"] = str(newerr["ex"])
            newerr["date"] = self.format_date(newerr["date"])
            errs.append(newerr)
        if reset is True:
            self.reset()
        return json.dumps(errs, indent=indent)

    def format_date(self, date):
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def to_html(self, reset=False, reverse=False):
        msg = ""
        errs = self.errs
        if reverse is True:
            errs = reversed(self.errs)
        for error in errs:
            ex = str(error["ex"])
            date = error["date"].strftime('%Y-%m-%d %H:%M:%S')
            errmsg = error["msg"]
            func = error["function"]
            tb = error["error"]
            tb = tb.replace("[0m", "")
            tb = tb.replace("[1m", "")
            tb = tb.replace(" line ", " <b>line</b> ")
            tb = tb.replace("\n", "<br />")
            msg += '<p class="error"><em>' + errmsg + '</em>'
            if errmsg:
                if func:
                    msg = msg + " from function <b>" + func + "</b>"
                msg += ' ' + date + "x"
            if ex != "None":
                msg += "<em>" + ex + "</em>"
            if tb:
                msg += '</p><p>' + tb
            msg += "</p>"
        if reset is True:
            self.reset()
        return msg

    def to_dict(self):
        return self.errs

    def _str(self, err, i):
        msg = err["msg"]
        funcstr = ""
        if err["function"] is not None:
            funcstr = "from " + colors.bold(err["function"])
        msg = colors.red("Error " + str(i)) + " " + funcstr + " : " + msg
        return msg

    def _check_args(self, args):
        """
        Returns exception, message
        """
        exc = None
        msg = None
        funcname = None
        for arg in args:
            if isinstance(arg, str):
                msg = arg
            elif isinstance(arg, Exception):
                exc = arg
            elif callable(arg):
                funcname = arg.__name__
        return exc, msg, funcname

    def _err(self, msg):
        print(msg)

    def _new(self, *args):
        num_args = len(args[0])
        if num_args == 0:
            self._err(
                "Goerr error: either a string or an Exception object are required to create an err object")
            # TODO : handle internal error
            raise
        msg = None
        ex = None
        # verify types and get values from args
        for uargs in args:
            ex, msg, funcname = self._check_args(uargs)
        # verify values
        if ex is None and msg is None:
            self._err(
                "Goerr error: either a 'str' or 'Exception' type must be passed to 'err' constructor")
            # TODO : handle internal error
            raise
        # handle exception
        _err = ""
        if ex is not None:
            # first exception storage
            if self.first_ex is None:
                self.first_ex = ex
            # get info from exception
            _, _, exc_tb = sys.exc_info()
            if funcname is not None:
                _, _, funcname, _ = traceback.extract_tb(exc_tb)[-1]
            # set values
            _err = traceback.format_exc()
        # ensure that msg is str type
        if msg is None:
            msg = ""
        line = colors.bold(" line ")
        _err = _err.replace(" line ", line)
        # init err object
        err = {}
        err["function"] = funcname
        err["error"] = _err
        err["msg"] = msg
        err["ex"] = ex
        err["date"] = datetime.now()
        return err


err = Trace()
