import sys
import random

"""
Orden ejemplo: {idOrder:22, time:2145, x:43, y:-23, idDelivery:4}
Consideramos el rango tanto para las cordenadas x como y entre -50 y 50
"""

""" 
Módulo que contiene la función de generar pedidos (esta funcion es un ejemplo)
"""
ordersList = []

# Genera una lista de diccionarios que contiene las ordenes


def generateOrders(openTime, closeTime, maxOrders):
    time = random.sample(range(openTime, closeTime), maxOrders)
    for o in range(maxOrders):
        idOrder = o
        # el 80% de los pedidos viene de zona 1
        if (random.randint(0, 100) < 70):
            x = random.randint(1, 50)
        else:
            x = random.randint(-50, 0)
        # se asigna 0 a y porque solo hay dos zonas divididas en X
        y = 0
        # asignamos delivery en base a que zona pertenece
        if (x > 0):
            # zona 1
            if (random.randint(0, 100) < 50):
                idDelivery = 0
            else:
                idDelivery = 2
        else:
            # zona 2
            idDelivery = 1
        order = {'idOrder': idOrder, 'time': time[o],
                 'x': x, 'y': y, 'idDelivery': idDelivery}
        ordersList.append(order)
    # Ordena la lista de ordenes
    sortedList = sorted(ordersList, key=lambda i: i['time'])
    return sortedList


sys.modules[__name__] = generateOrders
