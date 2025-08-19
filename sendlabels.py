from pymongo import MongoClient  # Importa MongoClient desde pymongo
import requests


# Conexión a la base de datos MongoDB
client = pymongo.MongoClient("mongodb+srv://admin:sYRn8eIUA8ITkgdd@beflowoms-prod.xryel.mongodb.net/test")  # Cambia la URL si es necesario
db = client['andescc']

# Colecciones
orders_col = db['orders']
couriers_col = db['couriers']
fulfillments_col = db['fulfillments']

# Función para armar el JSON y enviar el POST request
def procesar_pedidos(lista_pedidos):
    for pedido in lista_pedidos:
        # Buscar el pedido en la colección orders
        order = orders_col.find_one({
            "$or": [
                {"remote_order_id": pedido},
                {"name": pedido}
            ]
        })
        
        if not order:
            print(f"Pedido {pedido} no encontrado en la colección orders.")
            continue

        # Buscar fulfillment relacionado
        fulfillment_id = order['fulfillments'][0]['$oid']
        fulfillment = fulfillments_col.find_one({"_id": pymongo.ObjectId(fulfillment_id)})
        
        if not fulfillment:
            print(f"Fulfillment para el pedido {pedido} no encontrado.")
            continue

        # Buscar courier relacionado
        courier_id = fulfillment['courier']['$oid']
        courier = couriers_col.find_one({"_id": pymongo.ObjectId(courier_id)})
        
        if not courier:
            print(f"Courier para el pedido {pedido} no encontrado.")
            continue

        # Construir el JSON para el pedido
        json_data = {
            "order_id": str(order['_id']['$oid']),
            "remote_order_id": order['remote_order_id'],
            "merchant_id": str(order['merchant_id']['$oid']),
            "label_url": fulfillment['labels']['pdf'],
            "tracking_number": "tracking.tracking_number",  # Actualiza con el campo correcto
            "sales_channel": str(order['sales_channel']['$oid']),
            "delivery_method": order['delivery_methods'][0],
            "courier_name": courier['public_name'],
            "shipping_service": {
                "name": courier['services'][0]['name']
            },
            "barcode": "tracking.barcode"  # Actualiza con el campo correcto
        }

        # Enviar solicitud POST
        headers = {
            'Token': '3434343hg',
            'Content-Type': 'application/json'
        }
        response = requests.post(
            "https://webhook.site/5c799c59-5812-4609-bd7c-23cd7bbbd633",
            json=json_data,
            headers=headers
        )

        # Comprobar la respuesta
        if response.status_code == 200:
            print(f"Pedido {pedido} procesado correctamente.")
        else:
            print(f"Error al procesar el pedido {pedido}: {response.status_code}")

# Lista de pedidos a procesar (puedes modificar esta lista con los pedidos reales)
lista_pedidos = ["272700176", "6457344550991"]

# Procesar pedidos
procesar_pedidos(lista_pedidos)
