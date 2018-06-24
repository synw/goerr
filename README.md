# Goerr

[![Build Status](https://travis-ci.org/synw/goerr.svg?branch=master)](https://travis-ci.org/synw/goerr) [![Coverage Status](https://coveralls.io/repos/github/synw/goerr/badge.svg?branch=master)](https://coveralls.io/github/synw/goerr?branch=master)

Go style explicit error handling in Python. Propagates errors up the call stack in the same style as Go.

   ```bash
   pip install goerr
   ```

## Quick example

   ```python
import pandas as pd
from goerr import Trace


class TestRun(Trace):

    def run0(self):
        self.err("Error run zero")

    def run1(self):
        self.run0()
        try:
            pd.DataFrame("err")
        except Exception as e:
            self.err(e, "Can no construct dataframe")

    def run(self):
        self.run1()
        try:
            "x" > 2
        except Exception as e:
            self.err(e)


err = TestRun()
err.reset()
err.run()
print("----------- End of the run, checking ------------")
err.check()
   ```

Output:

![Stack trace screenshot](docs/img/output.png)

Or use in a functionnal style:

   ```python
   from goerr import Trace
   
   
   tr = Trace()
   tr.err("Error message")
   ```

## API

### Methods:

**`err`**: creates a new error and store it in the trace: parameters: 

- `ex`: an exception (optional)
- `msg`: the message string (optional)
Either a message string or an exception has to be provided as argument.

**`trace`**: prints the errors trace

**`check`**: check if error exists and run `trace()` if it does

**`fatal`**: check if error exists, run `trace()` if it does and raise an exception

**`stack`**: add an error to the trace with no message if one previous error exists. Used
to keep track of the call stack

**`log`**: returns a log message from the first error

### Properties:

**`exists`**: check if there are some errors in the trace. Returns `True` or `False`

## Why?

I like the explicit errors management in Go (unlike many people) and I wanted to have the
same kind of experience in Python: a fined grained control over errors all across the call
stack.

The same lib in Go: [terr](https://github.com/synw/terr)