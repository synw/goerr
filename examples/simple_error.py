from goerr import err

"""
Print basic errors
"""


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
        err(e)
    run_func("func1")


func1()
print("Run finished")

