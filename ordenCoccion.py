import random
import math
import numpy as np

# print(y)
def cpd(x):
    if x <= 2:
        return 0
    elif 2< x < 4:
        return ((x**2) -(4*x) + 4)/10
    elif 4<= x < 7:
        return -((x**2)-(14*x)+(40))/15 + 2/5
    elif x >= 7:
        return 1

def coccion():
    y = random.randint(0, 1000)/1000
    a = 2
    b = 7
    for i in range(0, 100):
        m = (a + b)/2
        if (y - cpd(a)) * (y - cpd(m)) < 0:
            b = m
        else:
            a = m
    return m
print(coccion())