def integral(x):
    if x < 20:
        return 0
    elif x < 35:
        return (1/225)*(((x**2)/2)-200)-(((4*x)-80)/3)
    elif x < 50:
        return (-(((x**2)-1225)/450))+(((2*x)-70)/9)
    elif x >= 50:
        return 1



for x in range(20,50):
    print(integral(x))

