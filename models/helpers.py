"""Helper methods"""

from math import gcd, sqrt

def divisors(number):
    """Returns a list of all divisors of the input"""
    divs = [1]
    for candidate in range(2,int(sqrt(number))+1):
        if number%candidate == 0:
            divs.extend([candidate,number//candidate])
    divs.extend([number])
    return list(set(divs))

def lcm(number1,number2):
    """Compute the least common multiple of two numbers"""
    return number1*number2//gcd(number1, number2)
