import random

def cpd(x):
    if x < 20:
        return 0
    elif x <= 35:
        return ((x**2)/450)-((4*x)/45)-(8/9)+(16/9)
    elif x < 50:
        return ((-(((x**2)-1225)/450))+(((2*x)-70)/9))+(1/2)
    elif x >= 50:
        return 1

def deliveryVelocity():
    N = 1000
    y = random.randint(0,N)/N
    a = 20
    b = 50
    m = (a + b)/2

    if (y-cpd(a))*(y-cpd(m)) < 0:
        b = m
    else:
        a = m

    x = m
    return x



# for x in range(20,50):
#     print(x, cpd(x))


