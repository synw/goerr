import pprint
from goerr import Err

"""
Custom error handling using the error data dict
"""

errs = Err()
errs.trace_errs = True


def run_func(funcname):
    i = 3
    while i > 0:
        print(funcname + "running")
        i -= 1


def func1():
    run_func("func1")
    try:
        1 > "bar"
    except Exception as e:
        error = errs.err(e)
        pp = pprint.PrettyPrinter(indent=4)
        print("Error data:")
        pp.pprint(error.errdict())
    run_func("func1")


func1()
print("Run finished")
