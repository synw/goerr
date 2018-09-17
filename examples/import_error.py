from goerr import err

try:
    import foobar
except ImportError as e:
    err(e)
    
print("This will not print")
