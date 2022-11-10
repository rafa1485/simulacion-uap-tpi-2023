"""
orders = [{'idOrder': 2, 'time': 3, 'x': -14, 'y': 20, 'idDelivery': 0, 'preparedTime': 23},
        {'idOrder': 5, 'time': 12, 'x': -1, 'y': 4, 'idDelivery': 0, 'preparedTime': 32},
        #{'idOrder': 6, 'time': 7, 'x': -30, 'y': 32, 'idDelivery': 0, 'preparedTime': 28},
        #{'idOrder': 1, 'time': 1, 'x': -45, 'y': 24, 'idDelivery': 0, 'preparedTime': 18}
]
repartidoresList = [{'id': 0, 'available': False, 'returnTime': 0}, {'id': 1, 'available': False, 'returnTime': 0}]
"""

#Devuelve la orden con destino mas cercano al punto pasado por parámetros.
def getClosestOrder(orderList, currentPoint):

    orderClosest = orderList[0]

    for order in orderList:
        #Se calcula la distancia del punto actual a la orden analizada.
        newDistance = abs(order['x'] - currentPoint[0]) + abs(order['y'] - currentPoint[1])
        #Se calcula la distancia más cercana hasta esta iteración
        currentClosestDistance = abs(orderClosest['x'] - currentPoint[0]) + abs(orderClosest['y'] - currentPoint[1])
        
        if (newDistance < currentClosestDistance):
            orderClosest = order
    
    return orderClosest
#print(getMinDistance(orders, [-28,21]))

#Devuelve el tiempo que tomara entregar la orden desde el punto actual.
def calculateTimeToDelivery(currentPoint, order, deliveryVelocity):

    distance =  abs(order['x'] - currentPoint[0]) + abs(order['y'] - currentPoint[1])
    deliveredTime = distance / deliveryVelocity

    return deliveredTime
#print(calculateTimeToDelivery([-2,4], orders[0], 4))


#FUNCIÓN A UTILIZAR=====================================
#Devuelve una lista con dos elementos: [[], float]
#   1: Lista de órdenes para repartir ya ordenadas
#   2:Tiempo absoluto en el que regresará el repartidor
#=======================================================
def getRoute(readyToDeliverList, actualTime, deliveryVelocity):
    
    #Lista ordenada de pedidos para repartir.
    ordersToDelivery = []
    #Punto 0,0 donde se definio que estaria el negocio
    currentPoint = [0,0]
    #Se acumulan los tiempos de los distintos pedidos.
    timePreviousDeliveries = 0
    ordersQuantity = len(readyToDeliverList)

    #El rango se adapta en caso de que los ítems para repartir sean menos que tres que es el tope por repartidor.
    for i in (range(3) if ordersQuantity>3 else range(ordersQuantity)):
        ordersToDelivery.append(getClosestOrder(readyToDeliverList, currentPoint))
        #Se suma el tiempo que tomará entregar el último pedido agregado.
        timePreviousDeliveries += ordersToDelivery[i]['preparedTime']
        #Se calcula el tiempo en el que se va a entregar el pedido
        ordersToDelivery[i]['deliveredTime'] = actualTime + calculateTimeToDelivery(currentPoint, ordersToDelivery[i], deliveryVelocity)
        #Se elimina el elemento agregado para reparto para que no se repita.
        readyToDeliverList.remove(ordersToDelivery[i])
        #Se setea el nuevo punto de referencia
        currentPoint = [ordersToDelivery[i]['x'], ordersToDelivery[i]['y']]
        actualTime = ordersToDelivery[i]['deliveredTime']

    #Se calcula el tiempo de vuelta al local.
    try:
        returnTime = actualTime + calculateTimeToDelivery([0,0], ordersToDelivery[-1], deliveryVelocity)
    except:
        breakpoint()
    
    return [ordersToDelivery, returnTime]

#print(getRoute(orders, 32, 4))

#TESTS
#[[{'idOrder': 5, 'time': 12, 'x': -1, 'y': 4, 'idDelivery': 0, 'preparedTime': 32, 'deliveredTime': 33.25},
#  {'idOrder': 2, 'time': 3, 'x': -14, 'y': 20, 'idDelivery': 0, 'preparedTime': 23, 'deliveredTime': 40.5},
#  {'idOrder': 6, 'time': 7, 'x': -30, 'y': 32, 'idDelivery': 0, 'preparedTime': 28, 'deliveredTime': 47.5}],
#  63.0]

#[[{'idOrder': 5, 'time': 12, 'x': -1, 'y': 4, 'idDelivery': 0, 'preparedTime': 32, 'deliveredTime': 33.25},
#  {'idOrder': 2, 'time': 3, 'x': -14, 'y': 20, 'idDelivery': 0, 'preparedTime': 23, 'deliveredTime': 40.5}],
#  49.0]