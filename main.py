from pybit.spot import HTTP
import json
from huepy import *
import datetime as date

#Variables
AVERAGE = 0.0
TOTAL_PRICE = 0.0
TOTAL_QTY = 0.0
CONTADOR_SELL = 0
CONTADOR_BUY = 0
TOTAL_PRICE_Sum = 0.0
TOTAL_QTY_Sum = 0.0
TOTAL_PRICE_Res = 0.0
TOTAL_QTY_Res = 0.0

#Conexion con API
conf = json.loads(open('conf.json').read())
client = HTTP(
    endpoint=conf['endpoint'], 
    api_key=conf['api_key'],
    api_secret=conf['api_secret']
)

#Conversion de tiempo
startTime = date.datetime.strptime(conf['startTime'], '%Y-%m-%d - %H:%M:%S.%f %p')
startTime = int(startTime.timestamp() * 1000)
endTime = date.datetime.strptime(conf['endTime'], '%Y-%m-%d - %H:%M:%S.%f %p')
endTime = int(endTime.timestamp() * 1000)

#Conseguir los trades dentro del tiempo
orders = client.get_active_order(startTime=startTime, endTime=endTime)
orders = json.dumps(orders, indent=4)
orders = json.loads(orders)
orders_founds = orders['result'].__len__()
                                  
print(run(f'Getting orders from {conf["startTime"]} to {conf["endTime"]}'))
print(good(f'Found {orders_founds} orders'))

#Mostrar los pares visibles en la fecha
symbols = []
for i, st in enumerate(orders['result']):
    symbols.append(orders['result'][i]['symbol'])
symbols = list(dict.fromkeys(symbols))
for i,elements in enumerate(symbols):
    print(f"{red([i])} {elements}")


input_symbol = input(("Select a trade to calculate average cost: "))
print(run(f"Calculating average cost for {symbols[int(input_symbol)]}..."))

#Iterar la lista
for i, st in enumerate(orders['result']):
    if orders['result'][i]['symbol'] == symbols[int(input_symbol)]:
        if "CANCELED" not in orders['result'][i]['status']:
            print(run(f"{orders['result'][i]['symbol']} - PRICE: {orders['result'][i]['avgPrice']} - QTY: {orders['result'][i]['origQty']} - SIDE: {orders['result'][i]['side']}"))
            if orders['result'][i]['side'] == "BUY":
                TOTAL_PRICE_Sum += float(orders['result'][i]['cummulativeQuoteQty'])
                TOTAL_QTY_Sum += float(orders['result'][i]['origQty'])
                CONTADOR_BUY += 1
            if  orders['result'][i]['side'] == "SELL":
                TOTAL_PRICE_Res += float(orders['result'][i]['cummulativeQuoteQty'])
                TOTAL_QTY_Res += float(orders['result'][i]['origQty'])
            if  orders['result'][i]['side'] == 'SELL' :    
                CONTADOR_SELL += 1

#Calcular el total de las sumas
TOTAL_QTY = TOTAL_QTY_Sum - TOTAL_QTY_Res
TOTAL_PRICE = TOTAL_PRICE_Sum - TOTAL_PRICE_Res

#Si solo hay 1 venta en esa fecha:
if CONTADOR_SELL == 1 and CONTADOR_BUY <= 0:
    print("ONLY 1 SELL")
    print(good(f"Total cost: {TOTAL_PRICE}"))
    input("Press enter to exit...")
    quit()

print(CONTADOR_SELL, CONTADOR_BUY)
#Si solo hay 1 compra en esa fecha:
if CONTADOR_BUY == 1 and CONTADOR_SELL <= 0:
    print("ONLY 1 BUY")
    print(good(f"Total cost: {TOTAL_PRICE}"))
    input("Press enter to exit...")
    quit()

#En caso de que nuestra cantidad total sea negativa
#NOTA: Lo que ves en precio en teoria es tu ganancia
if TOTAL_QTY <= 0:
    TOTAL_QTY = 0
    print(good(f"Total cost: {abs(TOTAL_PRICE)}"))
    print(good(f"YOUR TOTAL QTY WAS NEGATIVE OR 0"))
    input("Press enter to exit...")
    quit()
AVERAGE = TOTAL_PRICE / TOTAL_QTY
    
print(good(f"Total cost: {TOTAL_PRICE} - Total qty: {TOTAL_QTY}"))
print(good(f"Average cost for {symbols[int(input_symbol)]} is {AVERAGE}"))
input("Press enter to exit...")
quit()