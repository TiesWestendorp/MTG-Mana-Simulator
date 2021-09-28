from math import gcd, sqrt

def divisors(n):
    divs = [1]
    for i in range(2,int(sqrt(n))+1):
        if n%i == 0:
            divs.extend([i,n//i])
    divs.extend([n])
    return list(set(divs))

def lcm(a,b):
    return a*b//gcd(a,b)
