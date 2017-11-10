# -*- coding: utf-8 -*-

from __future__ import print_function
import traceback
import sys
from _ast import arg
import json
from datetime import datetime
from .colors import cols
DJANGO = False
try:
    from django.core.mail import send_mail
    from django.conf import settings
    try:
        ADMINS = settings.ADMINS
        DJANGO = True
    except:
        pass
except:
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

    def trace(self):
        i = len(self.errs) - 1
        for err in self.errs[::-1]:
            print(self._str(err, i))
            print(err["error"])
            i -= 1
        self.reset()

    def throw(self):
        self.trace()
        if self.first_ex is not None:
            raise self.first_ex
        else:
            print("No exception to raise")

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

    def to_json(self, indent=None):
        errs = []
        for err in self.errs:
            err.pop("ex")
            err["date"] = int(err["date"].strftime('%s'))
            errs.append(err)
        return json.dumps(errs, indent=indent)

    def to_dict(self):
        return self.errs

    def _str(self, err, i):
        msg = err["msg"]
        funcstr = ""
        if err["function"] is not None:
            funcstr = " from " + cols.BOLD + err["function"] + cols.ENDC
        msg = cols.FAIL + "Error " + \
            str(i) + cols.ENDC + funcstr + " : " + msg
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
                "Goerr error: either a 'str' or an 'Exception' object are required to create an 'err' object")
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
            _, _, func_name, _ = traceback.extract_tb(exc_tb)[-1]
            # set values
            funcname = func_name
            _err = traceback.format_exc()
        # ensure that msg is str type
        if msg is None:
            msg = ""
        # init err object
        err = {}
        err["function"] = funcname
        err["error"] = _err
        err["msg"] = msg
        err["ex"] = ex
        err["date"] = datetime.now()
        return err


err = Trace()
