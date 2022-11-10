import random
import matplotlib.pyplot as plt

# Nuestros módulos
import generateOrders
from calculateRoutes import *


# order = {'idOrder': 22, 'time': 2145, 'x': 43, 'y': -23, 'idDelivery': 4}

# Fijo la semilla del generador random para que las corridas sean reproducibles
# durante la depuracion
random.seed(352)

# GLOBAL VARS
openTime = 0
closeTime = 250
endOfDeliveryTime = closeTime + 30  # Tiempo de margen para que termine el reparto
maxOrders = 100
maxOrdersPerDeliver = 3

# ====================================
# Variables y módulos de Órdenes 
# ====================================
orderList = generateOrders(openTime, closeTime, maxOrders)
preparationList = []
readyToDeliverList = []
pedidosEntregados = []
# ====================================
print("ordenes:", len(orderList))

# ====================================
# Variables y módulos de repartidores
# ====================================
repartidoresList = [
    {'id': 0, 'available': False, 'returnTime': 0},
    {'id': 1, 'available': False, 'returnTime': 0},
    {'id': 2, 'available': False, 'returnTime': 0}]
repartidoresOrdersList = {
    0: [],
    1: [],
    2: [],
}


# ====================================
# Variables y módulos de repartidores
# ====================================
deliveredOrdersList = []
deliveryVelocity = 6
contadores = [0, 0]  # preparados, listos
comtadoresrepartidores = [0, 0, 0]


