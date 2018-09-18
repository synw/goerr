# Goerr

[![Build Status](https://travis-ci.org/synw/goerr.svg?branch=master)](https://travis-ci.org/synw/goerr) [![Coverage Status](https://coveralls.io/repos/github/synw/goerr/badge.svg?branch=master)](https://coveralls.io/github/synw/goerr?branch=master)

Go style explicit error handling in Python. Features:

  - **Pretty print** of error details  
  - **Trace** errors across the call stack  
  - **Log** errors

   ```bash
   pip install goerr
   ```

## API

Class **`Err`**

### Properties:

#### Trace

**`trace_errs`**: activate the errors trace: `True` or `False`. Default is `False`. If not activated the program
will exit on the first error encountered (same behavior as exceptions). If activated the program will print the 
error and continue. A complete errors trace can be printed when needed  

#### Logging

**`log_errs`**: log errors: `True` or `False`. Default is `False`  
**`log_path`**: path of the file where to log. Default is `"errors.log"`  
**`log_format`**: csv or text. Default is `"csv"`. Note: the tracebacks are not recorded if the format is csv.

### Methods:

**`err`**: creates a new error, print it and store it in the trace if the option is activated. Exit the program
if the trace is not activated. Parameters: 

- `ex`: an exception (optional)
- `msg`: the message string (optional)
Either a message string or an exception has to be provided as argument for the error to be
printed. If no argument is provided it will just record the function name to keep a trace of
the call stack

**`warning`**: prints a warning message

**`info`**: prints an info message

**`debug`**: prints a debug message

**`trace`**: prints the errors trace and reset it

**`panic`**: force program exit after an error even if the errors trace is activated

**`errdict`**: returns a dictionnary with the error details 

Check the examples directory for code

## Example

Trace errors across the call stack:

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
