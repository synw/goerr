from goerr import Err

err = Err()
try:
    import foobar
except ImportError as e:
    err.fatal(e)
