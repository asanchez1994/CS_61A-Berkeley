def square(x):
    return x*x

def make_repeater(f,n):
    if n == 0:
        return lambda x: x
    elif n == 1:
        return f
    else:
        return make_repeater(f, n-1)
    
