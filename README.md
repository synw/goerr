# Goerr

Go style explicit error handling in Python. Propagates errors up the stack in the same style as Go.

## Example

Print the errors trace:

   ```python
   from goerr import error
   
   def function1():
      function2()
      try:
         1 + "1"
      except Exception as e:
         err.new("error message with exception in first function", e)
      return None
    
   def function2():
      function3()
      err.new("error message in second function", function2)
      
   def function3():
      try:
         {} > 1
      except Exception as e:
         err.new(e)
      return None
      
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

- `ex`: the first exception that was raised in the stack (optional)
- `msg`: the message string (optional)
- `isfrom`: the name of the function that raised the error (optional) 

Either a message string or an exception has to be provided as argument.

Example: `error.new("An error has occured", "function_name", exception_object)`

**`trace`**: prints the errors trace. Example: see the code above

**`throw`**: prints the errors trace and raise the first exception that was passed to the trace. Example: `err.throw()`

**`to_json`**: get a json object that represents the errors trace. Params: `indent`.Example: `err.to_json(indent=2)`.

**`to_dict`**: get a dictionnary object that represents the errors trace. Example: `err.to_dict()`.

Properties:

**`exists`**: check if there are some errors in the trace
