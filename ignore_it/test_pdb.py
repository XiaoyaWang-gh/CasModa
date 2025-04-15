def g(data):
    return data * data


def f(x):
    breakpoint()
    lst = []
    for i in range(x):
        val = g(i)
        lst.append(val)
    return lst


f(3)
