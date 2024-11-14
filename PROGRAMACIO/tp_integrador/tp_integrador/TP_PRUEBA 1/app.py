# Importación de las bibliotecas necesarias
from flask import Flask, jsonify, request  # Flask para crear la API y manejar solicitudes HTTP
import requests  # requests para hacer peticiones HTTP a otras APIs
import json  # json para manejar datos en formato JSON
from datetime import datetime, timedelta  # datetime para trabajar con fechas
from flask_cors import CORS  # CORS para manejar solicitudes entre dominios (Cross-Origin Resource Sharing)

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde cualquier origen para las rutas /api/*
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# Lista para almacenar las cotizaciones obtenidas
cotizaciones = []

# Función para obtener las cotizaciones desde una API externa
def obtener_cotizaciones():
    api_url = "https://dolarapi.com/v1/dolares"  # URL de la API que proporciona las cotizaciones del dólar
    response = requests.get(api_url)  # Realiza la solicitud GET
    datos_api = response.json()  # Convierte la respuesta a formato JSON

    # Itera sobre los datos obtenidos y extrae información relevante
    for cotizacion in datos_api:
        nombre = cotizacion.get("nombre", "Desconocido")  # Obtiene el nombre de la cotización (si existe)
        tipo = cotizacion.get("casa", "Desconocido")  # Obtiene el tipo de cotización (si existe)
        compra = cotizacion.get("compra")  # Obtiene el valor de compra
        venta = cotizacion.get("venta")  # Obtiene el valor de venta
        fecha = cotizacion.get("fechaActualizacion")  # Obtiene la fecha de la última actualización

        # Añade la cotización a la lista 'cotizaciones'
        cotizaciones.append({
            "nombre": nombre,
            "tipo": tipo,
            "compra": compra,
            "venta": venta,
            "fecha": fecha
        })
   
    return cotizaciones  # Devuelve la lista de cotizaciones obtenidas

# Ruta para la API que devuelve las cotizaciones como respuesta
@app.route("/api/cotizaciones", methods=["GET"])
def api_cotizaciones():
    return jsonify(obtener_cotizaciones())  # Llama a la función obtener_cotizaciones y devuelve los datos en formato JSON

# Ruta para manejar solicitudes POST a /api/contacto/ (para enviar un mensaje de contacto)
@app.route('/api/contacto/', methods=['POST', 'OPTIONS'])
def contacto():
    if request.method == 'OPTIONS':  # Maneja la solicitud OPTIONS (usada por el navegador para CORS)
        # Responde con los encabezados necesarios para permitir solicitudes CORS
        response = app.response_class(status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    # Si la solicitud es POST, obtiene los datos enviados en formato JSON
    data = request.get_json()
   
    # Si no se envían datos, devuelve un error
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
   
    # Llama a la función mail_enviar para enviar un correo electrónico con los datos de contacto
    mail_enviar(data['nombre'], data['apellido'], 'tobianfuso@gmail.com', data['mensaje'])
   
    # Devuelve una respuesta JSON indicando que el mensaje de contacto ha sido recibido
    return jsonify({"status": "Contacto recibido", "data": data}), 200

# Función para enviar un correo electrónico usando la API de EmailJS
def mail_enviar(nombre, apellido, email, informacion_enviar):
    # Datos para la solicitud de correo
    data = {
        'service_id': 'service_tq6wwwh',
        'template_id': 'template_mx23lgn',
        'user_id': 'kPneVDwcNx4UK_xyp',
        'accessToken': 'vs9nufahysZPpyZwuUS9L',
        'template_params': {
            'from_name': 'Pagina Cotizaciones',
            'to_name': f'{nombre} {apellido}',
            'to_mail': f'{email}',
            'message': f'Cotizacion pedida {informacion_enviar}'
        }
    }

    # Encabezados para la solicitud HTTP
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept': 'application/json, text/javascript, /; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://your-website.com',  # Reemplazar con la URL de tu sitio web
        'Referer': 'https://your-website.com/'  # Reemplazar con la URL de tu sitio web
    }

    try:
        # Realiza una solicitud POST para enviar el correo
        response = requests.post(
            'https://api.emailjs.com/api/v1.0/email/send',
            data=json.dumps(data),
            headers=headers
        )
        response.raise_for_status()  # Lanza una excepción si la solicitud falla
        print('Your mail is sent!')  # Mensaje de éxito
    except requests.exceptions.RequestException as error:
        # Maneja errores de la solicitud
        print(f'Oops... {error}')
        if error.response is not None:
            print(error.response.text)

# Ruta para obtener los datos históricos de las cotizaciones de un tipo de dólar entre dos fechas
@app.route('/api/historico/<tipo_dolar>/<fecha_inicio>/<fecha_fin>/<int:valores>', methods=["GET"])
def api_historico(tipo_dolar, fecha_inicio, fecha_fin, valores):
    # URL de la API externa que proporciona las cotizaciones históricas
    api_url = f"https://api.argentinadatos.com/v1/cotizaciones/dolares/{tipo_dolar}"
   
    try:
        # Realiza la solicitud GET a la API externa
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza una excepción si la solicitud falla
        datos = response.json()  # Convierte la respuesta a formato JSON
       
        # Convierte las fechas de inicio y fin a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
       
        # Calcula la diferencia entre las fechas y genera las fechas intermedias
        diferencia_fechas = (fecha_fin - fecha_inicio) / (valores - 1)
        fechas = [((fecha_inicio + diferencia_fechas * cont).strftime("%Y-%m-%d")) for cont in range(valores)]

        # Filtra los datos históricos para obtener solo las cotizaciones correspondientes a las fechas generadas
        datos_historicos = []
        for fecha in fechas:
            for dato in datos:
                if dato['fecha'] == fecha:
                    datos_historicos.append({
                        'fecha': dato['fecha'],
                        'valor': dato['compra']  # Se almacena solo el valor de compra
                    })
       
        # Devuelve los datos históricos en formato JSON
        return jsonify(datos_historicos)

    except requests.exceptions.RequestException as e:
        # Maneja errores de la solicitud
        print("Error al obtener datos de la API externa:", e)
        return jsonify({"error": "No se pudieron obtener los datos"}), 500

# Ejecuta la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)  # Inicia el servidor de desarrollo en modo debug