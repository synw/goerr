# Goerr

Go style explicit error handling in Python. Propagates errors up the call stack in the same style as Go.

   ```bash
   pip install goerr
   ```

## Usage

Print the errors trace:

   ```python
   from goerr import err
   
   def function1():
      function2()
      try:
         1 + "1"
      except Exception as e:
         err.new("error message with exception in first function", e)
    
   def function2():
      function3()
      err.new("error message in second function", function2)
      
   def function3():
      try:
         {} > 1
      except Exception as e:
         err.new(e)
      
   def main():
      function1()
      if err.exists is True:
         err.trace()
         print("------------------")
         print("Json error object:")
         print("------------------")
         print(err.to_json(indent=2))
   ```

Output:

![Stack trace screenshot](https://raw.github.com/synw/goerr/master/docs/img/output.png)

## API

Methods:

**`new`**: creates a new error and store it in the trace: parameters: 

- `ex`: an exception (optional)
- `msg`: the message string (optional)
- `function`: the function object that raised the error (optional: usefull only when no exception is provided) 

Either a message string or an exception has to be provided as argument.

Example: `err.new("An error has occured", exception_object)`

**`trace`**: prints the errors trace. Example: see the code above

**`throw`**: prints the errors trace and raise the first exception that was passed to the trace. Example: `err.throw()`

**`report`**: if Django is installed this will send an email to the admins declared in settings. Otherwise it will
behave like `throw()`

**`check`**: check if error exists and run `trace()` if it does

**`fatal`**: check if error exists and run `throw()` if it does

**`to_json`**: get a json object that represents the errors trace. Params: `indent`.Example: `err.to_json(indent=2)`.

**`to_dict`**: get a dictionnary object that represents the errors trace. Example: `err.to_dict()`.

Properties:

**`exists`**: check if there are some errors in the trace
