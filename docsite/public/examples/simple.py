from goerr import Err

err = Err()
err.new("An error")


def error_func():
    err.new("Error from a function")

    
error_func()

err.info("An info message")


def msgs_func():
    err.warning("A warning message")
    err.debug("A debug message")

    
msgs_func()

try:
    a > 1
except Exception as e:
    err.new(e)

