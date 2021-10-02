from math import gcd, sqrt

def divisors(n):
    """Returns a list of all divisors of the input"""
    divs = [1]
    for i in range(2,int(sqrt(n))+1):
        if n%i == 0:
            divs.extend([i,n//i])
    divs.extend([n])
    return list(set(divs))

def lcm(a,b):
    """Compute the least common multiple of two numbers"""
    return a*b//gcd(a,b)
