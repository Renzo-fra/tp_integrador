from flask import Flask, jsonify #flask sirve para crear la aplicacion web y jsonify convierte los datos de python en un formato JSON para enviarlos como respuestas
from flask_cors import CORS  #cors permite que el servidor acepte solicitudes desde otros dominios, uril cuando accede a esta API desde un fronted en un dominio diferente
import requests #resquests se utiliza para hacer solictudes HTTP a la API externa desde donde se obtiene las cotizaciones 
import json

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


@app.route('/api/contacto/', methods=['POST', 'OPTIONS'])
def contacto():
    if requests.method == 'OPTIONS':
        # Responde a la solicitud preflight con un estado 200 y headers de CORS
        response = app.response_class(status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    # Procesa la solicitud POST aquí
    data = requests.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    # Aquí puedes agregar el procesamiento que necesites con data, como guardar en una base de datos o enviar un correo
    # print(f"Contacto recibido: {data}")  # Ejemplo de procesamiento
    mail_enviar(data['nombre'],data['apellido'],'tobianfuso@gmail.com',data['mensaje'],data['email'])
    return jsonify({"status": "Contacto recibido", "data": data}), 200

def mail_enviar(nombre,apellido,email,informacion_enviar):
    data = {
        'service_id': 'service_tq6wwwh',
        'template_id': 'template_mx23lgn',
        'user_id': 'kPneVDwcNx4UK_xyp',
        'accessToken': 'vs9nufahysZPpyZwuUS9L',
        'template_params': {
            'from_name': 'Pagina Cotizaciones',
            'to_name': f'{nombre} {apellido}',
            'to_mail':f'{email}',
            'message': f'Cotizacion pedida {informacion_enviar}'
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept': 'application/json, text/javascript, /; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://your-website.com',  
        'Referer': 'https://your-website.com/'
    }

    try:
        response = requests.post(
            'https://api.emailjs.com/api/v1.0/email/send',
            data=json.dumps(data),
            headers=headers
        )
        response.raise_for_status()
        print('Your mail is sent!')
    except requests.exceptions.RequestException as error:
        print(f'Oops... {error}')
        if error.response is not None:
            print(error.response.text)


#inicia el servidor
if __name__ == "__main__":
    app.run(debug=True) 
