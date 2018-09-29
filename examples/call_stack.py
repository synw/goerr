import time
from goerr import Trace

err = Trace()


def func1():
    print("Func 1 running")
    time.sleep(0.5)
    try:
        'x' > 1
    except Exception as e:
        err.new("Errmsg frun func1", e)
    print("Func 1 finished")

    
def func2():
    func1()
    time.sleep(0.5)
    err.via("Errmsg frun func2")
    print("Func 2 running")

        
def func3():
    func2()
    time.sleep(0.5)
    err.via()
    print("Func 3 running")

        
func3()
err.trace()
