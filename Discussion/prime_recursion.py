def func_tester(f, x):
    for i in range(x):  
        print(i, ": ",f(i)) 

def return_trues(f, x):
    list = []
    for i in range(x):
        if f(i) == True:
            list.append(i)
    return list

def is_prime(y):
    def prime_helper(index = 2):
        if y == index:
            return True
        elif y % index == 0 or y == 1:
            return False
        else: 
            return prime_helper(index + 1)
    return prime_helper()

def primes_list(n):
    return return_trues(is_prime, n)
