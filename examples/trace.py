import time
from datetime import datetime
from goerr import Trace

err = Trace()


def run_func(funcname):
    i = 3
    while i > 0:
        print(funcname + "running")
        time.sleep(0.5)
        i -= 1


def func1():
    run_func("func1")
    try:
        1 > "bar"
    except Exception as e:
        err.new(e)
    run_func("func1")


def func2():
    run_func("func2")
    try:
        now = datetime.later()
    except Exception as e:
        err.new(e, "Now is not later!")
    run_func("func2")


func1()
func2()
print("Run finished, checking:")
time.sleep(1)
err.trace()