def Simular(openTime, closeTime):

    # Recorre el tiempo
    for t in range(openTime, closeTime):

        # ===================================
        #  ¿En el t actual, hay algún repartidor que complete su recorrido?
        # ===================================
        for repartidorIndex in range(len(repartidoresList)):
            # Si el horario de vuelta coincide con el tiempo actual
            if repartidoresList[repartidorIndex]['returnTime'] == t:
                # print("El repartidor: ", repartidoresList[repartidorIndex]['id'], "volvió a la base y se encuentra disponible")
                repartidoresList[repartidorIndex]['available'] = True

        # ===================================
        # Recorre la lista de ordenes que entraron
        # ===================================
        for o in range(len(orderList)):
            preparationTime = random.randint(10, 15)
            # Si el horario coincide con la hora de la orden
            if orderList[o]['time'] == t:
                # TIEMPO
                #print("=======  Tiempo: ",t, "=======")
                # print(orderList[o])
                ##
                # Crea un nuevo item en la orden que presenta el tiempo que estará listo el pedido
                orderList[o]['preparedTime'] = orderList[o]['time'] + \
                    preparationTime
                # Traspaso de lista de ordenes generadas o lista de ordenes para preparar
                preparationList.append(orderList[o])
                contadores[0] = contadores[0] + 1

        # ===================================
        # Recorre la lista de ordenes que están en preparación para ser trasladados a reparto
        # ===================================
        for p in range(len(preparationList)):
            # Si el horario coincide con la hora de preparado de la orden
            if preparationList[p]['preparedTime'] == t:
                ##
                # print(preparationList[p])
                ##
                # Traspaso de lista de ordenes en preparacion a lista de ordenes listas para enviar
                readyToDeliverList.append(preparationList[p])
                contadores[1] = contadores[1] + 1

        # Se ordenan los pedidos listos para repartir según cual termino de prepararse antes
        sorted(readyToDeliverList, key=lambda i: i['preparedTime'])

        # ===================================
        #  Recorrer la cola de repartidores disponibles y asignarle un pedido de los que estén preparados y listos.
        # ===================================

        # ===================================
        #  Recorremos la lista de repartidores y buscamos si hay ordenes para los que ese encuentran activos
        #  estas ordenes se agregan a la lista de ordenes hasta completar la capacidad del repartidor
        # ===================================
        for repartidorIndex in range(len(repartidoresList)):

            # ¿El repartidor se encuentra activo?
            if repartidoresList[repartidorIndex]['available'] == True:
                # print("El repartidor: ", repartidoresList[repartidorIndex]['id'], "se encuentra activo:")

                # Recorremos la lista de ordenes para entregar y comprobamos si existe alguno asignado al repartidos actual
                for orderIndex, order in enumerate(readyToDeliverList):

                    # Comprobamos que el repartidor actual no se encuentre con la capacidad completa de ordenes
                    if len(repartidoresOrdersList[repartidoresList[repartidorIndex]['id']]) < maxOrdersPerDeliver:
                        if order['idDelivery'] == repartidoresList[repartidorIndex]['id']:
                            # print(readyToDeliverList[orderIndex])

                            # Traspaso de lista de ordenes en preparacion a lista de ordenes listas para enviar
                            repartidoresOrdersList[repartidoresList[repartidorIndex]['id']].append(
                                order)
                            del readyToDeliverList[orderIndex]

                # print(repartidoresOrdersList[repartidoresList[repartidorIndex]['id']])
                # breakpoint()

                # ===================================
                # Recorrer el diccionario de repartidores que tienen al menos un pedido para llevar y generar recorrido
                # -> funciones sugeridas
                #        getRoute(pedidosRepartidor) # retorna la ruta
                # ===================================

                # comprobamos si el repartidor actual tiene pedidos en la cola de entrega
                if len(repartidoresOrdersList[repartidoresList[repartidorIndex]['id']]) > 0:

                    # Si la cola tiene al menos un pedido, el repartidor sale a enviarlo.
                    # Para ello planificamos la ruta para saber en que momento realizará cada entrega
                    entregasPedidos, tiempoRegreso = getRoute(
                        repartidoresOrdersList[repartidoresList[repartidorIndex]['id']], t, deliveryVelocity)

                    # Y guardamos las entidades "pedido" en la lista de salidas
                    for p in entregasPedidos:
                        pedidosEntregados.append(p)
                        comtadoresrepartidores[repartidorIndex] = comtadoresrepartidores[repartidorIndex] + 1

                    # vaciamos la lista de pedidos del repartidor (como si ya hubiera hecho todos los pedidos, total ya sabemos como lo va  a hacer)
                    repartidoresOrdersList[repartidoresList[repartidorIndex]['id']] = [
                    ]

                    # Ponemos en False el flag de Disponivilidad del repartidor (y se mantendrá así hasta que se cumpla el tiempo de retorno)
                    repartidoresList[repartidorIndex]['available'] == False

    # print(pedidosEntregados)
    print("pedidos preparados:", contadores[0])
    print("pedidos listos:", contadores[1])
    print("pedidos entregados:", len(pedidosEntregados))

    # Hacemos un postprocesamiento de los datos de cada entidad "pedido" para calcular el tiempo de demora para en la entrega de los pedidos.
    # print('Demoras')
    delayList1 = []
    delayList2 = []
    zonasTotal = [0, 0]  # 2 zonas

    for p in pedidosEntregados:

        # print(p['x'], p['y'])
        if (p['x'] > 0):
            demora = p['deliveredTime'] - p['time']
            delayList1.append(demora)
            zonasTotal[0] = zonasTotal[0]+1
        else:
            demora = p['deliveredTime'] - p['time']
            delayList2.append(demora)
            zonasTotal[1] = zonasTotal[1]+1
    
    # print(demora)
    print("Total de pedidos por zona:")
    print(zonasTotal)
    print("Total de pedidos por repartidor:")
    print(comtadoresrepartidores)

    plt.hist(delayList1, label='Zona 1')
    plt.hist(delayList2, label='Zona 2')
    plt.ylim([0, 25])
    plt.legend()
    plt.show()

    # ===================================
    # Acá se retornarán resultados una vez termine el tiempo:
    # ===================================
    # print(deliveredOrdersList)
    # FIN


# EJECUTAMOS LA SIMULACION
# DEJAMOS UN MARGEN DE TIEMPO PARA QUE REPARTA LOS ÚLTIMOS PEDIDOS EN BASE A LOS RETRASOS POR PREPARACIÓN.
Simular(openTime, endOfDeliveryTime)
