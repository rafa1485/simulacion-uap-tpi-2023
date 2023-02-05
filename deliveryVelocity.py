import random
import math


def calculateKmHToHmH(xt):
    velocity = xt*10/60
    return velocity

def cpd(x):
    if x < calculateKmHToHmH(20):
        return 0
    elif x <= calculateKmHToHmH(35):
        return ((x**2)/450)-((4*x)/45)-(8/9)+(16/9)
    elif x < calculateKmHToHmH(50):
        return ((-(((x**2)-1225)/450))+(((2*x)-70)/9))+(1/2)
    elif x >= calculateKmHToHmH(50):
        return 1

def calculateM(a,b):
    return (a+b)/2


def deliveryVelocity():
    N = 1000
    y = random.randint(0,N)/N

    # velocidad en kilometros por hora (km/h). Maxima (50) y minima(20) velocidad de una moto
    a = 20
    b = 50
    a = calculateKmHToHmH(a)
    b = calculateKmHToHmH(b)

    m = calculateM(a,b)

    if (y-cpd(a))*(y-cpd(m)) < 0:
        b = m
    else:
        a = m

    m = calculateM(a,b)


    x = m

    return math.ceil(x)



# for x in range(20,50):
#     print(x, cpd(x))
