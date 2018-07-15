# Goerr

[![Build Status](https://travis-ci.org/synw/goerr.svg?branch=master)](https://travis-ci.org/synw/goerr) [![Coverage Status](https://coveralls.io/repos/github/synw/goerr/badge.svg?branch=master)](https://coveralls.io/github/synw/goerr?branch=master)

Go style explicit error handling in Python. Propagates errors up the call stack in the same style as Go.

   ```bash
   pip install goerr
   ```

## Quick example

   ```python
from datetime import datetime
from goerr import Err


def run_func(funcname):
    i = 3
    while i > 0:
        print(funcname + "running")
        i -= 1


class Foo(Err):
	# activate the errors trace
	trace_errs = True

    def func1(self):
        run_func("func1")
        try:
            1 > "bar"
        except Exception as e:
            self.err(e)
        run_func("func1")

    def func2(self):
        run_func("func2")
        try:
            now = datetime.later()
        except Exception as e:
            self.err(e, "Now is not later!")
        run_func("func2")


foo = Foo()
foo.func1()
foo.func2()
print("Run finished, checking:")
foo.trace()
   ```

Output:

![Stack trace screenshot](docs/img/output.png)

## API

### Methods:

**`err`**: creates a new error, print it and store it in the trace: parameters: 

- `ex`: an exception (optional)
- `msg`: the message string (optional)
Either a message string or an exception has to be provided as argument for the error to be
printed. If no argument is provided it will just record the function name to keep trace of
the call stack

**`fatal`**: check if error exists, run `trace()` if it does and raise an exception

**`warning`**: prints a warning message and add it to the trace

**`info`**: prints an info message and add it to the trace

**`debug`**: prints a debug message and add it to the trace

**`trace`**: prints the errors trace and reset it

**`log`**: returns a log message from the first error

**error**: creates a single error and print it without recording it in the trace. This is only useful when the `trace_errs` option is activated

- `ex`: an exception (optional)
- `msg`: the message string (optional)
Either a message string or an exception has to be provided as argument

### Properties:

**`errors`**: list of the errors

**`trace_errs`**: activate the errors trace: True or False. Default is False.

**`errs_traceback`**: print the stack trace when displaying the errors. Default is True

Check the examples directory for code

## Testing errors in programs

A helper function is available to test errors:

**`testing.assert_err`**: parameters: 

- `error type`: a string with the error type
- `function to run`: the function to test
- `*args`: function arguments
- `**kwargs`: function keyword arguments

Example:

   ```python
# the program
from goerr import Err
   
   class Foo(Err):
      def func1(self, param1, param2):
          try:
              param1 > param2
          except Exception as e:
              self.err(e)

# the test
import unittest
from goerr.testing import assert_err
from myprogram import Foo

   class MyTest(unittest.TestCase):
	  def test_myprogram(self):
          foo = Foo()
          assert_err("TypeError", foo.func1, 1, "bar")
   ```

## Why?

I like the explicit errors management in Go (unlike many people) and I wanted to have the
same kind of experience in Python: a fined grained control over errors all across the call
stack.

The same lib in Go: [terr](https://github.com/synw/terr)
