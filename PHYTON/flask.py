from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Función para obtener datos de la API de Dolar y procesarlos
def obtener_cotizaciones():
    api_url = "https://dolarapi.com/v1/dolares"
    response = requests.get(api_url)
    datos_api = response.json()
    cotizaciones = []

    for cotizacion in datos_api:
        nombre = cotizacion.get("nombre", "Desconocido")
        tipo = cotizacion.get("casa", "Desconocido")
        compra = cotizacion.get("compra")
        venta = cotizacion.get("venta")
        fecha = cotizacion.get("fechaActualizacion")

        cotizaciones.append({
            "nombre": nombre,
            "tipo": tipo,
            "compra": compra,
            "venta": venta,
            "fecha": fecha
        })

    return cotizaciones

# Endpoint para servir los datos de cotizaciones
@app.route("/api/cotizaciones", methods=["GET"])
def api_cotizaciones():
    return jsonify(obtener_cotizaciones())

if __name__ == "__main__":
    app.run(debug=True)
