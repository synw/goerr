# Goerr

Go style error handling in Python. Propagates errors up the stack in the same style as Go.

## Example

Print the errors that occured:

   ```python
   from goerr import error
   
   def f1():
      err = f2()
      try:
         c = 1 + "1"
      except Exception as e:
         err = error.new("Error in f1", "f1")
         return err
      return None
    
   def f2():
      try:
         a = [1]
         c = a[1]
      except Exception as e:
         err = error.new("Error in f2", "f2", e)
         return err
    return None
    
   def main():
      err = f1()
      if err is not None:
         err.trace()
    
   if __name__ == "__main__":
      main()
   ```

Output:

![Stack trace screenshot](https://raw.github.com/synw/goerr/master/docs/img/output.png)

## API

Methods:

**`new`**: creates a new error and store it in the trace: parameters: 

- `msg`: the message string
- `isfrom`: the name of the function that raised the error (optional) 
- `ex`: the first exception that was raised in the stack (optional)

Example: `error.new("An error has occured", "function_name", exception_object)`

**`trace`**: prints the errors trace. Example: see the code above

**`throw`**: prints the errors trace and raise the first exception that was passed to the trace. Example: `err.throw()`

**`get`**: get a json object represents the errors trace. Example: `err.get()`
