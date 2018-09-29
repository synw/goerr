from goerr import Err

err = Err()


def func1():
    print("Func 1 is running")
    try:
        'x' > 1
    except Exception as e:
        err.panic("Errmsg frun func1", e)
    print("Func 1 is finished")

    
def func2():
    func1()
    print("Func 2 is finished")

        
func2()
