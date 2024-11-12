from flask import Flask, jsonify #flask sirve para crear la aplicacion web y jsonify convierte los datos de python en un formato JSON para enviarlos como respuestas
from flask_cors import CORS  #cors permite que el servidor acepte solicitudes desde otros dominios, uril cuando accede a esta API desde un fronted en un dominio diferente
import requests #resquests se utiliza para hacer solictudes HTTP a la API externa desde donde se obtiene las cotizaciones 

app = Flask(__name__) #inicia la aplicacion de flask
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}}) #habilita CORS para la aplicacion permitiendo que cualquier origen * pueda hacer solicitudes a la API en las rutas que empiecen con /api/*

# Función para obtener datos de la API de Dolar y procesarlos
def obtener_cotizaciones():
    api_url = "https://dolarapi.com/v1/dolares"
    response = requests.get(api_url) #hace una solicitud GET a la URL de la API y almacena la respuesta 
    datos_api = response.json() #convierte la repuesta en JSON, luego procesa cada elemento de datos_api, obteniendo las claves nombre, casa (tipo), compra, venta, y fechaActualizacion y añadiéndolas a una lista cotizaciones.
    cotizaciones = []

    for cotizacion in datos_api:
        nombre = cotizacion.get("nombre", "Desconocido")
        tipo = cotizacion.get("casa", "Desconocido")
        compra = cotizacion.get("compra")
        venta = cotizacion.get("venta")
        fecha = cotizacion.get("fechaActualizacion")

        cotizaciones.append({ #este enfoque es muy común cuando se trabaja con datos provenientes de APIs, ya que facilita la recolección y procesamiento de grandes cantidades de información
            "nombre": nombre,
            "tipo": tipo,
            "compra": compra,
            "venta": venta,
            "fecha": fecha
        })

    return cotizaciones #la función devuelve cotizaciones, una lista de diccionarios con los datos de cada tipo de cambio del dólar.

# Endpoint para servir los datos de cotizaciones
@app.route("/api/cotizaciones", methods=["GET"]) #define un endpoint /api/cotizaciones que acepta solo solicitudes GET
def api_cotizaciones():
    return jsonify(obtener_cotizaciones()) #llama a obtener_cotizaciones para obtener los datos y utiliza jsonify para enviarlos en formato JSON al cliente que hizo la solicitud

#inicia el servidor
if __name__ == "__main__":
    app.run(debug=True) 
